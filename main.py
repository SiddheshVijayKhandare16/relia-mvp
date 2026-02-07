import streamlit as st
import openai

st.set_page_config(page_title="Relia", layout="wide")

# Get API key
openai.api_key = st.secrets.get("OPENAI_API_KEY")

st.title("Relia")

mode = st.radio("Select Mode", ["Teacher", "Student"])

# Store questions
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 25

# Store answers
if "answers" not in st.session_state:
    st.session_state.answers = [""] * 25


# ---------------- TEACHER MODE ----------------
if mode == "Teacher":
    st.header("Relia – Teacher Panel")

    for i in range(25):
        q = st.text_input(f"Question {i+1}", st.session_state.questions[i], key=f"q{i}")
        st.session_state.questions[i] = q

    st.divider()

    if st.button("Generate AI Insight"):
        with st.spinner("Analyzing student answers..."):
            all_answers = "\n".join([a for a in st.session_state.answers if a.strip() != ""])

            if all_answers.strip() == "":
                st.warning("No student answers yet")
            else:
                prompt = f"""
You are an expert teacher.

Analyze these student answers and give:
1. Overall class understanding
2. Weak areas
3. What teacher should reteach
4. Smart teaching suggestion

Student answers:
{all_answers}
"""

                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

                insight = response.choices[0].message.content
                st.subheader("AI Teacher Insight")
                st.write(insight)


# ---------------- STUDENT MODE ----------------
if mode == "Student":
    st.header("Relia – Student Answer Page")

    for i, q in enumerate(st.session_state.questions):
        if q.strip() != "":
            ans = st.text_area(f"Q{i+1}: {q}", key=f"a{i}")
            st.session_state.answers[i] = ans

    if st.button("Submit All Answers"):
        st.success("Answers submitted successfully")
