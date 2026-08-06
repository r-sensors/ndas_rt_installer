import os, threading, time, gpsd, datetime
import logging

class SYSTEM_TIMING_AND_GPS:
    def __init__(self):
        self.gpsd_running = False
        self.gps_receiver_ok = False
        self.running = True  # Флаг для остановки потока
        
        self.previous_gps_timestamp = 0
        self.previous_timestamp_time = 0
        self.receiver_timeout = 5  # секунд
        
        # Настройка логирования
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.update_thread = threading.Thread(target=self.__periodic_update, args=())
        self.update_thread.daemon = True  # Поток завершится с программой
        self.update_thread.start()
    
    def stop(self):
        """Метод для остановки потока"""
        self.running = False
        self.update_thread.join(timeout=2)
    
    def __parse_packet(self, packet):
        """Парсинг GPS-пакета с улучшенной обработкой ошибок"""
        try:
            if not packet.time:
                return None
            
            # Преобразование времени
            gps_timestamp = datetime.datetime.fromisoformat(
                packet.time[:-1]
            ).replace(tzinfo=datetime.timezone.utc).timestamp()
            
            # Проверка дубликатов
            if gps_timestamp == self.previous_gps_timestamp:
                return None
            
            self.previous_timestamp_time = time.time()
            self.previous_gps_timestamp = gps_timestamp
            
            # Определение статуса
            mode = packet.mode
            if mode == 1:
                fix = 'no fix'
                state = 'error'
                height = 'unknown'
            elif mode == 2:
                fix = '2d fix'
                state = 'warning'
                height = 'unknown'
            elif mode == 3:
                fix = '3d fix'
                state = 'normal'
                height = packet.altitude()
            else:
                fix = 'unknown'
                state = 'error'
                height = 'unknown'
            
            return {
                'fix': fix,
                'numSV': packet.sats,
                'lat': packet.lat,
                'lon': packet.lon,
                'hi': height,
                'time': gps_timestamp,
                'is_ok': True,
                'state': state
            }
        except Exception as e:
            self.logger.error(f"Parse error: {e}")
            return None
        
    def __get_gps_data(self):
        """Получение данных GPS с корректной обработкой ошибок"""
        gps_stats = {'is_ok': False}
        
        # Подключение к gpsd
        if not self.gpsd_running:
            try:
                gpsd.connect()
                self.gpsd_running = True
                self.logger.info("Connected to GPSD")
            except Exception as e:
                self.logger.error(f"Cannot connect to GPSD: {e}")
                return gps_stats
        
        # Получение данных
        try:
            packet = gpsd.get_current()
        except UserWarning as e:
            self.logger.warning(f"GPSD warning: {e}")
            packet = None
        except Exception as e:
            self.logger.error(f"GPSD error: {e}")
            self.gpsd_running = False
            packet = None
        
        # Обработка пакета
        if packet is not None:
            parsed = self.__parse_packet(packet)
            if parsed is not None:
                self.gps_receiver_ok = True
                gps_stats = parsed
                self.logger.debug(f"GPS OK: {gps_stats['fix']}, SV:{gps_stats['numSV']}")
            else:
                # Данные получены, но невалидны
                pass
        else:
            # Проверка таймаута
            if self.previous_gps_timestamp > 0:
                elapsed = time.time() - self.previous_timestamp_time
                if elapsed > self.receiver_timeout:
                    if self.gps_receiver_ok:
                        self.logger.warning(f"GPS timeout: {elapsed:.1f}s")
                    self.gps_receiver_ok = False
            else:
                self.gps_receiver_ok = False
        
        return gps_stats
        
    def __periodic_update(self):
        """Периодический цикл обновления"""
        self.logger.info("GPS update thread started")
        
        while self.running:
            try:
                self.__get_gps_data()
            except Exception as e:
                self.logger.error(f"Unexpected error in update loop: {e}")
            
            time.sleep(1)
        
        self.logger.info("GPS update thread stopped")
    
    def get_current_status(self):
        """Публичный метод для получения текущего статуса"""
        return {
            'gps_ok': self.gps_receiver_ok,
            'gpsd_connected': self.gpsd_running,
            'last_timestamp': self.previous_gps_timestamp
        }

# Пример использования
if __name__ == "__main__":
    gpss = SYSTEM_TIMING_AND_GPS()
    
    try:
        # Основной цикл программы
        while True:
            # Здесь можно использовать gpss.get_current_status()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nStopping GPS reader...")
        gpss.stop()