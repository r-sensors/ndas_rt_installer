import can, struct
 
can.rc['interface'] = 'socketcan_ctypes'
bus = can.interface.Bus('can1')
ch1 = open('ch_1', 'wb')
ch2 = open('ch_2', 'wb')
ch3 = open('ch_3', 'wb')
ch4 = open('ch_4', 'wb')
ch5 = open('ch_5', 'wb')
ch6 = open('ch_6', 'wb')

conv = (1<<15) / 14.76
try:
    message_counter = 0
    while True:
        Message = bus.recv(0.0)
        if Message:
            m_id = Message.arbitration_id
            m_dat = Message.data
            #print("ID:%d DATA:%s"%(m_id, str(m_dat)))
            print_now = message_counter % 50 == 0
            if(m_id == 1 or m_id == 3):
                ch1.write(m_dat[2:4])
                ch2.write(m_dat[4:6])
                ch3.write(m_dat[6:8])
                if print_now:
                    dummy, ch1_s16, ch2_s16, ch3_s16 = struct.unpack('<4h', m_dat)
            if(m_id == 2 or m_id == 4):
                ch3.write(m_dat[2:4])
                ch4.write(m_dat[4:6])
                ch5.write(m_dat[6:8])
                if print_now:
                    dummy, ch4_s16, ch5_s16, ch6_s16 = struct.unpack('<4h', m_dat)
                    print("\033[F\033[A\033[A\033[A\033[A", end = '')
                    print("Linear: %.3fV %.3fV %.3fV" %(ch1_s16/conv, ch2_s16/conv, ch3_s16/conv))
                    print("Rotational: %.3fV %.3fV %.3fV" %(ch4_s16/conv, ch5_s16/conv, ch6_s16/conv))
                    print("Total %d samples recvd"%message_counter)
                message_counter += 1
        
             
except  KeyboardInterrupt:
    bus.shutdown()
finally:
    ch1.close()
    ch2.close()
    ch3.close()
    ch4.close()
    ch5.close()
    ch6.close()