import streamlit as st
import json
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from openai import OpenAI

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Relia", layout="wide")

# ----------------- FIREBASE CONNECT -----------------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ----------------- OPENAI -----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ----------------- MODE -----------------
query = st.query_params
mode = query.get("mode", "teacher")
session_id = query.get("session", None)

# ----------------- STUDENT PAGE -----------------
if mode == "student":

    st.title("Relia – Student Page")

    if not session_id:
        st.error("Invalid session")
        st.stop()

    session_ref = db.collection("sessions").document(session_id).get()

    if not session_ref.exists:
        st.error("Session not found")
        st.stop()

    session_data = session_ref.to_dict()

    if not session_data.get("active"):
        st.warning("Session closed")
        st.stop()

    questions = session_data.get("questions", [])

    st.subheader("Enter Details")
    name = st.text_input("Student Name")
    roll = st.text_input("Roll No")

    answers = []

    st.subheader("Answer Questions")

    for i, q in enumerate(questions):
        ans = st.text_area(f"Q{i+1}: {q}")
        conf = st.slider(f"Confidence Q{i+1}", 1, 5, 3)
        answers.append({"question": q, "answer": ans, "confidence": conf})

    if st.button("Submit Answers"):
        db.collection("responses").add({
            "session": session_id,
            "name": name,
            "roll": roll,
            "answers": answers
        })
        st.success("Submitted successfully")

# ----------------- TEACHER PAGE -----------------
else:

    st.title("Relia – Teacher Panel")

    st.subheader("Enter Questions")

    questions = []
    for i in range(5):
        q = st.text_input(f"Question {i+1}")
        if q:
            questions.append(q)

    if "session_live" not in st.session_state:
        st.session_state.session_live = False
        st.session_state.session_id = ""

    if st.button("Start Session & Generate QR"):
        if len(questions) == 0:
            st.error("Enter at least 1 question")
        else:
            sid = str(uuid.uuid4())[:6]
            st.session_state.session_id = sid
            st.session_state.session_live = True

            db.collection("sessions").document(sid).set({
                "active": True,
                "questions": questions
            })

    if st.session_state.session_live:
        sid = st.session_state.session_id

        st.success(f"Session Live | Code: {sid}")

        student_link = f"https://relia-mvp-qselxk47cwgfz3mbatjxa9.streamlit.app/?mode=student&session={sid}"
        st.markdown("### Student Link")
        st.code(student_link)

        st.markdown("### QR Code")
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={student_link}")

        if st.button("Stop Session"):
            db.collection("sessions").document(sid).update({"active": False})
            st.session_state.session_live = False
            st.warning("Session stopped")

        if st.button("Generate AI Insight"):
            responses = db.collection("responses").where("session","==",sid).stream()

            full_text = ""
            for r in responses:
                data = r.to_dict()
                full_text += json.dumps(data) + "\n"

            if full_text == "":
                st.warning("No responses yet")
            else:
                prompt = f"""
                Analyze student understanding from responses:
                {full_text}

                Give:
                1. Understanding summary
                2. Where confused
                3. Teaching suggestions
                4. Class level
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.3,
                )

                insight = response.choices[0].message.content
                st.markdown("## AI Insight")
                st.write(insight)

