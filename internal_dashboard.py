import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="E-Business Dashboard", page_icon="🛠️")
st.title("🛠️ Internal Complaints Dashboard")

if os.path.exists("complaints_log.csv"):
    df = pd.read_csv("complaints_log.csv")
    st.subheader(f"📂 {len(df)} Complaints Logged")
    
    filter_type = st.selectbox("Filter by Complaint Type", ["All"] + df["Complaint Type"].unique().tolist())
    if filter_type != "All":
        df = df[df["Complaint Type"] == filter_type]

    st.dataframe(df)

    st.download_button("⬇️ Download All Complaints", data=df.to_csv(index=False), file_name="complaints_log.csv", mime="text/csv")
else:
    st.warning("No complaints submitted yet.")
