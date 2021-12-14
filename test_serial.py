# import serial
# import struct
# 
# def main():
# 	
# 	ser = serial.Serial ("/dev/ttyS0")    #Open named port 
# 	ser.baudrate = 9600                     #Set baud rate to 9600
# 	
# 	data = 12.34567890
# 	data_bytes = bytearray(struct.pack("f", data))
# 	
# 	print(data_bytes)
# 	
# 	ser.write(data_bytes)                         #Send back the received data
# 	# data_bytes = ser.read(4)                     #Read ten characters from serial port to data
# 	
# 	
# 	# print(data_bytes)
# 	
# 	ser.close()
# 
# if __name__ == "__main__":
#     main()
#

import serial
import time

port = serial.Serial("/dev/ttyS0", baudrate = 16000, timeout = 2)

port.write("yeeeeeeeteeeeeee".encode('ascii'))

time.sleep(1)

rcv = port.read(9)
print(rcv)