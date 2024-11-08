import os # เกี่ยวกับการล้างค่าหน้าจอ ที่กด enter to continue
import csv
import datetime 

################## config ระบบ ###############################
#ใช้ config เป็นไฟล์กลางในการ access รายชื่อห้อง รวมไปถึง รายชื่อนักเรียนกับการจอง
# ในบรรรทัด data ไฟล์ config เป็น dict เลยต้องใช้ delimeter เป็น ':' เพื่อ access จากนั้นค่อยแยกในไฟล์ที่จะนำไปใช้ด้วย comma
config={}
file = open("config.csv", "r")
data = list(csv.reader(file, delimiter=":")) 

for g in data:
    config[g[0]] = g[1]

file.close()
##############################################################
##### ตรวจสอบรายชื่อนักเรียนว่าอยู่ใน csv ไหม ##########
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
##################################################
####### ตรวจสอบวันที่ ###############################
def check_date(ddmmyyyy):
    dates = ddmmyyyy.split("-")
    if len(dates) == 3:
        dd = int(dates[0])
        mm = int(dates[1])
        yyyy = int(dates[2])
        numday = [31,28,31,30,31,30,31,31,30,31,30,31] #function ตรวจสอบวันที่ด้วยตัวเอง
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
##### ตรวจสอบว่าห้องว่างไหม ################################
def check_room_available(room,date):
    file = open(config['reserve_file'], "r")
    data = list(csv.reader(file, delimiter=","))
    available = True
    for g in data:
        if g[2] == room and g[3] == date:
            available = False
            break        
    file.close()
    return(available)
##############################################################
####################### จบ function เสริม #####################


###########################################################
## function 1 (printชื่อ นักเรียน)
def print_student_list():
    file = open(config['student_file'], "r")
    data = list(csv.reader(file, delimiter=","))
    j = -1
    for i in data:
        if j >= 0:
            print ("{:>0} {:>8} {:>20} {:>20}".format(j,i[0],i[1],i[2]))
        else:
            print ("{:>0} {:>8} {:>20} {:>20}".format('',i[0],i[1],i[2]))
        #print(i[0]+"\t"+"\t"+i[1]+"\t"+"\t"+i[2])
        j = j + 1
    file.close()



###########################################################
########## function 2 (ส่งรายการจองห้อง)######################
def print_submit_a_booking_request():
    ### เช็ค นักเรียน
    id = input('Student ID:')
    if not check_student(id):
        print('id not found')
        return False
    
    ### เช็คห้อง
    room = input('Room types 1(Lecture) / 2(lab): ')
    
    if room == '1':
        roomlist  = config['roomlist_lecture'].split(',')
        print(roomlist)
    elif room == '2':
        roomlist = config['roomlist_lab'].split(',')

        print(roomlist)
    else:
        print('not have room')
        return False
    ####### เพิ่มห้องไหม
    roomno = input('room:')
    roomno = roomno.upper()    
    if roomno not in roomlist:
        print('room number does not exist')
        confirm = input('Do you want to create new room?(y/n)')
        
        if confirm == 'y':
            print('ok')
            add(room,roomno)
        else:
            return False
            

    ### รับวันที่
    x = datetime.datetime.now() #เพื่อต้องการดูวันที่ปัจจุบันด้วย
    #print(x.date())
    bookdate = x.date()
    bookdate = input('Booking date (DD-MM-YYYY):')
    if check_date(bookdate) == False:    
        print("Incorrect data format")
        return False
    if not check_room_available(roomno,bookdate):
        print('room not available')
        return False



    ### บันทึกเข้าไปในไฟล์
    column_name = ["ID","Type","Room","Date"]
    file = open(config['reserve_file'], "a+", newline='')
    writer = csv.writer(file)
    if os.stat(config['reserve_file']).st_size == 0:
        writer.writerow(column_name)
    if room == '1':
        room = 'lecture'
    elif room == '2':
        room = 'lab'
    row = [id,room,roomno,bookdate]
    writer.writerow(row)
    file.close()
    print('OK! booking done')

### function 3 ###################################################
def add(roomtype,roomnumber): 
    # เวลาจะแอดห้องกับไปต้อง + comma ให้ด้วย
    if roomtype == '1':
        config['roomlist_lecture'] = config['roomlist_lecture'] + ',' + roomnumber
    elif roomtype == '2':
        config['roomlist_lab'] = config['roomlist_lab'] + ',' + roomnumber
    

def check_booking_room(g):
    from datetime import datetime
    k = g.upper()
    file = open('reserve.csv', "r")
    data = list(csv.reader(file, delimiter=","))
    lst = []
    for i in data :
        if i[2] == k:
            lst.append([i[3],i])
    if lst == []:
        print('No booking')
        c = input('Do you want to create new room?(y/n)')
        if c == 'y' or c == 'Y':
            k = input('lecture or lab:')
            add(k,g)
    else:
        if lst != []:
            # ใช้ lambda เพราะเวลาเราอินพุตเข้าไปเราสามารถ ใส่ 1 ได้ แทน 01 ex: 2-1-2020 แปลงเป็น 02-01-2020
            lst.sort(key=lambda d: datetime.strptime(d[0], "%d-%m-%Y"))
            print('Current booking')
            for row in lst:
                print(f'Date: {row[0]}  Student ID: {row[1][0]}')
        #print(row[1])
    file.close()
##############################################################################
######## function 4 ##########################################################
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
####################################################################
########################## function 5 ##############################
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
                print(f'Room: {i[2]} Date: {i[3]}')

        if lst == []: # เช็คการจอง
            print('No booking')
####################################################################
############################ function 6 ############################
def check_booking_student_id(name):
    file = open(config['student_file'], "r")
    data = list(csv.reader(file, delimiter=","))
    data.pop(0) ## ลบหัวรายการออก พวก id name l name
    reservefile = open(config['reserve_file'], "r")
    reservedata = list(csv.reader(reservefile, delimiter=","))
    student = [x for x in data if name.lower() in x[1].lower() or name.lower() in x[2].lower()]
    studentdict={}
    if student == [] :
        print('Not found')
    else:
        print(student)
        
        for i in student:
            studentdict[i[0]] = i 
        print(studentdict)
    
    for k,v in studentdict.items():
        print(f'{v[0]} {v[1]} {v[2]}')
        nodata = True ##ตรวจสอบการพิม current booking และ no booking
        
        for i in reservedata:
            if k == i[0]:
                if nodata == True:
                    print('Current Booking')
                    nodata = False
                #print(i[3])
                print(f'Room: {i[2]} Date: {i[3]}')
        if nodata == True:
            print('No booking: ')

    file.close()
####################################################################
########################## function 7 ###############################
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
        # ใช้เพื่ออำนวยความสะดวกเหมือนกับที่พิมพ์ไปด้านบน
        lst.sort(key=lambda d: datetime.strptime(d[3], "%d-%m-%Y"))
        
        if lst != []:
            for i in lst:
                print(f'    dates: {i[3]} student id: {i[0]}')
        else:
            print('   No booking')         
    
    file.close()
######################################################################

######################### Main Program #############################
while True:
    os.system('cls')
    print('  ##    ##    ##      ##')
    print(' # #   # #    ##     ##')
    print('#   ##   #     ### ###   ')

    print('MUICT Student Room Booking System')
    print('1. print a list of students ')
    print('2. submit a booking request ')
    print('3. check the current booking via room number')
    print('4. check the available rooms via date')
    print('5. check booking with student ID')
    print('6. check booking with student first name')
    print('7. print booking summary ')
    print('0. exit')
    choice = input("Option: ")
    if choice == '0':
        break

    if  choice < '1' or choice > '7' or len(choice) > 1:
        print('1-7 only')
    
    if choice == '1':
        #print('execute function1')
        print_student_list()

    elif choice == '2':
        #print('execute function2')
        print_submit_a_booking_request()

    elif choice == '3':
        g = input('Room number: ')
        check_booking_room(g)
        

    elif choice == '4':
        dates = input('Booking date (DD-MM-YYYY):')
        check_available_room_by_date(dates)
        #print('execute function4')

    elif choice == '5':
        #print('execute function5')
        id = input('รหัสนักศึกษา:')
        check_booking_student_id(id)

    elif choice == '6':
        #print('execute function6')
        name = input('Search for first /last name: ')## หาทุกอย่างที่ตรงกับที่ใส่เข้าไป
        check_booking_student_id(name)
    elif choice =='7':
        #print('execute function7')
        summary()

    h = input('enter to continue ...')

######## update config file ###########################
file = open('config.csv', "w", newline='')
writer = csv.writer(file,delimiter=":")

for k,v in config.items():
    row = [k,v]
    writer.writerow(row)
file.close()
print('update done')






