const messages = document.getElementById("messages");
const userInput = document.getElementById("userInput");
const synth = window.speechSynthesis;

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

function addMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.className = sender;
    messageDiv.innerHTML = text.replace(/\n/g, "<br>");
    messages.appendChild(messageDiv);
}

function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    const voices = synth.getVoices();
    utterance.voice = voices.find(voice => voice.name.includes("Female")) || voices[1];
    utterance.rate = 1;
    utterance.pitch = 1;
    synth.speak(utterance);
}

function startSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        addMessage("bot", "Sorry, your browser does not support speech recognition.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false; // Only final results
    recognition.maxAlternatives = 1;

    try {
        recognition.start();
    } catch (err) {
        addMessage("bot", "Could not start speech recognition: " + err.message);
        return;
    }

    recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript.trim();
        if (speechResult) {
            userInput.value = speechResult;
            sendMessage();
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        addMessage("bot", "Speech recognition error: " + event.error);
    };

    recognition.onend = () => {
        console.log("Speech recognition ended.");
    };
}

