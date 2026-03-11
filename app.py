import streamlit as st
from ai_engine import generate_notes, chat_with_notes
from flashcard_engine import generate_flashcards
from quiz_engine import generate_quiz
from pdf_reader import extract_text

# ---------------------------
# Page Config
# ---------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Study Assistant")

# ---------------------------
# Session State Setup
# ---------------------------

if "text" not in st.session_state:
    st.session_state.text = ""

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "flash_index" not in st.session_state:
    st.session_state.flash_index = 0

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

# ---------------------------
# Sidebar Navigation
# ---------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Upload Material",
        "Study Notes",
        "Flashcards",
        "Quiz",
        "Chat with Notes"
    ]
)

# ==========================================================
# Upload Page
# ==========================================================

if page == "Upload Material":

    st.header("Upload Study Material")

    option = st.radio(
        "Choose input type",
        ["Text Input", "PDF Upload"]
    )

    if option == "Text Input":

        text = st.text_area(
            "Paste your study material here",
            height=300
        )

        if st.button("Save Material"):

            st.session_state.text = text
            st.success("Material saved!")

    else:

        pdf_file = st.file_uploader(
            "Upload PDF",
            type="pdf"
        )

        if pdf_file:

            text = extract_text(pdf_file)
            st.session_state.text = text

            st.success("PDF loaded successfully!")

# ==========================================================
# Study Notes
# ==========================================================

elif page == "Study Notes":

    st.header("AI Generated Study Notes")

    if st.session_state.text == "":
        st.warning("Upload or paste study material first.")
    else:

        if st.button("Generate Study Notes"):

            with st.spinner("Generating notes..."):

                notes = generate_notes(st.session_state.text)

            st.markdown(notes)

# ==========================================================
# Flashcards
# ==========================================================

elif page == "Flashcards":

    st.header("Flashcards")

    if st.session_state.text == "":
        st.warning("Upload study material first.")

    else:

        if st.button("Generate Flashcards"):

            with st.spinner("Creating flashcards..."):

                cards = generate_flashcards(
                    st.session_state.text
                )

            st.session_state.flashcards = cards
            st.session_state.flash_index = 0

        cards = st.session_state.flashcards

        if cards:

            index = st.session_state.flash_index
            total = len(cards)

            question, answer = cards[index]

            st.markdown(f"### Flashcard {index+1} / {total}")
            st.write(question)

            if st.button("Show Answer"):
                st.success(answer)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("⬅ Previous"):
                    if index > 0:
                        st.session_state.flash_index -= 1
                        st.rerun()

            with col2:
                if st.button("Next ➡"):
                    if index < total - 1:
                        st.session_state.flash_index += 1
                        st.rerun()

# ==========================================================
# Quiz
# ==========================================================

elif page == "Quiz":

    st.header("Quiz")

    if st.session_state.text == "":
        st.warning("Upload study material first.")

    else:

        if st.button("Generate Quiz"):

            with st.spinner("Creating quiz..."):

                q, a = generate_quiz(
                    st.session_state.text
                )

            st.session_state.questions = q
            st.session_state.answers = a
            st.session_state.q_index = 0

        if st.session_state.questions:

            i = st.session_state.q_index
            total = len(st.session_state.questions)

            # Quiz Finished
            if i >= total:

                st.success("🎉 Quiz Completed!")

                if st.button("Restart Quiz"):
                    st.session_state.q_index = 0
                    st.rerun()

            else:

                question = st.session_state.questions[i]

                st.markdown(
                    f"### Question {i+1} / {total}"
                )

                st.write(question)

                user_answer = st.text_input(
                    "Your Answer"
                )

                col1, col2, col3 = st.columns(3)

                # Submit
                with col1:
                    if st.button("Submit Answer"):

                        correct = st.session_state.answers[i]

                        if user_answer.lower().strip() == correct.lower().strip():
                            st.success("✅ Correct!")
                        else:
                            st.error("❌ Incorrect")

                # Hint
                with col2:
                    if st.button("Hint"):
                        st.info(
                            st.session_state.answers[i]
                        )

                # Next
                with col3:
                    if st.button("Next Question"):
                        st.session_state.q_index += 1
                        st.rerun()

# ==========================================================
# Chat with Notes
# ==========================================================

elif page == "Chat with Notes":

    st.header("Chat with your Study Material")

    if st.session_state.text == "":
        st.warning("Upload study material first.")

    else:

        question = st.text_input(
            "Ask something about your notes"
        )

        if st.button("Ask AI"):

            with st.spinner("Thinking..."):

                response = chat_with_notes(
                    question,
                    st.session_state.text
                )

            st.markdown("### AI Answer")
            st.write(response)