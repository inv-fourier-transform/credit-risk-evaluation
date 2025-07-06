import joblib
import numpy as np
import pandas as pd
# from sklearn.preprocessing import MinMaxScaler

# ------------------------------------------
# Load Model and Preprocessing Components
# ------------------------------------------

# Path to the saved model and associated components
MODEL_PATH = 'artifacts/model_data2.joblib'

# Load the model and associated data from the file
model_data = joblib.load(MODEL_PATH)

# Extract individual components from the loaded dictionary
model = model_data['model']                # Trained model
scaler = model_data['scaler']              # MinMaxScaler for preprocessing
features = model_data['features']          # List of feature column names expected by the model
cols_to_scale = model_data['cols_to_scale']  # Columns that need to be scaled

# ------------------------------------------
# Prepare Input Function
# ------------------------------------------

def prepare_input(input_data: dict):
    """
    Prepares a user-provided input dictionary for prediction.
    Adds derived fields, encodes categories, applies scaling, and matches model features.

    Parameters:
        input_data (dict): Dictionary of raw input features from the user.

    Returns:
        pd.DataFrame: A single-row DataFrame formatted and scaled for the model.
    """

    # ➤ Derived Feature: loan_to_income
    input_data['LTI'] = (
        input_data['loan_amount'] / input_data['income']
        if input_data['income'] > 0 else 0
    )

    # ➤ Categorical Encoding using .update()
    # Add binary (0/1) fields for each category option
    input_data.update({
        'residence_type_Owned': 1 if input_data['residence_type'] == 'Owned' else 0,
        'residence_type_Rented': 1 if input_data['residence_type'] == 'Rented' else 0,
        'loan_purpose_Education': 1 if input_data['loan_purpose'] == 'Education' else 0,
        'loan_purpose_Home': 1 if input_data['loan_purpose'] == 'Home' else 0,
        'loan_purpose_Personal': 1 if input_data['loan_purpose'] == 'Personal' else 0,
        'loan_type_Unsecured': 1 if input_data['loan_type'] == 'Unsecured' else 0,
    })

    # ➤ Add Dummy Variables using .update()
    # These are required to satisfy the expected feature set by the model
    dummy_fields = {
        'number_of_dependants': 1,
        'years_at_current_address': 1,
        'zipcode': 1,
        'sanction_amount': 1,
        'processing_fee': 1,
        'gst': 1,
        'net_disbursement': 1,
        'principal_outstanding': 1,
        'bank_balance_at_application': 1,
        'number_of_closed_accounts': 1,
        'enquiry_count': 1
    }
    input_data.update(dummy_fields)

    # ➤ Convert the updated dictionary to a DataFrame
    df = pd.DataFrame([input_data])  # One row only

    # ➤ Apply scaling only to selected columns
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # ➤ Ensure only the features the model expects are passed in
    df = df[features]

    return df

# ------------------------------------------
# Prediction Function
# ------------------------------------------

def predict(input_data: dict):
    """
    Generates credit score prediction for the given input data.

    Parameters:
        input_data (dict): User input values in dictionary format.

    Returns:
        tuple: (default_probability, credit_score, rating_label)
    """

    # Step 1: Preprocess input data
    input_df = prepare_input(input_data)

    # Step 2: Compute probability and score
    probability, credit_score, rating = calculate_credit_score(input_df)

    return probability, credit_score, rating
    # return input_df

# ------------------------------------------
# Credit Score Calculation Function
# ------------------------------------------

def calculate_credit_score(input_df, base_score=300.0, scale_length=600.0):
    """
    Calculates credit score and rating based on model output.

    Parameters:
        input_df (pd.DataFrame): Scaled and formatted input for prediction.
        base_score (int): Starting point for credit score scale (default: 300)
        scale_length (int): Range of the score (default: 600 to make 300-900 range)

    Returns:
        tuple: (default_probability, credit_score, rating_label)
    """

    # ➤ Linear model prediction: dot product + intercept
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_

    # ➤ Logistic transformation to get probability (sigmoid function)
    default_probability = 1 / (1 + np.exp(-x))
    print(f"Default probability: {default_probability}")

    # ➤ Non-default probability (1 - default probability)
    non_default_probability = 1 - default_probability

    # ➤ Convert probability to credit score within 300–900 range
    credit_score = base_score + non_default_probability.flatten() * scale_length
    print(f"Credit score: {credit_score}")

    rating = get_rating(credit_score[0])
    print(f"Rating :{rating}")

    return f"{default_probability.flatten()[0]:.6f}", int(credit_score[0]), rating

# ➤ Translate credit score into rating category
def get_rating(score):
    if 300.0 <= score < 500.0:
        return 'Poor'
    elif 500.0 <= score < 650.0:
        return 'Average'
    elif 650.0 <= score < 750.0:
        return 'Good'
    elif 750.0 <= score <= 900.0:
        return 'Excellent'
    else:
        return 'Undefined'