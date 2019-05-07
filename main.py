import bz2
import os
from urllib.request import urlopen
from model import create_model
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from align import AlignDlib
import csv
import pandas as pd

def download_landmarks(dst_file):
    url = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
    decompressor = bz2.BZ2Decompressor()
    
    with urlopen(url) as src, open(dst_file, 'wb') as dst:
        data = src.read(1024)
        while len(data) > 0:
            dst.write(decompressor.decompress(data))
            data = src.read(1024)

dst_dir = 'models'
dst_file = os.path.join(dst_dir, 'landmarks.dat')

if not os.path.exists(dst_file):
    os.makedirs(dst_dir)
    download_landmarks(dst_file)
    

nn4_small2_pretrained = create_model()
nn4_small2_pretrained.load_weights('weights/nn4.small2.v1.h5')




def load_image(path):
    img = cv2.imread(path, 1)
    # OpenCV loads images with color channels
    # in BGR order. So we need to reverse them
    return img[...,::-1]

# Initialize the OpenFace face alignment utility
alignment = AlignDlib('models/landmarks.dat')
def align_image(img):
    return alignment.align(96, img, alignment.getLargestFaceBoundingBox(img), 
                           landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)

def get_embidding(img):
    img = align_image(img)
    # scale RGB values to interval [0,1]
    img = (img / 255.).astype(np.float32)
    # obtain embedding vector for image
    return nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]
    
    
def distance(emb1, emb2):
    return np.sum(np.square(emb1 - emb2))

def login(username):
    name=username
    colnames=['id','name','path']
    data = pd.read_csv('/home/heba/Documents/ml_and_dl/ipprojectanothercopy/data.csv',names=colnames, header=None)
    data.set_index("name", inplace=True)        
    image_path=data.loc[name]['path']
    return image_path


username=input("please enter your username")
image_path=login(username)
print(image_path)
im=load_image(image_path)
e=get_embidding(im)

haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/heba/output.avi',fourcc, 20.0, (640,480))
count_t=0
count_f=0
alert=0
while(True):
    if(alert>2):
        break
    if(count_f>60):
        alert+=1
        _=input("be infront of the camera,press c to continue ")
        count_f=0

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out.write(frame)
    cv2.imshow('frame',frame)
    faces=haar_face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
    num_faces=len(faces)
    if (num_faces==1):
        try:
            img= get_embidding(frame)
        except TypeError:
            print("from empeding the foto isnt clean")
            count_f+=1
            continue
        if(distance(img,e)>0.6):
            print("not you ")
            count_f+=1
            if(count_f%5==0):
                print("################################")
        else:       
            count_t+=1 
            count_f=0
            print("thats you")
    elif (num_faces>1):
        print("more than one person in front of the lab")
        count_f+=2
    else:
        print("you should be infront of the lab")
        count_f+=1
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print(count_f,count_t)
        break
cap.release()
out.release()














