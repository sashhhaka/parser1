import logging
import serial
import time
import logging
from custom_logger import CustomFormatter

# create logger with 'spam_application'
logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)


loggerf = logging.getLogger("test1")
loggerf.setLevel(logging.INFO)

# create console handler with a log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)


# file handler
zh = logging.FileHandler('/home/sashafab/progrmms/parser_result.txt',  mode='a')
zh.setLevel(logging.INFO)

zh.setFormatter(CustomFormatter())

loggerf.addHandler(zh)



ser = serial.Serial('/dev/ttyUSB1', baudrate = 19200, timeout = 1 )#timeouts =?

inter_byte_timeout = 0.5
t = inter_byte_timeout



class Message:


     def __init__(self, bytes = []):
          self.bytes = bytes
          self.slave_id = 0
          self.function_id = 0


     def get_function_id(self):
          #read the hat, input bytes in a list and return function id
          for i in range(2):
               time.sleep(t)
               if (ser.in_waiting > 0):
                    self.bytes.append(ser.read())

          self.slave_id = self.bytes[0]
          self.function_id = self.bytes[1]
          return self.function_id


     def get_hat(self, flag):
          function_id = self.function_id
          #read the hat if necessary (number of bytes)

          if function_id == 0x26:
               st = 2
               ln = 6
          if function_id == 0x29 and flag%2 == 0:
               st = 2
               ln = 4
          else:
               st = 0
               ln = 0

          for i in range(st, ln):
               time.sleep(t)
               if (ser.in_waiting > 0):
                    self.bytes.append(ser.read())

          
     def get_length(self, flag):
          #depends on function_id and if it is a slave or a master
          function_id = self.function_id
          if (function_id == 0x06) or (function_id == 0x29 and flag%2 == 1): #write register
               len = 8
               start = 2

          if function_id == 0x19: #read register
               len = 6
               start = 2
          
          if function_id == 0x26: #write registers
               len = self.bytes[4]*16 + self.bytes[5] + 6 + 2
               start = 6

          if function_id == 0x29 and flag%2 == 0:
               len = self.bytes[2]*16 + self.bytes[3] + 4 + 2
               start = 4

          return start, len


     def read_message(self, start, len):
          for i in range(start, len):
               time.sleep(t)
               if (ser.in_waiting > 0):
                    self.bytes.append(ser.read())


     def print_message(self):
          logger.info(" ".join(map(str, self.bytes)))
          loggerf.info(" ".join(map(str, self.bytes)))
          self.bytes.clear()