"""Sidebar rendering and controls."""

import streamlit as st

from skillforge.constants import DAYS_IN_PLAN, SUPPORTED_LANGUAGES
from skillforge.services.gamification import level_for_xp
from skillforge.ui.state import completed_day_count


def render_sidebar() -> tuple[str, bool, bool]:
    """Render the sidebar and return language, generate, and refresh actions."""
    with st.sidebar:
        st.header("User Input")
        language = st.selectbox("Programming Language", SUPPORTED_LANGUAGES, key="language_picker")
        generate_requested = st.button("Generate Plan", use_container_width=True)

        st.header("📊 Your Stats")
        xp = int(st.session_state.get("xp", 0))
        completed = completed_day_count(st.session_state)
        st.metric("XP", xp)
        st.write(f"Level: {level_for_xp(xp)}")
        st.metric("Days Completed", f"{completed}/{DAYS_IN_PLAN}")
        st.progress(completed / DAYS_IN_PLAN)
        refresh_requested = st.button("Refresh", use_container_width=True)
    return language, generate_requested, refresh_requested
