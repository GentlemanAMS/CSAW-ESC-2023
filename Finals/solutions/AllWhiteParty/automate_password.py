import serial
import time

import sys
import os

os.system("avrdude  -v  -patmega328p -carduino -P/dev/ttyACM0 -b115200 -D -Uflash:w:./week1/AllWhiteParty.hex")

ser1 = serial.Serial('/dev/ttyACM0', 115200, timeout = 5)
ser2 = serial.Serial('/dev/ttyUSB0', 115200, timeout = 0.1)

# Clearing buffers
ser1.reset_input_buffer()
ser1.reset_output_buffer()

ser2.reset_input_buffer()
ser2.reset_output_buffer()

all_passwords = []

original_password = [3, 8, 0, 5, 0, 3, 2, 7, 0, 4]




def get_password_guess():

    password = original_password
    to_send = 0
    for i in range(10):
        to_send += password[i]*10**(9-i)
    to_send = str(to_send)
    to_send = '0'*(10-len(to_send)) + to_send
    to_send1 = to_send[:5] + '\n'
    to_send2 = to_send[5:] + '\n'

    return to_send1, to_send2




def get_ser1_data_line():
    try:
        data = ser1.readline()
        time_end = time.time()
        print(f"Arduino says:{data}")
    except Exception as e:
        print(f"Serial port error: {str(e)}")
    return data, time_end



def get_single_byte_ser1():
    try:
        data2 = ser1.read().decode('ASCII')
    except:
        data2 = ''
    return data2



def get_single_byte_ser2():
    try:
        data2 = ser2.read().decode('ASCII')
    except:
        data2 = ''
    return data2


def get_ser1_data():
    res = ''
    data1 = get_single_byte_ser1()
    while (data1 != ''):
            res += data1
            print(data1, end='')
            data1 = get_single_byte_ser1()
    print('\n')
    return res

def get_ser2_data():
    res = ''
    data2 = get_single_byte_ser2()
    while (data2 != ''):
            res += data2
            print(data2, end='')
            data2 = get_single_byte_ser2()
    print('\n')
    return res



username_i = 0

def get_user_name():
    global username_i

    username = "Barry12345"
    username = username.encode()

    for i in range(username_i):
        username += b'\x00'

    if (username_i > 650):
        sys.exit(0)
    else:
        username_i += 1

    print(username)
    return username



state = 0
final_state = 5

def proceed_func():

    to_send_password1, to_send_password2 = get_password_guess()
    print(f"Password: {to_send_password1[:-1] + to_send_password2[:-1]}")
    ser2.write(to_send_password1.encode())
    ser2.write(to_send_password2.encode())
    time.sleep(0.01)
    get_ser2_data()


    username = get_user_name()
    ser1.write(username)

    data, _ = get_ser1_data_line()
    if data[:5] == b'10-di':
        print("Stage 1 done")
        _, time_start = get_ser1_data_line()
        _, time_end = get_ser1_data_line()
        print(f"Time from Password: {time_end - time_start}")
        
        temp_str, _ = get_ser1_data_line()
        file_time_store2 = open("store_time_q1a2.txt", 'a')
        file_time_store2.write(f"Username: {username_i} Hash: {temp_str}\n")
        file_time_store2.close()


        file_time_store1 = open("store_time_q1a1.txt", 'a')
        file_time_store1.write(f"Password: {to_send_password1[:-1] + to_send_password2[:-1]} Time: {time_end - time_start}\n")
        file_time_store1.close()

while True:

    data, _ = get_ser1_data_line()

    if data[:5] == b'/****':
        data, _ = get_ser1_data_line()
        if data[:5] == b'Chall':
            data, _ = get_ser1_data_line()
            if data[:5] == b'/****':            
                data, _ = get_ser1_data_line()
                if data[:5] == b'Welco':
                    data, _ = get_ser1_data_line()
                    if data[:5] == b'Enter':
                        proceed_func()
                    else: continue
                else: continue
            else: continue
        else: continue

    elif data[:5] == b'Welco':
        data, _ = get_ser1_data_line()
        if data[:5] == b'Enter':
            proceed_func()
        else: continue

    elif data[:5] == b'Enter':
        proceed_func()

    else: 
        continue
            

