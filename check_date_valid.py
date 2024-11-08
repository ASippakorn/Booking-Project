import datetime
import csv
'''
# function 5 #####################################
def check_booking_id(id):
    found = False
    file = open("reserve.csv", "r")
    data = list(csv.reader(file, delimiter=","))
    for i in data:
        if i[0] == str(id):  
            found = True
            print(i)  
    file.close()
    return found
print(check_booking_id(input()))
'''
###################################################
'''
# function 7 ######################################
def print_booking_summary():
    file = open("students.csv", "r")
    data = list(csv.reader(file, delimiter=","))
    for i in data:
        print(i)
'''

def check_date(ddmmyyyy):
    dates = ddmmyyyy.split("-")
    dd = int(dates[0])
    mm = int(dates[1])
    yyyy = dates[2]
    numday = [31,28,31,30,31,30,31,31,30,31,30,31]
    
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
    if yyyy < datesnow[0]:
        return False
    elif yyyy == datesnow[0]:
        if mm < datesnow[1]:
            return False
    return True
print(check_date('30-12-2024'))