const room_name = 'notifications'

let count = 1
const notificationsSocket = new WebSocket (
    `ws://${window.location.host}/ws/chatapp/notifications/${room_name}`
)

notificationsSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
        
    document.querySelector('#notifications').innerHTML = count;    
    count = count + 1;
}