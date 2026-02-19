import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from Core.prediction_helper import predict

# -------------------------------------------------
# Page config and theming
# -------------------------------------------------
st.set_page_config(
    page_title="CredVibe Credit Rating and Risk Assessment tool",
    page_icon="🏦",
    layout="centered",
)

# Custom CSS for modern look
custom_css = """
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #111827 100%);
        color: #e5e7eb;
    }

    .title-text {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 0.2rem !important;
        padding-top: 0.5rem;
        color: #f9fafb !important;
    }

    .subtitle-text {
        text-align: center;
        color: #9ca3af;
        font-size: 0.95rem;
        margin-bottom: 1.8rem;
    }

    .section-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #e5e7eb;
        margin: 1rem 0 0.4rem 0;
    }

    .result-card {
        background: radial-gradient(circle at top left, #1f2937 0%, #020617 60%);
        border-radius: 18px;
        padding: 1.8rem 1.5rem;
        box-shadow: 0 18px 35px rgba(0, 0, 0, 0.6);
        margin-top: 1.5rem;
        border: 1px solid rgba(148, 163, 184, 0.4);
    }

    .metric-box {
        background: linear-gradient(145deg, rgba(15,23,42,0.9), rgba(30,64,175,0.7));
        border-radius: 14px;
        padding: 0.9rem 0.8rem;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.4);
    }

    .metric-label {
        color: #cbd5f5;
        font-size: 0.8rem;
        margin-bottom: 0.15rem;
    }

    .metric-value {
        color: #e5e7eb;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0.1rem 0 0.4rem 0;
    }

    .rating-badge {
        display: inline-block;
        padding: 0.4rem 1.3rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 1.05rem;
        color: #020617;
        background: linear-gradient(135deg, #22c55e, #a3e635);
        border: 1px solid rgba(22, 163, 74, 0.7);
    }

    .rating-badge-medium {
        background: linear-gradient(135deg, #facc15, #f97316);
        border-color: rgba(234, 179, 8, 0.7);
        color: #111827;
    }

    .rating-badge-high {
        background: linear-gradient(135deg, #f97373, #ef4444);
        border-color: rgba(248, 113, 113, 0.8);
        color: #111827;
    }

    .stButton>button {
        background: linear-gradient(135deg, #10b981, #22c55e);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.7rem 2.2rem;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 8px 18px rgba(34, 197, 94, 0.4);
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 26px rgba(34, 197, 94, 0.5);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown('<h1 class="title-text">🏦 CredVibe</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle-text">Credit Rating and Risk Assessment tool – estimate default probability, score, and rating in seconds</p>',
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Inputs
# -------------------------------------------------
st.markdown('<p class="section-header">👤 Applicant & Loan Details</p>', unsafe_allow_html=True)

row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

# Row 1
with row1[0]:
    age = st.number_input(
        "🎂 Age",
        min_value=18,
        max_value=100,
        value=35,
        step=1,
        help="Enter your age (18–100)",
    )
with row1[1]:
    income = st.number_input(
        "💰 Annual Income (₹)",
        min_value=100_000,
        max_value=100_000_000,
        value=1_200_000,
        step=50_000,
        help="Enter your annual income (₹100,000 – ₹100,000,000)",
    )
with row1[2]:
    loan_amount = st.number_input(
        "🏦 Loan Amount (₹)",
        min_value=0,
        max_value=10_000_000,
        value=500_000,
        step=50_000,
        help="Desired loan amount (₹0 – ₹10,000,000)",
    )

# Row 2
with row2[0]:
    LTI = loan_amount / income if income > 0 else 0
    st.number_input(
        "📊 LTI (Loan-to-Income)",
        value=round(LTI, 4),
        disabled=True,
        help="Loan amount divided by annual income (auto-calculated)",
    )

with row2[1]:
    loan_tenure_months = st.number_input(
        "📅 Loan Tenure (months)",
        min_value=1,
        max_value=36,
        value=12,
        step=1,
        help="Loan tenure in months",
    )

with row2[2]:
    avg_dpd_per_delinquency = st.number_input(
        "⏰ Avg DPD per Delinquency",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        help="Average days past due for delinquent months",
    )

# Row 3
with row3[0]:
    delinquency_ratio_in_pc = st.number_input(
        "⚠️ Delinquency Ratio (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        help="Delinquent loans as % of total loans",
    )
with row3[1]:
    credit_utilization_ratio = st.number_input(
        "💳 Credit Utilization (%)",
        min_value=0,
        max_value=100,
        value=30,
        step=1,
        help="Used credit as % of total sanctioned credit",
    )
with row3[2]:
    number_of_open_accounts = st.number_input(
        "📂 Open Accounts",
        min_value=1,
        max_value=4,
        value=2,
        step=1,
        help="Number of active loan/credit accounts",
    )

# Row 4
with row4[0]:
    residence_type = st.selectbox(
        "🏠 Residence Type",
        ["Owned", "Rented", "Mortgage"],
    )
with row4[1]:
    loan_purpose = st.selectbox(
        "🎯 Loan Purpose",
        ["Education", "Home", "Auto", "Personal"],
    )
with row4[2]:
    loan_type = st.selectbox(
        "🔒 Loan Type",
        ["Unsecured", "Secured"],
    )

st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    run_model = st.button("📊 Run Credit Risk Assessment")

# -------------------------------------------------
# Results
# -------------------------------------------------
if run_model:
    input_dict = {
        "age": age,
        "income": income,
        "loan_amount": loan_amount,
        "loan_tenure_months": loan_tenure_months,
        "avg_dpd_per_delinquency": avg_dpd_per_delinquency,
        "delinquency_ratio_in_pc": delinquency_ratio_in_pc,
        "credit_utilization_ratio": credit_utilization_ratio,
        "number_of_open_accounts": number_of_open_accounts,
        "residence_type": residence_type,
        "loan_purpose": loan_purpose,
        "loan_type": loan_type,
    }

    with st.spinner("🔍 Evaluating credit profile and computing risk metrics..."):
        probability, credit_score, rating = predict(input_dict)

    # Convert to appropriate types in case predict returns strings
    probability = float(probability)
    credit_score = int(credit_score)

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(
        "<h3 style='color:#e5e7eb; margin-top:0;'>📋 Credit Assessment Summary</h3>",
        unsafe_allow_html=True,
    )

    # Decide badge style from rating / probability
    rating_lower = str(rating).lower()
    badge_class = "rating-badge"
    if "high" in rating_lower or probability > 0.5:
        badge_class += " rating-badge-high"
    elif "moderate" in rating_lower or 0.25 < probability <= 0.5:
        badge_class += " rating-badge-medium"

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(
            "<div class='metric-label'>⚡ Default Probability</div>",
            unsafe_allow_html=True,
        )
        prob_color = "#22c55e" if probability < 0.25 else "#facc15" if probability < 0.5 else "#f97373"
        st.markdown(
            f"<div class='metric-value' style='color:{prob_color};'>{probability:.1%}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with m2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(
            "<div class='metric-label'>📈 Credit Score</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='metric-value'>{credit_score}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with m3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(
            "<div class='metric-label'>🏆 Rating</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<span class='{badge_class}'>{rating}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📚 How to interpret these results"):
        st.markdown(
            """
- **Default probability**: Lower values indicate lower chance of missed payments.
- **Credit score**: Higher scores reflect stronger repayment history and affordability.
- **Rating**: Overall risk bucket combining probability, score, and behavioral indicators.
            """
        )
