document.addEventListener('DOMContentLoaded', function() {
    const startGameButton = document.getElementById('start-game');
    if (startGameButton) {
        startGameButton.addEventListener('click', function() {
            window.location.href = '/chat';
        });
    }

    const sendMessageButton = document.getElementById('send-message');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.querySelector('.chat-container');

    if (sendMessageButton && userInput && chatContainer) {
        sendMessageButton.addEventListener('click', function() {
            const message = userInput.value.trim();
            if (message) {
                addMessage('user', message);
                userInput.value = '';
                // Here you would typically send the message to the server and get a response
                // For now, we'll just simulate a response after a short delay
                setTimeout(() => {
                    addMessage('character', 'This is a placeholder response from the character.');
                }, 1000);
            }
        });

        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessageButton.click();
            }
        });
    }
});

function addMessage(sender, message) {
    const chatContainer = document.querySelector('.chat-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
