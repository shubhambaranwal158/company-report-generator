import streamlit as st

from components.sidebar import render_sidebar

from services.excel_loader import (
    get_frameworks_for_report
)

from services.prompt_builder import (
    build_report_prompt
)

from services.gemini_service import (
    generate_framework
)

st.set_page_config(
    page_title="AI Company Intelligence",
    page_icon="📊",
    layout="wide"
)

company, persona, report, generate = render_sidebar()

st.title("📊 AI Company Intelligence Platform")

st.write(
    "Generate AI-powered executive company reports using consulting frameworks."
)

st.divider()

if generate:

    framework_ids = get_frameworks_for_report(
        persona,
        report
    )

    # Build the master prompt
    master_prompt = build_report_prompt(
        company,
        framework_ids
    )

    # Generate report (spinner disappears automatically when complete)
    with st.spinner(
        f"Generating report with {len(framework_ids)} frameworks..."
    ):
        response = generate_framework(master_prompt)

    st.success("✅ Executive Report generated successfully")

    from services.html_renderer import render_report
    from services.report_exporter import save_html

    complete_html = render_report(response)

    st.markdown(
        complete_html,
        unsafe_allow_html=True
    )

    save_html(
        f"{company}.html",
        complete_html
    )
    
    st.download_button(

        label="📄 Download HTML Report",

        data=complete_html,

        file_name=f"{company}_Executive_Report.html",

        mime="text/html"

    )