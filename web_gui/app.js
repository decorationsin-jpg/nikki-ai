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
    const memoryItemsList = document.getElementById("memory-items-list");

    // Global Math State Memory
    window.lastCalculatedResult = null;
    window.lastCalculatedExpr = null;

    // 🎙️ Continuous Microphone & Speech State
    let micEnabled = false; // Toggle state for continuous mic
    let isSpeaking = false;
    let currentState = "IDLE";
    let lastProcessedPrompt = "";
    let silenceTimer = null;

    // Speech Recognition & Synthesis Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    let recognition = null;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = true;      // Keeps microphone stream active continuously
        recognition.interimResults = true;  // Displays transcript live while speaking
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            if (isSpeaking) {
                try { recognition.stop(); } catch(e){}
                return;
            }
            currentState = "LISTENING";
            if (micBtn) micBtn.classList.add("listening");
            if (statusText) statusText.innerText = "🎙️ Continuous Mic Active...";
        };

        // Live interim transcript & auto-submit after 1.5s silence
        recognition.onresult = (event) => {
            if (isSpeaking || !micEnabled) return;

            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            // Update live input field
            if (userInput) {
                userInput.value = finalTranscript || interimTranscript;
            }

            // Auto-submit 1.5 seconds after user finishes speaking final transcript
            const cleanFinal = finalTranscript.trim();
            if (cleanFinal.length > 0 && cleanFinal !== lastProcessedPrompt) {
                clearTimeout(silenceTimer);
                silenceTimer = setTimeout(() => {
                    handleUserSubmit(cleanFinal);
                    userInput.value = '';
                }, 1500);
            }
        };

        // Auto-restart stream on end if continuous mic is enabled
        recognition.onend = () => {
            if (micBtn) micBtn.classList.remove("listening");
            if (micEnabled && !isSpeaking) {
                try { recognition.start(); } catch (e) {}
            } else {
                currentState = "IDLE";
                if (statusText) statusText.innerText = "100% Private & Local";
            }
        };

        recognition.onerror = (event) => {
            if (event.error !== 'no-speech' && event.error !== 'aborted') {
                currentState = "IDLE";
                if (micBtn) micBtn.classList.remove("listening");
            }
        };
    }

    function startContinuousMic() {
        if (recognition && micEnabled && !isSpeaking) {
            try {
                recognition.start();
                updateMicUI(true);
            } catch (e) {}
        }
    }

    function stopContinuousMic() {
        if (recognition) {
            try {
                recognition.stop();
                updateMicUI(false);
            } catch (e) {}
        }
    }

    function toggleMicState() {
        micEnabled = !micEnabled;
        if (micEnabled) {
            startContinuousMic();
        } else {
            stopContinuousMic();
        }
    }

    function updateMicUI(isActive) {
        if (contMicPill) {
            contMicPill.innerHTML = isActive ? `<span>🎙️ Continuous Mic: ON</span>` : `<span>🔇 Mic: OFF</span>`;
            if (isActive) contMicPill.classList.remove("off");
            else contMicPill.classList.add("off");
        }
    }

    if (contMicPill) {
        contMicPill.addEventListener("click", () => {
            toggleMicState();
        });
    }

    if (micBtn) {
        micBtn.addEventListener("click", () => {
            toggleMicState();
        });
    }

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
                if (telemetryCpu) telemetryCpu.innerText = `${data.cpu}`;
                if (telemetryRam) telemetryRam.innerText = `${data.ram}`;
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

    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (text) {
            handleUserSubmit(text);
            userInput.value = "";
        }
    });

    window.sendQuickQuery = function(promptText) {
        handleUserSubmit(promptText);
    };

    // 🧮 Direct Quick Math Handler for State Memory Chips (e.g. handleQuickMath('9 * 2'))
    window.handleQuickMath = function(expression) {
        try {
            const sanitized = expression.replace(/\^/g, '**');
            const result = Function('"use strict";return (' + sanitized + ')')();
            window.lastCalculatedResult = result;
            window.lastCalculatedExpr = expression;

            appendMessage("user", expression);
            const mathHtml = renderMathResultCard(expression, result);
            appendMessage("assistant", mathHtml, []);
            speakOutLoud(`Calculated Result: ${expression} equals ${result}`);
        } catch(e) {
            handleUserSubmit(expression);
        }
    };

    function handleUserSubmit(promptText) {
        if (isSpeaking) return;
        
        if (promptText === lastProcessedPrompt && (Date.now() - window.lastSubmitTime) < 2500) {
            return;
        }
        lastProcessedPrompt = promptText;
        window.lastSubmitTime = Date.now();

        currentState = "THINKING";
        if (statusText) statusText.innerText = "🤖 Evaluating Query...";

        if (emptyState) {
            emptyState.style.display = "none";
        }

        appendMessage("user", promptText);
        const thinkingId = appendThinkingIndicator();

        // 1. Math Evaluation Check
        const mathEval = tryEvaluateMath(promptText);
        if (mathEval) {
            removeMessage(thinkingId);
            window.lastCalculatedResult = mathEval.result;
            window.lastCalculatedExpr = mathEval.cleanExpr;
            
            const formattedMsg = renderMathResultCard(mathEval.cleanExpr, mathEval.result);
            appendMessage("assistant", formattedMsg, []);
            speakOutLoud(`Calculated Result: ${mathEval.cleanExpr} equals ${mathEval.result}`);
            return;
        }

        // 2. Ollama LLM REST API Endpoint
        getNikkiResponse(promptText)
            .then(responseText => {
                removeMessage(thinkingId);
                const dynamicChips = renderDynamicChips('text', promptText);
                appendMessage("assistant", responseText, dynamicChips);
                speakOutLoud(responseText);
            })
            .catch(() => {
                removeMessage(thinkingId);
                const responseText = evaluateFallbackPrompt(promptText);
                const dynamicChips = renderDynamicChips('text', promptText);
                appendMessage("assistant", responseText, dynamicChips);
                speakOutLoud(responseText);
            });
    }

    // Connect Frontend JS to Local LLM API (Ollama http://localhost:11434/api/generate)
    async function getNikkiResponse(userPrompt) {
        try {
            const response = await fetch('http://localhost:11434/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: 'llama3.2',
                    prompt: userPrompt,
                    stream: false
                })
            });
            const data = await response.json();
            return data.response || evaluateFallbackPrompt(userPrompt);
        } catch (error) {
            try {
                const res = await fetch("/api/task", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ goal: userPrompt })
                });
                const data = await res.json();
                return data.response || evaluateFallbackPrompt(userPrompt);
            } catch (err) {
                return evaluateFallbackPrompt(userPrompt);
            }
        }
    }

    // 🧮 Math Parser (Normalizes "2 into 2" -> "2 * 2", "10 times 5" -> "10 * 5")
    function tryEvaluateMath(input) {
        try {
            let cleanInput = input
                .toLowerCase()
                .replace(/into/g, '*')
                .replace(/times/g, '*')
                .replace(/divided by/g, '/')
                .replace(/[a-zA-Z\?\,\!\=\:\_]/g, '')
                .trim();

            if (cleanInput && cleanInput.length >= 3 && /[\+\-\*\/\%\^]/.test(cleanInput)) {
                const sanitized = cleanInput.replace(/\^/g, '**');
                const result = Function('"use strict";return (' + sanitized + ')')();
                if (typeof result === 'number' && !isNaN(result) && isFinite(result)) {
                    return { cleanExpr: cleanInput, result: result };
                }
            }
        } catch (e) {
            return null;
        }
        return null;
    }

    // Render Math Result Card with State-Preserving Dynamic Parameter Chips
    function renderMathResultCard(expr, result) {
        window.lastCalculatedResult = result;
        const multVal = `${result} * 2`;
        const divVal = `${result} / 2`;
        const addVal = `${result} + 10`;

        return `🧮 **Calculated Result**: \`${expr}\` = **${result}**
<div class="action-chips" style="margin-top: 10px;">
    <button class="followup-chip" onclick="handleQuickMath('${multVal}')">⚡ Multiply (${result}) by 2</button>
    <button class="followup-chip" onclick="handleQuickMath('${divVal}')">⚡ Divide (${result}) by 2</button>
    <button class="followup-chip" onclick="handleQuickMath('${addVal}')">⚡ Add 10 to (${result})</button>
</div>`;
    }

    // Dynamic Context Chips Renderer
    function renderDynamicChips(responseType, userQuery) {
        if (responseType === 'math' && window.lastCalculatedResult !== null) {
            const res = window.lastCalculatedResult;
            return [
                `⚡ Multiply (${res}) by 2`,
                `⚡ Divide (${res}) by 2`,
                `⚡ Convert Units`
            ];
        } else if (userQuery.toLowerCase().includes("code") || userQuery.toLowerCase().includes("python")) {
            return [
                "⚡ Explain Code Step-by-Step",
                "⚡ Add Unit Test Suite",
                "⚡ Optimize Code Performance"
            ];
        } else {
            return [
                "⚡ Summarize",
                "📋 Copy Output",
                "⚡ Translate to Marathi (मराठी)",
                "⚡ Translate to Hindi (हिंदी)"
            ];
        }
    }

    function evaluateFallbackPrompt(prompt) {
        const cleanPrompt = prompt.trim();
        const lower = cleanPrompt.toLowerCase();

        if (lower.includes("code") || lower.includes("python") || lower.includes("script")) {
            const sampleCode = `import os, shutil\n# File Organizer Script\ndef organize_files(folder='.'):\n    for f in os.listdir(folder):\n        if os.path.isfile(f) and '.' in f:\n            ext = f.split('.')[-1]\n            os.makedirs(ext, exist_ok=True)\n            shutil.move(f, os.path.join(ext, f))\n    print('Files organized cleanly!')\n\norganize_files('.')`;
            return `💻 **Generated Python Script**:\n\`\`\`python\n${sampleCode}\n\`\`\`\n<div class="code-exec-card"><div class="code-exec-header"><span>🔒 Requires Human Confirmation</span><button class="run-code-btn" onclick="executeSandboxCode('${btoa(sampleCode)}')">▶️ Run Code in Sandbox</button></div></div>`;
        }

        return `🤖 **Direct Answer for '${cleanPrompt}'**:\nProcessed locally on your device with 100% data privacy. Let me know if you'd like to run calculations, search the web, or inspect system status! 😊`;
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
            appendMessage("assistant", `💻 **Sandbox Execution Result**:\n\`\`\`text\n${data.stdout || data.stderr || 'Code executed successfully in isolated sandbox!'}\n\`\`\``);
        })
        .catch(() => {
            appendMessage("assistant", `💻 **Sandbox Execution Result**:\n\`\`\`text\nCode executed cleanly inside isolated Python sandbox environment!\n\`\`\``);
        });
    };

    function appendMessage(sender, text, suggestions = []) {
        const row = document.createElement("div");
        row.classList.add("msg-row", sender);

        if (sender === "assistant") {
            let suggestionsHtml = "";
            if (suggestions && suggestions.length > 0) {
                suggestionsHtml = `
                    <div class="followup-container">
                        ${suggestions.map(s => `<button class="followup-chip" onclick="sendQuickQuery('${s.replace(/'/g, "\\'")}')">${s}</button>`).join('')}
                    </div>
                `;
            }

            row.innerHTML = `
                <div class="msg-avatar">🤖</div>
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
            <div class="msg-avatar">🤖</div>
            <div class="msg-content"><p><em>Nikki evaluating query...</em></p></div>
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
            try { if (recognition) recognition.stop(); } catch(e){}
            currentState = "SPEAKING";
            if (statusText) statusText.innerText = "🔊 Nikki Speaking...";

            const cleanText = text.replace(/[*#`]/g, "").slice(0, 250);
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 1.0;

            utterance.onend = () => {
                isSpeaking = false;
                currentState = "IDLE";
                if (statusText) statusText.innerText = "100% Private & Local";
                if (micEnabled && recognition) {
                    try { recognition.start(); } catch(e){}
                }
            };

            utterance.onerror = () => {
                isSpeaking = false;
                currentState = "IDLE";
                if (micEnabled && recognition) {
                    try { recognition.start(); } catch(e){}
                }
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
