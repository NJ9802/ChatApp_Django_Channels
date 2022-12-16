const userId = JSON.parse(document.getElementById('userId').textContent);
let userUnreadNotifications = JSON.parse(document.getElementById('userUnreadNotifications').textContent);

const url1 = `ws://${window.location.host}/ws/chatapp/notifications/${userId}`;

let noti = document.getElementById('notifications');
noti.innerHTML = userUnreadNotifications;

if (userUnreadNotifications === 0) {
    noti.innerHTML = '';

}

const notificationsSocket1 = new WebSocket (url1);

notificationsSocket1.onmessage = function (e) {
    const data = JSON.parse(e.data);
        
    userUnreadNotifications = userUnreadNotifications + 1;
    noti.innerHTML = userUnreadNotifications;

};

