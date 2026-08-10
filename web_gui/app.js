document.addEventListener("DOMContentLoaded", () => {
    const messagesList = document.getElementById("messages-list");
    const emptyState = document.getElementById("empty-state");
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const micBtn = document.getElementById("mic-btn");
    const chatScroll = document.getElementById("chat-scroll");

    // Speech Synthesis & Recognition
    const synth = window.speechSynthesis;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            micBtn.style.color = "#4285f4";
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            handleUserSubmit(transcript);
        };

        recognition.onend = () => {
            micBtn.style.color = "";
        };
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
            handleUserSubmit(text);
            userInput.value = "";
        }
    });

    window.sendQuickPrompt = function(promptText) {
        handleUserSubmit(promptText);
    };

    function handleUserSubmit(promptText) {
        if (emptyState) {
            emptyState.style.display = "none";
        }

        // Add User Message
        appendMessage("user", promptText);

        // Add Thinking Indicator
        const thinkingId = appendThinkingIndicator();

        // Send to Local API
        fetch("/api/task", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ goal: promptText })
        })
        .then(res => res.json())
        .then(data => {
            removeMessage(thinkingId);
            const responseText = data.response || "Task processed by Nikki.";
            appendMessage("assistant", responseText);
            speakOutLoud(responseText);
        })
        .catch(err => {
            removeMessage(thinkingId);
            const fallbackText = `Nikki processed your request: "${promptText}". Running offline engine.`;
            appendMessage("assistant", fallbackText);
            speakOutLoud(fallbackText);
        });
    }

    function appendMessage(sender, text) {
        const row = document.createElement("div");
        row.classList.add("msg-row", sender);

        if (sender === "assistant") {
            row.innerHTML = `
                <div class="msg-avatar sparkle-avatar">✦</div>
                <div class="msg-content">${formatMarkdown(text)}</div>
            `;
        } else {
            row.innerHTML = `
                <div class="msg-content">${escapeHtml(text)}</div>
            `;
        }

        messagesList.appendChild(row);
        chatScroll.scrollTop = chatScroll.scrollHeight;
    }

    function appendThinkingIndicator() {
        const id = "thinking-" + Date.now();
        const row = document.createElement("div");
        row.id = id;
        row.classList.add("msg-row", "assistant");
        row.innerHTML = `
            <div class="msg-avatar sparkle-avatar">✦</div>
            <div class="msg-content"><p><em>Nikki is reasoning and executing tools...</em></p></div>
        `;
        messagesList.appendChild(row);
        chatScroll.scrollTop = chatScroll.scrollHeight;
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function speakOutLoud(text) {
        if (synth) {
            const cleanText = text.replace(/[*#`]/g, "").slice(0, 200);
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 1.0;
            synth.speak(utterance);
        }
    }

    function formatMarkdown(text) {
        let html = escapeHtml(text);
        // Code Blocks
        html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        // Bold
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Line breaks
        html = html.replace(/\n/g, '<br>');
        return html;
    }

    function escapeHtml(text) {
        return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
});
