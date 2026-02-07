import streamlit as st
import uuid
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Relia", layout="wide")

# 🔐 Password for teacher login (change later)
TEACHER_PASSWORD = "WHITEmushroom@123"

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# SESSION STATE
# -----------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "questions" not in st.session_state:
    st.session_state.questions = [""] * 5

if "responses" not in st.session_state:
    st.session_state.responses = []

if "session_active" not in st.session_state:
    st.session_state.session_active = False

# -----------------------------
# MODE DETECTION
# -----------------------------
query = st.query_params
mode = query.get("mode", "student")

# =========================================================
# 🧑‍🏫 TEACHER PANEL
# =========================================================
if mode == "teacher":

    st.title("Relia – Teacher Panel")

    # 🔐 LOGIN
    if "logged_in" not in st.session_state:
        password = st.text_input("Enter teacher password", type="password")
        if st.button("Login"):
            if password == TEACHER_PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Wrong password")
        st.stop()

    # -----------------------------
    # QUESTIONS INPUT
    # -----------------------------
    st.subheader("Enter today's questions")

    for i in range(5):
        st.session_state.questions[i] = st.text_input(
            f"Question {i+1}",
            value=st.session_state.questions[i]
        )

    # -----------------------------
    # START SESSION
    # -----------------------------
    if st.button("Start Session & Generate QR"):
        st.session_state.session_id = str(uuid.uuid4())[:6]
        st.session_state.responses = []
        st.session_state.session_active = True

    # -----------------------------
    # SESSION LIVE
    # -----------------------------
    if st.session_state.session_active:

        st.success(f"Session Live | Code: {st.session_state.session_id}")

        student_link = f"{st.query_params.get('base','')}/?mode=student&session={st.session_state.session_id}"

        st.markdown("### Student QR")
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={student_link}")

        st.markdown("### Student Link")
        st.code(student_link)

        if st.button("Stop Session"):
            st.session_state.session_active = False
            st.rerun()

    # -----------------------------
    # AI INSIGHT
    # -----------------------------
    st.divider()
    st.subheader("Generate AI Insight")

    if st.button("Generate AI Insight"):

        if not st.session_state.responses:
            st.warning("No student answers yet")
        else:
            all_text = "\n".join(st.session_state.responses)

            prompt = f"""
You are an expert teacher coach.

Analyze student answers and give:

1. Student understanding summary  
2. Where students are confused  
3. Teaching suggestions  
4. Class performance level  

Answers:
{all_text}
"""

            with st.spinner("Analyzing class..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

            st.success("AI Insight Generated")
            st.write(response.choices[0].message.content)

# =========================================================
# 👨‍🎓 STUDENT PAGE
# =========================================================
else:

    st.title("Relia – Student Answer Page")

    session = query.get("session")

    if not session:
        st.warning("Session not started by teacher")
        st.stop()

    name = st.text_input("Your Name")
    roll = st.text_input("Roll No")
    batch = st.text_input("Batch")

    answers = []

    for i, q in enumerate(st.session_state.questions):
        if q.strip() != "":
            ans = st.text_area(q, key=f"ans_{i}")
            answers.append(ans)

    confidence = st.slider("Confidence level", 1, 5)

    if st.button("Submit Answers"):

        combined = f"""
Name: {name}
Roll: {roll}
Batch: {batch}
Confidence: {confidence}

Answers:
{answers}
"""
        st.session_state.responses.append(combined)
        st.success("Submitted successfully")
