const roomName = JSON.parse(document.getElementById('chat-name').textContent);
const user_username = JSON.parse(document.getElementById('username').textContent);
const user2Id = JSON.parse(document.getElementById('user2Id').textContent);

const online_div = document.getElementById('online')

// JavaScript function to
// Display 12 hour format

var date = new Date();
var hours = date.getHours();
var minutes = date.getMinutes();

// Check whether AM or PM
var newformat = hours >= 12 ? 'p.m.' : 'a.m.'; 

// Find current hour in AM-PM Format
hours = hours % 12; 

// To display "0" as "12"
hours = hours ? hours : 12; 
minutes = minutes < 10 ? '0' + minutes : minutes;

// document.getElementById("change").innerHTML = 
//   hours + ':' + minutes + ' ' + newformat;
// obtener la fecha y la hora
let now = hours + ':' + minutes + ' ' + newformat;
 


const input = document.querySelector('#chat_input')
let intervalo;


document.querySelector('#chat_button').onclick = function (e) {
    if (input.value !== '') {

        clearInterval(intervalo);
        roomsocket.send(JSON.stringify({
            'writing':'False',
            'userId': userId,
            })
        );

        const messageInputDom = document.querySelector('#chat_input');
        const message = messageInputDom.value;
        
        notificationsSocket2.send(JSON.stringify({
            'chatname': roomName,
            'from_to':userId,
            'to': user2Id,
        }));
        
        roomsocket.send(JSON.stringify({
            'message': message,
            'username': user_username,
            'chatname': roomName,
            'datetime': now
        }));
        messageInputDom.value = '';
    }
};    

const url2 = `ws://${window.location.host}/ws/chatapp/notifications/${user2Id}`
const notificationsSocket2 = new WebSocket (url2)

const roomsocket = new WebSocket(
        'ws://' + 
        window.location.host +
        '/ws/chat/' + 
        roomName +
        '/'
    );

    input.focus();
    input.onkeyup = function (e) {
        if (e.keyCode == 13) {
            document.querySelector('#chat_button').click();
        }

    };

    // Send typing data to consumer

    input.addEventListener("input", function(e){
            console.log(e.data);
            if (e.data !== null) {
                roomsocket.send(JSON.stringify({
                    'writing':'True',
                    'userId': userId,
                    })
                );

                clearInterval(intervalo); //Al escribir, limpio el intervalo
                intervalo = setInterval(function(){ //Y vuelve a iniciar
                    roomsocket.send(JSON.stringify({
                        'writing':'False',
                        'userId': userId,
                        })
                    );    
                        clearInterval(intervalo); //Limpio el intervalo
                }, 400);
            }
    }, false);

    let mainDiv;
    let headerDiv;

roomsocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);
        if (data.online === 'True') {
            if (data.chatname === roomName) {
                if (data.userId === user2Id) {
                        online_div.innerHTML = 'online';
                }
            }
        }
        
        else if (data.online === 'False') {
            online_div.innerHTML = '';
        }

        else if (data.writing === 'True') {
            if (data.userId !== userId) {
                online_div.innerHTML = 'writing...';
            }
        }

        else if (data.writing === 'False') {
            if (data.userId !== userId) {
                setTimeout(() => {
                    online_div.innerHTML = 'online';            
                }, 1000);
            }
        }

        else if (data.last_seen === 'True') {
            let hour = data.last_seen_hour;
            let minute = data.last_seen_minute;
            let format = hour >= 12 ? 'p.m.' : 'a.m.'; 

            // Find current hour in AM-PM Format
            hour = hour % 12; 

            // To display "0" as "12"
            hour = hour ? hour : 12; 
            minute = minute < 10 ? '0' + minute : minute;
            // document.getElementById("change").innerHTML = 
            //   hours + ':' + minutes + ' ' + newformat;
            // obtener la fecha y la hora
            let last_seen_time = hour + ':' + minute + ' ' + format;

            online_div.innerHTML = "last seen " + "today " +"at "+ last_seen_time;
            
        }
        
        else {

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
                html += '<small class="ml-1 time">' + now + '</small>';
                html += '</div></div></div></div>';


            document.querySelector('#chat_area').innerHTML += html;
            scrollToBottom()
        }    
    }
    function scrollToBottom() {
    
        const objDiv = document.querySelector('#chat_area');
    
        objDiv.scrollTop = objDiv.scrollHeight;
    
    }
        
    
    scrollToBottom()
        
