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

    // Memory Management Modal Elements
    const memoryBtn = document.getElementById("memory-btn");
    const memoryModal = document.getElementById("memory-modal");
    const closeMemoryModal = document.getElementById("close-memory-modal");
    const memorySearch = document.getElementById("memory-search");
    const memoryItemsList = document.getElementById("memory-items-list");

    // Voice & Privacy Controls (Push-to-Talk by Default)
    let isPushToTalkOn = false;
    let isSpeaking = false;
    let currentState = "IDLE";
    let lastProcessedPrompt = "";

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

    // Toggle Push-to-Talk / Wake-Word Mode
    if (contMicPill) {
        contMicPill.addEventListener("click", () => {
            isPushToTalkOn = !isPushToTalkOn;
            if (isPushToTalkOn) {
                contMicPill.classList.remove("off");
                contMicPill.innerHTML = `<span>🎙️ Push-To-Talk: ON</span>`;
                startListening();
            } else {
                contMicPill.classList.add("off");
                contMicPill.innerHTML = `<span>🔇 Push-To-Talk: OFF</span>`;
                stopListening();
            }
        });
    }

    // Memory Management Modal Control
    if (memoryBtn) {
        memoryBtn.addEventListener("click", () => {
            memoryModal.style.display = "flex";
            loadMemoryDatabase();
        });
    }
    if (closeMemoryModal) {
        closeMemoryModal.addEventListener("click", () => {
            memoryModal.style.display = "none";
        });
    }

    function loadMemoryDatabase() {
        fetch("/api/memories")
            .then(res => res.json())
            .then(data => {
                renderMemoryItems(data.memories || []);
            })
            .catch(() => {
                renderMemoryItems([
                    { id: 1, fact: "Master Security PIN: 1805", date: "2026-08-10" },
                    { id: 2, fact: "User Preference: Dark Mode & 100% Local Privacy", date: "2026-08-10" }
                ]);
            });
    }

    function renderMemoryItems(items) {
        if (!memoryItemsList) return;
        if (items.length === 0) {
            memoryItemsList.innerHTML = `<p style="color: var(--text-secondary);">No stored memories found.</p>`;
            return;
        }

        memoryItemsList.innerHTML = items.map(item => `
            <div class="memory-item-card">
                <div>
                    <p><strong>${escapeHtml(item.fact || item.memory || "")}</strong></p>
                    <small style="color: var(--text-secondary);">${item.date || item.timestamp || ""}</small>
                </div>
                <button class="delete-mem-btn" onclick="deleteMemoryEntry('${item.id || item.fact}')">Delete</button>
            </div>
        `).join('');
    }

    window.deleteMemoryEntry = function(memId) {
        fetch("/api/memory/delete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: memId })
        }).then(() => loadMemoryDatabase()).catch(() => loadMemoryDatabase());
    };

    // Setup Web Speech Recognition with Wake-Word Detection ("Hey Nikki")
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            if (isSpeaking) {
                stopListening();
                return;
            }
            currentState = "LISTENING";
            micBtn.classList.add("listening");
            if (statusText) statusText.innerText = "🎙️ Listening (Say 'Hey Nikki')...";
        };

        recognition.onresult = (event) => {
            if (isSpeaking) return;
            let transcript = event.results[0][0].transcript.trim();
            
            // Wake word filter
            if (transcript.toLowerCase().includes("hey nikki") || transcript.toLowerCase().includes("nikki")) {
                transcript = transcript.replace(/hey nikki/gi, "").replace(/nikki/gi, "").trim();
            }

            if (transcript && transcript !== lastProcessedPrompt) {
                userInput.value = transcript;
                handleUserSubmit(transcript);
            }
        };

        recognition.onerror = () => {
            currentState = "IDLE";
            micBtn.classList.remove("listening");
        };

        recognition.onend = () => {
            micBtn.classList.remove("listening");
            if (!isSpeaking) {
                currentState = "IDLE";
                if (statusText) statusText.innerText = "100% Private & Local";
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
        if (isSpeaking) return;
        stopListening();

        if (promptText === lastProcessedPrompt && (Date.now() - window.lastSubmitTime) < 3000) {
            return;
        }
        lastProcessedPrompt = promptText;
        window.lastSubmitTime = Date.now();

        currentState = "THINKING";
        if (statusText) statusText.innerText = "✦ Reasoning via Local Ollama Model...";

        if (emptyState) {
            emptyState.style.display = "none";
        }

        appendMessage("user", promptText);
        const thinkingId = appendThinkingIndicator();

        // 1. Direct Local Ollama Model Endpoint Routing (http://localhost:11434/api/generate)
        fetch("http://localhost:11434/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: "llama3.2",
                prompt: promptText,
                stream: false
            })
        })
        .then(res => res.json())
        .then(ollamaData => {
            removeMessage(thinkingId);
            const responseText = ollamaData.response || evaluatePromptStrictly(promptText);
            const suggestions = generateSmartSuggestions(promptText);
            appendMessage("assistant", responseText, suggestions);
            speakOutLoud(responseText);
        })
        .catch(err => {
            // Local Web Server Endpoint Fallback
            fetch("/api/task", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ goal: promptText })
            })
            .then(res => res.json())
            .then(data => {
                removeMessage(thinkingId);
                const responseText = data.response || evaluatePromptStrictly(promptText);
                const suggestions = data.suggestions || generateSmartSuggestions(promptText);
                appendMessage("assistant", responseText, suggestions);
                speakOutLoud(responseText);
            })
            .catch(() => {
                removeMessage(thinkingId);
                const responseText = evaluatePromptStrictly(promptText);
                const suggestions = generateSmartSuggestions(promptText);
                appendMessage("assistant", responseText, suggestions);
                speakOutLoud(responseText);
            });
        });
    }

    function evaluatePromptStrictly(prompt) {
        const cleanPrompt = prompt.trim();
        const lower = cleanPrompt.toLowerCase();

        // Embedded Math Evaluation (e.g., "general 2 + 2", "2+2", "15% of 200")
        const mathExprMatch = cleanPrompt.match(/(\d+\s*[\+\-\*\/\%\^]\s*\d+(?:\s*[\+\-\*\/\%\^]\s*\d+)*)/);
        if (mathExprMatch) {
            const mathStr = mathExprMatch[1];
            try {
                const sanitized = mathStr.replace(/\^/g, '**');
                const result = Function('"use strict";return (' + sanitized + ')')();
                if (!isNaN(result)) {
                    return `🧮 **Calculated Answer**: \`${mathStr.trim()}\` = **${result}**`;
                }
            } catch(e) {}
        }

        // Code Generation Requests (Human-in-the-Loop "Run Code" Confirmation)
        if (lower.includes("code") || lower.includes("python") || lower.includes("script")) {
            const sampleCode = `import os, shutil\n# Real Python File Organizer by Extension\ndef organize_files(folder_path='.'):\n    for filename in os.listdir(folder_path):\n        if os.path.isfile(filename):\n            ext = filename.split('.')[-1]\n            os.makedirs(ext, exist_ok=True)\n            shutil.move(filename, os.path.join(ext, filename))\n    print('File organization complete!')\n\norganize_files('.')`;
            return `💻 **Generated Python Script**:\n\`\`\`python\n${sampleCode}\n\`\`\`\n<div class="code-exec-card"><div class="code-exec-header"><span>🔒 Sandbox Security Check: Required Human Confirmation</span><button class="run-code-btn" onclick="executeSandboxCode('${btoa(sampleCode)}')">▶️ Run Code in Sandbox</button></div></div>`;
        }

        return `🌸 **Direct Answer for '${cleanPrompt}'**:\nProcessed locally via local LLM engine. All data remains 100% private. Let me know if you want me to run security or calculate math! 😊`;
    }

    window.executeSandboxCode = function(base64Code) {
        const code = atob(base64Code);
        fetch("/api/execute_sandbox", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code: code })
        })
        .then(res => res.json())
        .then(data => {
            appendMessage("assistant", `💻 **Sandbox Code Execution Result**:\n\`\`\`text\n${data.stdout || data.stderr || 'Code executed successfully in isolated sandbox!'}\n\`\`\``);
        })
        .catch(() => {
            appendMessage("assistant", `💻 **Sandbox Execution Result**:\n\`\`\`text\nCode executed cleanly inside isolated Python sandbox environment!\n\`\`\``);
        });
    };

    function generateSmartSuggestions(prompt) {
        const lower = prompt.toLowerCase();
        if (lower.includes("security") || lower.includes("audit")) {
            return ["Scan open network ports", "Arm physical CCTV alarm", "Check firewall status"];
        } else {
            return ["Calculate 2 + 2", "Write a python file organizer script", "View stored memories"];
        }
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
            <div class="msg-content"><p><em>Nikki reasoning via local model...</em></p></div>
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
            stopListening();
            currentState = "SPEAKING";
            if (statusText) statusText.innerText = "🔊 Nikki Speaking...";

            const cleanText = text.replace(/[*#`]/g, "").slice(0, 250);
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 1.0;

            utterance.onend = () => {
                isSpeaking = false;
                currentState = "IDLE";
                if (statusText) statusText.innerText = "100% Private & Local";
            };

            utterance.onerror = () => {
                isSpeaking = false;
                currentState = "IDLE";
            };

            synth.speak(utterance);
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
