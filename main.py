import streamlit as st

st.set_page_config(page_title="Relia", layout="centered")

# Read mode from URL
mode = st.query_params.get("mode", "student")

# Shared question storage
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 25

# ---------------- TEACHER PAGE ----------------
if mode == "teacher":
    st.title("Relia – Teacher Panel")

    st.subheader("Paste today's 25 questions")

    for i in range(25):
        q = st.text_input(f"Question {i+1}", st.session_state.questions[i])
        st.session_state.questions[i] = q

    st.success("Questions saved. Send student link.")

# ---------------- STUDENT PAGE ----------------
else:
    st.title("Relia – Student Answer Page")

    for i, q in enumerate(st.session_state.questions):
        if q.strip() != "":
            st.subheader(f"Q{i+1}: {q}")
            st.text_area("Your answer", key=f"ans{i}")

    if st.button("Submit All Answers"):
        st.success("Answers submitted successfully")

