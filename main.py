import streamlit as st
from openai import OpenAI
import qrcode
from io import BytesIO
import uuid

# ---------- CONFIG ----------
TEACHER_PASSWORD = "WHITEmushroom@123"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Relia", layout="wide")

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "session_active" not in st.session_state:
    st.session_state.session_active = False
if "session_id" not in st.session_state:
    st.session_state.session_id = ""
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 10
if "responses" not in st.session_state:
    st.session_state.responses = []
if "allow_anonymous" not in st.session_state:
    st.session_state.allow_anonymous = True

mode = st.sidebar.radio("Mode", ["Teacher", "Student"])

# =====================================================
# TEACHER LOGIN
# =====================================================
if mode == "Teacher" and not st.session_state.logged_in:
    st.title("Relia Teacher Login")
    pwd = st.text_input("Enter password", type="password")

    if st.button("Login"):
        if pwd == TEACHER_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful")
        else:
            st.error("Wrong password")

# =====================================================
# TEACHER PANEL
# =====================================================
if mode == "Teacher" and st.session_state.logged_in:
    st.title("Relia — Classroom Panel")

    coaching = st.text_input("Coaching Name")
    teacher = st.text_input("Teacher Name")
    subject = st.text_input("Subject")
    batch = st.text_input("Batch")

    session_type = st.selectbox(
        "Session Type",
        ["Instant Insight", "Revision", "Test"]
    )

    st.session_state.allow_anonymous = st.checkbox(
        "Allow anonymous answers",
        value=True
    )

    st.divider()
    st.subheader("Enter Questions")

    for i in range(5):
        st.session_state.questions[i] = st.text_input(
            f"Question {i+1}",
            st.session_state.questions[i]
        )

    # -------- START SESSION --------
    if st.button("Start Session & Generate QR"):
        st.session_state.session_active = True
        st.session_state.session_id = str(uuid.uuid4())[:6]
        st.session_state.responses = []

    # -------- SHOW QR --------
    if st.session_state.session_active:
        st.success(f"Session Live | Code: {st.session_state.session_id}")

        base = st.text_input("Paste your app link once")
        if base:
            student_link = f"{base}?mode=student&session={st.session_state.session_id}"

            qr = qrcode.make(student_link)
            buf = BytesIO()
            qr.save(buf)

            st.image(buf)
            st.code(student_link)

    # -------- STOP SESSION --------
    if st.button("Stop Session"):
        st.session_state.session_active = False

    # -------- AI INSIGHT --------
    if st.button("Generate AI Insight"):
        if len(st.session_state.responses) == 0:
            st.warning("No responses yet")
        else:
            combined = "\n".join(st.session_state.responses)

            prompt = f"""
Analyze class responses and give teacher insight:
1. Overall understanding
2. Weak areas
3. What to reteach
4. Class level

Responses:
{combined}
"""
            with st.spinner("Analyzing class..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )
                st.write(response.choices[0].message.content)

# =====================================================
# STUDENT PANEL
# =====================================================
if mode == "Student":
    params = st.query_params
    session = params.get("session")

    if not session:
        st.title("Relia Student")
        st.info("Scan QR from teacher")
    else:
        st.title("Answer")

        if not st.session_state.allow_anonymous:
            name = st.text_input("Name")
        else:
            name = st.text_input("Name (optional)")

        answers = []
        for i in range(5):
            q = st.session_state.questions[i]
            if q:
                ans = st.text_area(q)
                answers.append(ans)

        confidence = st.selectbox(
            "Confidence",
            ["Low", "Medium", "High"]
        )

        if st.button("Submit"):
            entry = f"{name}: {' | '.join(answers)} ({confidence})"
            st.session_state.responses.append(entry)
            st.success("Submitted")
