
import requests
import requests_cache
import cv2,csv
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from helper_functions.helper_functions import login,load_image,get_embidding,check1

# Creating a flask app and using it to instantiate a socket object
app = Flask(__name__)
socketio = SocketIO(app)

requests_cache.install_cache('github_cache', backend='sqlite', expire_after=180)

# Handler for default flask route
@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/save_register')
def save_register():
    name=request.values.get('username')
    img_path=request.values.get('image_file')
    print(name,img_path)
    with open(r'data.csv', 'a', newline='') as csvfile:
        fieldnames = ['id','name','path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({'id':0 , 'name':name ,'path':img_path})

    return render_template('index2.html')

@app.route('/startExam')
def startExam():
    username=request.values.get('username')
    print('#################################')
    print(username)
    img_path=login(username)
    im=load_image(img_path)
    global e
    e=get_embidding(im)
#     print(e)
    return render_template('index3.html')


i=3
count_f=0
@socketio.on('video')
def value_changed(message):
        global e,i,count_f
        cap = cv2.VideoCapture("/home/heba/Downloads/"+message["url"])
        print('reading from ',message["url"])
        cnt=295
        while  cnt>0:
            print(count_f)
            cnt-=1
            _, frame =  cap.read()
            alert=check1(frame,e)
            if(not alert):
                if(i<0):
                    return render_template('finished.html')
                if(count_f>60):
                    i-=1
                    count_f=0
                    socketio.emit('alert', { 'msg':'you should be infront of the lap an alone you have {0} more tries ' .format(i)})
                else:
                    count_f+=1
            else:
                count_f=0
            
        cap.release()
        cv2.destroyAllWindows()  
        

if __name__ == '__main__':
        socketio.run(app, host='0.0.0.0')
