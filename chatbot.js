const socket = new WebSocket('ws://localhost:8000'); // Change this to your server's WebSocket address

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const chatBox = document.getElementById('chat-box');
    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot');
    botMessage.innerText = data.text;
    chatBox.appendChild(botMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Convert the bot's reply to speech if the input was voice-based
    if (data.voice) {
        speak(data.text);
    }
};

socket.onclose = function(event) {
    console.log('Connection closed:', event);
};

socket.onerror = function(error) {
    console.log('WebSocket Error:', error);
};

function sendMessage(isVoice = false) {
    const userInput = document.getElementById('user-input');
    const message = userInput.value;
    if (message.trim() !== '') {
        const chatBox = document.getElementById('chat-box');
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user');
        userMessage.innerText = message;
        chatBox.appendChild(userMessage);
        chatBox.scrollTop = chatBox.scrollHeight;

        socket.send(JSON.stringify({text: message, voice: isVoice}));
        userInput.value = '';
    }
}

function startListening() {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Your browser does not support speech recognition. Please use Google Chrome.');
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = function(event) {
        const userInput = document.getElementById('user-input');
        userInput.value = event.results[0][0].transcript;
        sendMessage(true); // Send with voice flag set to true
    };

    recognition.start();
}

function speak(text) {
    const synth = window.speechSynthesis;
    const utterThis = new SpeechSynthesisUtterance(text);
    synth.speak(utterThis);
}

// Send keep-alive messages every 30 seconds to keep the connection alive
setInterval(() => {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({type: 'ping'}));  // Change 'ping' message format
    }
}, 30000);
