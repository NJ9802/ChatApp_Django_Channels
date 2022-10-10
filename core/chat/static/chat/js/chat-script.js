const roomName = JSON.parse(document.getElementById('chat-name').textContent);
const user_username = JSON.parse(document.getElementById('username').textContent);

// JavaScript function to
// Display 12 hour format

var date = new Date();
var hours = date.getHours();
var minutes = date.getMinutes();

// Check whether AM or PM
var newformat = hours >= 12 ? 'pm' : 'am'; 

// Find current hour in AM-PM Format
hours = hours % 12; 

// To display "0" as "12"
hours = hours ? hours : 12; 
minutes = minutes < 10 ? '0' + minutes : minutes;

// document.getElementById("change").innerHTML = 
//   hours + ':' + minutes + ' ' + newformat;
// obtener la fecha y la hora
let now = hours + ':' + minutes + ' ' + newformat;;
// console.log(now);
 



document.querySelector('#chat_button').onclick = function (e) {
        const messageInputDom = document.querySelector('#chat_input');
        const message = messageInputDom.value;
        roomsocket.send(JSON.stringify({
            'message':message,
            'username': user_username,
            'chatname': roomName,
            'datetime': now
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
    let mainDiv;
    let headerDiv;

roomsocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        // console.log(data)
        

        if (user_username===data.username) {
            mainDiv = '<div class="container m-1 d-flex justify-content-end">';
            headerDiv = '<div class="messages-items bg-primary">';
        }
        else {
            mainDiv = '<div class="container m-1 d-flex justify-content-start">';
            headerDiv = '<div class="messages-items bg-secondary">';
        }
        let html = mainDiv;
            html += headerDiv;     
            html += '<header><small class="mx-1">' + '@'+ data.username + ':' + '</small></header>';
            html += '<div class="d-flex">';
            html += '<p class="mx-1">' + data.message + '</p>';
            html += '<div class="d-flex align-items-end">';
            html += '<small class="mx-1 time">' + now + '</small>';
            html += '</div></div></div></div>';


        document.querySelector('#chat_area').innerHTML += html;
        scrollToBottom()
    }    
     
    function scrollToBottom() {
    
        const objDiv = document.querySelector('#chat_area');
    
        objDiv.scrollTop = objDiv.scrollHeight;
    
    }
        
    
    scrollToBottom()
        
