import streamlit as st

from services.excel_loader import (
    get_personas,
    get_reports,
    get_frameworks,
    get_additional_frameworks,
    get_all_frameworks
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

        recommended_frameworks = get_frameworks(
            persona,
            report
        )

        additional_frameworks = get_additional_frameworks(
            persona,
            report
        )

        all_frameworks = get_all_frameworks()

        state_key = f"{persona}_{report}_frameworks"

        if state_key not in st.session_state:
            st.session_state[state_key] = [
                f["id"] for f in recommended_frameworks
            ]

        col1, col2, col3 = st.columns([1.6, 1, 1])

        with col1:

            if st.button(
                "Select Recommended",
                use_container_width=True
            ):
                st.session_state[state_key] = [
                    framework["id"]
                    for framework in recommended_frameworks
                ]

                for framework in all_frameworks:
                    st.session_state[
                        f"framework_{framework['id']}"
                    ] = framework["id"] in st.session_state[state_key]

                st.rerun()

        with col2:
            if st.button(
                "Select All",
                use_container_width=True
            ):
                st.session_state[state_key] = [
                    framework["id"] 
                    for framework in all_frameworks
                ]

                for framework in all_frameworks:
                    st.session_state[
                        f"framework_{framework['id']}"
                    ] = True

                st.rerun()

        with col3:
            if st.button(
                "Clear All",
                use_container_width=True
            ):
                st.session_state[state_key] = []

                for framework in all_frameworks:
                    st.session_state[
                        f"framework_{framework['id']}"
                    ] = False

                st.rerun()
        
        with st.expander(
            f"Recommended Frameworks ({len(recommended_frameworks)})",
            expanded=True
        ):

            for framework in recommended_frameworks:

                checkbox_key = f"framework_{framework['id']}"

                if checkbox_key not in st.session_state:
                    st.session_state[checkbox_key] = (
                        framework["id"] in st.session_state[state_key]
                    )

                st.checkbox(
                    framework["name"],
                    key=checkbox_key
                )

        with st.expander(
            f"Additional Frameworks ({len(additional_frameworks)})",
            expanded=False
        ):

            for framework in additional_frameworks:

                checkbox_key = f"framework_{framework['id']}"

                if checkbox_key not in st.session_state:

                    st.session_state[checkbox_key] = (
                        framework["id"] in st.session_state[state_key]
                    )

                st.checkbox(
                    framework["name"],
                    key=checkbox_key
                )

        selected_frameworks = [
            framework["id"]
            for framework in all_frameworks
            if st.session_state.get(f"framework_{framework['id']}", False)
        ]

        st.session_state[state_key] = selected_frameworks

        st.caption(
            f"Selected Frameworks: {len(selected_frameworks)} / {len(all_frameworks)}"
        )

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