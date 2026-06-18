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

## 🧩 Challenges Faced, Solutions & Learnings

During the development of this project, one of the main challenges was connecting the backend logic with the Streamlit frontend. Since this was my first time building a full application using Streamlit, it initially took some time to understand how Streamlit’s execution model and `session_state` work together to manage dynamic UI updates and persistent data.

Another difficulty was adapting certain features to fit within Streamlit’s limitations, especially around real-time updates, state persistence, and interactive components. Instead of forcing traditional frontend patterns, I had to rethink and redesign parts of the application to align with Streamlit’s reactive nature.

### 🛠️ How I solved it

I solved these issues by designing the application architecture around Streamlit’s constraints rather than against them. This included:

* Relying heavily on `st.session_state` for persistent data flow
* Structuring UI updates to work with Streamlit’s rerun behavior
* Breaking features into modular logic that fits Streamlit’s execution cycle
* Iteratively testing and adjusting interactions to behave as expected in a reactive environment

### 📚 What I learned

This project helped me gain strong practical experience with Streamlit and reactive Python-based UI development. I learned how to quickly build and ship full-stack prototypes using only Python, and how to design applications that work naturally within Streamlit’s architecture.

Most importantly, I discovered how powerful Streamlit can be for rapidly turning backend logic into a functional and interactive frontend, which will significantly speed up my future projects and prototyping workflows.

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

### 🏆 XP Rewards

| Action | XP |
|----------|----------:|
| Correctly solve a coding question | +10 XP |
| Complete Day 1 (First Day Achievement) | +10 XP Bonus |
| Complete Day 30 (Final Day Achievement) | +50 XP Bonus |

### 💡 XP Costs

| Action | XP Cost |
|----------|----------:|
| Use Hint 2 (Advanced Hint) | -5 XP |

### 📈 Level Progression

| Level | XP Required |
|---------|---------:|
| 🌱 Beginner | 0 - 99 XP |
| ⚡ Apprentice | 100 - 299 XP |
| 🔥 Intermediate | 300 - 599 XP |
| 🚀 Advanced | 600 - 999 XP |
| 👑 SkillForge Master | 1000+ XP |

### 🎯 Progress Tracking

Users earn XP by solving coding challenges and completing roadmap milestones. Progress is tracked throughout the learning journey and reflected in the sidebar dashboard, which displays:

- Current XP
- Current Level
- Days Completed
- Overall Roadmap Progress

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
or

```bash
pip install -r requirements.txt
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