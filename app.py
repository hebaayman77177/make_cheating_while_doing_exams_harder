
import requests
import requests_cache

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from helper_functions.helper_functions import login,load_image,get_embidding,check

# Creating a flask app and using it to instantiate a socket object
app = Flask(__name__)
socketio = SocketIO(app)

requests_cache.install_cache('github_cache', backend='sqlite', expire_after=180)

# Handler for default flask route
@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/startExam')
def startExam():
    username=request.args.get('username')
    print('#################################')
    print(username)
    img_path=login(username)
    im=load_image(img_path)
    global e
    e=get_embidding(im)
#     print(e)
    return render_template('index.html')


i=3
count_f=0
@socketio.on('video')
def value_changed(message):
        global i,e,count_f
        alert=check(message['data'],message['h'],message['w'],e)
        if(not alert):
            if(count_f>60):
                i-=1
                count_f=0
                _=input('you have {0} more tries,you shoud be infront of the camera and there shoud not be any person be with you press any key to continue'.format(i))
            else:
                count_f+=1

if __name__ == '__main__':
        socketio.run(app, host='0.0.0.0')
