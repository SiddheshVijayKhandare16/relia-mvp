import streamlit as st

st.title("Relia MVP")
st.subheader("Quiet classroom insight tool")

# STEP 1: Teacher enters question
st.markdown("### 👩‍🏫 Teacher: Enter today's question")

teacher_question = st.text_input("Type your question here:")

if teacher_question:
    st.markdown("---")

    st.markdown("### 🧑‍🎓 Student View")

    st.write("📌 Question:")
    st.info(teacher_question)

    answer = st.text_area("✍️ Student Answer:")

    if st.button("Submit Answer"):
        if answer.strip() == "":
            st.warning("Please write an answer before submitting.")
        else:
            st.success("✅ Answer submitted!")

            st.markdown("### 📊 Teacher Insight")
            st.write("Student attempted the question.")
else:
    st.warning("Teacher must enter a question first.")
