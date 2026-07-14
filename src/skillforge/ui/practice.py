"""Interactive practice-zone rendering."""

from collections.abc import Callable

import streamlit as st
from streamlit_ace import st_ace

from skillforge.constants import (
    ACHIEVEMENT_SOUND_PATH,
    ADVANCED_HINT_COST_XP,
    DAY_COMPLETE_SOUND_PATH,
)
from skillforge.models import PracticeDay, PracticePlan
from skillforge.services.gamification import can_buy_advanced_hint, completion_reward
from skillforge.ui.shared import display_day_name, play_sound, show_result_dialog
from skillforge.ui.state import completed_day_count, question_key, result_key, update_day_progress


def render_practice_zone(
    practice_plan: PracticePlan,
    language: str,
    evaluate: Callable[[str, str], str],
    request_hint: Callable[[str, int], str],
) -> None:
    """Render the coding exercises and delegate AI work to supplied callables."""
    st.divider()
    st.header(f"🧠 Practice Zone ({language})")
    selected_day = st.selectbox(
        "📅 Select a Day", list(practice_plan), format_func=_format_day_option, key="selected_day"
    )
    day_data = practice_plan[selected_day]
    if not day_data:
        st.info("No coding practice for this day (setup/theory day).")
        return
    st.subheader(f"📘 {display_day_name(selected_day)}")
    for topic, questions in day_data.items():
        with st.expander(f"📌 {topic}"):
            for index, question in enumerate(questions):
                _render_question(
                    selected_day, topic, index, question, language, day_data, evaluate, request_hint
                )
    correct, total = update_day_progress(st.session_state, selected_day, day_data)
    if total and correct == total:
        _complete_day(selected_day)
        st.success("🏁 Day Completed!")


def _format_day_option(day: str) -> str:
    label = display_day_name(day)
    return f"{label} (✅ Passed)" if st.session_state.get(f"done_{day}") else label


def _render_question(
    day: str,
    topic: str,
    index: int,
    question: str,
    language: str,
    day_data: PracticeDay,
    evaluate: Callable[[str, str], str],
    request_hint: Callable[[str, int], str],
) -> None:
    st.markdown(f"### ❓ Question {index + 1}")
    st.write(question)
    key = question_key(day, topic, index)
    feedback_key = result_key(day, topic, index)
    answer = st_ace(
        value=st.session_state.get(key, ""),
        language=language,
        theme="monokai",
        height=250,
        key=f"ace_{key}",
        auto_update=True,
    )
    check_column, _, hint_column = st.columns([2, 6, 2])
    with check_column:
        if st.button("🧪 Check", key=f"check_{key}"):
            st.session_state[feedback_key] = evaluate(question, answer or "")
            correct, total = update_day_progress(st.session_state, day, day_data)
            if total and correct == total:
                _complete_day(day)
            show_result_dialog(st.session_state[feedback_key])
    with hint_column:
        first_hint_column, second_hint_column = st.columns(2)
        with first_hint_column:
            if st.button("💡 Hint 1", key=f"hint1_{key}"):
                st.session_state[f"hint_{key}_1"] = request_hint(question, 1)
        with second_hint_column:
            if st.button("🧠 Hint 2 (-5 XP)", key=f"hint2_{key}"):
                _request_advanced_hint(key, question, request_hint)
    if f"hint_{key}_1" in st.session_state:
        st.info(st.session_state[f"hint_{key}_1"])
    if f"hint_{key}_2" in st.session_state:
        st.warning(st.session_state[f"hint_{key}_2"])
    if st.session_state.get(f"completed_{feedback_key}"):
        st.success("✅ Question Completed!")


def _request_advanced_hint(
    key: str, question: str, request_hint: Callable[[str, int], str]
) -> None:
    charged_key = f"hint_charged_{key}_2"
    if not st.session_state.get(charged_key) and not can_buy_advanced_hint(
        int(st.session_state.get("xp", 0))
    ):
        st.error("You don't have enough XP to use this hint!")
        return
    st.session_state[f"hint_{key}_2"] = request_hint(question, 2)
    if not st.session_state.get(charged_key):
        st.session_state["xp"] -= ADVANCED_HINT_COST_XP
        st.session_state[charged_key] = True


def _complete_day(day: str) -> None:
    """Persist a new completion and announce any applicable milestone reward."""
    done_key = f"done_{day}"
    if st.session_state.get(done_key):
        return
    st.session_state[done_key] = True
    reward = completion_reward(
        day_number=int(day.removeprefix("day_")),
        completed_day_count=completed_day_count(st.session_state),
        first_bonus_given=bool(st.session_state.get("first_day_bonus_given")),
    )
    if reward.achievement == "first_completion":
        st.session_state["first_day_bonus_given"] = True
        st.session_state["xp"] = int(st.session_state.get("xp", 0)) + reward.xp
        st.toast("🏆 First Day Completed! +10 XP Bonus", icon="🎉")
        st.balloons()
        play_sound(ACHIEVEMENT_SOUND_PATH)
    elif reward.achievement == "final_completion":
        st.session_state["xp"] = int(st.session_state.get("xp", 0)) + reward.xp
        st.toast("👑 Final Day Completed! +50 XP Bonus", icon="🔥")
        st.balloons()
    else:
        play_sound(DAY_COMPLETE_SOUND_PATH)
    st.toast("🏁 Day Completed!", icon="🎉")
    st.balloons()
