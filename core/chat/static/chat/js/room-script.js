const user_username = JSON.parse(document.getElementById('user_username').textContent);
const roomId = JSON.parse(document.getElementById('room-id').textContent);


// crea un nuevo objeto `Date`
let today = new Date();
 
// obtener la fecha y la hora
let now = today.toLocaleString();
// console.log(now);
 
/*
    Resultado: 1/27/2020, 9:30:00 PM
*/

document.querySelector('#submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    roomsocket.send(JSON.stringify({
        'message':message,
        'username': user_username,
        'chatname': roomId,
        'datetime': now,

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