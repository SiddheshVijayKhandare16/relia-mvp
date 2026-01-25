import streamlit as st

st.set_page_config(page_title="Relia", layout="wide")

# ----------------------------
# APP TITLE
# ----------------------------
st.title("Relia")

st.markdown("---")

# ----------------------------
# SESSION STATE STORAGE
# ----------------------------
if "questions" not in st.session_state:
    st.session_state.questions = [""] * 25

if "answers" not in st.session_state:
    st.session_state.answers = [""] * 25

if "submitted" not in st.session_state:
    st.session_state.submitted = False


# ----------------------------
# TEACHER QUESTION INPUT
# ----------------------------
st.header("👩‍🏫 Teacher: Enter Today's Questions")

for i in range(25):
    st.session_state.questions[i] = st.text_input(
        f"Question {i+1}",
        value=st.session_state.questions[i],
        placeholder="Type question here..."
    )

st.markdown("---")

# ----------------------------
# STUDENT ANSWER PAGE
# ----------------------------
st.header("🧑‍🎓 Student: Answer All Questions")

for i in range(25):
    if st.session_state.questions[i].strip() != "":
        st.session_state.answers[i] = st.text_area(
            f"Answer for Question {i+1}: {st.session_state.questions[i]}",
            value=st.session_state.answers[i],
            placeholder="Write student answer here..."
        )

# Submit button
if st.button("Submit All Answers"):
    st.session_state.submitted = True
    st.success("All answers submitted successfully!")

st.markdown("---")

# ----------------------------
# TEACHER INSIGHT PAGE
# ----------------------------
st.header("📊 Teacher Insight (All Responses)")

if not st.session_state.submitted:
    st.info("No answers submitted yet.")
else:
    for i in range(25):
        q = st.session_state.questions[i].strip()
        a = st.session_state.answers[i].strip()

        if q != "":
            st.subheader(f"Q{i+1}: {q}")

            if a == "":
                st.warning("⚠️ No answer submitted.")
            else:
                st.write(f"✅ Student Answer: {a}")

            st.markdown("---")
