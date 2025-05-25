<a name="readme-top"></a>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]](https://www.linkedin.com/in/chater-marzougui-342125299/)
</div>


## ⚠️ Ethical Use Statement

**ScreenSolver is designed as a study aid and learning tool only.**

This software is intended for:
- Self-assessment during study sessions
- Practicing with sample questions
- Educational purposes to understand question patterns and formats

**This software should NOT be used for:**
- Cheating during exams, tests, or assessments
- Circumventing academic integrity policies
- Any form of dishonest academic conduct

Using this software in violation of educational institution policies may result in serious academic consequences. The developers of ScreenSolver do not condone or support any unethical use of this software.

By using ScreenSolver, you agree to use it responsibly and in accordance with all applicable academic integrity policies.

---

# 🎯 ScreenSolver

**Your automated assistant for timed multiple-choice questions.**  
Built with ❤️ in Python and Gemini AI.

---

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#📱-about-screensolver">About ScreenSolver</a></li>
    <li><a href="#✨-features">Features</a></li>
    <li><a href="#🧠-tech-stack">Tech Stack</a></li>
    <li><a href="#📁-project-structure">Project Structure</a></li>
    <li><a href="#🛠️-installation">Installation</a></li>
    <li><a href="#🔑-getting-a-gemini-api-key">Getting a Gemini API Key</a></li>
    <li><a href="#🧑‍💻-how-to-use">How to Use</a></li>
    <li><a href="#⚙️-configuration">Configuration</a></li>
    <li><a href="#📋-requirements">Requirements</a></li>
    <li><a href="#🔧-troubleshooting">Troubleshooting</a></li>
    <li><a href="#📃-license">License</a></li>
    <li><a href="#🤝-contributing">Contributing</a></li>
    <li><a href="#📧-contact">Contact</a></li>
    <li><a href="#⚠️-disclaimer">Disclaimer</a></li>
  </ol>
</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 📱 About ScreenSolver

**ScreenSolver** is a lightweight desktop utility designed to help users with timed multiple-choice questions. It automatically captures your screen, analyzes question content using Google's Gemini AI, and displays the most likely correct answer - all with a minimal, unobtrusive interface that stays out of your way.

This project demonstrates practical AI integration in a desktop application - combining screen capture, OCR capabilities, AI reasoning, and a clean user interface to create a helpful study companion.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## ✨ Features

- 🔄 **Automatic Screen Monitoring** with configurable intervals (12 seconds default)
- 🤖 **AI-Powered Answer Detection** using Google's Gemini 2.0 Flash model
- 💡 **Instant Answer Display** in a compact, floating interface
- ⌨️ **Global Hotkey Support**:
  - `Ctrl+Alt` - Toggle visibility
  - `Ctrl+Shift` - Take immediate screenshot
  - `Ctrl+Space` - Toggle pause/resume
- 🖱️ **Right-Click Menu** for quick access to controls
- 🔝 **Always-on-Top Display** that never interferes with your workflow
- 🔢 **Countdown Timer** showing seconds until next analysis
- 🔍 **JSON Response Parsing** for structured answer extraction
- 📁 **Custom Answer Examples** support via `forwlan.txt`
- ⏸️ **Pause/Resume Functionality** for better control

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🧠 Tech Stack

| Component | Technologies |
|-----------|--------------|
| **UI** | Tkinter |
| **Image Processing** | PIL (Pillow) |
| **AI Integration** | Google Generative AI (Gemini) |
| **Input Handling** | Keyboard library |
| **Threading** | Python threading module |
| **Environment Management** | python-dotenv |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 📁 Project Structure

```
screensolver/
├── app.py                       # Main application file
├── requirements.txt             # Dependencies
├── .env                         # API key configuration (create this)
├── .env_example                 # Environment template
├── forwlan.txt                  # Custom answer examples (optional)
├── screenshots/                 # Temporary screenshot storage
└── README.md                    # Documentation
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🛠️ Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd screensolver
```

### Step 2: Set Up Virtual Environment
Create and activate a virtual environment to isolate dependencies:

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
1. Create your `.env` file by copying the example:
```bash
cp .env_example .env
```

2. Edit the `.env` file and add your Google Generative AI API key:
```
API_KEY=your_gemini_api_key_here
```

### Step 5: Create Required Directories
```bash
mkdir screenshots
```

### Step 6: Run the Application
```bash
python app.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🔑 Getting a Gemini API Key

1. Visit the [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and paste it into your `.env` file

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🧑‍💻 How to Use

1. **Launch the application** - A small purple window will appear in the bottom-left corner of your screen

2. **Let it run** - The application will automatically:
   - Take screenshots every 12 seconds
   - Analyze any multiple-choice questions visible on screen
   - Display the detected answer in the right box
   - Show a countdown timer in the left box

3. **Controls**:
   - **Ctrl+Alt** - Toggle visibility of the window
   - **Ctrl+Shift** - Take immediate screenshot and reset timer
   - **Ctrl+Space** - Pause/resume automatic screenshots
   - **Right-click** on the window for additional options:
     - Close the application
     - Toggle visibility
     - Take screenshot now

4. **Interpreting Results**:
   - The right box displays the detected answer choice (A, B, C, D, etc.)
   - "WAIT..." appears during processing
   - "X" is displayed if no question is detected
   - "Paused" appears when screenshot loop is paused

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file with:
```
API_KEY=your_gemini_api_key_here
```

### Customizable Settings
You can modify these variables in `app.py`:
- `countdown` - Time between screenshots (default: 12 seconds)
- `bg_color` - Background color of the interface
- `text_color` - Text color of the interface

### Custom Answer Examples
Create a `forwlan.txt` file in the project root to provide custom question/answer examples that help improve accuracy for specific question types.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 📋 Requirements

- Python 3.6+
- Internet connection (for Gemini API access)
- Google Generative AI API key
- Required libraries (automatically installed via requirements.txt):
  - `tkinter` (usually included with Python)
  - `Pillow`
  - `google-generativeai`
  - `keyboard`
  - `python-dotenv`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🔧 Troubleshooting

### Common Issues

**"No Key" Error:**
- Ensure your `.env` file exists and contains a valid API key
- Check that the API key is correctly formatted

**"GE Err" Error:**
- Verify your internet connection
- Confirm your Gemini API key is valid and has proper permissions
- Check if you've exceeded API rate limits

**Application Not Responding:**
- Try the global hotkeys (`Ctrl+Alt`, `Ctrl+Shift`, `Ctrl+Space`)
- Right-click on the window for the context menu
- Force close and restart if necessary

**Screenshots Not Working:**
- Ensure the `screenshots/` directory exists
- Check file permissions in the project directory
- Verify screen capture permissions on your system

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 📃 License

MIT License — free to use, modify, and build upon.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 📧 Contact

- Chater Marzougui - [@Chater-marzougui](linkedin-url) - chater.mrezgui2002@gmail.com <br/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## ⚠️ Disclaimer

This tool is provided for educational purposes only. Users are responsible for ensuring their use complies with all applicable laws, regulations, and institutional policies. The developers assume no responsibility for any misuse of this software.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

🎓 _ScreenSolver: Because every second counts when you're taking a test._


[contributors-shield]: https://img.shields.io/github/contributors/chater-marzougui/ScreenSolver.svg?style=for-the-badge
[contributors-url]: https://github.com/chater-marzougui/ScreenSolver/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/chater-marzougui/ScreenSolver.svg?style=for-the-badge
[forks-url]: https://github.com/chater-marzougui/ScreenSolver/network/members
[stars-shield]: https://img.shields.io/github/stars/chater-marzougui/ScreenSolver.svg?style=for-the-badge
[stars-url]: https://github.com/chater-marzougui/ScreenSolver/stargazers
[issues-shield]: https://img.shields.io/github/issues/chater-marzougui/ScreenSolver.svg?style=for-the-badge
[issues-url]: https://github.com/chater-marzougui/ScreenSolver/issues
[license-shield]: https://img.shields.io/github/license/chater-marzougui/ScreenSolver.svg?style=for-the-badge
[license-url]: https://github.com/chater-marzougui/ScreenSolver/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/chater-marzougui-342125299