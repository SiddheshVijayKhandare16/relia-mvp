import streamlit as st

st.set_page_config(page_title="Relia", layout="centered")

st.title("Relia")

# ------------------------------
# STORE QUESTIONS
# ------------------------------
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 25

if "answers" not in st.session_state:
    st.session_state.answers = [[] for _ in range(25)]

mode = st.radio("Select mode", ["Teacher", "Student"])

# ==============================
# TEACHER MODE
# ==============================
if mode == "Teacher":
    st.header("Teacher Panel — Enter 25 Questions")

    for i in range(25):
        q = st.text_input(f"Question {i+1}", value=st.session_state.questions[i], key=f"q{i}")
        st.session_state.questions[i] = q

    st.success("Questions saved automatically")

    st.divider()
    st.header("View Student Answers")

    for i in range(25):
        if st.session_state.questions[i]:
            st.subheader(f"Q{i+1}: {st.session_state.questions[i]}")
            answers = st.session_state.answers[i]

            if len(answers) == 0:
                st.write("No answers yet")
            else:
                for a in answers:
                    st.write("•", a)

# ==============================
# STUDENT MODE
# ==============================
if mode == "Student":
    st.header("Student Answer Page")

    for i in range(25):
        question = st.session_state.questions[i]

        if question:
            st.subheader(f"Q{i+1}: {question}")
            ans = st.text_area(f"Your answer for Q{i+1}", key=f"a{i}")

            if st.button(f"Submit Q{i+1}", key=f"btn{i}"):
                if ans.strip() != "":
                    st.session_state.answers[i].append(ans)
                    st.success("Answer submitted")
                else:
                    st.warning("Write answer first")
