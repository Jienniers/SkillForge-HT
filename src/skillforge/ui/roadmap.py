"""Roadmap presentation and actions."""

from collections.abc import Callable

import streamlit as st

from skillforge.models import PracticePlan, Roadmap
from skillforge.services.pdf import generate_roadmap_pdf
from skillforge.ui.shared import display_day_name


def render_roadmap(
    plan: Roadmap,
    language: str,
    generate_practice: Callable[[], PracticePlan],
) -> None:
    """Display a roadmap and its practice-generation/PDF actions."""
    st.header(f"📚 {language} - 30 Day Learning Plan")
    columns = st.columns(3)
    for index, (day, topics) in enumerate(plan.items()):
        with columns[index % 3], st.expander(display_day_name(day), expanded=False):
            for topic in topics:
                if topic.lower() == "rest day":
                    st.success("😴 Rest Day")
                else:
                    st.write(f"✅ {topic}")

    generate_column, download_column, _ = st.columns([2, 2, 6])
    with generate_column:
        if st.button("🧠 Generate Practice Questions"):
            try:
                with st.spinner("Generating practice questions..."):
                    st.session_state["practice_questions"] = generate_practice()
            except Exception as error:
                st.error(f"Failed to generate practice questions: {error}")
    with download_column:
        st.download_button(
            label="📄 Download Roadmap PDF",
            data=generate_roadmap_pdf(plan),
            file_name="SkillForge_Roadmap.pdf",
            mime="application/pdf",
        )
