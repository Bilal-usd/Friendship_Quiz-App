import json
import os
import random
import string
import requests
import streamlit as st
from streamlit_lottie import st_lottie

DB_FILE = "quizzes.json"


def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


# Fetching cool animation links
lottie_quiz = load_lottieurl(
    "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
)
lottie_success = load_lottieurl(
    "https://assets2.lottiefiles.com/packages/lf20_u4yeeo3k.json"
)
lottie_friends = load_lottieurl(
    "https://assets8.lottiefiles.com/private_files/lf30_vpyup3.json"
)  # Professional hand-holding animation


def load_quizzes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}


def save_quizzes(quizzes):
    with open(DB_FILE, "w") as f:
        json.dump(quizzes, f, indent=4)


def generate_quiz_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=5))


# Page Configuration
st.set_page_config(
    page_title="Friendship Quiz Hub | Portfolio", page_icon="⚡", layout="centered"
)

# Professional UI & Modern CSS Styling (Professional Theme)
st.markdown(
    """
    <style>
    /* Main Background & Font */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Card Container Styling */
    .quiz-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }

    /* Headers styling */
    h1, h2, h3 {
        color: #1e293b;
        font-weight: 700;
        text-align: center;
    }

    /* Buttons Styling (Professional Indigo) */
    .stButton>button {
        width: 100%;
        background-color: #4f46e5;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }

    /* Clean Tabs Styling (No Solid Blue Box) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #64748b !important;
        font-weight: 700 !important;
        padding: 12px 16px !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #4f46e5 !important;
        border-bottom: 3px solid #4f46e5 !important;
        border-radius: 0px !important;
    }
    
    /* Professional Header Text (Similar to provided image) */
    .main-title {
        color: #1e293b;
        font-weight: 800;
        font-size: 32px;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #4f46e5;
        font-weight: 700;
        font-size: 18px;
        text-align: center;
        margin-top: -10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# App Header Section with the Handshake Animation from Image
st.markdown("<br>", unsafe_allow_html=True)
if lottie_friends:
    st_lottie(lottie_friends, height=180, key="friends_anim")

st.markdown("<h1 class='main-title'>⚡ FRIENDSHIP HUB</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-title'>TEST YOUR BOND</h3>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Tabs (Professional Style)
tab1, tab2 = st.tabs(["📝 CREATE A QUIZ", "🎮 PLAY A QUIZ"])

# ---------------------------------------------------------
# TAB 1: CREATE A QUIZ
# ---------------------------------------------------------
with tab1:
    st.markdown(
        """<div class="quiz-card">""", unsafe_allow_html=True
    )
    st.header("Build Your Custom Quiz")
    creator_name = st.text_input(
        "Your Name:", placeholder="e.g., Aqsa", key="creator_name"
    )

    num_questions = st.number_input(
        "How many questions? (Max 10):",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
    )

    num_opts = st.radio(
        "Options per question:",
        [2, 3],
        horizontal=True,
        key="global_num_opts",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    questions_data = []

    for i in range(int(num_questions)):
        st.markdown(
            f"""<div class="quiz-card">""", unsafe_allow_html=True
        )
        st.subheader(f"Question {i+1}")
        q_text = st.text_input(
            f"Enter Question {i+1}:",
            placeholder="e.g., What is my dream career?",
            key=f"q_{i}",
        )

        if num_opts == 2:
            opt1 = st.text_input(f"Option A:", key=f"opt1_{i}")
            opt2 = st.text_input(f"Option B:", key=f"opt2_{i}")
            options_list = [opt1, opt2]
        else:
            opt1 = st.text_input(f"Option A:", key=f"opt1_{i}")
            opt2 = st.text_input(f"Option B:", key=f"opt2_{i}")
            opt3 = st.text_input(f"Option C:", key=f"opt3_{i}")
            options_list = [opt1, opt2, opt3]

        correct_opt = st.selectbox(
            f"Select Correct Answer for Q{i+1}:", options_list, key=f"ans_{i}"
        )

        questions_data.append({
            "question": q_text,
            "options": options_list,
            "correct_answer": correct_opt,
        })
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 GENERATE QUIZ CODE"):
        if not creator_name.strip():
            st.error("⚠️ Please enter your name!")
        else:
            valid = True
            for q in questions_data:
                if not q["question"] or any(not opt for opt in q["options"]):
                    valid = False
                    break

            if not valid:
                st.warning("⚠️ Please fill in all questions and options!")
            else:
                quiz_code = generate_quiz_code()
                quizzes = load_quizzes()
                quizzes[quiz_code] = {
                    "creator": creator_name,
                    "questions": questions_data,
                }
                save_quizzes(quizzes)

                st.markdown(
                    f"""<div class="quiz-card" style="background-color: #eff6ff; border-color: #bfdbfe;">
            <h3 style="color: #1e40af;">🎉 Quiz Created Successfully!</h3>
            <p>Your Unique Quiz Code: <b style="font-size: 20px; color: #1d4ed8;">{quiz_code}</b></p>
            <p style="color: #1e40af; margin-bottom: 0;">Share this code with your friends so they can play your quiz on LinkedIn or WhatsApp! 🎈</p>
        </div>""",
                    unsafe_allow_html=True,
                )

# ---------------------------------------------------------
# TAB 2: PLAY A QUIZ
# ---------------------------------------------------------
with tab2:
    st.markdown(
        """<div class="quiz-card">""", unsafe_allow_html=True
    )
    st.header("Play a Friend's Quiz")

    player_name = st.text_input(
        "Your Name:", placeholder="e.g., Ali", key="player_name"
    )
    input_code = st.text_input(
        "Enter Quiz Code:", placeholder="e.g., A1B2C", key="input_code"
    ).upper()
    st.markdown("</div>", unsafe_allow_html=True)

    if input_code:
        quizzes = load_quizzes()

        if input_code in quizzes:
            quiz_info = quizzes[input_code]
            st.info(f"✨ Playing Quiz created by **{quiz_info['creator']}**!")

            user_answers = {}
            total_q = len(quiz_info["questions"])

            for idx, q in enumerate(quiz_info["questions"]):
                st.markdown(
                    f"""<div class="quiz-card">""", unsafe_allow_html=True
                )
                st.markdown(f"**Q{idx+1}: {q['question']}**")
                user_choice = st.radio(
                    "Select answer:",
                    q["options"],
                    key=f"play_q_{input_code}_{idx}",
                    label_visibility="collapsed",
                )
                user_answers[idx] = user_choice
                st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🏆 SUBMIT ANSWERS"):
                score = 0
                st.balloons()

                if lottie_success:
                    st_lottie(lottie_success, height=130, key="success_anim")

                for idx, q in enumerate(quiz_info["questions"]):
                    if user_answers.get(idx) == q["correct_answer"]:
                        score += 1

                percentage = (score / total_q) * 100

                # Result Summary Card
                st.markdown(
                    f"""<div class="quiz-card" style="background-color: #eff6ff; border-color: #bfdbfe;">
            <h3 style="color: #1e40af;">🎉 {player_name if player_name else 'Player'}, Your Scorecard</h3>
            <p style="font-size: 18px; font-weight: bold; color: #1d4ed8;">Final Score: {score} / {total_q} ({percentage:.0f}%)</p>
        </div>""",
                    unsafe_allow_html=True,
                )

                if percentage == 100:
                    st.success("🌟 Outstanding! You know them inside out! 🥇")
                elif percentage >= 50:
                    st.info("👍 Not bad! You guys share a good bond. 😉")
                else:
                    st.warning("😅 Looks like you need to catch up more often! ☕")

                # --- Detailed Review Section inside Professional Cards (Color-coded) ---
                st.markdown("---")
                st.subheader("📋 Detailed Answer Review:")
                for idx, q in enumerate(quiz_info["questions"]):
                    user_ans = user_answers.get(idx)
                    correct_ans = q["correct_answer"]

                    st.markdown(
                        f"""<div class="quiz-card">""", unsafe_allow_html=True
                    )
                    st.markdown(f"**Q{idx+1}: {q['question']}**")

                    for opt in q["options"]:
                        if opt == correct_ans:
                            st.markdown(
                                f"<p style='color: #166534; margin-left: 15px; font-weight:"
                                f" 600;'>✅ {opt} (Correct Answer)</p>",
                                unsafe_allow_html=True,
                            )
                        elif opt == user_ans and user_ans != correct_ans:
                            st.markdown(
                                f"<p style='color: #991b1b; margin-left: 15px; font-weight:"
                                f" 600;'>❌ {opt} (Your Answer)</p>",
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f"<p style='color: #475569; margin-left: 15px;'>• {opt}</p>",
                                unsafe_allow_html=True,
                            )
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ Invalid Quiz Code! Please enter a valid code.")