"""Streamlit application composition root."""

import logging

import streamlit as st
from dotenv import load_dotenv

from skillforge.config import Settings
from skillforge.services.gemini import GeminiGenerator
from skillforge.services.generation import (
    create_practice_plan,
    create_roadmap,
    evaluate_answer,
    generate_hint,
)
from skillforge.services.roadmaps import load_roadmap_steps
from skillforge.ui.practice import render_practice_zone
from skillforge.ui.roadmap import render_roadmap
from skillforge.ui.sidebar import render_sidebar
from skillforge.ui.state import reset_learning_session

logging.basicConfig(level=logging.INFO)


def run() -> None:
    """Configure and render one Streamlit application run."""
    load_dotenv()
    st.set_page_config(page_title="SkillForge", page_icon="🚀", layout="wide")
    st.title("🚀 SkillForge")
    st.write("Generate a personalized 30-day programming roadmap.")
    if "plan" not in st.session_state:
        st.info("👇 Generate a roadmap to start your 30-day journey!")
    display_language, generate_requested, refresh_requested = render_sidebar()
    if refresh_requested:
        st.session_state["selected_day"] = "day_1"
        st.rerun()
    if generate_requested:
        _generate_roadmap(display_language)
    plan = st.session_state.get("plan")
    language = st.session_state.get("language", display_language.lower())
    if not plan:
        return
    generator = _generator()
    render_roadmap(plan, display_language, lambda: create_practice_plan(generator, plan))
    practice_plan = st.session_state.get("practice_questions")
    if practice_plan:
        render_practice_zone(
            practice_plan, language,
            lambda question, code: evaluate_answer(generator, question, code, language),
            lambda question, level: generate_hint(generator, question, language, level),
        )


def _generator() -> GeminiGenerator:
    """Create the AI gateway only when an AI feature needs it."""
    return GeminiGenerator(Settings.from_environment())


def _generate_roadmap(display_language: str) -> None:
    """Reset prior state and generate a curriculum for the selected language."""
    reset_learning_session(st.session_state)
    language = display_language.lower()
    st.session_state["language"] = language
    try:
        with st.spinner("Generating roadmap..."):
            settings = Settings.from_environment()
            steps = load_roadmap_steps(settings.roadmap_path, language)
            st.session_state["plan"] = create_roadmap(_generator(), steps)
    except Exception as error:
        st.error(f"Failed to generate roadmap: {error}")
        return
    st.rerun()
