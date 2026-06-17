import streamlit as st


def check_achievements(selected_day):
    bonus_given = set(st.session_state.get("bonus_given", []))

    if "xp" not in st.session_state:
        st.session_state["xp"] = 0

    completed_days = len(
        [k for k, v in st.session_state.items() if k.startswith("done_") and v]
    )

    print("Completed Days:", completed_days)
    print("Bonus Given:", bonus_given)
    print("Selected Day:", selected_day)

    # FIRST DAY
    if selected_day == 1 and selected_day not in bonus_given:
        st.session_state["xp"] += 10
        st.toast("🏆 First Day Completed! +10 XP Bonus", icon="🎉")
        st.balloons()

        bonus_given.add(selected_day)

    # LAST DAY
    if selected_day == 30:

        # if completed_days < 29:
        #     st.toast("⛔ Complete previous 29 days first!", icon="⚠️")
        #     return

        st.session_state["xp"] += 50
        print("HI")
        st.toast("👑 Final Day Completed! +50 XP Bonus", icon="🔥")
        st.balloons()

        bonus_given.add(selected_day)
    # # LAST DAY
    # if selected_day == 30 and selected_day not in bonus_given:

    #     if completed_days < 29:
    #         st.toast("⛔ Complete previous 29 days first!", icon="⚠️")
    #         return

    #     st.session_state["xp"] += 50
    #     st.toast("👑 Final Day Completed! +50 XP Bonus", icon="🔥")
    #     st.balloons()

    #     bonus_given.add(selected_day)


check_achievements("30")
