import streamlit as st

st.title("Relia MVP")
st.subheader("Quiet classroom insight tool")

question = "What is Photosynthesis?"

st.write("📌 Question:")
st.info(question)

answer = st.text_area("✍️ Student Answer:")

if st.button("Submit Answer"):
    st.success("✅ Answer submitted!")

    st.write("### Teacher Insight")
    st.write("Student understands the topic at a basic level.")
