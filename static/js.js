
  if (navigator.getUserMedia) {
    // request video and audio stream from the user's webcam
    navigator.mediaDevices.getUserMedia({
        audio: true,
        video: true
    }).then((stream) => {
      var video = document.querySelector('video');
      video.srcObject = stream;
      video.play();
    }).catch((error) => {
      console.log('navigator.getUserMedia error: ', error);
    });}

    function connect(host) {
      ws = new WebSocket(host);
      ws.onopen = function () {
          console.log('connected');
      };

      ws.onclose = function () {
        console.log('socket closed');
      };

      ws.onerror = function (evt) { 
        console.log('error in socket conntection'); 
      };
  };

  if('WebSocket' in window){
    connect('ws://localhost:8000/echo');        
} else {
    log ('web sockets not supported');
 }

 function send(msg){  
  if (ws != null) {  
      if(ws.readyState === 1) {
         ws.send(msg);
      }        
  } else {
      //log ('not ready yet');
  }
}   


var back = document.getElementsByTagName('canvas');
var backcontext = back.getContext('2d');
cw = 120;//240;//video.clientWidth;
ch = 200;//400;//video.clientHeight;
back.width = cw;
back.height = ch;
draw(video, backcontext, cw, ch);
function draw(v, bc, w, h) {
    
  // First, draw it into the backing canvas
  bc.drawImage(v, 0, 0, w, h);
  
  // Grab the pixel data from the backing canvas
  var stringData=back.toDataURL();
  
  // send it on the wire
  send(stringData);
  
  // Start over! 10 frames a second = 100milliseconds
  setTimeout(function(){ draw(v, bc, w, h); });
}
