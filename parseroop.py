from messageclass import Message


flag = 1 #master, 2n - slave

m = Message()

while True:
     m.get_function_id()

     m.get_hat(flag)

     start, len = m.get_length(flag)

     m.read_message(start, len)

     m.print_message()

     if m.slave_id == 0x00:
          break
     else:
          flag+=1     



