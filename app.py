import streamlit as st

st.title("Company Report Generator")

company = st.text_input("Enter Company Name")

if st.button("Generate Report"):
    st.success(f"Generating report for {company}")