"""Small Streamlit-only presentation helpers."""

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


@st.dialog("Result")
def show_result_dialog(text: str) -> None:
    """Show code-evaluation feedback in the existing modal presentation."""
    st.markdown(text)


def play_sound(path: Path) -> None:
    """Embed an autoplaying bundled MP3 without creating a temporary file."""
    encoded_audio = base64.b64encode(path.read_bytes()).decode("ascii")
    components.html(
        f'<audio autoplay><source src="data:audio/mp3;base64,{encoded_audio}" '
        'type="audio/mp3"></audio>',
        height=0,
    )


def display_day_name(day: str) -> str:
    """Format a canonical day key for display."""
    return day.replace("_", " ").title()
