const chatSocket = new WebSocket('ws://localhost:8000/ws/api/chat/' + chatId + '/');
console.log('WebSocket URL: ', 'ws://localhost:8000/ws/api/chat/' + chatId + '/');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data['message'];
    // Добавьте логику для отображения сообщения на странице
    console.log('Received message: ', message);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // Если нажата клавиша Enter
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    }
};

