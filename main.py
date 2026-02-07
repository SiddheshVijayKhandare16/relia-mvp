import streamlit as st

st.set_page_config(page_title="Relia", layout="centered")

# ---- MODE SELECT ----
mode = st.sidebar.radio("Select Mode", ["Teacher", "Student"])

# ---- SESSION STORAGE ----
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 25

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ===============================
# TEACHER PAGE
# ===============================
if mode == "Teacher":
    st.title("Relia – Teacher Panel")

    st.write("Enter today's 25 questions:")

    for i in range(25):
        st.session_state.questions[i] = st.text_input(
            f"Question {i+1}",
            st.session_state.questions[i]
        )

    if st.button("Save Questions"):
        st.success("Questions saved. Send students to Student page.")

# ===============================
# STUDENT PAGE
# ===============================
if mode == "Student":
    st.title("Relia – Student Answer Page")

    answers = []

    for i, q in enumerate(st.session_state.questions):
        if q.strip() != "":
            ans = st.text_area(f"Q{i+1}: {q}")
            answers.append(ans)

    if st.button("Submit All Answers"):
        st.success("Answers submitted successfully")


