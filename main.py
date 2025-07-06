import streamlit as st
from prediction_helper import predict

# Set the page configuration and title
st.set_page_config(page_title="Goobe Finance: Credit Risk Modeling", layout="centered")
st.title("💳 Goobe Finance: Credit Risk Modeling")

# Create a 4x3 grid of input fields
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

# --- Row 1 Inputs ---
with row1[0]:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=85,
        step=1,
        help="Enter your age (18-100)"
    )
with row1[1]:
    income = st.number_input(
        "Income",
        min_value=100_000,
        max_value=100_000_000,
        value=500_000,

        help="Enter your annual income (₹100,000 - ₹100,000,000)"
    )
with row1[2]:
    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0,
        max_value=10_000_000,
        value=100_000,

        help="Enter desired loan amount (₹0 - ₹10,000,000, step=100)"
    )

# --- Row 2 Inputs ---
with row2[0]:
    # LTI is auto-calculated
    if income > 0:
        LTI = loan_amount / income
    else:
        LTI = 0
    st.number_input(
        "LTI",
        value=round(LTI, 4),
        disabled=True,
        help="Loan to Income Ratio"
    )
with row2[1]:
    loan_tenure_months = st.number_input(
        "Loan Tenure (Months)",
        min_value=1,
        max_value=36,
        value=12,
        step=1,
        help="Loan tenure (in months)"
    )
with row2[2]:
    avg_dpd_per_delinquency = st.number_input(
        "Avg DPD per Delinquency",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        help="Average days past the due date for all delinquent months"
    )

# --- Row 3 Inputs ---
with row3[0]:
    delinquency_ratio_in_pc = st.number_input(
        "Delinquency Ratio (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        help="Proportion of number of delinquent loans divided by total number of loans in a portfolio expressed as a percentage"
    )
with row3[1]:
    credit_utilization_ratio = st.number_input(
        "Credit Utilization Ratio (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        help="Proportion of the total sanctioned credit amount currently being utilized expressed as a percentage"
    )
with row3[2]:
    number_of_open_accounts = st.number_input(
        "Number of Open Accounts",
        min_value=1,
        max_value=4,
        value=1,
        step=1,
        help="Number of active loan accounts"
    )

# --- Row 4 Inputs ---
with row4[0]:
    residence_type = st.selectbox(
        "Residence Type",
        ['Owned', 'Rented', 'Mortgage']
    )
with row4[1]:
    loan_purpose = st.selectbox(
        "Loan Purpose",
        ['Education', 'Home', 'Auto', 'Personal']
    )
with row4[2]:
    loan_type = st.selectbox(
        "Loan Type",
        ['Unsecured', 'Secured']
    )

# --- Submit Button and Display ---
if st.button("Calculate risk"):

    input_dict = {"age": age, "income": income, "loan_amount": loan_amount, "loan_tenure_months": loan_tenure_months,
                  "avg_dpd_per_delinquency": avg_dpd_per_delinquency,
                  "delinquency_ratio_in_pc": delinquency_ratio_in_pc, "credit_utilization_ratio": credit_utilization_ratio,
                  "number_of_open_accounts": number_of_open_accounts,
                  "residence_type": residence_type, "loan_purpose": loan_purpose, "loan_type": loan_type}

    probability, credit_score, rating = predict(input_dict)
    # input_df = predict(input_dict)

    st.table({
        "Parameter" : ["Default probability", "Credit score", "Rating"],
        "Value" : [probability, credit_score, rating]
    })

    #st.write(input_df)


    # st.markdown("### Entered Details")
    # st.table({
    #     "Field": [
    #         "Age", "Income", "Loan Amount", "LTI", "Loan Tenure (Months)",
    #         "Avg DPD per Delinquency", "Delinquency Ratio (%)", "Credit Utilization Ratio (%)",
    #         "Number of Open Accounts", "Residence Type", "Loan Purpose", "Loan Type"
    #     ],
    #     "Value": [
    #         age,
    #         f"₹{income:,}",
    #         f"₹{loan_amount:,}",
    #         round(lti, 4),
    #         loan_tenure_months,
    #         avg_dpd_per_delinquency,
    #         delinquency_ratio,
    #         credit_utilization_ratio,
    #         num_open_accounts,
    #         residence_type,
    #         loan_purpose,
    #         loan_type
    #     ]
    # })

