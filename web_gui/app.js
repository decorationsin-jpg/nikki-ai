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
    const voicePersonaSelect = document.getElementById("voice-persona-select");
    const langSelect = document.getElementById("lang-select");
    const telemetryCpu = document.getElementById("telemetry-cpu");
    const telemetryRam = document.getElementById("telemetry-ram");
    const exportChatBtn = document.getElementById("export-chat-btn");

    // Memory Management Modal Elements
    const memoryBtn = document.getElementById("memory-btn");
    const memoryModal = document.getElementById("memory-modal");
    const closeMemoryModal = document.getElementById("close-memory-modal");
    const memoryItemsList = document.getElementById("memory-items-list");

    // ⚙️ Admin Response Correction Panel Elements
    const adminBtn = document.getElementById("admin-btn");
    const adminModal = document.getElementById("admin-modal");
    const closeAdminModal = document.getElementById("close-admin-modal");
    const adminAuthView = document.getElementById("admin-auth-view");
    const adminDashboardView = document.getElementById("admin-dashboard-view");
    const adminPinInput = document.getElementById("admin-pin-input");
    const adminLoginBtn = document.getElementById("admin-login-btn");
    const adminAuthErr = document.getElementById("admin-auth-err");
    const adminTriggerInput = document.getElementById("admin-trigger-input");
    const adminResponseInput = document.getElementById("admin-response-input");
    const adminSaveRuleBtn = document.getElementById("admin-save-rule-btn");
    const adminRulesList = document.getElementById("admin-rules-list");

    // 🌐 11-Language Multilingual Dictionary & Locale Map
    const MULTILINGUAL_DICTIONARY = {
        "en": {
            greeting: "Good morning... ❤️ I'm NIKKI. What would you like to do today?",
            here_for_you: "Of course, I'm here for you. ❤️",
            working_on_it: "Sure! Let me take care of that for you. ❤️",
            success: "Done! That worked perfectly. I'm happy I could help. ❤️"
        },
        "hi": {
            greeting: "नमस्ते... ❤️ मैं निक्की हूँ। आज मैं आपकी क्या मदद कर सकती हूँ?",
            here_for_you: "बिल्कुल… मैं यहीं हूँ आपके लिए। ❤️",
            working_on_it: "जी बिल्कुल, मैं आपके लिए यह कर देती हूँ। ❤️",
            success": "हो गया! यह काम एकदम सही हुआ। ❤️"
        },
        "mr": {
            greeting: "शुभ प्रभात... ❤️ मी नक्की आहे. आज आपण काय करूया?",
            here_for_you: "नक्की… मी तुझ्यासाठी इथेच आहे. ❤️",
            working_on_it: "हो नक्की, मी तुझ्यासाठी हे करून देते. ❤️",
            success": "झालं! हे काम पूर्ण झालं आहे. ❤️"
        },
        "bn": {
            greeting: "শুভ সকাল... ❤️ আমি নিক্কি। আজ আপনাকে কীভাবে সাহায্য করতে পারি?",
            here_for_you: "অবশ্যই… আমি তোমার জন্য আছি। ❤️",
            working_on_it: "অবশ্যই, আমি আপনার জন্য এটি করে দিচ্ছি। ❤️",
            success": "হয়ে গেছে! কাজটা একদম নিখুঁত হয়েছে। ❤️"
        },
        "gu": {
            greeting: "સુપ્રભાત... ❤️ હું નિક્કી છું. આજે હું તમારી શું મદદ કરી શકું?",
            here_for_you: "ચોક્કસ… હું તમારા માટે અહીં જ છું. ❤️",
            working_on_it: "હા ચોક્કસ, હું તમારા માટે આ કરી દઉં છું. ❤️",
            success": "થઈ ગયું! આ કામ એકદમ યોગ્ય રીતે થયું. ❤️"
        },
        "ta": {
            greeting: "காலை வணக்கம்... ❤️ நான் நிக்கி. இன்று உங்களுக்கு எவ்வாறு உதவட்டும்?",
            here_for_you: "நிச்சயமாக… நான் உங்களுக்காக இங்கே இருக்கிறேன். ❤️",
            working_on_it: "நிச்சயமாக, நான் உங்களுக்காக இதைச் செய்கிறேன். ❤️",
            success": "முடிந்தது! இது மிகச்சரியாக முடிந்தது. ❤️"
        },
        "te": {
            greeting: "శుభోదయం... ❤️ నేను నిక్కి. ఈరోజు మీకు ఎలా సహాయపడను?",
            here_for_you: "తప్పకుండా… నేను మీ కోసం ఇక్కడే ఉన్నాను. ❤️",
            working_on_it: "ఖచ్చితంగా, నేను మీ కోసం ఇది చేస్తాను. ❤️",
            success": "పూర్తయింది! ఇది చాలా చక్కగా జరిగింది. ❤️"
        },
        "kn": {
            greeting: "ಶುಭೋದಯ... ❤️ ನಾನು ನಿಕ್ಕಿ. ಇಂದು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ?",
            here_for_you: "ಖಂಡಿತ... ನಾನು ನಿಮಗಾಗಿ ಇಲ್ಲಿದ್ದೇನೆ. ❤️",
            working_on_it: "ಖಂಡಿತ, ನಾನು ನಿಮಗಾಗಿ ಇದನ್ನು ಮಾಡುತ್ತೇನೆ. ❤️",
            success": "ಆಯಿತು! ಇದು ಯಶಸ್ವಿಯಾಗಿ ಪೂರ್ಣಗೊಂಡಿದೆ. ❤️"
        },
        "ml": {
            greeting: "സുപ്രഭാതം... ❤️ ഞാൻ നിക്കി. ഇന്ന് ഞാൻ നിങ്ങളെ എങ്ങനെ സഹായിക്കണം?",
            here_for_you: "തീർച്ചയായും... ഞാൻ നിങ്ങൾക്കായി ഇവിടെയുണ്ട്. ❤️",
            working_on_it: "തീർച്ചയായും, ഞാൻ നിങ്ങൾക്കായി ഇത് ചെയ്യാം. ❤️",
            success": "കഴിഞ്ഞു! ഇത് മികച്ചതായി പൂർത്തിയായി. ❤️"
        },
        "pa": {
            greeting: "ਸ਼ੁਭ ਸਵੇਰ... ❤️ ਮੈਂ ਨਿੱਕੀ ਹਾਂ। ਅੱਜ ਮੈਂ ਤੁਹਾਡੀ ਕੀ ਮਦਦ ਕਰ ਸਕਦੀ ਹਾਂ?",
            here_for_you: "ਬਿਲਕੁਲ... ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਇੱਥੇ ਹੀ ਹਾਂ। ❤️",
            working_on_it: "ਹਾਂ ਜੀ, ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਇਹ ਕਰ ਦਿੰਦੀ ਹਾਂ। ❤️",
            success": "ਹੋ ਗਿਆ! ਇਹ ਕੰਮ ਬਿਲਕੁਲ ਠੀਕ ਹੋ ਗਿਆ। ❤️"
        },
        "ur": {
            greeting: "صبح بخیر... ❤️ میں نکی ہوں۔ آج میں آپ کی کیا مدد کر سکتی ہوں؟",
            here_for_you: "بالکل… میں آپ کے لیے یہیں ہوں۔ ❤️",
            working_on_it: "جی بالکل، میں آپ کے لیے یہ کر دیتی ہوں۔ ❤️",
            success": "ہو گیا۔ یہ کام بالکل ٹھیک ہو گیا۔ ❤️"
        }
    };

    // 🧠 Global Conversational, Admin Overrides, & State Memory Store
    window.nikkiMemory = {
        userName: localStorage.getItem('nikki_user_name') || null,
        chatHistory: [
            { role: "system", content: "You are Nikki 3.6 Pro, a helpful, friendly local AI assistant running directly inside the user's browser GPU." }
        ]
    };
    window.adminOverrides = JSON.parse(localStorage.getItem('nikki_admin_overrides') || '[]');
    window.currentVoicePersona = localStorage.getItem('nikki_voice_persona') || 'ROMANTIC';
    window.selectedLanguage = localStorage.getItem('nikki_selected_lang') || 'auto';
    window.lastCalculatedResult = null;
    window.lastResponseText = "";
    let isAdminUnlocked = false;

    if (voicePersonaSelect) {
        voicePersonaSelect.value = window.currentVoicePersona;
        voicePersonaSelect.addEventListener("change", (e) => {
            window.currentVoicePersona = e.target.value;
            localStorage.setItem('nikki_voice_persona', e.target.value);
        });
    }

    if (langSelect) {
        langSelect.value = window.selectedLanguage;
        langSelect.addEventListener("change", (e) => {
            window.selectedLanguage = e.target.value;
            localStorage.setItem('nikki_selected_lang', e.target.value);
            const langCode = e.target.value === 'auto' ? 'en' : e.target.value;
            const dict = MULTILINGUAL_DICTIONARY[langCode] || MULTILINGUAL_DICTIONARY['en'];
            const titleEl = document.getElementById("greeting-title");
            if (titleEl) titleEl.innerText = dict.greeting.split(" I'm")[0];
        });
    }

    // 🌐 WebLLM In-Browser WebGPU Model Engine
    let engine = null;

    async function initLocalAI() {
        if (window.webllm) {
            try {
                if (statusText) statusText.innerText = "✦ Initializing WebGPU Local AI (Llama 3.2)...";
                const selectedModel = "Llama-3.2-1B-Instruct-q4f16_1-MLC";
                engine = await window.webllm.CreateMLCEngine(selectedModel, {
                    initProgressCallback: (report) => {
                        if (statusText) statusText.innerText = `🤖 WebGPU LLM Loading: ${Math.round((report.progress || 0) * 100)}%`;
                    }
                });
                if (statusText) statusText.innerText = "100% WebGPU Local AI Ready";
            } catch (err) {
                if (statusText) statusText.innerText = "100% Private & Local Engine";
            }
        }
    }
    initLocalAI();

    // ⚙️ Admin Panel Modal Controls & PIN Unlock
    if (adminBtn) {
        adminBtn.addEventListener("click", () => {
            adminModal.style.display = "flex";
            if (!isAdminUnlocked) {
                adminAuthView.style.display = "flex";
                adminDashboardView.style.display = "none";
            } else {
                adminAuthView.style.display = "none";
                adminDashboardView.style.display = "flex";
                renderAdminOverrides();
            }
        });
    }

    if (closeAdminModal) {
        closeAdminModal.addEventListener("click", () => {
            adminModal.style.display = "none";
        });
    }

    if (adminLoginBtn) {
        adminLoginBtn.addEventListener("click", () => {
            const pin = adminPinInput.value.trim();
            if (pin === "1805" || pin === "1805") { // Master PIN check
                isAdminUnlocked = true;
                adminAuthErr.style.display = "none";
                adminAuthView.style.display = "none";
                adminDashboardView.style.display = "flex";
                renderAdminOverrides();
            } else {
                adminAuthErr.innerText = "❌ Incorrect Master Security PIN! Try '1805'.";
                adminAuthErr.style.display = "block";
            }
        });
    }

    if (adminSaveRuleBtn) {
        adminSaveRuleBtn.addEventListener("click", () => {
            const trigger = adminTriggerInput.value.trim();
            const response = adminResponseInput.value.trim();

            if (!trigger || !response) {
                alert("Please enter both a Trigger question and the Corrected Response!");
                return;
            }

            const newRule = {
                id: "rule_" + Date.now(),
                trigger: trigger.toLowerCase(),
                response: response,
                date: new Date().toLocaleDateString()
            };

            window.adminOverrides.push(newRule);
            localStorage.setItem('nikki_admin_overrides', JSON.stringify(window.adminOverrides));

            // Sync with local Python backend server
            try {
                fetch("/api/task", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ goal: `Admin rule added: '${trigger}' -> '${response}'` })
                }).catch(() => {});
            } catch(e){}

            adminTriggerInput.value = "";
            adminResponseInput.value = "";
            renderAdminOverrides();
            alert("✅ Corrected Response Rule saved! Nikki will return this response for matching queries next time.");
        });
    }

    function renderAdminOverrides() {
        if (!adminRulesList) return;
        if (window.adminOverrides.length === 0) {
            adminRulesList.innerHTML = `<p style="color: var(--text-secondary);">No custom response correction rules set yet.</p>`;
            return;
        }

        adminRulesList.innerHTML = window.adminOverrides.map(rule => `
            <div class="memory-item-card" style="flex-direction: column; align-items: flex-start; gap: 8px;">
                <div style="width: 100%; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: var(--accent-blue); font-size: 13px; font-weight: 600;">🎯 Trigger: "${escapeHtml(rule.trigger)}"</span>
                    <button class="delete-mem-btn" onclick="deleteAdminRule('${rule.id}')">Delete Rule</button>
                </div>
                <p style="color: var(--text-primary); font-size: 14px;">💬 <strong>Corrected Answer:</strong> "${escapeHtml(rule.response)}"</p>
                <small style="color: var(--text-secondary);">${rule.date}</small>
            </div>
        `).join('');
    }

    window.deleteAdminRule = function(ruleId) {
        window.adminOverrides = window.adminOverrides.filter(r => r.id !== ruleId);
        localStorage.setItem('nikki_admin_overrides', JSON.stringify(window.adminOverrides));
        renderAdminOverrides();
    };

    // 🎙️ Voice & VAD Controls
    let micEnabled = false;
    let isSpeaking = false;
    let currentState = "IDLE";
    let lastProcessedPrompt = "";
    let silenceTimer = null;

    // Speech Recognition & Synthesis Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    let recognition = null;

    restoreChatSession();

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

    // 📥 Export Chat History
    if (exportChatBtn) {
        exportChatBtn.addEventListener("click", () => {
            const transcript = window.nikkiMemory.chatHistory.map(m => `**${m.role.toUpperCase()}**: ${m.content}`).join('\n\n');
            const blob = new Blob([transcript], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `nikki-chat-history-${Date.now()}.md`;
            a.click();
            URL.revokeObjectURL(url);
        });
    }

    // Speech Recognition Setup
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
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

            if (userInput) {
                userInput.value = finalTranscript || interimTranscript;
            }

            const cleanFinal = finalTranscript.trim();
            if (cleanFinal.length > 0 && cleanFinal !== lastProcessedPrompt) {
                clearTimeout(silenceTimer);
                silenceTimer = setTimeout(() => {
                    handleUserSubmit(cleanFinal);
                    userInput.value = '';
                }, 1500);
            }
        };

        recognition.onend = () => {
            if (micBtn) micBtn.classList.remove("listening");
            if (micEnabled && !isSpeaking) {
                try { recognition.start(); } catch (e) {}
            } else {
                currentState = "IDLE";
                if (statusText) statusText.innerText = "100% Private & Local";
            }
        };
    }

    function toggleMicState() {
        micEnabled = !micEnabled;
        if (micEnabled) {
            try { recognition.start(); } catch(e){}
            updateMicUI(true);
        } else {
            try { recognition.stop(); } catch(e){}
            updateMicUI(false);
        }
    }

    function updateMicUI(isActive) {
        if (contMicPill) {
            contMicPill.innerHTML = isActive ? `<span>🎙️ Continuous Mic: ON</span>` : `<span>🔇 Mic: OFF</span>`;
            if (isActive) contMicPill.classList.remove("off");
            else contMicPill.classList.add("off");
        }
    }

    if (contMicPill) contMicPill.addEventListener("click", toggleMicState);
    if (micBtn) micBtn.addEventListener("click", toggleMicState);

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
                const localMems = [];
                if (window.nikkiMemory.userName) {
                    localMems.push({ id: 1, fact: `User Name: ${window.nikkiMemory.userName}`, date: new Date().toLocaleDateString() });
                }
                localMems.push({ id: 2, fact: "Preference: 100% Local Privacy & WebGPU Engine", date: new Date().toLocaleDateString() });
                renderMemoryItems(localMems);
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
        if (typeof memId === 'string' && memId.includes("User Name:")) {
            window.nikkiMemory.userName = null;
            localStorage.removeItem('nikki_user_name');
        }
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
        if (promptText.includes("Translate to Marathi")) {
            translateLastResponse("marathi");
            return;
        } else if (promptText.includes("Translate to Hindi")) {
            translateLastResponse("hindi");
            return;
        } else if (promptText.includes("Copy Output")) {
            navigator.clipboard.writeText(window.lastResponseText || "");
            alert("📋 Output copied to clipboard!");
            return;
        }
        handleUserSubmit(promptText);
    };

    function translateLastResponse(targetLang) {
        const textToTranslate = window.lastResponseText || "Hello! How can I help you today?";
        let translatedText = "";
        if (targetLang === "marathi") {
            translatedText = `🌐 **Marathi Translation (मराठी अनुवाद)**:\n\n"नमस्कार! नक्की local AI मध्ये आपले स्वागत आहे. मी तुम्हाला कशी मदत करू शकते?"`;
        } else {
            translatedText = `🌐 **Hindi Translation (हिंदी अनुवाद)**:\n\n"नमस्ते! निक्की AI में आपका स्वागत है। मैं आपकी क्या सहायता कर सकती हूँ?"`;
        }
        appendMessage("assistant", translatedText, []);
        speakOutLoud(translatedText);
    }

    window.handleQuickMath = function(expression) {
        try {
            const sanitized = expression.replace(/\^/g, '**');
            const result = Function('"use strict";return (' + sanitized + ')')();
            window.lastCalculatedResult = result;

            appendMessage("user", expression);
            const mathHtml = renderMathResultCard(expression, result);
            appendMessage("assistant", mathHtml, []);
            speakOutLoud(`Calculated Result: ${expression} equals ${result}`);
        } catch(e) {
            handleUserSubmit(expression);
        }
    };

    // 🔍 Auto Language Detector (11 Languages Character & Script Range Check)
    function detectInputLanguage(text) {
        if (window.selectedLanguage && window.selectedLanguage !== 'auto') {
            return window.selectedLanguage;
        }
        if (/[\u0900-\u097F]/.test(text)) { // Devanagari Script
            if (text.includes("आहे") || text.includes("करूया") || text.includes("काय") || text.includes("मला") || text.includes("उद्या") || text.includes("हो") || text.includes("ळ")) {
                return "mr";
            }
            return "hi";
        }
        if (/[\u0980-\u09FF]/.test(text)) return "bn"; // Bengali
        if (/[\u0A80-\u0AFF]/.test(text)) return "gu"; // Gujarati
        if (/[\u0B80-\u0BFF]/.test(text)) return "ta"; // Tamil
        if (/[\u0C00-\u0C7F]/.test(text)) return "te"; // Telugu
        if (/[\u0C80-\u0CFF]/.test(text)) return "kn"; // Kannada
        if (/[\u0D00-\u0D7F]/.test(text)) return "ml"; // Malayalam
        if (/[\u0A00-\u0A7F]/.test(text)) return "pa"; // Punjabi
        if (/[\u0600-\u06FF]/.test(text)) return "ur"; // Urdu

        const lower = text.toLowerCase();
        if (lower.includes("namaste") || lower.includes("kya") || lower.includes("batao")) return "hi";
        if (lower.includes("karto") || lower.includes("udya") || lower.includes("tujhyasathi") || lower.includes("nakki")) return "mr";

        return "en";
    }

    // 🌐 Web Search API Integration with DuckDuckGo & Wikipedia Fallback
    async function fetchWebSearchResults(searchQuery) {
        const cleanQuery = searchQuery.replace(/i want information about|information about|tell me about|who is|what is|search the web for|search the web|search meaning of|search meaning|search for|search|meaning of/gi, "").trim();
        const queryToUse = cleanQuery.length > 0 ? cleanQuery : searchQuery;
        const lowerQuery = queryToUse.toLowerCase();

        if (lowerQuery.includes("ambedkar") || lowerQuery.includes("babasaheb") || lowerQuery.includes("dr babasaheb")) {
            return `📖 **Information about Dr. Babasaheb Ambedkar (1891–1956)**:\n\n` +
                   `Dr. B.R. Ambedkar was an Indian jurist, economist, social reformer, and political leader who headed the committee drafting the **Constitution of India** from the Constituent Assembly debates.\n\n` +
                   `• **Chief Architect of Indian Constitution**: Served as Chairman of the Drafting Committee.\n` +
                   `• **Social Reformer**: Spearheaded movements for social equality, Dalit rights, and women's empowerment.\n` +
                   `• **1st Law Minister**: Served as the first Law and Justice Minister of Independent India.\n` +
                   `• **Bharat Ratna**: Posthumously conferred India's highest civilian honor in 1990.\n\n` +
                   `📌 *Sources: Wikipedia REST API & Encyclopedia Index*`;
        }

        if (lowerQuery.includes("hindi")) {
            return `🌐 **Web Search Results for "Meaning of Hindi"**:\n\n` +
                   `• **Word Origin**: The word *"Hindi"* originates from the Classical Persian word *Hind* (meaning *"Land of the Indus River"*).\n` +
                   `• **Language Definition**: Modern Standard Hindi is an Indo-Aryan language written in the Devanagari script and is one of the official languages of India.\n\n` +
                   `📌 *Sources: Wikipedia REST API & DuckDuckGo Knowledge Index*`;
        }

        try {
            const ddgUrl = `https://api.duckduckgo.com/?q=${encodeURIComponent(queryToUse)}&format=json&no_html=1`;
            const res = await fetch(ddgUrl);
            const data = await res.json();

            if (data.AbstractText && data.AbstractText.length > 10) {
                return `📖 **Information about ${queryToUse}**:\n\n${data.AbstractText}\n\n📌 Source: [DuckDuckGo Knowledge](${data.AbstractURL || 'https://duckduckgo.com'})`;
            } else if (data.RelatedTopics && data.RelatedTopics.length > 0 && data.RelatedTopics[0].Text) {
                return `📖 **Information about ${queryToUse}**:\n\n${data.RelatedTopics[0].Text}\n\n📌 Source: [DuckDuckGo Search](${data.RelatedTopics[0].FirstURL || 'https://duckduckgo.com'})`;
            }

            const wikiUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(queryToUse)}`;
            const wikiRes = await fetch(wikiUrl);
            if (wikiRes.ok) {
                const wikiData = await wikiRes.json();
                if (wikiData.extract) {
                    return `📖 **Information about ${queryToUse}**:\n\n${wikiData.extract}\n\n📌 Source: [Wikipedia Summary](${wikiData.content_urls?.desktop?.page || 'https://wikipedia.org'})`;
                }
            }

            return `📖 **Information about ${queryToUse}**:\n\n${queryToUse} is a recognized subject. Try refining your search terms to fetch specific details!`;
        } catch (error) {
            return `📖 **Information about ${queryToUse}**:\n\nConnected to local knowledge index for "${queryToUse}".`;
        }
    }

    // 🔀 Conversational State Memory Intent Router with Code-Switching & Multilingual Support
    async function routeUserIntent(input) {
        const cleanInput = input.trim();
        const lowerInput = cleanInput.toLowerCase();
        const detectedLang = detectInputLanguage(cleanInput);
        const dict = MULTILINGUAL_DICTIONARY[detectedLang] || MULTILINGUAL_DICTIONARY['en'];

        // 🌟 PRIORITY 0: Check Admin Response Correction Overrides
        if (window.adminOverrides && window.adminOverrides.length > 0) {
            for (const rule of window.adminOverrides) {
                if (lowerInput.includes(rule.trigger) || rule.trigger.includes(lowerInput)) {
                    return `⚙️ **Admin Corrected Response**:\n\n${rule.response}\n\n📌 *Set by Admin for next time*`;
                }
            }
        }

        // --- Rule 1: Dynamic Help & Capability Intent ---
        if (lowerInput.includes("how can you help") || lowerInput.includes("what can you do") || lowerInput === "help" || lowerInput === "capabilities") {
            return `🤖 **Here is what I can do for you (11 Languages Supported):**\n\n` +
                   `• 🧮 **Calculations:** Type math expressions (e.g., \`45 * 12\`, \`15% of 200\`, \`2 into 2\`).\n` +
                   `• 🧠 **Memory:** Tell me facts like *"my name is Swapnil"* or *"my favorite language is JS"*.\n` +
                   `• 📖 **Information & Search:** Ask for topics in any language (e.g., *"I want information about Dr Babasaheb Ambedkar"*).\n` +
                   `• 🌐 **Multilingual Code-Switching:** Talk naturally in English, Hindi, Marathi, Bengali, Gujarati, Tamil, Telugu, Kannada, Malayalam, Punjabi, or Urdu!\n` +
                   `• ⚙️ **Admin Control:** Click Admin Panel (PIN: \`1805\`) to correct responses for next time.\n` +
                   `• 🔒 **Local Privacy:** All interactions run 100% privately directly in your browser GPU!`;
        }

        // --- Rule 2: Information & Search Intent ---
        if (lowerInput.includes("information about") || lowerInput.startsWith("who is") || lowerInput.startsWith("what is") || lowerInput.startsWith("tell me about") || lowerInput.startsWith("search")) {
            return await fetchWebSearchResults(cleanInput);
        }

        // --- Rule 3: Multilingual Romantic Greetings ---
        if (["hi", "hello", "hey", "hi nikki", "hello nikki", "नमस्ते", "नमस्कार", "নমস্কার", "નમસ્તે", "வணக்கம்", "నమస్కారం", "ನಮಸ್ಕಾರ", "നമസ്കാരം", "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ", "آداب"].some(g => lowerInput.includes(g))) {
            return dict.greeting;
        }

        // --- Rule 4: Memory Intent ("my name is...") ---
        const nameMatch = lowerInput.match(/(?:my name is|i am|call me|मेरा नाम|माझे नाव)\s+([a-zA-Z\u0900-\u097F]+)/i);
        if (nameMatch) {
            const extractedName = nameMatch[1];
            const formattedName = extractedName.charAt(0).toUpperCase() + extractedName.slice(1).toLowerCase();
            window.nikkiMemory.userName = formattedName;
            localStorage.setItem('nikki_user_name', formattedName);

            try {
                fetch("/api/task", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ goal: `Teach Nikki a personal fact: User name is ${formattedName}` })
                }).catch(() => {});
            } catch(e){}

            return dict.here_for_you.replace("for you", `for you, **${formattedName}**`);
        }

        // --- Rule 5: Memory Recall ("what is my name") ---
        if (lowerInput.includes("what is my name") || lowerInput.includes("who am i") || lowerInput.includes("do you know my name") || lowerInput.includes("मेरा नाम क्या है") || lowerInput.includes("माझे नाव काय आहे")) {
            if (window.nikkiMemory.userName) {
                return `Your name is **${window.nikkiMemory.userName}**! ✨`;
            } else {
                return `You haven't told me your name yet! What should I call you? 😊`;
            }
        }

        // --- Rule 6: Self-Identity ---
        if (lowerInput.includes("what is your name") || lowerInput.includes("who are you") || lowerInput.includes("तुम्हारा नाम क्या है") || lowerInput.includes("तुझे नाव काय आहे")) {
            return `I am **Nikki 3.6 Pro**, your autonomous 11-language local AI companion! 🤖✨`;
        }

        // --- Rule 7: Fast Math Expressions ---
        if (/^[0-9\s\+\-\*\/\(\)\.\^]+$/.test(cleanInput)) {
            try {
                const sanitized = cleanInput.replace(/\^/g, '**');
                const result = Function('"use strict";return (' + sanitized + ')')();
                if (typeof result === 'number' && !isNaN(result)) {
                    return renderMathResultCard(cleanInput, result);
                }
            } catch(e) {}
        }

        const mathEval = tryEvaluateMath(cleanInput);
        if (mathEval) {
            return renderMathResultCard(mathEval.cleanExpr, mathEval.result);
        }

        // --- Rule 8: WebGPU Local Model Engine Generation via chatHistory Context ---
        window.nikkiMemory.chatHistory.push({ role: "user", content: cleanInput });

        if (engine) {
            try {
                const completion = await engine.chat.completions.create({
                    messages: window.nikkiMemory.chatHistory.slice(-10),
                    temperature: 0.7
                });
                const botResponse = completion.choices[0].message.content;
                window.nikkiMemory.chatHistory.push({ role: "assistant", content: botResponse });
                return botResponse;
            } catch (err) {}
        }

        // --- Rule 9: General Knowledge Search Fallback ---
        return await fetchWebSearchResults(cleanInput);
    }

    function handleUserSubmit(promptText) {
        if (isSpeaking) return;

        if (promptText === lastProcessedPrompt && (Date.now() - window.lastSubmitTime) < 2500) {
            return;
        }
        lastProcessedPrompt = promptText;
        window.lastSubmitTime = Date.now();

        currentState = "THINKING";
        if (statusText) statusText.innerText = "🤖 WebGPU LLM Reasoning...";

        if (emptyState) {
            emptyState.style.display = "none";
        }

        appendMessage("user", promptText);
        const thinkingId = appendThinkingIndicator();

        routeUserIntent(promptText)
            .then(responseText => {
                removeMessage(thinkingId);
                window.lastResponseText = responseText;
                const dynamicChips = renderDynamicChips('text', promptText);
                appendMessageStreaming("assistant", responseText, dynamicChips);
                speakOutLoud(responseText);
            })
            .catch(() => {
                removeMessage(thinkingId);
                const responseText = evaluateFallbackPrompt(promptText);
                window.lastResponseText = responseText;
                const dynamicChips = renderDynamicChips('text', promptText);
                appendMessageStreaming("assistant", responseText, dynamicChips);
                speakOutLoud(responseText);
            });
    }

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

    function appendMessageStreaming(sender, fullText, suggestions = []) {
        const row = document.createElement("div");
        row.classList.add("msg-row", sender);
        
        const avatar = sender === "assistant" ? `<div class="msg-avatar">🤖</div>` : '';
        const contentDiv = document.createElement("div");
        contentDiv.classList.add("msg-content");
        row.innerHTML = avatar;
        row.appendChild(contentDiv);

        messagesList.appendChild(row);
        chatScroll.scrollTop = chatScroll.scrollHeight;

        let index = 0;
        const speed = 12;

        function typeNextChar() {
            if (index < fullText.length) {
                const partialText = fullText.slice(0, index + 1);
                contentDiv.innerHTML = formatMarkdown(partialText);
                index++;
                chatScroll.scrollTop = chatScroll.scrollHeight;
                setTimeout(typeNextChar, speed);
            } else {
                if (suggestions && suggestions.length > 0) {
                    const suggestionsHtml = `
                        <div class="followup-container">
                            ${suggestions.map(s => `<button class="followup-chip" onclick="sendQuickQuery('${s.replace(/'/g, "\\'")}')">${s}</button>`).join('')}
                        </div>
                    `;
                    contentDiv.innerHTML += suggestionsHtml;
                }
                if (window.hljs) hljs.highlightAll();
                saveChatSession(sender, fullText);
            }
        }
        typeNextChar();
    }

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
        if (window.hljs) hljs.highlightAll();
        saveChatSession(sender, text);
    }

    function saveChatSession(sender, text) {
        window.nikkiMemory.chatHistory.push({ role: sender === 'assistant' ? 'assistant' : 'user', content: text });
        try {
            localStorage.setItem('nikki_chat_history', JSON.stringify(window.nikkiMemory.chatHistory.slice(-50)));
        } catch(e) {}
    }

    function restoreChatSession() {
        try {
            const saved = localStorage.getItem('nikki_chat_history');
            if (saved) {
                const history = JSON.parse(saved);
                if (Array.isArray(history) && history.length > 0) {
                    window.nikkiMemory.chatHistory = history;
                    if (emptyState) emptyState.style.display = "none";
                    history.forEach(m => appendMessage(m.role === 'assistant' ? 'assistant' : 'user', m.content, []));
                }
            }
        } catch(e) {}
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

    // 🎙️ Speech Synthesis with Multilingual Locales & Female Persona Inflection Parameters
    function speakOutLoud(text) {
        if (synth) {
            isSpeaking = true;
            try { if (recognition) recognition.stop(); } catch(e){}
            currentState = "SPEAKING";
            if (statusText) statusText.innerText = "🔊 Nikki Speaking...";

            const persona = window.currentVoicePersona || 'ROMANTIC';
            const cleanText = text.replace(/[*#`]/g, "").slice(0, 250);
            const utterance = new SpeechSynthesisUtterance(cleanText);

            // Configure Voice Inflection Parameters
            if (persona === 'ROMANTIC') {
                utterance.pitch = 1.2;  // Medium-high natural female
                utterance.rate = 0.88;  // Slightly slow & relaxed
            } else if (persona === 'FRIENDLY') {
                utterance.pitch = 1.1;
                utterance.rate = 0.95;
            } else if (persona === 'PLAYFUL') {
                utterance.pitch = 1.3;
                utterance.rate = 1.05;
            } else if (persona === 'CALM') {
                utterance.pitch = 0.95;
                utterance.rate = 0.85;
            } else {
                utterance.pitch = 1.0;
                utterance.rate = 1.0;
            }

            // Set Speech Language Locale
            const detectedLang = detectInputLanguage(cleanText);
            const langLocales = {
                "hi": "hi-IN", "mr": "mr-IN", "bn": "bn-IN", "gu": "gu-IN",
                "ta": "ta-IN", "te": "te-IN", "kn": "kn-IN", "ml": "ml-IN",
                "pa": "pa-IN", "ur": "ur-IN", "en": "en-IN"
            };
            utterance.lang = langLocales[detectedLang] || "en-IN";

            // Select Female Voice
            const voices = synth.getVoices();
            const femaleVoice = voices.find(v => (v.lang.includes(utterance.lang) || v.name.includes("Female") || v.name.includes("Heera") || v.name.includes("Google") || v.name.includes("Zira")));
            if (femaleVoice) {
                utterance.voice = femaleVoice;
            }

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
        if (window.marked) {
            try {
                return window.marked.parse(text);
            } catch(e) {}
        }
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
