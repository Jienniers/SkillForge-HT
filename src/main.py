from openai import OpenAI
import json
import streamlit as st
import re
from streamlit_ace import st_ace

jsonRoadmapFile = "./data/roadmap.json"

USE_BREAKS = "False"

PRACTICE_SYSTEM_PROMPT = """
You are an expert Python programming tutor and coding assessment generator.

You will be given a 30-day learning plan in JSON format.
Each day contains one or more programming topics.

Your task is to generate PRACTICAL CODING EXERCISES ONLY.

CRITICAL RULE:
You MUST strictly follow the structure of the input plan.
Do NOT move topics between days.
Do NOT merge or shuffle days.
Each day must only use its own topics.

TASK:
For each topic in each day:
Generate exactly 3 PRACTICAL CODING QUESTIONS.

QUESTION RULES:
- ALL questions must be coding-based (no theory-only questions)
- Each question must require writing actual code
- No explanations, no definitions, no conceptual questions
- No pseudo questions like "What is Flask?"
- Instead ask: "Write a Flask app that..."

QUESTION STYLE:
1. Easy → small code snippet task
2. Medium → function/class implementation
3. Hard → mini real-world program or feature

EXAMPLES OF GOOD QUESTIONS:
- "Write a Python function that reverses a list without using built-in reverse()"
- "Create a Flask API with one GET endpoint returning JSON"
- "Write a script that reads a file and counts word frequency"

OUTPUT FORMAT (STRICT JSON ONLY):

{
  "day_1": {
    "topic_name": [
      "coding question 1",
      "coding question 2",
      "coding question 3"
    ]
  }
}

RULES:
- Output ONLY valid JSON
- No explanations
- No markdown
- No extra text
- Every topic MUST have exactly 3 coding questions
- Must follow original day order exactly
- No topic merging or skipping
- All questions MUST require writing code

Now generate coding practice questions for the provided plan.
"""


PLAN = f"""
You are an expert programming curriculum designer.
THIS IS A HARD CONSTRAINT SYSTEM. YOU MUST FOLLOW ALL RULES EXACTLY. NO EXCEPTIONS.

You will be given a list of learning roadmap topics.

Your task is to convert them into a structured 30-day learning plan.

INPUT:
- Array of learning topics (roadmap steps)

---

CRITICAL PARSING RULE (VERY IMPORTANT):
- Treat USE_BREAKS as a REAL BOOLEAN
- If USE_BREAKS is True → rest days are allowed
- If USE_BREAKS is False → rest days are STRICTLY FORBIDDEN

Do NOT interpret this loosely.

---

CRITICAL PACING RULE (MOST IMPORTANT):
- Spread learning evenly across exactly 30 days
- Do NOT speedrun
- Do NOT compress learning into fewer days

---

STRICT LEARNING RULES:
- Maximum 1 core concept per day
- Large topics MUST be split into multiple sub-skills across multiple days
- Never combine multiple unrelated concepts in one day
- Learning must follow prerequisite order strictly

---

TOPIC EXPANSION RULE (CRITICAL FIX FOR REPETITION):

If total topics are fewer than 30 days:

You MUST NOT repeat identical topics.

Instead:

1. Break each topic into sub-skills:
- fundamentals
- implementation
- variations
- edge cases
- real-world usage

2. Convert into progression levels:
- beginner → intermediate → advanced → applied

3. Create applied days:
- mini projects
- debugging exercises
- real-world coding tasks
- refactoring tasks

ONLY if absolutely necessary:
You may revisit a topic, BUT it MUST be transformed
(e.g., "Functions - advanced usage", NOT "Functions" again)

---

LEARNING FLOW RULE:
- One concept must be fully understood before moving forward
- No jumping from basics to frameworks
- No clustering advanced topics early

---

LEARNING ORDER PRIORITY:
1. Syntax, variables, data types
2. Control flow (if/else, loops)
3. Functions
4. Data structures (lists, dicts, sets, tuples)
5. OOP (must be spread across multiple days)
6. File handling & error handling
7. Libraries (requests, numpy, pandas)
8. Web frameworks (Flask/Django)
9. Projects and applied practice

---

ANTI-SPEEDRUN RULE:
- Do NOT finish early
- You MUST use all 30 days meaningfully
- No filler repetition allowed
- Every day must be unique in learning purpose

---

TASK:
1. Expand roadmap into sub-skills
2. Map them into 30 days
3. Ensure correct order
4. Ensure balanced difficulty progression
5. Ensure no repetition unless transformed
6. Respect USE_BREAKS exactly

---

OUTPUT FORMAT (STRICT JSON ONLY):

{{
"day_1": ["topic"],
"day_2": ["topic"],
...
"day_30": ["topic"]
}}

RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- No extra text
- Always return exactly 30 days

Now generate the 30-day plan.
"""


def generate_answer(prompt, promptStructure):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    response = client.chat.completions.create(
        model="qwen2.5-coder-7b-instruct",
        messages=[
            {"role": "system", "content": promptStructure},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content


def roadmapExtract(language):
    with open(jsonRoadmapFile, "r", encoding="utf-8") as f:
        data = json.load(f)

    steps = data["roadmaps"][language]["steps"]
    return steps


def clean_json(text: str):
    # remove ```json or ``` wrappers
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    text = text.strip()

    # extract first {...last...}
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found")

    return text[start : end + 1]


def createPlan(roadmap):
    roadmap_text = json.dumps(roadmap)

    raw = generate_answer(roadmap_text, PLAN)

    cleaned = clean_json(raw)

    try:
        return json.loads(cleaned)
    except Exception as e:
        print("RAW OUTPUT:\n", raw)
        raise ValueError("Model returned invalid JSON")


def check_answer(question, user_code):
    prompt = f"""
You are a strict but helpful coding evaluator.

TASK:
You are given a coding question and a user's answer.

Decide if the answer is correct.

RULES:
- If logic is correct or partially correct → mark as CORRECT
- If wrong → explain clearly what is wrong and how to fix it
- Be concise
- Focus on correctness, not style

OUTPUT FORMAT (STRICT):
If correct:
✅ Correct

If incorrect:
❌ Incorrect
Explanation: <what is wrong>
Fix: <how to fix it>

QUESTION:
{question}

USER CODE:
{user_code}
"""

    return generate_answer(prompt, "")


wholePlan = ""


st.set_page_config(page_title="SkillForge", page_icon="🚀", layout="wide")

st.title("🚀 SkillForge")
st.write("Generate a personalized 30-day programming roadmap.")

# Sidebar
with st.sidebar:
    st.header("Settings")

    language = st.selectbox("Programming Language", ["Python", "JavaScript", "Java"])

    generate = st.button("Generate Plan", use_container_width=True)

currentlyChosenLanguage = ""

# Generate plan when button is clicked
if generate:
    currentlyChosenLanguage = language.lower()
    roadmap = roadmapExtract(currentlyChosenLanguage)

    wholePlan = createPlan(roadmap)

    # Convert to dict if AI returned JSON string
    if isinstance(wholePlan, str):
        try:
            wholePlan = json.loads(wholePlan)
        except json.JSONDecodeError:
            st.error("The AI did not return valid JSON.")
            st.code(wholePlan)
            st.stop()

    # Save plan so it survives reruns
    st.session_state["plan"] = wholePlan
    st.session_state["language"] = language


# ----------------------------
# JSON CLEANER
# ----------------------------
def clean_prac_json(raw: str):
    if not raw:
        return "{}"

    raw = raw.strip()
    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)

    return raw.strip()


# Display plan
if "plan" in st.session_state:

    st.header(f"📚 {st.session_state['language']} - 30 Day Learning Plan")

    plan = st.session_state["plan"]

    cols = st.columns(3)

    for index, (day, topics) in enumerate(plan.items()):

        with cols[index % 3]:

            day_number = day.replace("_", " ").title()

            with st.expander(day_number, expanded=False):

                for topic in topics:

                    if topic.lower() == "rest day":
                        st.success("😴 Rest Day")
                    else:
                        st.write(f"✅ {topic}")

    if st.button("🧠 Generate Practice Questions"):

        raw = generate_answer(
            json.dumps(st.session_state["plan"]), PRACTICE_SYSTEM_PROMPT
        )

        cleaned = clean_prac_json(raw)

        try:
            st.session_state["practice_questions"] = json.loads(cleaned)
        except Exception:
            st.error("LLM returned invalid JSON ❌")
            st.code(raw)
            st.stop()


# ----------------------------
# AI CHECKER
# ----------------------------
def check_answer(question, user_code):
    prompt = f"""
        You are a strict Python unit test checker.

        RULES:
        - Only check if the code satisfies the EXACT requirement
        - Do NOT judge style or intent
        - If the condition exists exactly as required → mark CORRECT
        - If it logically satisfies requirement → mark CORRECT

        QUESTION:
        {question}

        USER CODE:
        {user_code}

        OUTPUT FORMAT:
        Either:
        ✅ Correct

        OR:
        ❌ Incorrect
        Explanation:
        Fix:
        """

    return generate_answer(prompt, "")


# ----------------------------
# POPUP RESULT
# ----------------------------
@st.dialog("Result")
def show_result(text):
    st.markdown(text)


PracticeQuestions = st.session_state.get("practice_questions", None)

if PracticeQuestions:
    # ----------------------------
    # HEADER
    # ----------------------------
    st.divider()
    st.header("🧠 Practice Zone (Python / JS / Java)")

    # ----------------------------
    # FORMAT DAY NAME
    # ----------------------------
    def format_day(day_key: str):
        base = day_key.replace("_", " ").title()

        if st.session_state.get(f"done_{day_key}", False):
            return f"{base} (✅ Passed)"

        return base

    # ----------------------------
    # DAY SELECTOR
    # ----------------------------
    days = list(PracticeQuestions.keys())

    selected_day = st.selectbox(
        "📅 Select a Day", list(PracticeQuestions.keys()), format_func=format_day
    )

    day_data = PracticeQuestions[selected_day]

    st.subheader(f"📘 {selected_day.replace('_', ' ').title()}")

    # ----------------------------
    # TRACK DAY PROGRESS
    # ----------------------------
    def get_day_progress(day_data, day_key):

        total = 0
        correct = 0

        for topic, questions in day_data.items():
            for i, q in enumerate(questions):

                result_key = f"result_{day_key}_{topic}_{i}"
                result = st.session_state.get(result_key, "")

                if "✅ Correct" in result:
                    correct += 1

                total += 1

        return correct, total

    # ----------------------------
    # QUESTIONS UI
    # ----------------------------
    for topic, questions in day_data.items():

        with st.expander(f"📌 {topic}"):

            for i, question in enumerate(questions):

                st.markdown(f"### ❓ Question {i + 1}")
                st.write(question)

                key = f"{selected_day}_{topic}_{i}"
                result_key = f"result_{selected_day}_{topic}_{i}"

                # ------------------------
                # ANSWER INPUT
                # ------------------------
                # answer = st.text_area("✍️ Your Code", key=key, height=120)

                answer = st_ace(
                    value=st.session_state.get(key, ""),
                    language=currentlyChosenLanguage,
                    theme="monokai",
                    height=250,
                    key=f"ace_{key}",
                    auto_update=True
                )

                col1, col2 = st.columns(2)

                # ------------------------
                # CHECK BUTTON (AI)
                # ------------------------
                with col1:
                    if st.button("🧪 Check", key=f"check_{key}"):

                        result = check_answer(question, answer)
                        st.session_state[result_key] = result

                        # 🔥 recompute progress instantly
                        correct, total = get_day_progress(day_data, selected_day)

                        if correct == total and total > 0:
                            st.session_state[f"done_{selected_day}"] = True
                            st.rerun()

                        show_result(result)

    # ----------------------------
    # MARK DAY COMPLETE
    # ----------------------------
    correct, total = get_day_progress(day_data, selected_day)

    if total > 0 and correct == total:
        st.success("🏁 Day Completed!")
        st.session_state[f"done_{selected_day}"] = True
