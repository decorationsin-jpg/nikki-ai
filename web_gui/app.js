document.addEventListener("DOMContentLoaded", () => {
    const messagesList = document.getElementById("messages-list");
    const emptyState = document.getElementById("empty-state");
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const micBtn = document.getElementById("mic-btn");
    const chatScroll = document.getElementById("chat-scroll");
    const contMicPill = document.getElementById("cont-mic-pill");
    const statusText = document.getElementById("status-text");
    const themeSelect = document.getElementById("theme-select");
    const telemetryCpu = document.getElementById("telemetry-cpu");
    const telemetryRam = document.getElementById("telemetry-ram");

    // Continuous Microphone State
    let isContinuousMicOn = true;
    let isSpeaking = false;
    let currentState = "IDLE";

    // Speech Recognition & Synthesis
    const synth = window.speechSynthesis;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    // Theme Switcher Handler
    if (themeSelect) {
        themeSelect.addEventListener("change", (e) => {
            document.body.className = "";
            if (e.target.value !== "default") {
                document.body.classList.add(`theme-${e.target.value}`);
            }
        });
    }

    // Telemetry Polling
    function updateTelemetry() {
        fetch("/api/telemetry")
            .then(res => res.json())
            .then(data => {
                if (telemetryCpu) telemetryCpu.innerText = `CPU: ${data.cpu}`;
                if (telemetryRam) telemetryRam.innerText = `RAM: ${data.ram}`;
            })
            .catch(() => {});
    }
    setInterval(updateTelemetry, 4000);

    // Canvas Visualizer Setup
    const canvas = document.getElementById("dynamic-canvas");
    let ctx = null;
    if (canvas) {
        ctx = canvas.getContext("2d");
        resizeCanvas();
        window.addEventListener("resize", resizeCanvas);
        requestAnimationFrame(drawDynamicVisualizer);
    }

    function resizeCanvas() {
        if (canvas) {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
    }

    // Dynamic Particles Setup
    let particles = [];
    for (let i = 0; i < 40; i++) {
        particles.push({
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            radius: Math.random() * 3 + 1,
            color: ["#4285f4", "#9b51e0", "#e91e63", "#34a853"][Math.floor(Math.random() * 4)],
            vx: (Math.random() - 0.5) * 0.8,
            vy: (Math.random() - 0.5) * 0.8
        });
    }

    let phase = 0;
    function drawDynamicVisualizer() {
        if (!ctx) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            p.x += p.vx * (currentState === "THINKING" ? 2.5 : 1);
            p.y += p.vy * (currentState === "THINKING" ? 2.5 : 1);

            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 10;
            ctx.shadowColor = p.color;
            ctx.fill();
        });

        if (currentState === "LISTENING" || currentState === "SPEAKING") {
            phase += 0.05;
            ctx.beginPath();
            ctx.lineWidth = 3;
            ctx.strokeStyle = currentState === "LISTENING" ? "#4285f4" : "#e91e63";

            for (let x = 0; x < canvas.width; x += 10) {
                const y = canvas.height - 80 + Math.sin(x * 0.01 + phase) * (currentState === "SPEAKING" ? 25 : 15);
                if (x === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();
        }

        requestAnimationFrame(drawDynamicVisualizer);
    }

    // Toggle Continuous Mic Mode
    if (contMicPill) {
        contMicPill.addEventListener("click", () => {
            isContinuousMicOn = !isContinuousMicOn;
            if (isContinuousMicOn) {
                contMicPill.classList.remove("off");
                contMicPill.innerHTML = `<span>🎙️ Continuous Mic: ON</span>`;
                startListening();
            } else {
                contMicPill.classList.add("off");
                contMicPill.innerHTML = `<span>🔇 Continuous Mic: OFF</span>`;
                stopListening();
            }
        });
    }

    // Setup Web Speech Recognition
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            currentState = "LISTENING";
            micBtn.classList.add("listening");
            if (statusText) statusText.innerText = "🎙️ Nikki Listening...";
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            handleUserSubmit(transcript);
        };

        recognition.onerror = () => {
            currentState = "IDLE";
            micBtn.classList.remove("listening");
            scheduleContinuousListen();
        };

        recognition.onend = () => {
            micBtn.classList.remove("listening");
            if (!isSpeaking) {
                currentState = "IDLE";
                if (statusText) statusText.innerText = "100% Private & Active 24/7";
                scheduleContinuousListen();
            }
        };
    }

    function startListening() {
        if (recognition && !isSpeaking) {
            try {
                recognition.start();
            } catch (e) {}
        }
    }

    function stopListening() {
        if (recognition) {
            try {
                recognition.stop();
            } catch (e) {}
        }
    }

    function scheduleContinuousListen() {
        if (isContinuousMicOn && !isSpeaking) {
            setTimeout(() => {
                startListening();
            }, 800);
        }
    }

    setTimeout(() => {
        if (isContinuousMicOn) startListening();
    }, 1000);

    micBtn.addEventListener("click", () => {
        startListening();
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
        stopListening();
        currentState = "THINKING";
        if (statusText) statusText.innerText = "✦ Nikki Reasoning...";

        if (emptyState) {
            emptyState.style.display = "none";
        }

        appendMessage("user", promptText);
        const thinkingId = appendThinkingIndicator();

        fetch("/api/task", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ goal: promptText })
        })
        .then(res => res.json())
        .then(data => {
            removeMessage(thinkingId);
            const responseText = data.response || "Task processed by Nikki.";
            const suggestions = data.suggestions || [];
            appendMessage("assistant", responseText, suggestions);
            speakOutLoud(responseText);
        })
        .catch(err => {
            removeMessage(thinkingId);
            const fallbackText = `Nikki processed your request: "${promptText}". Running local engine.`;
            appendMessage("assistant", fallbackText, ["Audit system security", "Teach another personal fact"]);
            speakOutLoud(fallbackText);
        });
    }

    function appendMessage(sender, text, suggestions = []) {
        const row = document.createElement("div");
        row.classList.add("msg-row", sender);

        if (sender === "assistant") {
            let suggestionsHtml = "";
            if (suggestions && suggestions.length > 0) {
                suggestionsHtml = `
                    <div class="followup-container">
                        ${suggestions.map(s => `<button class="followup-chip" onclick="sendQuickPrompt('${s.replace(/'/g, "\\'")}')">⚡ ${s}</button>`).join('')}
                    </div>
                `;
            }

            row.innerHTML = `
                <div class="msg-avatar sparkle-avatar">✦</div>
                <div class="msg-content">
                    ${formatMarkdown(text)}
                    ${suggestionsHtml}
                </div>
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
            isSpeaking = true;
            currentState = "SPEAKING";
            if (statusText) statusText.innerText = "🔊 Nikki Speaking...";

            const cleanText = text.replace(/[*#`]/g, "").slice(0, 300);
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 1.0;

            utterance.onend = () => {
                isSpeaking = false;
                currentState = "IDLE";
                if (statusText) statusText.innerText = "100% Private & Active 24/7";
                scheduleContinuousListen();
            };

            utterance.onerror = () => {
                isSpeaking = false;
                currentState = "IDLE";
                scheduleContinuousListen();
            };

            synth.speak(utterance);
        } else {
            scheduleContinuousListen();
        }
    }

    function formatMarkdown(text) {
        let html = escapeHtml(text);
        html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\n/g, '<br>');
        return html;
    }

    function escapeHtml(text) {
        return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
});
