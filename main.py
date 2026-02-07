import streamlit as st

st.set_page_config(page_title="Relia", layout="centered")

# =========================
# READ MODE FROM URL
# =========================
query_params = st.query_params
mode = query_params.get("mode", "student")

# =========================
# SESSION STORAGE
# =========================
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 25

# =========================
# TEACHER PAGE
# =========================
if mode == "teacher":
    st.title("Relia – Teacher Panel")

    st.info("Save questions and send student link")

    for i in range(25):
        st.session_state.questions[i] = st.text_input(
            f"Question {i+1}",
            st.session_state.questions[i]
        )

    if st.button("Save Questions"):
        st.success("Questions saved")

    st.divider()

    st.subheader("📎 Student Link")
    st.code("Open same app with ?mode=student", language="text")

# =========================
# STUDENT PAGE
# =========================
else:
    st.title("Relia – Student Answer Page")

    answers = []

    for i, q in enumerate(st.session_state.questions):
        if q.strip() != "":
            ans = st.text_area(f"Q{i+1}: {q}")
            answers.append(ans)

    if st.button("Submit All Answers"):
        st.success("Answers submitted successfully")
