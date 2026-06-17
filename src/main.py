from openai import OpenAI
import json
import streamlit as st
import re
import streamlit.components.v1 as components
from streamlit_ace import st_ace
from prompts import (
    PRACTICE_SYSTEM_PROMPT,
    PLAN,
    CHECK_ANSWER_PROMPT,
    HINT_SYSTEM_PROMPT,
    HINT_LEVEL_1,
    HINT_LEVEL_2,
)

jsonRoadmapFile = "./data/roadmap.json"


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
    return generate_answer(
        CHECK_ANSWER_PROMPT(question=question, user_code=user_code), ""
    )


wholePlan = ""


st.set_page_config(page_title="SkillForge", page_icon="🚀", layout="wide")

st.title("🚀 SkillForge")
st.write("Generate a personalized 30-day programming roadmap.")


def get_level(xp):
    if xp < 100:
        return "🌱 Beginner"
    elif xp < 300:
        return "⚡ Apprentice"
    elif xp < 600:
        return "🔥 Intermediate"
    elif xp < 1000:
        return "🚀 Advanced"
    else:
        return "👑 SkillForge Master"


# Sidebar
with st.sidebar:
    st.header("User Input")

    language = st.selectbox(
        "Programming Language", ["Python", "JavaScript", "Java", "C++", "Go"]
    )

    generate = st.button("Generate Plan", use_container_width=True)

    st.header("📊 Your Stats")

    st.metric("XP", st.session_state.get("xp", 0))

    st.write(f"Level: {get_level(st.session_state.get('xp', 0))}")

    passed_days = len(
        [
            key
            for key, value in st.session_state.items()
            if key.startswith("done_day_") and value
        ]
    )

    st.metric("Days Completed", f"{passed_days}/30")

    progress = passed_days / 30

    st.progress(progress)

    if st.button("Refresh", use_container_width=True):
        st.rerun()


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
    if "xp" not in st.session_state:
        st.session_state["xp"] = 0


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


def generate_practice_questions(plan, max_retries=3):
    for attempt in range(max_retries):

        raw = generate_answer(
            json.dumps(plan),
            PRACTICE_SYSTEM_PROMPT,
        )

        try:
            cleaned = clean_prac_json(raw)
            data = json.loads(cleaned)

            # ------------------------
            # Validate structure
            # ------------------------
            valid = True

            for day, day_content in data.items():

                # Every day must be a dict
                if not isinstance(day_content, dict):
                    valid = False
                    break

                for topic, questions in day_content.items():

                    # Every topic must have exactly 3 questions
                    if not isinstance(questions, list) or len(questions) != 3:
                        valid = False
                        break

                if not valid:
                    break

            if valid:
                return data

        except Exception:
            pass

    raise ValueError(
        "Failed to generate valid practice questions after multiple attempts."
    )


from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4


def generate_roadmap_pdf_bytes(plan):

    buffer = BytesIO()  # 👈 MEMORY FILE

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.HexColor("#4B7BEC"),
        spaceAfter=20,
    )

    day_style = ParagraphStyle(
        "DayStyle",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.black,
        spaceAfter=10,
    )

    topic_style = ParagraphStyle(
        "TopicStyle",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=5,
    )

    content = []

    content.append(Paragraph("🚀 SkillForge Roadmap", title_style))
    content.append(Spacer(1, 10))

    for day, topics in plan.items():

        content.append(Paragraph(day.replace("_", " ").title(), day_style))

        if not topics:
            content.append(Paragraph("😴 Rest / Theory Day", topic_style))
        else:
            for t in topics:
                content.append(Paragraph(f"• {t}", topic_style))

        content.append(Spacer(1, 10))

    doc.build(content)

    buffer.seek(0)  # 👈 rewind for download

    return buffer


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

    # -----------------------------
    # BUTTON ROW (SIDE BY SIDE)
    # -----------------------------
    btn_col1, btn_col2, btn_spacer = st.columns([2, 2, 6])

    with btn_col1:
        if st.button("🧠 Generate Practice Questions"):

            raw = generate_answer(
                json.dumps(st.session_state["plan"]), PRACTICE_SYSTEM_PROMPT
            )

            cleaned = clean_prac_json(raw)
            practice_questions = json.loads(cleaned)

            print("\n===== GENERATED PRACTICE QUESTIONS =====")
            print(json.dumps(practice_questions, indent=4))

            st.session_state["practice_questions"] = practice_questions

    with btn_col2:
        pdf_buffer = generate_roadmap_pdf_bytes(st.session_state["plan"])

        st.download_button(
            label="📄 Download Roadmap PDF",
            data=pdf_buffer,
            file_name="SkillForge_Roadmap.pdf",
            mime="application/pdf",
        )


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
def show_popup(text):
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

    # Handle theory/setup days
    if isinstance(day_data, list):

        if len(day_data) == 0:
            st.info("No coding practice for this day (setup/theory day).")
            st.stop()

        else:
            st.error(
                f"Invalid practice format for {selected_day}. "
                "Expected a dictionary but received a list."
            )
            st.write(day_data)
            st.stop()

    if not isinstance(day_data, dict):
        st.error(f"Unexpected format: {type(day_data)}")
        st.write(day_data)
        st.stop()

    if len(day_data) == 0:
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
                    if not st.session_state.get(f"xp_awarded_{result_key}", False):

                        st.session_state["xp"] += 10
                        st.session_state[f"xp_awarded_{result_key}"] = True
                        st.rerun()
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

                hint_key = f"hint_stage_{selected_day}_{topic}_{i}"
                hint_stage = st.session_state.get(hint_key, 0)

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

                col1, col_spacer, col2 = st.columns([2, 6, 2])

                # ------------------------
                # CHECK BUTTON
                # ------------------------
                with col1:
                    if st.button("🧪 Check", key=f"check_{key}"):

                        result = check_answer(question, answer)
                        st.session_state[result_key] = result

                        correct, total = get_day_progress(day_data, selected_day)

                        if correct == total and total > 0:
                            st.session_state[f"done_{selected_day}"] = True
                            st.rerun()

                        show_popup(result)

                # ------------------------
                # HINT BUTTONS (RIGHT SIDE)
                # ------------------------
                with col2:

                    hint_col1, hint_col2 = st.columns(2)

                    # ---------------- Hint 1 ----------------
                    with hint_col1:
                        if st.button(
                            "💡 Hint 1", key=f"hint1_{selected_day}_{topic}_{i}"
                        ):

                            hint = generate_answer(
                                HINT_LEVEL_1(question), HINT_SYSTEM_PROMPT
                            )
                            st.session_state[f"hint_{key}_1"] = hint

                    # ---------------- Hint 2 ----------------
                    with hint_col2:
                        if st.button(
                            "🧠 Hint 2 (-5 XP)", key=f"hint2_{selected_day}_{topic}_{i}"
                        ):

                            hint = generate_answer(
                                HINT_LEVEL_2(question), HINT_SYSTEM_PROMPT
                            )
                            st.session_state[f"hint_{key}_2"] = hint
                            st.session_state["xp"] -= 5

                # ------------------------
                # DISPLAY HINTS (below buttons)
                # ------------------------
                if f"hint_{key}_1" in st.session_state:
                    st.info(st.session_state[f"hint_{key}_1"])

                if f"hint_{key}_2" in st.session_state:
                    st.warning(st.session_state[f"hint_{key}_2"])

    # ----------------------------
    # MARK DAY COMPLETE
    # ----------------------------
    correct, total = get_day_progress(day_data, selected_day)

    if total > 0 and correct == total:
        st.success("🏁 Day Completed!")
        st.session_state[f"done_{selected_day}"] = True
