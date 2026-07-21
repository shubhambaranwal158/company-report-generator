import streamlit as st

from services.excel_loader import (
    get_personas,
    get_reports,
    get_framework_names
)


def render_sidebar():

    with st.sidebar:

        st.title("🏢 Company Intelligence")

        st.divider()

        company = st.text_input(
            "Company Name",
            placeholder="Microsoft"
        )

        personas = get_personas()

        persona = st.selectbox(
            "Select Persona",
            personas
        )

        reports = get_reports(persona)

        report = st.selectbox(
            "Select Report",
            reports
        )

        frameworks = get_framework_names(
            persona,
            report
        )

        st.divider()

        generate = st.button(
            "🚀 Generate Report",
            use_container_width=True
        )

        if generate:

            st.divider()

            st.subheader("Frameworks Selected")

            for framework in frameworks:
                st.write(f"✅ {framework}")

    return company, persona, report, generate