import streamlit as st

from c2c_engine import analyze_problem
from c2c_ml import predict_category

def get_urgency_color(urgency):
    urgency = str(urgency).strip().lower()

    if urgency == "low":
        return "#34D399"
    elif urgency == "medium":
        return "#FBBF24"
    elif urgency == "high":
        return "#FB923C"
    elif urgency == "very high":
        return "#F87171"
    else:
        return "#60A5FA"

st.set_page_config(
    page_title="Crisis2Clarity AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM DARK THEME ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080e1c 0%, #0c1426 55%, #101b31 100%);
    color: #edf4ff;
}

.block-container {
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f3f7ff !important;
    letter-spacing: -0.5px;
}

p, label, li {
    color: #c2cde0;
}

.hero {
    padding: 30px;
    border: 1px solid #243755;
    border-radius: 22px;
    background: linear-gradient(120deg, #121f38, #10182b);
    margin-bottom: 25px;
}

.eyebrow {
    color: #60a5fa;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 800;
    margin: 10px 0;
    color: #ffffff;
}

.hero-subtitle {
    color: #aebdd3;
    font-size: 1.05rem;
    line-height: 1.7;
}

.panel {
    background: #111c30;
    border: 1px solid #263853;
    border-radius: 16px;
    padding: 22px;
    margin: 12px 0;
}

.metric-card {
    background: linear-gradient(145deg, #142440, #101a2c);
    border: 1px solid #2b4164;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
}

.metric-label {
    color: #9fb2ce;
    font-size: 0.85rem;
    margin-bottom: 10px;
}

.metric-value {
    color: #70b7ff;
    font-size: 1.4rem;
    font-weight: 750;
    overflow-wrap: anywhere;
}


div[data-testid="stTextArea"] textarea {
    background-color: #0b1424 !important;
    color: #f0f6ff !important;
    border: 1px solid #344968 !important;
    border-radius: 12px !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 1px #3b82f6 !important;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white;
    border: 0;
    border-radius: 11px;
    padding: 0.7rem 1.2rem;
    font-weight: 700;
    min-height: 48px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #2563eb);
    border: 1px solid #60a5fa;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #263853;
}

.footer {
    text-align: center;
    color: #7386a3;
    font-size: 0.82rem;
    padding-top: 30px;
}
/* Dashboard polish */
.metric-card {
    background: linear-gradient(145deg, #172b49, #101c30);
    border: 1px solid #355781;
    border-radius: 18px;
    padding: 22px;
    min-height: 135px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    border-color: #60a5fa;
}

.metric-label {
    color: #b5c9e5;
    font-size: 0.85rem;
    margin-bottom: 12px;
}

.metric-value {
    color: #72b7ff;
    font-size: 1.5rem;
    font-weight: 800;
    overflow-wrap: anywhere;
}

.step-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: linear-gradient(110deg, #142642, #101c30);
    border: 1px solid #30496c;
    border-radius: 14px;
    padding: 17px;
    margin: 10px 0;
    color: #e6efff;
    line-height: 1.7;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

.step-item:hover {
    border-color: #60a5fa;
    transform: translateY(-2px);
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #2a4161;
    border-radius: 16px;

    /* Mobile-friendly layout */
@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 18px;
        border-radius: 16px;
    }

    .hero-title {
        font-size: 2rem;
    }

    .metric-card {
        padding: 14px;
        min-height: 110px;
        border-radius: 14px;
    }

    .metric-value {
        font-size: 1.15rem;
    }

    .step-item {
        padding: 13px;
        gap: 8px;
    }

    .stButton > button {
        width: 100%;
    }
}
}
</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
col1, col2 = st.columns([1, 5])

with col1:
    st.image("c2c_logo2.jpg", width=130)

with col2:
    st.markdown(
        """
        <div style="padding:10px 0; color:white;">
            <h1 style="margin:0;">Crisis2Clarity AI</h1>
            <p>From confusion to clear action.</p>
            <p>Understand the challenge. Find your next step. Move forward.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- INPUT PANEL ----------
st.markdown("## Tell us what's going on")
st.markdown(
    "Describe your study problem, assignment, or upcoming deadline. "
    "Your AI copilot will help organize your next steps."
)

with st.container(border=True):
    problem = st.text_area(
        "Describe your problem",
        placeholder=(
            "Example: I have a C++ assignment due tomorrow, "
            "and I don't understand pointers..."
        ),
        height=140,
        key="problem_input"
    )

    analyze_clicked = st.button(
        "✨  Analyze My Problem",
        type="primary",
        use_container_width=True
    )

# ---------- ANALYSIS ----------
if analyze_clicked:
    if problem.strip():
        with st.spinner("Analyzing your situation..."):
            result = analyze_problem(problem)
            ml_category = predict_category(problem)

        st.markdown("---")
        st.markdown("## Your clarity dashboard")
        st.caption("Analysis complete • Review your results and next steps")

        # Summary metric cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">ML prediction</div>
                <div class="metric-value">{ml_category.title()}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Detected problem</div>
                <div class="metric-value">
                {" + ".join(result.get("detected_intents", [result["intent"]]))}
            </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Priority score</div>
                <div class="metric-value">{result["priority"]}/10</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🔎 Understanding your problem")
        with st.container(border=True):
            st.markdown("**Your problem**")
            st.write(result["problem"])

            st.markdown("**Learning gap**")
            st.write(result["learning_gap"])

            st.info(result["next_step"])

       # Priority and urgency
        urgency = str(result["urgency"])
        urgency_color = get_urgency_color(urgency)

        st.markdown(
            f"""
            <div style="
                background: #111c30;
                border: 1px solid {urgency_color};
                border-left: 6px solid {urgency_color};
                border-radius: 12px;
                padding: 18px 20px;
                margin: 15px 0;
            ">
                <div style="color: #b5c9e5; font-size: 0.9rem;">
                    CURRENT URGENCY LEVEL
                </div>
                <div style="
                    color: {urgency_color};
                    font-size: 1.5rem;
                    font-weight: 800;
                    margin-top: 5px;
                ">
                    ⚡ {urgency.title()}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Two-column action area
        left, right = st.columns(2)

        with left:
            st.markdown("### 🗺️ Your action plan")
            for i, step in enumerate(result["action_plan"], start=1):
                st.markdown(
                    f'<div class="step-item"><strong>{i:02}</strong>'
                    f' &nbsp; {step}</div>',
                    unsafe_allow_html=True
                )

        with right:
            st.markdown("### 💡 Topic-specific guidance")
            for tip in result["topic_guidance"]:
                st.markdown(
                    f'<div class="step-item">• &nbsp; {tip}</div>',
                    unsafe_allow_html=True
                )

        st.success("Your next step is ready. Start with one action at a time.")

    else:
        st.warning("Please describe your problem first.")

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    CRISIS2CLARITY AI · Think clearly. Act confidently.
</div>
""", unsafe_allow_html=True)