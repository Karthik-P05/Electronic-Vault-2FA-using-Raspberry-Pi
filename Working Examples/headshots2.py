import cv2
import os

downloads_path = os.path.expanduser('~/facial rec/dataset')

folder_name = input('Name :') #replace with your name
folder_path = os.path.join(downloads_path, folder_name)
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

