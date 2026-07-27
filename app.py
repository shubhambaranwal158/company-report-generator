import re

import streamlit as st
import streamlit.components.v1 as components

from components.sidebar import render_sidebar

from services.prompt_builder import build_report_prompt
from services.gemini_service import generate_framework
from services.html_renderer import render_report
from services.report_exporter import save_html
# from services.pdf_exporter import save_pdf


st.set_page_config(
    page_title="AI Company Intelligence",
    page_icon="📊",
    layout="wide"
)


# -----------------------------
# Sidebar
# -----------------------------
company, company_website, persona, report, framework_ids, generate = render_sidebar()

current_inputs = (
    company,
    company_website,
    persona,
    report,
    tuple(sorted(framework_ids))
)


# -----------------------------
# Session State
# -----------------------------
if "generated_report" not in st.session_state:
    st.session_state.generated_report = None
    st.session_state.generated_filename = None
    #st.session_state.generated_pdf = None
    st.session_state.last_generated_inputs = None


# -----------------------------
# Page Header
# -----------------------------
st.title("📊 AI Company Overview Platform")

st.write(
    "Generate AI-powered executive company reports using consulting frameworks."
)

st.divider()


# -----------------------------
# Safe filenames
# -----------------------------
safe_company = re.sub(
    r"[^A-Za-z0-9]+",
    "_",
    company
).strip("_")

safe_report = re.sub(
    r"[^A-Za-z0-9]+",
    "_",
    report
).strip("_")

filename = f"{safe_company}_{safe_report}.html"


# -----------------------------
# Generate Report
# -----------------------------
if generate:

    master_prompt = build_report_prompt(
        company,
        company_website,
        report,
        framework_ids
    )

    with st.spinner(
        f"Generating report with {len(framework_ids)} frameworks..."
    ):

        try:
            response = generate_framework(master_prompt)

        except Exception as e:

            st.error(
                "❌ Failed to generate the report."
            )

            st.info(
                "Please verify your internet connection, Gemini API configuration, or try again later."
            )

            st.exception(e)

            st.stop()
        if not response or not response.strip():

            st.error(
                "❌ The AI returned an empty response."
            )

            st.info(
                "Please try generating the report again."
            )

            st.stop()

    st.success(
        "✅ Executive Report generated successfully"
    )

    complete_html = render_report(
        response,
        company,
        report
    )

    save_html(
       filename,
      complete_html
    )

    #pdf_path = save_pdf(
    #    filename,
    #    complete_html
    #)

    st.session_state.generated_report = complete_html
    st.session_state.generated_filename = filename
    #st.session_state.generated_pdf = pdf_path
    st.session_state.last_generated_inputs = current_inputs

# -----------------------------
# Input Change Warning
# -----------------------------
if (
    st.session_state.generated_report
    and
    current_inputs != st.session_state.last_generated_inputs
):

    st.warning(
        "⚠️ Report parameters have changed. "
        "The displayed report reflects the previous selections. "
        "Click **Generate Report** to refresh."
    )


# -----------------------------
# Display Report
# -----------------------------
if st.session_state.generated_report:

    components.html(
        st.session_state.generated_report,
        height=1500,
        scrolling=True
    )
    st.download_button(
        label="📄 Download HTML Report",
        data=st.session_state.generated_report,
        file_name=st.session_state.generated_filename,
        mime="text/html",
        use_container_width=True
    )

    #with col2:
    #    if st.session_state.generated_pdf:
    #        with open(
    #            st.session_state.generated_pdf,
    #            "rb"
    #        ) as pdf_file:
    #            st.download_button(
    #                label="📑 Download PDF Report",
    #                data=pdf_file,
    #                file_name=st.session_state.generated_pdf.name,
    #                mime="application/pdf",
    #                use_container_width=True
    #            )