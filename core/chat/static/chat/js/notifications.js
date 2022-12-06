const userId = JSON.parse(document.getElementById('userId').textContent);
let userUnreadNotifications = JSON.parse(document.getElementById('userUnreadNotifications').textContent);

const url1 = `ws://${window.location.host}/ws/chatapp/notifications/${userId}`;

document.getElementById('notifications').innerHTML = userUnreadNotifications;

if (userUnreadNotifications === 0) {
    document.getElementById('notifications').innerHTML = '';

}

const notificationsSocket1 = new WebSocket (url1);

notificationsSocket1.onmessage = function (e) {
    const data = JSON.parse(e.data);
        
    userUnreadNotifications = userUnreadNotifications + 1;
    document.getElementById('notifications').innerHTML = userUnreadNotifications;

};

