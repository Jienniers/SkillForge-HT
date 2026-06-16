from openai import OpenAI
import json
import streamlit as st
import re
from streamlit_ace import st_ace

jsonRoadmapFile = "./data/roadmap.json"

USE_BREAKS = "False"

PRACTICE_SYSTEM_PROMPT = """
You are an expert coding exercise generator for programming learners.

You MUST generate ONLY PRACTICAL CODING EXERCISES.

You are NOT allowed to generate:
❌ theory questions
❌ definitions
❌ explanations of concepts
❌ setup instructions
❌ environment setup
❌ installation steps
❌ "What is Python/Java/JS"
❌ multiple-choice questions
❌ conceptual discussion questions

---

CRITICAL RULE (ABSOLUTE):

Every question MUST require writing actual executable code.

If a question cannot be solved by writing code → DO NOT include it.

---

INPUT:

You will receive a structured 30-day learning plan.

Each day contains topics.

---

TASK:

For each day:

- Extract ONLY topics that involve hands-on coding
- Generate exactly 3 coding questions per topic
- If a topic has NO coding activity → IGNORE it
- If a day has NO coding topics at all → return EMPTY list for that day

---

VERY IMPORTANT RULE (NO EXCEPTIONS):

If a day contains only:

- setup
- installation
- theory
- introduction
- history
- "what is X"

👉 THEN OUTPUT:
That day must be:

"day_x": []

NO QUESTIONS at all.

---

QUESTION RULES:

Each question MUST:

✔ require writing real code
✔ be runnable or logically implementable
✔ involve solving a programming problem

Each question must NOT:

❌ ask for definitions
❌ ask for explanations
❌ ask for steps to install tools
❌ ask "what is X"
❌ ask conceptual theory

---

QUESTION STYLE ONLY:

Allowed formats:

✔ "Write a function that..."
✔ "Implement a class that..."
✔ "Build a small program that..."
✔ "Create a script that..."
✔ "Write an API endpoint that..."

---

DIFFICULTY RULE:

For each topic:

1. Easy → basic implementation
2. Medium → logic-based function/class
3. Hard → mini project or real-world feature

---

OUTPUT FORMAT (STRICT JSON ONLY):

{
  "day_1": {
    "topic_name": [
      "coding question 1",
      "coding question 2",
      "coding question 3"
    ]
  },
  "day_2": {}
}

OR if no coding exists:

{
  "day_3": {}
}

---

STRICT RULES:

- Output ONLY valid JSON
- No markdown
- No explanations
- No extra text
- No theory questions allowed
- No setup questions allowed
- Every question must be code-writing based
- If no coding exists → empty day object

---

FINAL RULE:

ONLY generate questions that require writing code.
If it cannot be solved with code → DO NOT INCLUDE IT.

Now generate the practice questions.
"""


PLAN = """
You are an expert programming curriculum restructuring engine.

YOU ARE NOT A TEACHER.
YOU ARE NOT A TUTOR.
YOU DO NOT ADD NEW KNOWLEDGE.

YOU ONLY TRANSFORM GIVEN INPUT.

---

CRITICAL RULE (ABSOLUTE):

You MUST ONLY use topics provided in the input roadmap JSON.

❌ NEVER add new topics
❌ NEVER add your own programming knowledge
❌ NEVER introduce Python/JS/Java concepts not present in input
❌ NEVER expand beyond given roadmap content

If something is missing, you MUST NOT guess or fill it.

---

LANGUAGE LOCK RULE (VERY IMPORTANT):

The roadmap is for a SPECIFIC programming language.

- Detect language ONLY from input context (NOT from your assumptions)
- Do NOT switch languages
- Do NOT mix languages
- Do NOT default to Python

If roadmap is JavaScript → only JavaScript concepts/examples
If Java → only Java concepts/examples
If Python → only Python concepts/examples

---

INPUT FORMAT:

You will receive:

1. A list of roadmap topics
2. A flag USE_BREAKS (boolean)

---

YOUR TASK:

Convert the given roadmap into a structured 30-day learning plan.

BUT STRICTLY FOLLOW THESE RULES:

---

CRITICAL TRANSFORMATION RULE:

You are allowed ONLY to:

✔ Reorder given topics
✔ Split given topics into sub-days
✔ Expand ONLY within same topic scope
✔ Break topics into smaller learning steps

You are NOT allowed to:

❌ Add new topics
❌ Add unrelated concepts
❌ Introduce external curriculum knowledge

---

CRITICAL PACING RULE:

- Spread content across exactly 30 days
- No speedrunning
- No compressing topics too much
- Every day must represent a meaningful step

---

STRICT LEARNING RULES:

- Maximum 1 core concept per day
- Large topics MUST be split across multiple days
- No mixing unrelated topics in same day
- Must follow prerequisite order strictly

---

TOPIC EXPANSION RULE (SAFE VERSION):

You may ONLY expand topics like this:

Example:
"Functions" →
- Functions basics
- Parameters & return values
- Higher-order usage (ONLY if applicable in roadmap language)
- Practical exercises

BUT you MUST NOT add unrelated concepts like OOP if not in input.

---

USE_BREAKS RULE:

- If USE_BREAKS = true → allow rest days (max 3)
- If USE_BREAKS = false → NO rest days allowed

---

ANTI-HALLUCINATION RULE (VERY IMPORTANT):

If a concept is NOT in the input roadmap:

❌ Do NOT include it
❌ Do NOT assume it belongs in beginner curriculum
❌ Do NOT fill gaps with generic programming knowledge

ONLY use what is explicitly provided.

---

OUTPUT FORMAT (STRICT JSON ONLY):

{
"day_1": ["topic"],
"day_2": ["topic"],
...
"day_30": ["topic"]
}

RULES:

- Output ONLY valid JSON
- No explanations
- No markdown
- No extra text
- Exactly 30 days required
- Must strictly respect input roadmap content
- No external knowledge injection

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

    language = st.selectbox(
        "Programming Language", ["Python", "JavaScript", "Java", "C++", "Go"]
    )

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
    st.header(f"🧠 Practice Zone ({language})")

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

    if not day_data:
        st.info("No coding practice for this day (setup/theory day).")
        st.stop()

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
                    auto_update=True,
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
