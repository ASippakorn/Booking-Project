import os # เกี่ยวกับการล้างค่าหน้าจอ 
import csv
import datetime

config={}
file = open("config.csv", "r")
data = list(csv.reader(file, delimiter=":"))
for g in data:
    config[g[0]] = g[1]
file.close()


def check_booking_student_id(name):
    file = open(config['student_file'], "r")
    data = list(csv.reader(file, delimiter=","))
    data.pop(0) ## ลบหัวรายการออก
    reservefile = open(config['reserve_file'], "r")
    reservedata = list(csv.reader(reservefile, delimiter=","))
    student = [x for x in data if name.lower() in x[1].lower() or name.lower() in x[2].lower()]
    
    if student == [] :
        print('Not found')
    else:
        print(student)

    
    for st in student:
        print(f'{st[0]} {st[1]} {st[2]}')
        nodata = True ##ตรวจสอบการพิม current booking และ no booking
    
        for i in reservedata:
        
            if st[0] == i[0]:
                
                if nodata == True:
                    print('Current Booking')
                    nodata = False
                #print(i[3])
                print(f'Room: {i[2]} Date: {i[3]}')
        if nodata == True:
            print('No booking: ')

    file.close()
    



### main program ##########    
name = input('Search for first /last name: ')## หาทุกอย่างที่ตรงกับที่ใส่เข้าไป
check_booking_student_id(name)
#print_student_list()