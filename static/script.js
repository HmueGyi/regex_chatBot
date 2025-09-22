const messages = document.getElementById("messages");
const userInput = document.getElementById("userInput");
const synth = window.speechSynthesis;
const listeningBtn = document.getElementById("ListeningBtn");

// Send user message to chatbot
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage("user", message);
    userInput.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });
        const data = await response.json();
        const botResponse = data.response;

        addMessage("bot", botResponse);
        speakText(botResponse);
    } catch (error) {
        addMessage("bot", "I'm having trouble connecting to the server.");
    }

    messages.scrollTop = messages.scrollHeight;
}

// Display messages in chat
function addMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.className = sender;
    messageDiv.innerHTML = text.replace(/\n/g, "<br>");
    messages.appendChild(messageDiv);
}

// Text-to-Speech
function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    const voices = synth.getVoices();
    utterance.voice = voices.find(voice => voice.name.includes("Female")) || voices[0];
    utterance.rate = 1;
    utterance.pitch = 1;
    synth.speak(utterance);
}

// Speech Recognition
listeningBtn.addEventListener("click", () => {
    startListening();
});

function startListening() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        addMessage("bot", "❌ Your browser does not support speech recognition.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        sendMessage(); // this will add the user message once
    };
    
    recognition.onerror = (event) => {
        addMessage("bot", "❌ Error during speech recognition: " + event.error);
    };
}
