import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import date

# ---------------- LOAD API KEY ----------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Check your .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-2.5-flash")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Smart Study Planner",
    page_icon="📚",
    layout="centered"
)

# ---------------- HEADER ----------------
st.title("📚 AI Smart Study Planner")
st.caption("Plan • Learn • Revise — Powered by Google Gemini")
st.markdown("---")

# ---------------- SIDEBAR CHATBOT ----------------
st.sidebar.title("🤖 AI Help Bot")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_question = st.sidebar.text_input("Ask anything:")

if st.sidebar.button("Ask"):
    if user_question.strip():
        reply = model.generate_content(
            f"Answer briefly in simple words for a student:\n{user_question}"
        ).text
        st.session_state.chat.append((user_question, reply))

for q, a in st.session_state.chat[::-1]:
    st.sidebar.markdown(f"**You:** {q}")
    st.sidebar.markdown(f"**AI:** {a}")
    st.sidebar.markdown("---")

# ---------------- INPUT FORM ----------------
with st.form("study_form"):
    subject = st.text_input("📘 Subject", placeholder="Example: Python Programming")
    level = st.selectbox("🎓 Skill Level", ["Beginner", "Intermediate", "Advanced"])
    hours = st.slider("⏰ Study hours per day", 1, 10, 2)

    exam_date = st.date_input(
        "📅 Select Exam Date",
        min_value=date.today()
    )

    submitted = st.form_submit_button("🚀 Generate Plan")

# ---------------- FUNCTIONS ----------------
def generate_plan(subject, level, hours, days_left):
    prompt = f"""
    Create a short day-wise study plan.
    Rules:
    - Bullet points
    - No paragraphs
    - Simple language

    Subject: {subject}
    Level: {level}
    Hours/day: {hours}
    Exam in {days_left} days
    """
    return model.generate_content(prompt).text


def generate_notes(subject):
    prompt = f"""
    Create very short revision notes.
    Rules:
    - Bullet points
    - Headings
    - Exam-focused

    Topic: {subject}
    """
    return model.generate_content(prompt).text

# ---------------- OUTPUT ----------------
if submitted:
    if not subject.strip():
        st.warning("⚠️ Please enter a subject.")
    else:
        days_left = (exam_date - date.today()).days

        with st.spinner("🧠 Gemini is working..."):
            try:
                plan = generate_plan(subject, level, hours, days_left)
                notes = generate_notes(subject)

                st.success("✅ Content Generated")

                st.markdown("## 🗓 Study Plan")
                st.markdown(plan)

                st.markdown("---")

                st.markdown("## 📝 Quick Revision Notes")
                st.markdown(notes)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Hackathon Project • Google Gemini API • Streamlit")
