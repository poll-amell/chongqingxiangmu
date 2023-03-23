from site import addsitedir
import threading
import time
import copy
from queue import Queue
import serial
import sqlite3  # 导入sqlite3模块
import requests
import json
import uuid
from concurrent.futures import ThreadPoolExecutor

ser = serial.Serial("/dev/ttyUSBA", 9600)  # 选择串口，并设置波特率
url = 'http://222.92.117.159:8089/postdata'
headers = {'Content-Type': 'application/json'}
ser.flushInput()

id = str(uuid.uuid1())
datadxsyewei = 0
datadxsEC = 0
datadxsph = 0
datadxstemp = 0
datatrph = 0
datatrtemp = 0
datatrEC = 0
datatrwet = 0

feedback_data_dxstemp = 0
feedback_data_dxsph = 0
feedback_data_dxsEC = 0
feedback_data_location = 0
feedback_data_trEC = 0
feedback_data_trwet = 0
feedback_data_trph = 0
feedback_data_trtemp = 0


def thread_jobdxsEC():
    #if ser.is_open:
    #print("port open success")
    #hex(16进制)转化
    while True:
        time.sleep(0.2)
        send_date = bytes.fromhex('04 03 00 00 00 04 44 5C')  # 发送数据转化为
        ser.write(send_date)  # 发送命令
        time.sleep(0.2)  # 延时，否则len return data将返回0，此处易忽视！
        len_return_data = ser .inWaiting()  # 获取缓冲数据（接收数据）长度
        print(len_return_data)
        if len_return_data:
            print(len_return_data)
            return_data = ser.read(len_return_data)  # 获取缓冲数据
            # print(return_data)
            # print(return_data)
            #bytes(2)转化为hex(16),注意python3和2的区别
            str_return_data = str(return_data.hex())

            feedback_data = str_return_data
            global feedback_data_dxsEC

            feedback_data_EC = str_return_data[6:10]

            #hex-> 十进制

            feedback_data_EC = (int(feedback_data_EC, 16))/10
            global datadxsEC
            datadxsEC = ('1', feedback_data_EC)
            feedback_data_dxsEC = feedback_data_EC
            # print(datadxsEC)
            # print('电导率 = ',feedback_data_temp,'μS/cm')
            #print('wet = ',feedback_data_wet)
            data = {"password": "cgqdata", "id": id, "dxsEC": feedback_data_EC}
            data = json.dumps(data)
            # try:
            #     rep = requests.post(url, data=data,headers=headers)
            #     print(rep.text)
            # except:
            #     continue

        return datadxsEC


def thread_jobdxsyewei():
    while True:

        time.sleep(0.2)
        send_date = bytes.fromhex('06 03 00 00 00 04 45 BE')  # 发送数据转化为
        # send_date = bytes.fromhex('03 03 00 01 00 05 D5 EB')
        ser.write(send_date)  # 发送命令
        time.sleep(0.2)  # 延时，否则len return data将返回0，此处易忽视！
        len_return_data = ser.inWaiting()  # 获取缓冲数据（接收数据）长度
        print("len_return_data", len_return_data)
        if len_return_data:
            #while True:
            return_data = ser.read(len_return_data)  # 获取缓冲数据
            #print(return_data)
            #bytes(2)转化为hex(16),注意python3和2的区别
            str_return_data = str(return_data.hex())
            feedback_data = str_return_data
            global feedback_data_location
            feedback_data_location = str_return_data[6:14]
            feedback_data_temp = str_return_data[14:18]
            feedback_data_pressure = str_return_data[18:26]

            #feedback_data = int(str_return_data[-6:-2],16)
            # print(feedback_data)
            # print(feedback_data_location)
            # print(feedback_data_temp)
            # print(feedback_data_pressure)
            #hex-> 十进制

            feedback_data_location = (int(feedback_data_location, 16))/1000
            feedback_data_temp = (int(feedback_data_temp, 16))/100
            feedback_data_pressure = (int(feedback_data_pressure, 16))

            print('location = ', feedback_data_location, 'm')
            data = {"password": "cgqdata", "id": id,
                    "yewei": feedback_data_location}
            data = json.dumps(data)
            # try:
            #     rep = requests.post(url, data=data,headers=headers)
            #     print(rep.text)
            # except:
            #     continue
            global datadxsyewei
            datadxsyewei = ('1', feedback_data_location)

        return datadxsyewei
        break


def thread_jobdxstemp():
    while True:
        time.sleep(0.2)
        send_date = bytes.fromhex('02 03 00 00 00 04 44 3A')  # 发送数据转化为
        ser.write(send_date)  # 发送命令
        time.sleep(0.2)  # 延时，否则len return data将返回0，此处易忽视！
        len_return_data = ser .inWaiting()  # 获取缓冲数据（接收数据）长度

        if len_return_data:
            return_data = ser.read(len_return_data)  # 获取缓冲数据
            # print(return_data)
            #bytes(2)转化为hex(16),注意python3和2的区别
            str_return_data = str(return_data.hex())
            feedback_data = str_return_data
            feedback_data_temp = str_return_data[14:18]

            #feedback_data = int(str_return_data[-6:-2],16)
            # print(feedback_data)
            #print(feedback_data_temp)
            #print(feedback_data_wet)
            #hex-> 十进制
            global feedback_data_dxstemp

            feedback_data_temp = (int(feedback_data_temp, 16))/10
            feedback_data_dxstemp = feedback_data_temp

            #print('temp = ',feedback_data_temp)
            data = {"password": "cgqdata", "id": id,
                    "dxstemp": feedback_data_temp}
            data = json.dumps(data)
            # try:
            #     rep = requests.post(url, data=data,headers=headers)
            #     print(rep.text)
            # except:
            #     continue
            global datadxstemp
            datadxstemp = ('1', feedback_data_temp)
        return datadxstemp
        break


def thread_jobdxsph():
    while True:
        time.sleep(0.2)
        send_date = bytes.fromhex('02 03 00 00 00 04 44 3A')  # 发送数据转化为
        ser.write(send_date)  # 发送命令
        time.sleep(0.2)  # 延时，否则len return data将返回0，此处易忽视！
        len_return_data = ser .inWaiting()  # 获取缓冲数据（接收数据）长度

        if len_return_data:
            return_data = ser.read(len_return_data)  # 获取缓冲数据
            # print(return_data)
            #bytes(2)转化为hex(16),注意python3和2的区别
            str_return_data = str(return_data.hex())
            feedback_data = str_return_data
            global feedback_data_dxsph
            feedback_data_ph = str_return_data[6:10]

            #feedback_data = int(str_return_data[-6:-2],16)
            # print(feedback_data)
            #print(feedback_data_temp)
            #print(feedback_data_wet)
            #hex-> 十进制

            feedback_data_ph = (int(feedback_data_ph, 16))/100
            feedback_data_dxsph = feedback_data_ph

            #print('temp = ',feedback_data_temp)
            data = {"password": "cgqdata", "id": id,
                    "dxstemp": feedback_data_ph}
            data = json.dumps(data)
            # try:
            #     rep = requests.post(url, data=data,headers=headers)
            #     print(rep.text)
            # except:
            #     continue
            global datadxsph
            datadxsph = ('1', feedback_data_ph)
        return datadxsph
        break


def thread_jobtrEC():

    while True:
        time.sleep(0.2)
        send_date = bytes.fromhex('05 03 00 00 00 04 45 8D')  # 发送数据转化为
        ser.write(send_date)  # 发送命令
        time.sleep(0.2)  # 延时，否则len return data将返回0，此处易忽视！
        len_return_data = ser .inWaiting()  # 获取缓冲数据（接收数据）长度

        if len_return_data:
            return_data = ser.read(len_return_data)  # 获取缓冲数据
            # print(return_data)
            #bytes(2)转化为hex(16),注意python3和2的区别
            str_return_data = str(return_data.hex())
            feedback_data = str_return_data
            feedback_data_EC = str_return_data[14:18]
            global feedback_data_trEC

            #feedback_data = int(str_return_data[-6:-2],16)
            # print(feedback_data)
            #print(feedback_data_temp)
            #print(feedback_data_wet)
            #hex-> 十进制

            feedback_data_EC = (int(feedback_data_EC, 16))
            feedback_data_trEC = feedback_data_EC

            #print('temp = ',feedback_data_temp)
            data = {"password": "cgqdata", "id": id, "trEC": feedback_data_EC}
            data = json.dumps(data)
            # try:
            #     rep = requests.post(url, data=data,headers=headers)
            #     print(rep.text)
            # except:
            #     continue
            global datatrEC
            datatrEC = ('1', feedback_data_EC)
        return datatrEC
        break


def thread_jobtrph():
    while True:
        time.sleep(0.2)
        send_date = bytes.fromhex('05 03 00 00 00 04 45 8D')  # 发送数据转化为
        ser.write(send_date)  # 发送命令
        time.sleep(0.2)  # 延时，否则len return data将返回0，此处易忽视！
        len_return_data = ser .inWaiting()  # 获取缓冲数据（接收数据）长度

        if len_return_data:
            return_data = ser.read(len_return_data)  # 获取缓冲数据
            # print(return_data)
            #bytes(2)转化为hex(16),注意python3和2的区别
            str_return_data = str(return_data.hex())
            feedback_data = str_return_data
            feedback_data_ph = str_return_data[18:22]
            #feedback_data = int(str_return_data[-6:-2],16)
            # print(feedback_data)
            #print(feedback_data_temp)
            #print(feedback_data_wet)
            #hex-> 十进制

            feedback_data_ph = (int(feedback_data_ph, 16))/10
            global feedback_data_trph
            feedback_data_trph = feedback_data_ph

            #print('temp = ',feedback_data_temp)
            data = {"password": "cgqdata", "id": id, "trph": feedback_data_ph}
            data = json.dumps(data)
            # try:
            #     rep = requests.post(url, data=data,headers=headers)
            #     print(rep.text)
            # except:
            #     continue
            global datatrph
            datatrph = ('1', feedback_data_ph)
        return datatrph
        break


def thread_jobtrtemp():

    while True:
        time.sleep(0.2)
        send_date = bytes.fromhex('01 03 00 00 00 04 44 09')  # 发送数据转化为
        ser.write(send_date)  # 发送命令
        time.sleep(0.2)  # 延时，否则len return data将返回0，此处易忽视！
        len_return_data = ser .inWaiting()  # 获取缓冲数据（接收数据）长度

        if len_return_data:
            return_data = ser.read(len_return_data)  # 获取缓冲数据
            # print(return_data)
            #bytes(2)转化为hex(16),注意python3和2的区别
            str_return_data = str(return_data.hex())
            feedback_data = str_return_data
            feedback_data_temp = str_return_data[10:14]

            #feedback_data = int(str_return_data[-6:-2],16)
            # print(feedback_data)
            #print(feedback_data_temp)
            #print(feedback_data_wet)
            #hex-> 十进制

            feedback_data_temp = (int(feedback_data_temp, 16))/10
            global feedback_data_trtemp
            feedback_data_trtemp = feedback_data_temp

            #print('temp = ',feedback_data_temp)
            data = {"password": "cgqdata", "id": id,
                    "trtemp": feedback_data_temp}
            data = json.dumps(data)
            # try:
            #     rep = requests.post(url, data=data,headers=headers)
            #     print(rep.text)
            # except:
            #     continue
            global datatrtemp
            datatrtemp = ('1', feedback_data_temp)
        return datatrtemp
        break


def thread_jobtrwet():

    while True:
        time.sleep(0.2)
        send_date = bytes.fromhex('01 03 00 00 00 04 44 09')  # 发送数据转化为
        ser.write(send_date)  # 发送命令
        time.sleep(0.2)  # 延时，否则len return data将返回0，此处易忽视！
        len_return_data = ser .inWaiting()  # 获取缓冲数据（接收数据）长度
        print(len_return_data)
        if len_return_data:
            return_data = ser.read(len_return_data)  # 获取缓冲数据
            # print(return_data)
            #bytes(2)转化为hex(16),注意python3和2的区别
            str_return_data = str(return_data.hex())
            feedback_data = str_return_data

            feedback_data_wet = str_return_data[6:10]
            #feedback_data = int(str_return_data[-6:-2],16)
            # print(feedback_data)
            #print(feedback_data_temp)
            #print(feedback_data_wet)
            #hex-> 十进制

            feedback_data_wet = (int(feedback_data_wet, 16))/10
            global feedback_data_trwet
            feedback_data_trwet = feedback_data_wet
            #print('temp = ',feedback_data_temp)
            data = {"password": "cgqdata", "id": id,
                    "trwet": feedback_data_wet}
            data = json.dumps(data)
            # try:
            #     rep = requests.post(url, data=data,headers=headers)
            #     print(rep.text)
            # except:
            #     continue
            global datatrwet
            datatrwet = ('1', feedback_data_wet)
        return datatrwet
        break


def main():
    while True:
        time.sleep(0.2)
        conn = sqlite3.connect(
            '/home/pi/Desktop/demo/demo.db', check_same_thread=False)
        cur = conn.cursor()
        print('ok')
        added_thread01 = threading.Thread(target=thread_jobdxsEC)
        added_thread02 = threading.Thread(target=thread_jobdxsph)
        added_thread03 = threading.Thread(target=thread_jobdxsyewei)
        added_thread04 = threading.Thread(target=thread_jobdxstemp)
        added_thread05 = threading.Thread(target=thread_jobtrEC)
        added_thread06 = threading.Thread(target=thread_jobtrph)
        added_thread07 = threading.Thread(target=thread_jobtrtemp)
        added_thread08 = threading.Thread(target=thread_jobtrwet)
        print('okk')
        time.sleep(1)
        added_thread01.start()
        time.sleep(1)
        added_thread02 .start()
        time.sleep(1)
        added_thread03 .start()
        time.sleep(1)
        added_thread04 .start()
        time.sleep(1)
        added_thread05.start()
        time.sleep(1)
        added_thread06 .start()
        time.sleep(1)
        added_thread07 .start()
        time.sleep(1)
        added_thread08 .start()

        # 创建包含2个线程的线程池
        pool = ThreadPoolExecutor(max_workers=8)
        # 向线程池提交一个任务

        future1 = pool.submit(added_thread01)
        future2 = pool.submit(added_thread02)
        future3 = pool.submit(added_thread03)
        future4 = pool.submit(added_thread04)
        future5 = pool.submit(added_thread05)
        future6 = pool.submit(added_thread06)
        future7 = pool.submit(added_thread07)
        future8 = pool.submit(added_thread08)

        # 判断future1线程是否结束---返回False表示该线程未结束，True表示该线程已经结束
        # print("future1线程的状态:" + str(future1.done()))
        # # 判断future2线程是否结束---返回False表示该线程未结束，True表示该线程已经结束
        # print("future2线程的状态:" + str(future2.done()))
        print(datadxsyewei)
        print(datadxsEC)
        print(datadxstemp)
        print(datadxsph)
        print(datatrph)
        print(datatrtemp)
        print(datatrEC)
        print(datatrwet)

# def main():
#     while True:
#         time.sleep(0.2)
#         conn = sqlite3.connect('/home/pi/Desktop/demo/demo.db',check_same_thread=False)
#         cur = conn.cursor()
#         print('ok')
#         # added_thread01 = threading.Thread(target=thread_jobdxsEC)
#         # added_thread02 = threading.Thread(target=thread_jobdxsph)
#         # added_thread03 = threading.Thread(target=thread_jobdxsyewei)
#         # added_thread04 = threading.Thread(target=thread_jobdxstemp)
#         # print('okk')
#         # added_thread01.start()
#         # datadxsEC = added_thread01
#         # time.sleep(0.5)
#         # added_thread02 .start()
#         # time.sleep(0.1)
#         # added_thread03 .start()
#         # time.sleep(0.5)
#         # added_thread04 .start()
#         # datadxstemp = added_thread04
#         # print(datadxstemp)
#         time.sleep(1)
#         datatrEC = thread_jobtrEC()
#         print(datatrEC)
#         time.sleep(1)
#         datatrph = thread_jobtrph()
#         print(datatrph)
#         time.sleep(1)
#         datatrtemp = thread_jobtrtemp()
#         print(datatrtemp)
#         time.sleep(1)
#         datatrwet = thread_jobtrwet()
#         print(datatrwet)
#         time.sleep(0.1)
        try:
            cur.execute('''INSERT INTO trEC_histroy (location,DATA) 
                    VALUES (?,?)''', datatrEC)
            conn.commit()

            cur.execute('DELETE FROM trEC_current')
            cur.execute('''INSERT INTO trEC_current (location,DATA) 
                    VALUES (?,?)''', datatrEC)
            conn.commit()
            cur.execute(
                "delete from trEC_histroy WHERE  CreatedTime BETWEEN  '2017-01-01 00:00:00'  AND  datetime('now','localtime','-90 days');")
            print('trECok')

            cur.execute('''INSERT INTO trph_histroy (location,DATA) 
                    VALUES (?,?)''', datatrph)
            conn.commit()

            cur.execute('DELETE FROM trph_current')
            cur.execute('''INSERT INTO trph_current (location,DATA) 
                    VALUES (?,?)''', datatrph)
            conn.commit()
            cur.execute(
                "delete from trph_histroy WHERE  CreatedTime BETWEEN  '2017-01-01 00:00:00'  AND  datetime('now','localtime','-90 days');")
            print('trphok')

            cur.execute('''INSERT INTO trwendu_histroy (location,DATA) 
                    VALUES (?,?)''', datatrtemp)
            conn.commit()

            cur.execute('DELETE FROM trwendu_current')
            cur.execute('''INSERT INTO trwendu_current (location,DATA) 
                    VALUES (?,?)''', datatrtemp)
            conn.commit()
            cur.execute(
                "delete from trwendu_histroy WHERE  CreatedTime BETWEEN  '2017-01-01 00:00:00'  AND  datetime('now','localtime','-90 days');")
            print('trtempok')

            cur.execute('''INSERT INTO trshidu_histroy (location,DATA) 
                    VALUES (?,?)''', datatrwet)
            conn.commit()

            cur.execute('DELETE FROM trshidu_current')
            cur.execute('''INSERT INTO trshidu_current (location,DATA) 
                    VALUES (?,?)''', datatrwet)
            conn.commit()
            cur.execute(
                "delete from trshidu_histroy WHERE  CreatedTime BETWEEN  '2017-01-01 00:00:00'  AND  datetime('now','localtime','-90 days');")
            print('trwetok')
        except:
            pass
        # time.sleep(1)
        # datadxsEC = thread_jobdxsEC()
        # print(datadxsEC)
        # time.sleep(1)
        # datadxsph = thread_jobdxsph()
        # print(datadxsph)
        # time.sleep(1)
        # datadxstemp = thread_jobdxstemp()
        # print(datadxstemp)
        # time.sleep(1)
        # datadxsyewei = thread_jobdxsyewei()
        # print(datadxsyewei)
        try:
            cur.execute('''INSERT INTO dxsEC_history (location,DATA) 
                            VALUES (?,?)''', datadxsEC)
            conn.commit()
            cur.execute('DELETE FROM dxsEC_current')
            cur.execute('''INSERT INTO dxsEC_current (location,DATA) 
                            VALUES (?,?)''', datadxsEC)
            conn.commit()
            cur.execute(
                "delete from dxsEC_history WHERE  CreatedTime BETWEEN  '2017-01-01 00:00:00'  AND  datetime('now','localtime','-90 days');")
            print('dxsECok')

            cur.execute('''INSERT INTO dxsyewei_history(location,data) 
                            VALUES (?,?)''', datadxsyewei)
            conn.commit()
            cur.execute('DELETE FROM dxsyewei_current')
            cur.execute('''INSERT INTO dxsyewei_current(location,data) 
                        VALUES (?,?)''', datadxsyewei)
            conn.commit()
            cur.execute(
                "delete from dxsyewei_history WHERE  CreatedTime BETWEEN  '2017-01-01 00:00:00'  AND  datetime('now','localtime','-90 days');")
            print('okk')

            cur.execute('''INSERT INTO dxsph_history (location,DATA) 
                    VALUES (?,?)''', datadxsph)
            conn.commit()
            cur.execute(
                "delete from dxsph_history WHERE  CreatedTime BETWEEN  '2017-01-01 00:00:00'  AND  datetime('now','localtime','-90 days');")

            cur.execute('DELETE FROM dxsph_current')
            cur.execute('''INSERT INTO dxsph_current (location,DATA) 
                    VALUES (?,?)''', datadxsph)
            conn.commit()

            cur.execute('''INSERT INTO dxstemp_history (location,DATA) 
                    VALUES (?,?)''', datadxstemp)
            conn.commit()

            cur.execute('DELETE FROM dxstemp_current')
            cur.execute('''INSERT INTO dxstemp_current (location,DATA) 
                    VALUES (?,?)''', datadxstemp)
            conn.commit()
            cur.execute(
                "delete from dxstemp_history WHERE  CreatedTime BETWEEN  '2017-01-01 00:00:00'  AND  datetime('now','localtime','-90 days');")
            print('dxsphtempok')
        except:
            pass
        start = time.time()

        data = {
            "password": "cgqdata",
            "id": "1",
            "time": time.strftime("%Y-%m-%d %X"),
            "dxstemp": feedback_data_dxstemp,
            "dxsph": feedback_data_dxsph,
            "dxsEC": feedback_data_dxsEC,
            "yewei": feedback_data_location,
            "trEC": feedback_data_trEC,
            "trwet": feedback_data_trwet,
            "trph": feedback_data_trph,
            "trtemp": feedback_data_trtemp
        }
        print(data)

        data = json.dumps(data)

        try:
            print('`1234')
            rep = requests.post(url, data=data, headers=headers)
            print(rep.text)
        except:
            continue


if __name__ == '__main__':
 while True:
    try:
        main()
    except:
        continue
