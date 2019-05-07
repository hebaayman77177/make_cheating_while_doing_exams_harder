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
import numpy as np
import pandas as pd


nn4_small2_pretrained = create_model()
nn4_small2_pretrained.load_weights('weights/nn4.small2.v1.h5') 

haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

def download_landmarks(dst_file):
    url = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
    decompressor = bz2.BZ2Decompressor()
    
    with urlopen(url) as src, open(dst_file, 'wb') as dst:
        data = src.read(1024)
        while len(data) > 0:
            dst.write(decompressor.decompress(data))
            data = src.read(1024)


def load_image(path):
    img = cv2.imread(path, 1)
    # OpenCV loads images with color channels
    # in BGR order. So we need to reverse them
    return img[...,::-1]


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


def check(frame,h,w,e):
    frame=np.asarray(frame)
    frame=frame.reshape((h, w,4))
    frame=np.uint8(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    faces=haar_face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
    num_faces=len(faces)
    if (num_faces==1):
        try:
            img= get_embidding(frame)
        except TypeError:
            print("from empeding the foto isnt clean")
            return False
        if(distance(img,e)>0.6):
            print("not you ")
            return False
        else:
            print('finaly you ')
            return True     
    elif (num_faces>1):
        print("more than one person in front of the lab")
        return False
    else:
        print("you should be infront of the lab")
        return False

def check1(frame,e):
    faces=haar_face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
    num_faces=len(faces)
    if (num_faces==1):
        try:
            img= get_embidding(frame)
        except TypeError:
            print("from empeding the foto isnt clean")
            return False
        if(distance(img,e)>0.6):
            print("not you ")
            return False
        else:
            print('finaly you ')
            return True     
    elif (num_faces>1):
        print("more than one person in front of the lab")
        return False
    else:
        print("you should be infront of the lab")
        return False





dst_dir = 'models'
dst_file = os.path.join(dst_dir, 'landmarks.dat')

if not os.path.exists(dst_file):
    os.makedirs(dst_dir)
    download_landmarks(dst_file)
    

# Initialize the OpenFace face alignment utility
alignment = AlignDlib('models/landmarks.dat')



