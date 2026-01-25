import streamlit as st

st.title("Relia MVP")
st.subheader("Quiet classroom insight tool")

# -----------------------------
# STEP 1: Teacher sets question
# -----------------------------
st.markdown("### 👩‍🏫 Teacher Question Setup")

teacher_question = st.text_input(
    "Enter today’s classroom question:",
    "What is Photosynthesis?"
)

st.divider()

# -----------------------------
# Student Answer Section
# -----------------------------
st.markdown("### ✍️ Student Response")

student_answer = st.text_area("Student Answer (type here):")

if st.button("Submit Answer"):
    if student_answer.strip() == "":
        st.warning("Please write an answer before submitting.")
    else:
        st.success("✅ Answer submitted!")

        # Teacher insight (basic MVP logic)
        st.markdown("## Teacher Insight")

        if len(student_answer) < 20:
            st.info("Student response is very short — may need more explanation.")
        else:
            st.success("Student understands the topic at a basic level.")
