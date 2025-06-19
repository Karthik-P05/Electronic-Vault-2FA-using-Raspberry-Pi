import hashlib
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from RPLCD.gpio import CharLCD
from RPi import GPIO
import pymysql
import os
import shutil

pos = 0

db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
curs=db.cursor()
f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
while True:
    iD = input("Enter ID to be deleted : ")
    curs.execute("SELECT * FROM data11 WHERE id=%s",iD)
    row=curs.fetchone()
    
    if row is None:
        print('User not found')
    else:
        
        break
        
pos = row[3]
#print(pos)
pos=int(pos)
f.deleteTemplate(pos)
q = "DELETE FROM data11 WHERE id = %s"
curs.execute(q,iD)
db.commit()
db.close()

#delete folder with given id
downloads_path = os.path.expanduser('~/facial rec/dataset')

#folder_name = input('Name of User to be deleted :') #replace with your name
folder_path = os.path.join(downloads_path, iD)
if os.path.exists(folder_path):
    shutil.rmtree(folder_path)
    print(f'Deleted ID : {iD}')
else:
    print(f'{iD} not exists')
print('Deleted successfully')