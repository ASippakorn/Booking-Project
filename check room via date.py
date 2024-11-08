import os # เกี่ยวกับการล้างค่าหน้าจอ 
import csv
import datetime

config={}
file = open("config.csv", "r")
data = list(csv.reader(file, delimiter=":"))
for g in data:
    config[g[0]] = g[1]
file.close()





def check_available_room_by_date(dates):
    from datetime import datetime
    file = open('reserve.csv', "r")
    data = list(csv.reader(file, delimiter=","))
    if not check_date(dates):
        print('wrong date format')
    else:
        roomlecture  = config['roomlist_lecture'].split(',')
        roomlab = config['roomlist_lab'].split(',')
        databydate=[] #เอาแต่ข้อมูลของวันที่ที่เราใส่เข้าไปเท่านั้น
        print('Room available')
        for i in data:
            if i[3] == dates:
                databydate.append(i)
        for i in databydate:
            if i[2] in roomlecture: # ถ้าสมาชิกที่อยู่ใน databydate ตรงกับ roomlecture
                print(i[2])
                roomlecture.remove(i[2])
                #listlab.remove(i[2])
            if i[2] in roomlab: # ถ้าสมาชิกที่อยู่ใน databydate ตรงกับ roomlab
                print(i[2])
                roomlab.remove(i[2])
                #listlab.remove(i[2])
        
        print(roomlecture)
        print(roomlab)
    file.close()
####### ตรวจสอบวันที่ ###############################
def check_date(ddmmyyyy):
    dates = ddmmyyyy.split("-")
    if len(dates) == 3:
        dd = int(dates[0])
        mm = int(dates[1])
        yyyy = int(dates[2])
        numday = [31,28,31,30,31,30,31,31,30,31,30,31]
    else:
        return False
    if mm > 12:
        return False
    if mm == '02' and int(yyyy) % 4 == 0:
        numday[1] = 29

    #print(numday[mm-1])
    if dd > int(numday[mm-1]):
        return False
    x = datetime.datetime.now()
    y = str(x.date())
   
    datesnow = y.split("-")
    if yyyy < int(datesnow[0]):
        return False
    elif yyyy == int(datesnow[0]):
        if mm < int(datesnow[1]):
            return False
    return True
#########################################################


### main program ##########    
dates = input('Booking date (DD-MM-YYYY):')
check_available_room_by_date(dates)