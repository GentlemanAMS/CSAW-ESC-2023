import serial
import time

# Define the serial ports
ser1 = serial.Serial('/dev/ttyACM0', 115200, 0.005)  # Adjust the port and baud rate as needed
ser2 = serial.Serial('/dev/ttyUSB0', 115200, 1)  # Adjust the port and baud rate as needed

while True:
    try:
        if ser1.read(1) == b'E':
            print("Received 'E' on ser1. Sending 'ERR' to ser2.")
            ser2.write(b'ERR')  # Send 'ERR' to ser2
            print(ser2.readline())
        else:
            pass
    except:
        pass
        
# Close the serial ports
ser1.close()
ser2.close()
