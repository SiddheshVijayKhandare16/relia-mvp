import streamlit as st

# -----------------------------
# Relia MVP (Mode Based)
# -----------------------------

st.set_page_config(page_title="Relia", layout="centered")

# Read mode from URL
mode = st.query_params.get("mode", "student")

# Shared question storage
if "question" not in st.session_state:
    st.session_state.question = "What is Photosynthesis?"

if "answers" not in st.session_state:
    st.session_state.answers = []

# -----------------------------
# Teacher Mode
# -----------------------------
if mode == "teacher":
    st.title("Relia")

    st.subheader("👩‍🏫 Teacher Panel")

    new_q = st.text_input(
        "Enter today's question:",
        value=st.session_state.question
    )

    if st.button("Update Question"):
        st.session_state.question = new_q
        st.success("Question updated!")

    st.markdown("---")

    st.subheader("📊 Answers Received")

    if len(st.session_state.answers) == 0:
        st.info("No student answers yet.")
    else:
        for i, ans in enumerate(st.session_state.answers, 1):
            st.write(f"{i}. {ans}")

# -----------------------------
# Student Mode
# -----------------------------
else:
    st.title("Relia")

    st.subheader("🧑‍🎓 Student View")

    st.markdown("### Question:")
    st.info(st.session_state.question)

    answer = st.text_area("Your Answer:")

    if st.button("Submit Answer"):
        if answer.strip():
            st.session_state.answers.append(answer)
            st.success("Answer submitted!")
        else:
            st.warning("Please type an answer first.")
