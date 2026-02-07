import streamlit as st
from openai import OpenAI

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Relia", layout="wide")

mode = st.sidebar.radio("Select Mode", ["Teacher", "Student"])

# Storage
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 25
if "answers" not in st.session_state:
    st.session_state.answers = [""] * 25

# ---------------- TEACHER MODE ----------------
if mode == "Teacher":
    st.title("Relia – Teacher Panel")
    st.subheader("Enter today's 25 questions:")

    for i in range(25):
        st.session_state.questions[i] = st.text_input(
            f"Question {i+1}",
            value=st.session_state.questions[i]
        )

    st.divider()

    if st.button("Generate AI Insight"):
        all_answers = "\n".join(st.session_state.answers)
        all_questions = "\n".join(st.session_state.questions)

        prompt = f"""
You are an expert teacher assistant.

Questions asked:
{all_questions}

Student answers:
{all_answers}

Give:
1. Student understanding summary
2. Where students are confused
3. Teaching suggestion
4. Class performance level
"""

        with st.spinner("Analyzing class..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )

            insight = response.choices[0].message.content
            st.success("AI Insight Generated")
            st.write(insight)

# ---------------- STUDENT MODE ----------------
if mode == "Student":
    st.title("Relia – Student Answer Page")

    for i in range(25):
        if st.session_state.questions[i]:
            st.session_state.answers[i] = st.text_input(
                st.session_state.questions[i],
                value=st.session_state.answers[i]
            )

    if st.button("Submit All Answers"):
        st.success("Answers submitted successfully")
