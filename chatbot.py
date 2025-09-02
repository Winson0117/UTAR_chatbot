import streamlit as st
import google.generativeai as genai

# --- Setup Gemini ---
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("models/gemini-2.5-flash")

# --- Custom Q&A knowledge base ---
faq = {
    # Campus Basics
    "where is the library": "📚 The library is located in Block G, next to Block H.",
    "what are the cafeteria hours": "🍴 The cafeteria is open from 8:00 AM to 6:00 PM daily.",
    "where is the computer lab": "💻 The computer lab is in Block C, First floor and second floor.",

    # Academic Questions
    "how do i check the final examination timetable": "📝 Login into the student portal and find the exact schedule in the final examination timetable tab.",
    "how do i reset my student portal password": "🔑 Go to the IT helpdesk page and click 'Forgot Password'.",
    "how do i view my grades": "📊 Grades are available on the student portal under 'My Results'.",
    "what courses are offered": "📖 You can check the full list of courses on the programme structure page of the university website.",

    # Staff & Offices
    "where is the administration office": "🏢 The admin office is in Block B, Ground Floor.",
    "how do i contact my lecturer": "📧 You can find lecturer emails on the university directory or contact them directly in Microsoft Teams.",

    # Student Life
    "what clubs can i join": "🎭 There are clubs for sports, debate, drama, robotics, music, and more!",
    "how do i apply for a hostel": "🏠  UTAR does not provide hostels. Students usually rent rooms or apartments near Kampar or Sungai Long campus. You can find listings on property rental sites or student Facebook groups.",

    # Finance & Scholarships
    "how do i pay my fees": "💳 Fees can be paid online via the student portal or at the Finance Office.",
    "are there scholarships available": "🎓 Yes, the university offers merit-based and need-based scholarships. Check the Financial Aid Office.",

    # UTAR-Specific
    "how many libraries does utar have": "🏛 UTAR has two libraries: the Main Library at Kampar Campus and the Mary KUOK Pick Hoo Library at Sungai Long Campus.",
    "what facilities are available on campus": "🏫 UTAR campuses have counselling centre, physiotherapy clinic, bookstore, e-commerce parcel centre, prayer rooms, sports complex, and more.",
    "where are utar campuses located": "📍 UTAR has two main campuses: Kampar Campus in Perak and Sungai Long Campus in Selangor.",
    "does utar support international students": "🌏 Yes, UTAR has International Student Services offering support with visas, welfare, and arrival assistance."
}

# --- Streamlit App ---
st.set_page_config(page_title="Uni Q&A Chatbot", page_icon="🎓")
st.title("🎓 University Q&A Chatbot")

# Store chat history in session_state
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_input = st.text_input("Ask me a question about university life:")

if st.button("Ask"):
    if user_input:
        # Default response
        response = None

        # Step 1: Check FAQ
        for q, ans in faq.items():
            if q in user_input.lower():
                response = ans
                break

        # Step 2: If not in FAQ, ask Gemini
        if response is None:
            try:
                gemini_response = model.generate_content(user_input)
                response = gemini_response.text if gemini_response else "🤔 I couldn't find an answer."
            except Exception as e:
                response = f"⚠️ Error with Gemini API: {e}"

        # Save to history
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", response))

# Display conversation history
if st.session_state.history:
    st.subheader("💬 Conversation")
    for speaker, text in st.session_state.history:
        st.write(f"**{speaker}:** {text}")