import serial
import time


ser = serial.Serial('/dev/ttyUSB1', baudrate = 19200, timeout = 1 )#timeouts =?

flag = 1 #master, 2n - slave
N = 256 #max len of package
buf = []*N
inter_byte_timeout = 0.5
t = inter_byte_timeout

while True:

     #read length of package from itself
     if (ser.in_waiting > 0):
          buf.append(ser.read())

          time.sleep(t) #acceptable time between bytes

          if (ser.in_waiting > 0):
               buf.append(ser.read())
          else:
               logger.error("uncomlete package: %s", " ".join(map(str,buf)))
               loggerf.errorf("uncomlete package: %s", " ".join(map(str,buf)))
               continue

     slave_id = buf[0]
     function_id = buf[1]
     len = 0

     if (function_id == 0x06) or (function_id == 0x29 and flag%2 == 1): #write register
          len = 8
          start = 2

     if function_id == 0x19: #red register
          len = 6
          start = 2

     if function_id == 0x26:  #write registers
          for i in range(2, 6):
               time.sleep(t)

               if (ser.in_waiting > 0):
                    buf.append(ser.read())
               else:
                    logger.error("uncomlete package: %s", " ".join(map(str,buf)))
                    loggerf.errorf("uncomlete package: %s", " ".join(map(str,buf)))
                    break_out_flag = True
                    break

          if break_out_flag:
               continue

          len = buf[4]*16 + buf[5] + 6 + 2
          start = 6


     if function_id == 0x29 and flag%2 == 0:
          for i in range(2, 4):
               time.sleep(t)
               if (ser.in_waiting > 0):
                    buf.append(ser.read())
               else:
                    logger.error("uncomlete package: %s", " ".join(map(str,buf)))
                    loggerf.errorf("uncomlete package: %s", " ".join(map(str,buf)))
                    break_out_flag = True
                    break

          if break_out_flag:
               continue

          len = buf[2]*16 + buf[3] + 4 + 2
          start = 4

     #put full message in a buffer

     for i in range(start, len):
          time.sleep(t)
          if (ser.in_waiting > 0):
               buf.append(ser.read())
          else:
               logger.error("uncomlete package: %s", " ".join(map(str,buf)))
               loggerf.errorf("uncomlete package: %s", " ".join(map(str,buf)))
               break_out_flag = True
               break

     if break_out_flag:
          continue               

     

     if flag%2 == 1: #we could check if everefing is correct in message-response pair after input of slave responce
          master = buf
     else:
          slave = buf

     
     #output the package
     logger.info(" ".join(map(str,buf)))
     loggerf.info(" ".join(map(str,buf)))


     
     buf.clear()

     if slave_id == 0x00:
          break
     else:
          flag+=1

     

     

     


     
