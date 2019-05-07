import cv2
import csv
def check_and_save(img_path,frame):
    haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    face=haar_face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
    if(len(face) ==1):
        cv2.imwrite(img_path,frame)
        print("gegister succeeded :)")
    else:
         print('refused registeration because of the photo !!!')
#take the name
name=input("please enter your name \n")
#put id
f=open('auto_increment.txt','r')
old_id=int(f.read())
user_id=old_id+1
f.close()
f=open('auto_increment.txt','w')
f.write(str(user_id))
f.close()
#take aphoto ,save it and its path
print("please enter s to save the photo")
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/heba/output.avi',fourcc, 20.0, (640,480))
img_path="Images/img"+str(user_id)+".jpg"
ii=1
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out.write(frame)
    if(ii==1):
        print(frame)
        print("##########################")
        print(len(frame))
    ii+=1
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        check_and_save(img_path,frame);
        break
cap.release()
out.release()



#save user_id,name,img_path to an csv file

with open(r'data.csv', 'a', newline='') as csvfile:
    fieldnames = ['id','name','path']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writerow({'id':user_id, 'name':name ,'path':img_path})
















