const user_username = JSON.parse(document.getElementById('user_username').textContent);
const roomId = JSON.parse(document.getElementById('room-id').textContent);

document.querySelector('#submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    roomsocket.send(JSON.stringify({
        'message':message,
        'username': user_username,
    }));
    messageInputDom.value = '';
}


const roomsocket = new WebSocket(
    'ws://' + 
    window.location.host +
    '/ws/chat/' +
    'room' + 
    roomId +
    '/'
);

document.querySelector('#input').focus();
document.querySelector('#input').onkeyup = function (e) {
    if (e.keyCode == 13) {
        document.querySelector('#submit').click();
    }
}; 

roomsocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)
    
    document.querySelector('#chat-text').value += (data.username + ': '+
    data.message + '\n')
}