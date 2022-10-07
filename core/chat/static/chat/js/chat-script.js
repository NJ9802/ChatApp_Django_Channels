const roomName = JSON.parse(document.getElementById('chat-name').textContent);
const user_username = JSON.parse(document.getElementById('username').textContent);
const messagea = JSON.parse(document.getElementById('message').textContent);

document.querySelector('#chat_button').onclick = function (e) {
        const messageInputDom = document.querySelector('#chat_input');
        const message = messageInputDom.value;
        roomsocket.send(JSON.stringify({
            'message':message,
            'username': user_username,
            'chatname': roomName,
        }));
        messageInputDom.value = '';
    };    

const roomsocket = new WebSocket(
        'ws://' + 
        window.location.host +
        '/ws/chat/' + 
        roomName +
        '/'
    );

    const input = document.querySelector('#chat_input')
    input.focus();
    input.onkeyup = function (e) {
        if (e.keyCode == 13) {
            document.querySelector('#chat_button').click();
        }
    };

    input.addEventListener('keydown', typing);

    function typing () {
        document.getElementById('typing').innerText = 'typing...';
        document.getElementById('typing').innerText = '';
    }

roomsocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data)
        
        let html = '<div class="container">';
            html += '<p>' + data.username + '</p>';
            html += '<p>' + data.message + '</p></div><hr>';
        
        document.querySelector('#chat_area').innerHTML += html;
        scrollToBottom()
    }    
     
    function scrollToBottom() {
    
        const objDiv = document.querySelector('#chat_area');
    
        objDiv.scrollTop = objDiv.scrollHeight;
    
    }
        
    
    scrollToBottom()
        // document.querySelector('#chat_area').value += (data.username + ': '+
        // data.message + messagea + '\n')
    
