import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Company Report Generator",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("📊 AI Company Report Generator")
st.write("Generate professional company reports using AI.")

st.divider()

# -----------------------------
# Input Section
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    company = st.text_input(
        "Company Name",
        placeholder="Example: PalTech"
    )

with col2:
    persona = st.selectbox(
        "Select Persona",
        [
            "Leadership",
            "Sales",
            "Marketing",
            "HR",
            "Leads/Manager"
        ]
    )

report_type = st.radio(
    "Report Type",
    [
        "Executive Summary",
        "Detailed Report"
    ],
    horizontal=True
)

st.divider()

# -----------------------------
# Generate Button
# -----------------------------

if st.button(
    "🚀 Generate Report",
    use_container_width=True
):

    if company == "":
        st.warning("Please enter a company name.")
    else:

        st.success("Inputs captured successfully!")

        st.write("### Selected Inputs")

        st.write(f"**Company:** {company}")
        st.write(f"**Persona:** {persona}")
        st.write(f"**Report Type:** {report_type}")

        st.info("Gemini integration coming next...")