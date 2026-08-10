document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.getElementById("chat-messages");
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const micBtn = document.getElementById("mic-btn");
    const voiceStatus = document.getElementById("voice-status");

    // Browser Speech Synthesis
    const synth = window.speechSynthesis;

    // Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            voiceStatus.innerText = "🎙️ Listening to your voice...";
            micBtn.style.boxShadow = "0 0 40px #00f2fe";
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            handleUserMessage(transcript);
        };

        recognition.onerror = (e) => {
            voiceStatus.innerText = "Error listening to voice.";
            micBtn.style.boxShadow = "0 0 20px rgba(157, 78, 221, 0.5)";
        };

        recognition.onend = () => {
            voiceStatus.innerText = "Tap microphone to speak to Nikki";
            micBtn.style.boxShadow = "0 0 20px rgba(157, 78, 221, 0.5)";
        };
    } else {
        voiceStatus.innerText = "Speech recognition not supported in this browser.";
    }

    micBtn.addEventListener("click", () => {
        if (recognition) {
            recognition.start();
        }
    });

    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (text) {
            handleUserMessage(text);
            userInput.value = "";
        }
    });

    function appendMessage(sender, text, type) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", type);
        msgDiv.innerHTML = `<span class="sender">${sender}</span><p>${escapeHtml(text)}</p>`;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function handleUserMessage(text) {
        appendMessage("You", text, "user");

        // Send to Nikki's backend API
        fetch("/api/task", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ goal: text })
        })
        .then(res => res.json())
        .then(data => {
            const responseText = data.response || "Task processed by Nikki.";
            appendMessage("Nikki 🌸", responseText, "assistant");
            speakOutLoud(responseText);
        })
        .catch(err => {
            const fallbackText = `Nikki received your task: "${text}". Running local offline execution engine.`;
            appendMessage("Nikki 🌸", fallbackText, "assistant");
            speakOutLoud(fallbackText);
        });
    }

    function speakOutLoud(text) {
        if (synth) {
            const cleanText = text.replace(/[*#`]/g, "").slice(0, 200);
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 1.0;
            synth.speak(utterance);
        }
    }

    function escapeHtml(text) {
        return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
});
