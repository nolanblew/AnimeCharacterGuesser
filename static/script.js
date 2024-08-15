document.addEventListener('DOMContentLoaded', function() {
    const startGameButton = document.getElementById('start-game');
    const animeInput = document.getElementById('anime-search');
    const animeSuggestions = document.getElementById('anime-suggestions');
    const spinner = document.getElementById('spinner');
    const clearButton = document.getElementById('clear-anime');

    if (startGameButton && animeInput && animeSuggestions && spinner && clearButton) {
        let selectedAnime = '';
        let selectedAnimeId = null;

        animeInput.addEventListener('input', debounce(function(event) {
            const searchTerm = event.target.value.trim();
            if (searchTerm.length > 2) {
                fetch('/search_anime', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ search_term: searchTerm }),
                })
                .then(response => response.json())
                .then(data => {
                    displaySuggestions(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            } else {
                animeSuggestions.style.display = 'none';
            }
        }, 300));

        // Log for debugging
        console.log('Event listener added to animeInput');

        animeSuggestions.addEventListener('click', function(e) {
            const li = e.target.closest('li');
            if (li) {
                selectedAnime = li.querySelector('h6').textContent;
                selectedAnimeId = li.dataset.animeId;
                animeInput.value = selectedAnime;
                animeInput.readOnly = true;
                animeSuggestions.style.display = 'none';
                startGameButton.disabled = false;
                clearButton.style.display = 'block';
            }
        });

        clearButton.addEventListener('click', function() {
            animeInput.value = '';
            animeInput.readOnly = false;
            selectedAnime = '';
            selectedAnimeId = null;
            startGameButton.disabled = true;
            clearButton.style.display = 'none';
            animeInput.focus();
        });

        animeInput.addEventListener('focus', function() {
            if (selectedAnime) {
                clearButton.style.display = 'block';
            }
        });

        animeInput.addEventListener('blur', function() {
            if (!selectedAnime) {
                clearButton.style.display = 'none';
            }
        });

        startGameButton.addEventListener('click', function() {
            if (selectedAnime && selectedAnimeId) {
                startGame(selectedAnime, selectedAnimeId);
                // Disable input and button, show spinner
                animeInput.disabled = true;
                startGameButton.disabled = true;
                startGameButton.style.display = 'none';
                spinner.style.display = 'inline-block';
                clearButton.style.display = 'none';
            }
        });
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function displaySuggestions(animes) {
        animeSuggestions.innerHTML = '';
        if (animes.length > 0) {
            animes.forEach(anime => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex align-items-center';
                li.innerHTML = `
                    <div class="d-flex align-items-center">
                        <img src="${anime.coverImage}" alt="${anime.title}" class="me-3" style="width: 50px; height: 70px; object-fit: cover;">
                        <div class="flex-grow-1">
                            <h6 class="mb-0">${anime.title}</h6>
                            <small class="text-muted">${anime.season} ${anime.seasonYear} | ${anime.format}</small>
                        </div>
                    </div>
                `;
                li.dataset.animeId = anime.id;
                animeSuggestions.appendChild(li);
            });
            animeSuggestions.style.display = 'block';
        } else {
            animeSuggestions.style.display = 'none';
        }
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

        // Show loading screen
        showLoadingScreen();

        // Fetch and display the initial greeting
        fetch('/get_initial_greeting')
            .then(response => response.json())
            .then(data => {
                // Hide loading screen
                hideLoadingScreen();
                if (data.message) {
                    addMessage('character', data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching initial greeting:', error);
                // Hide loading screen even if there's an error
                hideLoadingScreen();
            });
    }
});

function showLoadingScreen() {
    const loadingScreen = document.createElement('div');
    loadingScreen.id = 'loading-screen';
    loadingScreen.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    loadingScreen.style.position = 'fixed';
    loadingScreen.style.top = '0';
    loadingScreen.style.left = '0';
    loadingScreen.style.width = '100%';
    loadingScreen.style.height = '100%';
    loadingScreen.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
    loadingScreen.style.display = 'flex';
    loadingScreen.style.justifyContent = 'center';
    loadingScreen.style.alignItems = 'center';
    loadingScreen.style.zIndex = '1000';
    document.body.appendChild(loadingScreen);
}

function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.remove();
    }
}

function startGame(animeName, animeId, animeDescription) {
    fetch('/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ anime_name: animeName, anime_id: animeId, anime_description: animeDescription }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/select_character';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const characterGrid = document.getElementById('character-grid');
    if (characterGrid) {
        characterGrid.addEventListener('click', function(e) {
            const card = e.target.closest('.character-card');
            if (card) {
                const characterName = card.dataset.characterName;
                const characterDescription = card.dataset.characterDescription;
                selectCharacter(characterName, characterDescription);
            }
        });
    }
});

function selectCharacter(characterName, characterDescription) {
    fetch('/set_character', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ character_name: characterName, character_description: characterDescription }),
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
        userInput.style.height = '38px'; // Reset to initial height
        fetchResponse(message);
    }
}

function autoResizeTextarea() {
    const textarea = document.getElementById('user-input');
    textarea.style.height = '38px'; // Reset to initial height
    textarea.style.height = textarea.scrollHeight + 'px';
}

document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    if (userInput) {
        userInput.addEventListener('input', autoResizeTextarea);
        userInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault(); // Prevent default newline
                sendMessage();
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
    scrollToBottom();
}

function fetchResponse(message) {
    // Delay adding the typing indicator by 1 second
    setTimeout(() => {
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
            if (data.response) {
                addMessage('character', data.response);
            } else {
                addMessage('character', 'Sorry, there was an error processing your message.');
            }
            
            if (data.correct_guess) {
                addMessage('system', `Congratulations! You've correctly guessed the character: ${data.character_name} from ${data.anime_name}`);
                showStartAgainButton();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator(typingIndicator);
            addMessage('character', 'Sorry, there was an error processing your message.');
        });
    }, 1000); // 1 second delay
}

function showStartAgainButton() {
    const inputGroup = document.querySelector('.input-group');
    inputGroup.style.display = 'none';

    const startAgainButton = document.createElement('button');
    startAgainButton.textContent = 'Start Again';
    startAgainButton.classList.add('btn', 'btn-primary', 'btn-lg', 'mt-4', 'mb-3', 'px-4', 'py-2', 'd-block', 'mx-auto');
    startAgainButton.addEventListener('click', () => {
        window.location.href = '/';
    });

    const chatContainer = document.querySelector('.chat-container');
    chatContainer.parentNode.insertBefore(startAgainButton, chatContainer.nextSibling);
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
