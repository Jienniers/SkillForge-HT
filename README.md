# 🚀 SkillForge – AI Powered 30-Day Coding Learning Platform

---

## 📌 Short Description

SkillForge is an interactive AI-powered coding practice platform built with Streamlit.  
It generates a personalized 30-day learning roadmap, provides coding practice questions, and evaluates user answers using a local LLM (Qwen 2.5 Coder via OpenAI-compatible API).

---

## 🧠 What This Project Does

SkillForge transforms a static learning roadmap into an interactive coding experience:

- Users select a programming language (Python, JavaScript, Java, C++, Go)
- The system generates a **30-day structured learning plan**
- Each day contains topics and coding exercises
- Users solve coding problems directly in the browser using an embedded editor
- AI evaluates answers and returns:
  - Correct / Incorrect feedback
  - Explanation and fix suggestions
- Users earn **XP points** for correct answers
- A gamified system tracks:
  - Completed days
  - Progress across the 30-day roadmap
- Users can request:
  - AI-generated practice questions per day
  - Hints (with XP penalty for advanced hints)
- A downloadable **PDF roadmap** is generated for offline use

---

## 🐍 How Python is Used

Python is the core engine of SkillForge:

### 🔹 Backend Logic
- Handles roadmap generation and transformation
- Parses and validates AI-generated JSON responses
- Manages user progress and scoring logic

### 🔹 Streamlit UI
- Builds interactive web interface
- Uses buttons, selectboxes, expanders, and layout columns
- Displays real-time feedback and progress updates

### 🔹 Session State Management
- `st.session_state` is used to persist:
  - XP system
  - Completed days
  - Practice question results
  - Generated roadmap
  - Achievements and hints

### 🔹 AI Integration (Local LLM)
- Uses `OpenAI` Python SDK
- Connected to a **local model server (LM Studio / OpenAI-compatible API)**
- Model used: `qwen2.5-coder-7b-instruct`
- Responsible for:
  - Roadmap generation
  - Code evaluation
  - Hint generation
  - Practice question creation

---

## 🖼️ Screenshots

![Main Page](/Screenshots/Screenshot1.png)
![Correct Answer Page](/Screenshots/Screenshot2.png)
![Day Completed Page](/Screenshots/Screenshot3.png)



---

## ⚙️ Key Features

### 🎯 AI-Generated Learning Roadmap
- Generates a structured 30-day coding plan per language

### 💻 Interactive Coding Environment
- Built-in code editor using `streamlit-ace`

### 🤖 AI Code Evaluation
- Checks correctness of user solutions using local LLM

### 🧠 Practice Question Generator
- Generates structured coding exercises per day/topic

### 💡 Hint System
- Multi-level AI hints
- XP penalty system for advanced hints

### 🏆 Gamification System
- XP points for correct answers
- Day completion tracking
- Achievement triggers (first day, final day, etc.)

### 📊 Progress Tracking
- Tracks completed days
- Displays XP level progression

### 📄 PDF Export
- Generates downloadable roadmap PDF using ReportLab

---

## 📁 File Structure

This project is currently implemented as a **single-file Streamlit application** for simplicity and rapid development. As the project evolves, the codebase is intended to be modularized into multiple files and packages to improve maintainability, scalability, and separation of concerns.

Main logical sections inside the file:

- 🔹 AI model interface (`generate_answer`)
- 🔹 Roadmap generation system
- 🔹 Practice question generator
- 🔹 Answer checking engine
- 🔹 XP and achievement system
- 🔹 Streamlit UI layout
- 🔹 Session state management
- 🔹 PDF generator
- 🔹 Hint system

Supporting file:
- `./data/roadmap.json` → contains learning roadmap templates

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install streamlit openai streamlit-ace reportlab
````

### 2. Run local LLM

Make sure LM Studio or any OpenAI-compatible server is running:

* Model: `qwen2.5-coder-7b-instruct`
* Base URL: `http://localhost:1234/v1`

### 3. Start Streamlit app

```bash
streamlit run src/main.py
```

---

## ⚠️ Important Notes

* This project depends on a **local LLM (not cloud OpenAI API)**
* All AI responses are generated locally via OpenAI-compatible endpoint
* Session state is heavily used for persistence
* All progress is stored only during runtime (no database yet)
* Accuracy depends on local model response quality

---

## 🏆 Project Highlights

* Fully AI-driven learning system
* Gamified coding practice environment
* Local-first LLM architecture
* Real-time evaluation + feedback loop
* 30-day structured learning system

---