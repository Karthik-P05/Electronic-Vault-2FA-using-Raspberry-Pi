import hashlib
import time
from pyfingerprint.pyfingerprint import PyFingerprint
#from RPLCD.gpio import CharLCD
from RPi import GPIO
import pymysql
import cv2
import os
from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2
import os
import pymysql

#lcd = CharLCD(pin_rs=7, pin_e=8, pins_data = [25, 24, 23, 18],numbering_mode=GPIO.BCM, cols=16, rows=2, dotsize=8, charmap='A02', auto_linebreaks=True)
db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
curs=db.cursor()

f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

if not f.verifyPassword():
    raise ValueError('The given fingerprint sensor is wrong !')


print('Waiting for finger...')
        
        #Wait finger is reading
while ( f.readImage() == False ):
    pass
    
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

    
    #f.storeTemplate()
iD = input('Enter ID : ')     
name = input('Enter you name : ')
    
    
    #fin = f.downloadCharacteristics()
chara = str(f.downloadCharacteristics()).encode('utf-8')
fin = hashlib.sha256(chara).hexdigest()
    
f.storeTemplate()
result = f.searchTemplate()
positionNumber1 = result[0]
print('Enrolled data position : ' + str(positionNumber1))
    
    #print(fin1)

#query= "INSERT INTO data11 (id,name,fing_encod,temp_pos) VALUES (%s,%s,%s,%s)"
#val =[name,fin1]
    
#curs.execute(query,(iD,name,fin,positionNumber1))
    
#db.commit()
#db.close()
  

print('Finger enrolled successfully!')
time.sleep(2)

downloads_path = os.path.expanduser('~/facial rec/dataset')

#folder_name = input('Name :') #replace with your name
folder_path = os.path.join(downloads_path, iD)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f'Created folder: {folder_path}')
else:
    print(f'Folder already exists: {folder_path}')
    
cam = cv2.VideoCapture(0)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 500, 300)

count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        
        file_path = os.path.join(folder_path, f'img' +str(count)+'.jpg')
        #img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(file_path, frame)
        print("{} written!".format(file_path))
        count += 1

cam.release()

cv2.destroyAllWindows()

#name = input("Name : ")

#construct the path to the folder containing the images
folder_path = os.path.join("dataset",iD)
# our images are located in the dataset folder
print("[INFO] start processing faces...")
imagePaths = list(paths.list_images(folder_path))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model="hog")

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()

with open('encodings.pickle', 'rb') as h:
    data = pickle.load(h)
data_bin = pickle.dumps(data)

#curs.execute('UPDATE TABLE data11 SET img_encod = (%s) WHERE id  = (%s)',(data_bin,iD))
query= "INSERT INTO data11 (id,name,fing_encod,temp_pos,img_encod) VALUES (%s,%s,%s,%s,%s)"
curs.execute(query,(iD,name,fin,positionNumber1,data_bin))
db.commit()
db.close()


