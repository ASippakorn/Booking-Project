import os # เกี่ยวกับการล้างค่าหน้าจอ 
import csv
import datetime

config={}
file = open("config.csv", "r")
data = list(csv.reader(file, delimiter=":"))
for g in data:
    config[g[0]] = g[1]
file.close()


def summary():
    data.pop(0) ## ลบหัวรายการออก
    reservefile = open(config['reserve_file'], "r")
    reservedata = list(csv.reader(reservefile, delimiter=","))
    roomlec = config['roomlist_lecture'].split(',')
    roomlab = config['roomlist_lab'].split(',')
    from datetime import datetime
    print('lecture')
    for lec in roomlec:
        lst=[]
        print(f'{lec}: ')
        for res in reservedata:
            if res[2] == lec:
                lst.append(res)
        lst.sort(key=lambda d: datetime.strptime(d[3], "%d-%m-%Y"))
        
        if lst != []:
            for i in lst:
                print(f'    dates: {i[3]} student id: {i[0]}')
        else:
            print('   No booking')
    
    print('lab')
    for lec in roomlab:
        lst=[]
        print(lec)
        for res in reservedata:
            if res[2] == lec:
                lst.append(res)
        lst.sort(key=lambda d: datetime.strptime(d[3], "%d-%m-%Y"))
        
        if lst != []:
            for i in lst:
                print(f'    dates: {i[3]} student id: {i[0]}')
        else:
            print('   No booking')         
    
    file.close()
    



### main program ##########    
#name = input('Search for first /last name: ')## หาทุกอย่างที่ตรงกับที่ใส่เข้าไป
summary()
#print_student_list()