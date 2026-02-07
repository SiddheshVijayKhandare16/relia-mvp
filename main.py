import streamlit as st
import uuid
from openai import OpenAI

st.set_page_config(page_title="Relia", layout="wide")

# ---------------- CONFIG ----------------
APP_URL = "https://relia-mvp-qselxk47cwgfz3mbatjxa9.streamlit.app"
TEACHER_PASSWORD = "WHITEmushroom@123"

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- MODE ----------------
query = st.query_params
mode = query.get("mode", "student")

# ---------------- SESSION STORAGE ----------------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

# =====================================================
# 👩‍🏫 TEACHER PANEL
# =====================================================
if mode == "teacher":

    st.title("Relia – Teacher Panel")

    # ---- LOGIN ----
    if "logged" not in st.session_state:
        pwd = st.text_input("Enter teacher password", type="password")
        if st.button("Login"):
            if pwd == TEACHER_PASSWORD:
                st.session_state.logged = True
                st.rerun()
            else:
                st.error("Wrong password")
        st.stop()

    coaching = st.text_input("Coaching Name")
    teacher = st.text_input("Teacher Name")
    subject = st.text_input("Subject")
    batch = st.text_input("Batch")

    st.subheader("Enter Questions")
    questions = []
    for i in range(5):
        q = st.text_input(f"Question {i+1}", key=f"q{i}")
        questions.append(q)

    if st.button("Start Session & Generate QR"):
        session_id = str(uuid.uuid4())[:6]

        st.session_state.sessions[session_id] = {
            "coaching": coaching,
            "teacher": teacher,
            "subject": subject,
            "batch": batch,
            "questions": questions,
            "responses": []
        }

        st.session_state.current_session = session_id

    # ---- SESSION LIVE ----
    if "current_session" in st.session_state:

        session_id = st.session_state.current_session
        student_link = f"{APP_URL}/?mode=student&session={session_id}"

        st.success(f"Session Live | Code: {session_id}")

        st.markdown("### Student QR")
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={student_link}")

        st.code(student_link)

        if st.button("Generate AI Insight"):
            data = st.session_state.sessions[session_id]["responses"]

            if not data:
                st.warning("No student responses yet")
            else:
                text = "\n".join(data)

                prompt = f"""
Analyze student answers and tell teacher:
1. Overall understanding
2. Weak areas
3. What to reteach
4. Class performance

Answers:
{text}
"""
                with st.spinner("Analyzing class..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                    )

                st.write(response.choices[0].message.content)

# =====================================================
# 👨‍🎓 STUDENT PAGE
# =====================================================
else:

    st.title("Relia – Student Page")

    session_id = query.get("session")

    if not session_id:
        st.warning("Session not started")
        st.stop()

    if session_id not in st.session_state.sessions:
        st.warning("Invalid session")
        st.stop()

    data = st.session_state.sessions[session_id]

    st.write(f"**Teacher:** {data['teacher']}")
    st.write(f"**Subject:** {data['subject']}")
    st.write(f"**Batch:** {data['batch']}")

    name = st.text_input("Your Name")
    roll = st.text_input("Roll No")
    batch = st.text_input("Batch")

    answers = []

    for q in data["questions"]:
        if q:
            ans = st.text_area(q)
            answers.append(ans)

    confidence = st.slider("Confidence", 1, 5)

    if st.button("Submit"):
        entry = f"{name} | {roll} | {batch} | Confidence:{confidence} | Answers:{answers}"
        st.session_state.sessions[session_id]["responses"].append(entry)
        st.success("Submitted")
