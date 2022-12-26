const userId = JSON.parse(document.getElementById('userId').textContent);
let userUnreadNotifications = JSON.parse(document.getElementById('userUnreadNotifications').textContent);

const url1 = `ws://${window.location.host}/ws/chatapp/notifications/${userId}`;

let noti = document.getElementById('notifications');
noti.innerHTML = userUnreadNotifications;

if (userUnreadNotifications === 0) {
    noti.innerHTML = '';

}

const notificationsSocket1 = new WebSocket(url1);

notificationsSocket1.onmessage = function (e) {
    const data = JSON.parse(e.data);
    // console.log(data);

    let chatDiv = document.querySelectorAll('.chat-div');
    let lastMessage = document.getElementById('last-message-' + data.receive_chat_id);
    let lastMessageTime = document.getElementById('last-message-time-' + data.receive_chat_id);
    let unreadMessages = document.getElementById('unread_messages-' + data.receive_chat_id);

    for (let i = 0; i < chatDiv.length; i++) {
        if (+chatDiv[i].id === data.receive_chat_id) {
            chatDiv[i].style.order = 1;
        }

        else {
            console.log(chatDiv[i].getAttribute("name"));
            chatDiv[i].style.order = +chatDiv[i].getAttribute("name") + 1;
        };
    };

    if (+unreadMessages.innerHTML === 0) {
        let div_0 = document.getElementById('div-0-' + data.receive_chat_id);
        div_0.classList.add('bg-success', 'text-center', 'rounded-circle');
        div_0.style.height = '19px';
        div_0.style.width = '19px';
    }

    unreadMessages.innerHTML = data.chat_unread_messages;
    lastMessage.innerHTML = data.chat_last_message;
    lastMessageTime.innerHTML = data.chat_last_message_time;

    userUnreadNotifications = userUnreadNotifications + 1;
    noti.innerHTML = userUnreadNotifications;

};

