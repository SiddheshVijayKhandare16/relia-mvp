import streamlit as st
from openai import OpenAI

# 🔑 PASTE YOUR OPENAI KEY HERE
client = OpenAI(api_key="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")

st.set_page_config(page_title="Relia", layout="wide")

# -------------------------------
# Mode select
# -------------------------------
mode = st.sidebar.radio("Select Mode", ["Teacher", "Student"])

# -------------------------------
# Storage
# -------------------------------
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 25

if "answers" not in st.session_state:
    st.session_state.answers = [""] * 25

# -------------------------------
# TEACHER PAGE
# -------------------------------
if mode == "Teacher":
    st.title("Relia – Teacher Panel")
    st.subheader("Enter today's 25 questions")

    for i in range(25):
        st.session_state.questions[i] = st.text_input(
            f"Question {i+1}",
            value=st.session_state.questions[i],
            key=f"q{i}"
        )

    if st.button("Generate Class Insight"):
        all_answers = "\n".join([
            f"Q{i+1}: {st.session_state.questions[i]} \nA: {st.session_state.answers[i]}"
            for i in range(25) if st.session_state.answers[i] != ""
        ])

        if all_answers.strip() == "":
            st.warning("No student answers yet")
        else:
            with st.spinner("AI analysing class understanding..."):

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert teacher coach. Analyse student understanding and give short teacher insight."},
                        {"role": "user", "content": f"Analyse this class response and tell teacher: overall understanding, weak students, strong students, and what to reteach:\n{all_answers}"}
                    ]
                )

                insight = response.choices[0].message.content
                st.success("Teacher Insight")
                st.write(insight)

# -------------------------------
# STUDENT PAGE
# -------------------------------
if mode == "Student":
    st.title("Relia – Student Answer Page")

    for i in range(25):
        q = st.session_state.questions[i]
        if q.strip() != "":
            st.session_state.answers[i] = st.text_area(
                f"Q{i+1}: {q}",
                value=st.session_state.answers[i],
                key=f"a{i}"
            )

    if st.button("Submit All Answers"):
        st.success("Answers submitted successfully")
