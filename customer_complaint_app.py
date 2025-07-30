import streamlit as st
import datetime
import uuid
import pandas as pd
import os

# Create a unique reference ID
def generate_ref():
    return "REF" + str(uuid.uuid4())[:8].upper()

st.set_page_config(page_title="Customer Complaint Form", page_icon="📨")
st.title("📨 Customer Complaint Form")

st.markdown("Fill this form to report a failed transaction or ATM issue.")

with st.form("complaint_form"):
    name = st.text_input("Full Name", max_chars=50)
    account_number = st.text_input("Account Number")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")

    txn_type = st.selectbox("Transaction Channel", ["ATM", "POS", "Transfer", "Mobile App", "USSD"])
    complaint_type = st.selectbox("Complaint Type", ["Dispense Error", "Failed Transfer", "Double Debit", "Reversal Delay", "Others"])
    txn_date = st.date_input("Transaction Date", datetime.date.today())
    txn_amount = st.number_input("Transaction Amount", min_value=0.0, format="%.2f")
    txn_ref = st.text_input("Transaction Reference (optional)")
    details = st.text_area("Describe the issue")
    file_upload = st.file_uploader("Upload screenshot or proof (optional)", type=["png", "jpg", "pdf", "jpeg"])
    submit = st.form_submit_button("Submit")

if submit:
    ref_id = generate_ref()

    # Save complaint
    new_entry = {
        "Reference ID": ref_id,
        "Full Name": name,
        "Account Number": account_number,
        "Email": email,
        "Phone": phone,
        "Transaction Type": txn_type,
        "Complaint Type": complaint_type,
        "Transaction Date": txn_date.strftime("%Y-%m-%d"),
        "Transaction Amount": txn_amount,
        "Transaction Reference": txn_ref,
        "Details": details,
        "Date Submitted": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if not os.path.exists("complaints_log.csv"):
        df = pd.DataFrame(columns=list(new_entry.keys()))
    else:
        df = pd.read_csv("complaints_log.csv")

    df = df.append(new_entry, ignore_index=True)
    df.to_csv("complaints_log.csv", index=False)

    st.success(f"✅ Complaint submitted successfully.\nYour Reference ID is **{ref_id}**. Please keep it for tracking.")
