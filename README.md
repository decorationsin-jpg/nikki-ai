# 🌸 Nikki - Autonomous Local AI Assistant (Zero API Keys)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![Privacy](https://img.shields.io/badge/privacy-100%25%20Local-success.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Android%20Termux-orange.svg)

Nikki is a 100% private, self-learning, emotion-aware, autonomous AI assistant that runs on your local computer or Android smartphone. She requires **no paid API keys**, works **offline and online**, creates files, searches the web for free, auto-executes commands, makes phone calls, speaks with genuine feelings, acts as a system defender & personal tutor, and monitors **WhatsApp**, **Instagram**, and **SMS**.

---

## 🌐 Live Web Page & Mobile App (GitHub Pages)

Nikki is now available as a **Live Web Page & Mobile App**!

👉 **Live Web Page**: **`https://decorationsin-jpg.github.io/nikki-ai/`**

### 📱 Install Nikki as an App on Android or iPhone:
1. Open **`https://decorationsin-jpg.github.io/nikki-ai/`** on your phone browser.
2. Tap the browser menu (`⋮` on Android / Share button on iPhone).
3. Click **"Add to Home Screen"** or **"Install App"**.
4. Nikki's icon will appear on your phone home screen as a native mobile app!

---

## 📸 Nikki Visual Face & Web GUI Dashboard

![Nikki Avatar Portrait](assets/nikki_avatar.jpg)

Launch Nikki's Web GUI Dashboard locally at `http://localhost:5000`:
```bash
python main.py --gui
```

---

## 🌟 Key Capabilities & Features

| Feature | How It Works | Requires API Key? | Works Offline? |
| :--- | :--- | :---: | :---: |
| **Local LLM Brain** | [Ollama](https://ollama.com/) running Llama 3.2, Qwen 2.5, or Mistral | ❌ No | ✅ Yes |
| **Conversational Memory** | Stores facts, habits, and preferences in `memory/user_teachings.json` | ❌ No | ✅ Yes |
| **Emotional Voice Engine** | Speaks with sentiment modulation (Happy, Caring, Excited, Serious, Calm) | ❌ No | ✅ Yes |
| **Master Security System** | Physical CCTV Intruder Alarm, PIN (`1805`) Lock & Device Defender | ❌ No | ✅ Yes |
| **24/7 Background Learning** | Continuous background web knowledge scraper & memory indexer | ❌ No | ⚡ Live |
| **Self-Modifying Code** | Auto-programs new Python skills in `custom_skills/` and runs `pip install` | ❌ No | ✅ Yes |
| **Free Web Search & Scraper** | `duckduckgo_search` + `BeautifulSoup` | ❌ No | ❌ (Needs Web) |
| **24/7 AI Personal Tutor** | Explains topics, creates quizzes, grades answers & generates study roadmaps | ❌ No | ✅ Yes |
| **Android Phone Engine** | Termux Native Engine (Calls, SMS, Camera, Voice) & ADB Screen Touch | ❌ No | ✅ Yes |
| **IP Camera & CCTV Reader** | Connects to RTSP / HTTP camera streams and saves JPEG snapshots | ❌ No | ✅ Yes |
| **Automated Scheduler** | Background voice timers, reminders, and daily alarm clocks | ❌ No | ✅ Yes |
| **Computer Vision** | PC desktop screenshot capture & webcam inspector | ❌ No | ✅ Yes |

---

## 🔒 100% Privacy Guarantee: ZERO Third-Party Data Sharing

- **100% Local Execution**: All AI processing runs on your own hardware (Ollama / llama-cpp).
- **No Cloud Servers**: Your chat history, voice audio, system files, and memory databases never leave your device.
- **No Third-Party API Keys**: Requires ZERO API keys (No OpenAI, No Anthropic, No Cloud Accounts).
- **Offline Ready**: Functions 100% offline without internet connection.
- **Your Data Remains Yours**: Stored strictly inside your local workspace folder.

---

## 📱 How to Run Directly ON Your Android Phone (Zero PC Needed!)

### Step 1: Install Termux & Termux API
1. Download [Termux from F-Droid](https://f-droid.org/en/packages/com.termux/).
2. Download [Termux:API from F-Droid](https://f-droid.org/en/packages/com.termux.api/).

### Step 2: Run Setup Commands in Termux
```bash
# Update & install dependencies
termux-setup-storage
pkg update && pkg install python git termux-api clang -y

# Install Ollama AI model on phone
pkg install ollama
ollama run llama3.2

# Clone Nikki repository
git clone https://github.com/your-username/nikki.git
cd nikki
pip install requests duckduckgo_search beautifulsoup4

# Run Nikki on phone natively!
python main.py --voice
```

---

## 💻 Quick Start on Windows / Linux / Mac

### 1. Install Ollama (Free Local AI Engine)
Download from [ollama.com](https://ollama.com/) and run in terminal:
```bash
ollama run llama3.2
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Launch Nikki
- **One-Click Windows Launcher**: Double click `start_nikki.bat`
- **Continuous Voice Mode**: `python main.py --voice`
- **Visual Web GUI Dashboard**: `python main.py --gui`

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.
