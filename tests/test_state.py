from skillforge.ui.state import reset_learning_session, result_key, update_day_progress


def test_progress_awards_xp_only_once_per_correct_question() -> None:
    state: dict[str, object] = {"xp": 0}
    day_data = {"Functions": ["Question"]}
    state[result_key("day_1", "Functions", 0)] = "✅ Correct"

    assert update_day_progress(state, "day_1", day_data) == (1, 1)
    assert state["xp"] == 10
    assert update_day_progress(state, "day_1", day_data) == (1, 1)
    assert state["xp"] == 10


def test_reset_removes_all_learning_progress() -> None:
    state: dict[str, object] = {
        "xp": 90,
        "done_day_1": True,
        "completed_result_day_1_topic_0": True,
        "hint_charged_day_1_topic_0_2": True,
        "plan": {"day_1": []},
        "unrelated_widget": "keep",
    }

    reset_learning_session(state)

    assert state == {"xp": 0, "unrelated_widget": "keep"}
