import hashlib
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from RPLCD.gpio import CharLCD
from RPi import GPIO
import pymysql

lcd = CharLCD(pin_rs=7, pin_e=8, pins_data = [25, 24, 23, 18],numbering_mode=GPIO.BCM, cols=16, rows=2, dotsize=8, charmap='A02', auto_linebreaks=True)
db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
curs=db.cursor()

f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

if not f.verifyPassword():
    raise ValueError('The given fingerprint sensor is wrong !')

def enroll():
    
    lcd.clear()
    lcd.write_string('Waiting')
    print('Waiting for finger...')
        
        #Wait finger is reading
    while ( f.readImage() == False ):
        pass
    
    ## Converts read image to characteristics and stores it in charbuffer 1
    #f.convertImage(0x01)
        ## Checks if finger is already enrolled
    #result = f.searchTemplate()
    #positionNumber = result[0]
        
    #if ( positionNumber >= 0 ):
    #   print('Template already exist')        

    ## Checks if finger is already enrolled
    lcd.clear()
    lcd.write_string('Remove finger')
    print('Remove finger...')
    time.sleep(2)
        
    f.convertImage(0x01)
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        
        print('Fingerprint already exist !')
        print('Template position : ' + str(positionNumber))
        temp = f.downloadCharacteristics()
        print(temp)
        return
    
    #f.storeTemplate()
    
    name = input('Enter you name : ')
    
    
    #fin = f.downloadCharacteristics()
    chara = str(f.downloadCharacteristics()).encode('utf-8')
    fin = hashlib.sha256(chara).hexdigest()
    
    f.storeTemplate()
    result = f.searchTemplate()
    positionNumber1 = result[0]
    print('Enrolled data position : ' + str(positionNumber1))
    
    #print(fin1)

    query= "INSERT INTO data9 (name,fing_encod,temp_pos) VALUES (%s,%s,%s)"
    #val =[name,fin1]
    
    curs.execute(query,(name,fin,positionNumber1))
    
    db.commit()
    
    lcd.clear()
    lcd.write_string('Finger enrolled.')
    print('Finger enrolled successfully!')
    time.sleep(2)
    
    
def search():
    ## Tries to search the finger and calculate hash
    lcd.clear()
    lcd.write_string('Waiting for finger')
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass
        
    f.convertImage(0x01)
    result = f.searchTemplate()
    positionNumber = result[0]
    #fin = f.downloadCharacteristics()
    

    if positionNumber == -1:
        print("Fingerprint not found")
    else:
        
    #template = f.downloadCharacteristics()
        print("Fingerprint found")
        f.loadTemplate(positionNumber, 0x01)
        chara = str(f.downloadCharacteristics(0x01)).encode('utf-8')
        find = hashlib.sha256(chara).hexdigest()

        print(find)

        #characterics = str(f.downloadCharacteristics(0x01))
        #print(characterics)
        #char = input("Enter name : ")
        query = "SELECT * FROM data9 WHERE fing_encod = %s"
        curs.execute(query,find)
    
        row = curs.fetchone()
        #id = float(row[0])
        print("Fingerprint found for ID : ", row[0])
        print("Name : ", row[1])
    
    
def delete():
    id = input("Enter Id to be deleted : ")
    curs.execute("SELECT * FROM data9 WHERE id=%s",id)
    row=curs.fetchone()
    if row is None:
        print('User not found')
        return
    pos = row[3]
    #print(pos)
    pos=int(pos)
    f.deleteTemplate(pos)
    q = "DELETE FROM data9 WHERE id = %s"
    curs.execute(q,id)
    db.commit()
    print('Deleted successfully')
    



while True:
    lcd.clear()
    lcd.write_string("1.Enroll 2.Find 3.Delete")
    print("----------------")
    print("Choose an option")
    print("e) enroll print")
    print("f) find print")
    print("d) delete print")
    print("----------------")
    c = input("> ")

    if c == "e":
        enroll()
        
    if c == "f":
        search()
        
    if c == "d":
        delete()

