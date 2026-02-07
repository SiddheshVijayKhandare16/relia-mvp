import streamlit as st
from openai import OpenAI
import qrcode
from io import BytesIO
import uuid

# -------- OpenAI ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Relia", layout="wide")

# ---------------- SESSION STORAGE ----------------
if "session_active" not in st.session_state:
    st.session_state.session_active = False
if "session_id" not in st.session_state:
    st.session_state.session_id = ""
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 25
if "answers" not in st.session_state:
    st.session_state.answers = []
if "meta" not in st.session_state:
    st.session_state.meta = {}

mode = st.sidebar.radio("Mode", ["Teacher", "Student"])

# =================================================
# TEACHER PANEL
# =================================================
if mode == "Teacher":
    st.title("Relia — Teacher Panel")

    # Teacher info
    coaching = st.text_input("Coaching Name")
    teacher = st.text_input("Teacher Name")
    subject = st.text_input("Subject")
    batch = st.text_input("Batch")

    session_type = st.selectbox(
        "Select Mode",
        ["Instant Insight", "Revision", "Test"]
    )

    st.divider()
    st.subheader("Enter Questions")

    for i in range(5):  # keep 5 for MVP now
        st.session_state.questions[i] = st.text_input(
            f"Question {i+1}",
            st.session_state.questions[i]
        )

    # -------- START SESSION --------
    if st.button("Generate QR & Start Session"):
        st.session_state.session_active = True
        st.session_state.session_id = str(uuid.uuid4())[:8]
        st.session_state.meta = {
            "coaching": coaching,
            "teacher": teacher,
            "subject": subject,
            "batch": batch,
            "type": session_type,
        }
        st.session_state.answers = []

    # -------- SHOW QR --------
    if st.session_state.session_active:
        st.success("Session Live")

        session_link = st.experimental_get_query_params()
        base_url = st.get_option("browser.serverAddress") or ""
        full_link = f"{st.get_option('browser.serverAddress')}?session={st.session_state.session_id}"

        # fallback link
        full_link = f"{st.runtime.scriptrunner.get_script_run_ctx().request.host_url}?session={st.session_state.session_id}"

        # create QR
        qr = qrcode.make(full_link)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf)

        st.code(full_link, language="text")

        if st.button("Close Session"):
            st.session_state.session_active = False

    # -------- AI INSIGHT --------
    if st.button("Generate AI Insight"):
        if len(st.session_state.answers) == 0:
            st.warning("No student answers yet")
        else:
            text = "\n".join(st.session_state.answers)

            prompt = f"""
Analyze these student responses and tell teacher:
1. Overall understanding
2. Weak areas
3. What to reteach
4. Class level
Responses:
{text}
"""
            with st.spinner("Analyzing class..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )
                st.write(response.choices[0].message.content)

# =================================================
# STUDENT PANEL
# =================================================
if mode == "Student":
    params = st.query_params
    session = params.get("session")

    if not session:
        st.title("Relia Student")
        st.info("Scan QR from teacher")
    else:
        st.title("Answer Questions")

        name = st.text_input("Your Name (optional)")
        roll = st.text_input("Roll No (optional)")

        answers = []

        for i in range(5):
            q = st.session_state.questions[i]
            if q:
                ans = st.text_area(f"{q}")
                answers.append(ans)

        confidence = st.selectbox(
            "Confidence level",
            ["Low", "Medium", "High"]
        )

        if st.button("Submit"):
            text = f"{name}-{roll}: " + " | ".join(answers) + f" (Confidence: {confidence})"
            st.session_state.answers.append(text)
            st.success("Submitted")

