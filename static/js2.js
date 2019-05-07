
    socket.on('my response', function(msg) {
        $('#log').append('<p>Received: ' + msg.data + '</p>');
    });
    $('form#emit').submit(function(event) {
        socket.emit('my event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });





    $(document).ready(function(){
        // sending a connect request to the server.
        var socket = io.connect('http://localhost:5000');
        
        socket.emit('video', {  
            data: "the frame should be this"
        });
    socket.on('after connect', function(msg){
        console.log('After connect', msg);
        });
    });
