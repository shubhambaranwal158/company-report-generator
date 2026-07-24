import streamlit as st

from services.excel_loader import (
    get_personas,
    get_reports,
    get_frameworks
)


def render_sidebar():

    with st.sidebar:

        st.title("🏢 Company Details")

        st.divider()

        company = st.text_input(
            "Company Name",
            placeholder="Enter company name..."
        )

        company = company.strip()

        company_website = st.text_input(
            "Official Company Website (Optional)",
            placeholder="https://www.company.com"
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

        frameworks = get_frameworks(
            persona,
            report
        )

        state_key = f"{persona}_{report}_frameworks"

        if state_key not in st.session_state:
            st.session_state[state_key] = [
                f["id"] for f in frameworks
            ]

        with st.expander(
            f"Frameworks Included ({len(st.session_state[state_key])}/{len(frameworks)})",
            expanded=True
        ):

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Select All",
                    use_container_width=True
                ):
                    st.session_state[state_key] = [
                        f["id"] for f in frameworks
                    ]

                    for framework in frameworks:
                        st.session_state[
                            f"framework_{framework['id']}"
                        ] = True

                    st.rerun()

            with col2:
                if st.button(
                    "Clear All",
                    use_container_width=True
                ):
                    st.session_state[state_key] = []

                    for framework in frameworks:
                        st.session_state[
                            f"framework_{framework['id']}"
                        ] = False

                    st.rerun()

            selected_frameworks = []

            for framework in frameworks:

                checkbox_key = f"framework_{framework['id']}"

                if checkbox_key not in st.session_state:
                    st.session_state[checkbox_key] = (
                        framework["id"] in st.session_state[state_key]
                    )

                if st.checkbox(
                    framework["name"],
                    key=checkbox_key
                ):
                    selected_frameworks.append(
                        framework["id"]
                    )

            st.session_state[state_key] = selected_frameworks

        st.divider()

        validation_errors = []

        if not company:
            validation_errors.append(
                "Please enter a company name."
            )

        if not selected_frameworks:
            validation_errors.append(
                "Please select at least one framework."
            )

        generate = st.button(
            "🚀 Generate Report",
            use_container_width=True,
            disabled=bool(validation_errors)
        )
        for error in validation_errors:
            st.caption(f"⚠ {error}")

    return (
        company,
        company_website,
        persona,
        report,
        selected_frameworks,
        generate
    )