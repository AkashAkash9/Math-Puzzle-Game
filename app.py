# Step 1: Project Setup already done (create folder and file)
# Step 2 & 3: app.py starts here

import streamlit as st
import random
import time

# Initialize session state variables if not already
if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.correct = 0
    st.session_state.timer = 30
    st.session_state.question = ""
    st.session_state.answer = 0
    st.session_state.user_answer = ""

# Function to generate questions based on difficulty
def generate_question(difficulty):
    operators = {'Easy': ['+', '-'], 'Medium': ['+', '-', '*'], 'Hard': ['+', '-', '*', '/', '**']}
    op = random.choice(operators[difficulty])
    a = random.randint(1, 10 if difficulty == 'Easy' else 20)
    b = random.randint(1, 10 if difficulty == 'Easy' else 20)
    if op == '/':
        b = random.randint(1, 10)
        a = b * random.randint(1, 10)
    question = f"{a} {op} {b}"
    try:
        answer = round(eval(question), 2)
    except:
        answer = 0
    return question, answer

# Timer control
if st.session_state.started:
    if st.session_state.timer > 0:
        st.session_state.timer -= 1
        time.sleep(1)
    else:
        st.session_state.started = False

st.title("🧠 Math Puzzle Game (Timed Challenges)")

# Difficulty selection before starting
if not st.session_state.started:
    difficulty = st.selectbox("Select Difficulty Level:", ['Easy', 'Medium', 'Hard'])
    if st.button("Start Game"):
        st.session_state.started = True
        st.session_state.timer = 30
        st.session_state.score = 0
        st.session_state.total = 0
        st.session_state.correct = 0
        st.session_state.difficulty = difficulty
        st.session_state.question, st.session_state.answer = generate_question(difficulty)
        st.rerun()
else:
    st.sidebar.markdown(f"**Time Left:** {st.session_state.timer} seconds")
    st.sidebar.markdown(f"**Score:** {st.session_state.score}")
    st.sidebar.markdown(f"**Correct:** {st.session_state.correct} / {st.session_state.total}")

    st.subheader(f"Question:")
    st.markdown(f"### `{st.session_state.question}`")
    answer_input = st.text_input("Your Answer:", key='user_input')

    if st.button("Submit"):
        st.session_state.total += 1
        try:
            if float(answer_input.strip()) == st.session_state.answer:
                st.success("Correct!")
                st.session_state.score += 1
                st.session_state.correct += 1
            else:
                st.error(f"Wrong! Correct answer was {st.session_state.answer}")
        except:
            st.error("Please enter a valid number.")

        st.session_state.question, st.session_state.answer = generate_question(st.session_state.difficulty)
        st.rerun()

# End of game summary
if not st.session_state.started and st.session_state.total > 0:
    st.subheader("⏱️ Time's up!")
    st.write(f"**Final Score:** {st.session_state.score}")
    st.write(f"**Correct Answers:** {st.session_state.correct} out of {st.session_state.total}")
    st.button("Play Again", on_click=lambda: st.session_state.clear())
