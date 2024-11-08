import os # เกี่ยวกับการล้างค่าหน้าจอ 
import csv
import datetime

config={}
file = open("config.csv", "r")
data = list(csv.reader(file, delimiter=":"))
for g in data:
    config[g[0]] = g[1]
file.close()


def check_booking_student_id(id):
    lst=[]
    if not check_student(id):
        print('ไม่มีรายชื่อนักเรียนในฐานข้อมูล')
    else:
        file = open('reserve.csv', "r")
        data = list(csv.reader(file, delimiter=","))
        print('Current bookings: ')
        for i in data:
            if i[0] == id:
                print(f'Room: {i[2]} Date:{i[3]}')

        if lst == []:
            print('No booking')






def check_student(id):
    found = False
    file = open(config['student_file'], "r")
    data = list(csv.reader(file, delimiter=","))
    for i in data:
        if i[0] == str(id):
            found = True
            break
    file.close()
    return found



### main program ##########    
id = input('รหัสนักศึกษา:')
check_booking_student_id(id)