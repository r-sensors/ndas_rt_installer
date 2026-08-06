import os, threading, subprocess, time, gpsd, datetime

class SYSTEM_TIMING_AND_GPS:
    def __init__(self):
        self.gpsd_running = False
        self.gps_receiver_ok = False

        self.update_thread = threading.Thread(target=self.__periodic_update, args=())
        self.update_thread.start()
        self.previous_gps_timestamp = 0
        self.previous_timestamp_time = 0
        self.receiver_timeout = 5
        
    def __parse_packet(self, packet):
        print(packet)
        if packet.time == '': return None
        gps_timestamp = datetime.datetime.fromisoformat(packet.time[:-1]).replace(tzinfo=datetime.timezone.utc).timestamp()
        #gps_timestamp -= 3600*24*30*2
        #print(gps_timestamp)
        if gps_timestamp == self.previous_gps_timestamp: return None
        self.previous_timestamp_time = time.time()
        self.previous_gps_timestamp = gps_timestamp
        mode = packet.mode
        height = 'unknown'
        state = 'error'
        if mode == 1: fix = 'no fix'
        elif mode == 2: 
            fix = '2d fix'
            state = 'warning'
        elif mode == 3: 
            fix = '3d fix'
            height = packet.altitude()
            state = 'normal'
        else: fix = 'unknown'
        return { 'fix':fix, 'numSV':packet.sats, 'lat':packet.lat, 'lon':packet.lon, 'hi':height, 'time':gps_timestamp, 'is_ok':True, 'state':state }
        
    def __get_gps_data(self):
        gps_stats = { 'is_ok':False }
        if not self.gpsd_running:
            try: 
                gpsd.connect()
                self.gpsd_running = True
            except: 
                print("GPSD not running")
        if self.gpsd_running:
            try: 
                packet = gpsd.get_current()
            except UserWarning as e:
                packet = None
            except: 
                self.gpsd_running = False
                packet = None
                
            if packet != None: packet = self.__parse_packet(packet)
            if packet != None:
                self.gps_receiver_ok = True
                gps_stats = packet
            elif time.time() - self.previous_gps_timestamp < self.receiver_timeout: self.gps_receiver_ok = False

            print(gps_stats)
        
        
    def __periodic_update(self):
        while True:
            self.__get_gps_data()
            
            time.sleep(1)
            
gpss = SYSTEM_TIMING_AND_GPS()