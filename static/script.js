document.addEventListener('DOMContentLoaded', function() {
    const startGameButton = document.getElementById('start-game');
    const animeInput = document.getElementById('anime-search');
    if (startGameButton && animeInput) {
        startGameButton.addEventListener('click', function() {
            const animeName = animeInput.value.trim();
            if (animeName) {
                startGame(animeName);
            }
        });
    }

    const sendMessageButton = document.getElementById('send-message');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.querySelector('.chat-container');

    if (sendMessageButton && userInput && chatContainer) {
        sendMessageButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});

function startGame(animeName) {
    fetch('/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ anime_name: animeName }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/chat';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (message) {
        addMessage('user', message);
        userInput.value = '';
        fetchResponse(message);
    }
}

function addMessage(sender, message) {
    const chatContainer = document.querySelector('.chat-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
    scrollToBottom();
}

function fetchResponse(message) {
    const typingIndicator = addTypingIndicator();

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        removeTypingIndicator(typingIndicator);
        addMessage('character', data.message);
        
        if (data.correct_guess) {
            addMessage('system', `Congratulations! You've correctly guessed the character: ${data.character_name} from ${data.anime_name}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        removeTypingIndicator(typingIndicator);
        addMessage('character', 'Sorry, there was an error processing your message.');
    });
}

function addTypingIndicator() {
    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('message', 'character', 'typing');
    typingIndicator.textContent = 'Character is typing...';
    const chatContainer = document.querySelector('.chat-container');
    chatContainer.appendChild(typingIndicator);
    scrollToBottom();
    return typingIndicator;
}

function removeTypingIndicator(typingIndicator) {
    if (typingIndicator && typingIndicator.parentNode) {
        typingIndicator.parentNode.removeChild(typingIndicator);
    }
}

function scrollToBottom() {
    const chatContainer = document.querySelector('.chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
