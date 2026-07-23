from services.excel_loader import get_framework_details


def build_prompt(company: str, framework_id: str) -> str:
    """
    Builds a prompt for a single framework.
    Useful for testing individual frameworks.
    """

    framework = get_framework_details(framework_id)

    if framework is None:
        return ""

    return framework["Prompt"].replace(
        "{Company_Name}",
        company
    )


def build_report_prompt(company: str, company_website: str, report_name: str, framework_ids: list[str]) -> str:
    """
    Builds one optimized master prompt for the complete report.
    """

    prompt_sections = []

    # ------------------------------------------------------------------
    # MASTER REPORT INSTRUCTIONS (Version 2.0)
    # ------------------------------------------------------------------

    prompt_sections.append(f"""
    You are a Senior Strategy Consultant with expertise in Corporate Strategy, Digital Transformation, Market Intelligence, 
    Competitive Intelligence, Financial Analysis, Technology Strategy and Executive Advisory.

    Write as if preparing a board-ready deliverable for executives, investors, strategy leaders and CXOs.

    Your reports should resemble the quality, structure and strategic thinking of McKinsey, Bain, BCG, Gartner, Deloitte, 
    EY or Accenture Strategy.

    ==================================================
    COMPANY
    ==================================================

    Company Name:
    {company}

    Official Company Website:
    {company_website if company_website else "Not Provided"}

    ==================================================
    COMPANY IDENTIFICATION
    ==================================================

    Before performing any analysis, correctly identify the intended company.

    If an Official Company Website is provided:

    • Treat it as the authoritative identifier of the intended company.
    • Use it ONLY to confirm the company's identity.
    • Do NOT limit your research to this website.
    • Use the website to verify the company's name, headquarters, industry, products/services, and key executives.
    • Ensure all facts, metrics, competitors, strategic insights and recommendations correspond to this exact company.
    • Never confuse the company with another organization having a similar or identical name.

    After confirming the company's identity, gather information from multiple credible public sources including, but not limited to:

    • Official Company Website
    • Annual Reports
    • Investor Presentations
    • Regulatory Filings
    • Earnings Call Transcripts
    • Industry Reports
    • Reputable Business News
    • Analyst Research

    If no Official Company Website is provided:

    • Identify the intended company using the company name and other credible public information.
    • If multiple companies have similar names and the intended company cannot be determined with reasonable confidence, explicitly state your assumption before proceeding.

    Do not generate the report until the company identity has been verified.

    ==================================================
    OBJECTIVE
    ==================================================

    Generate ONE cohesive Executive Company Intelligence Report by synthesizing all requested business frameworks into 
    a single consulting narrative.

    The report must read like one integrated strategy document—not multiple independent framework analyses.

    Every section should build upon previous findings and maintain a consistent storyline.

    ==================================================
    CONSULTING WRITING PRINCIPLES
    ==================================================

    Always:

    • Prioritize strategic insights over descriptions.
    • Explain WHY every finding matters.
    • Focus on business implications instead of definitions.
    • Connect observations to business outcomes.
    • Highlight competitive positioning.
    • Identify strategic risks.
    • Identify strategic opportunities.
    • Quantify observations wherever credible public information exists.
    • Clearly distinguish Facts, Analysis and Recommendations.
    • Build executive-level insights rather than academic explanations.
    • Avoid generic MBA textbook content.
    • Avoid repeating the same insight across multiple frameworks.
    • Cross-reference previous framework findings where relevant.
    • Prioritize recent publicly available information from multiple credible sources while ensuring all information 
    corresponds to the identified company.
    • If reliable information is unavailable, clearly state reasonable assumptions instead of fabricating facts.
    • Maintain an objective, evidence-based consulting tone.
    • Maintain entity consistency throughout the report. Every fact, executive, financial metric, business segment, 
    competitor and recommendation must refer to the identified company only.

    ==================================================
    REPORT DESIGN PRINCIPLES
    ==================================================

    The report should feel like a premium consulting deliverable.

    Design goals

    • Executive friendly
    • Insight dense
    • High readability
    • Structured
    • Professional
    • Decision oriented

    Avoid

    • Long paragraphs
    • Marketing language
    • Generic explanations
    • Excessive repetition
    • Unnecessary filler

    ==================================================
    OUTPUT FORMAT
    ==================================================

    Return ONLY semantic HTML.

    Allowed Tags

    <section>
    <h1>
    <h2>
    <h3>
    <p>
    <strong>
    <ul>
    <li>
    <table>
    <thead>
    <tbody>
    <tr>
    <th>
    <td>
    <hr>

    Do NOT generate

    <html>
    <head>
    <body>
    <style>
    <script>
    <div>
    <span>

    Do NOT use inline CSS.

    ==================================================
    REPORT STRUCTURE
    ==================================================

    Generate the report in EXACTLY the following order.
    
    ==================================================
    SECTION 1
    Executive Dashboard
    ==================================================

    Return

    <section class="dashboard">

    <h1>Executive Dashboard</h1>

    <table class="dashboard-table">

    Include:

    • Company Name
    • Industry
    • Headquarters
    • Region
    • Founded
    • Employee Count
    • Key Executives (Most recent CEO, CTO and other relevant technology/business leaders where publicly available)
    • Overall Position
    • Competitive Strength
    • Growth Outlook
    • Risk Level
    • Innovation Score (Out of 10)
    • Digital Maturity (Out of 10)
    • Overall Score (Out of 100)

    </table>

    </section>

    ==================================================
    SECTION 3
    TL;DR
    ==================================================

    Return

    <section class="tldr-box">

    <h1>TL;DR</h1>

    Provide an executive snapshot in 5 to 7 concise bullet points covering:

    • Current business position
    • Biggest opportunity
    • Biggest strategic risk
    • Competitive advantage
    • Growth outlook
    • Digital/AI maturity
    • One executive recommendation

    Keep the entire section under 200 words.

    ==================================================
    SECTION 4
    Executive Summary
    ==================================================

    Return

    <section class="summary-box">

    <h1>Executive Summary</h1>

    Include the following sections.

    <h2>Business Overview</h2>

    Summarize the company, business model and strategic position.

    <h2>Key Findings</h2>

    Provide 5 to 7 executive findings.

    <h2>Strategic Outlook</h2>

    Summarize future outlook over the next 3 to 5 years considering technology, market trends, competition and business priorities.

    Limit this section to approximately 250 to 300 words.

    </section>

    ==================================================
    SECTION 5
    Framework Analysis
    ==================================================

    Generate ALL requested frameworks.

    For EVERY framework

    Return

    <section class="framework-card">

    <h1>Framework Name</h1>

    Generate an executive-quality analysis.

    Every framework should include

    1. Executive Insight
    2. Analysis
    3. Business Implications
    4. Takeaways

    Under Takeaways provide exactly 3 concise actionable insights.

    Example

    <h2>Takeaways</h2>

    <ul>

    <li>...</li>

    <li>...</li>

    <li>...</li>

    </ul>

    Then include

    After the Takeaways section, include a compact footnote containing the primary sources used for that framework.

    Return:

    <hr>

    <p class="framework-sources">

    <strong>Sources:</strong>
    FY2025 Annual Report • Q2 FY26 Investor Presentation • Reuters • Gartner • Company Website
    
    Use concise source titles instead of raw URLs.
    Do not invent links. If an exact public URL cannot be determined with confidence, mention only the source title without a hyperlink.

    </p>    

    Separate every framework using

    <hr>

    ==================================================
    SECTION 6
    Strategic Recommendations
    ==================================================

    Return

    <section class="recommendation-box">

    <h1>Strategic Recommendations</h1>

    Generate 5 prioritized recommendations.

    Each recommendation should

    • Be actionable
    • Be linked to earlier findings
    • Explain expected business impact
    • Mention implementation priority where appropriate

    Return as

    <ul>

    <li>...</li>

    </ul>

    </section>

    ==================================================
    SECTION 7
    Overall References
    ==================================================

    Return

    <section class="references">

    <h1>Overall Information Sources</h1>

    <ul>

    <li>Official Company Website</li>
    <li>Annual Reports</li>
    <li>Investor Presentations</li>
    <li>Regulatory Filings</li>
    <li>Industry Reports</li>
    <li>Recent Public News</li>

    </ul>

    </section>

    After completing the References section, stop generating.
    """)

    # ------------------------------------------------------------------
    # Framework Prompts
    # ------------------------------------------------------------------

    for index, framework_id in enumerate(framework_ids, start=1):

        framework = get_framework_details(framework_id)

        if framework is None:
            continue

        framework_name = framework["Framework Name"]

        framework_prompt = framework["Prompt"].replace(
            "{Company_Name}",
            company
        )

        prompt_sections.append(f"""
        ============================================================
        FRAMEWORK {index}
        ==================================================

        Framework Name:
        {framework_name}

        IMPORTANT
        Generate this framework ONLY after completing:
        1. Report Header
        2. Executive Dashboard
        3. TL;DR
        4. Executive Summary

        Do not repeat information already discussed.

        Assume previous sections are available and build upon them.

        Keep the analysis strategic, concise and insight-driven.

        End every framework with:
        • Takeaways (exactly 3)
        • Framework-specific Sources as footnotes

        Avoid generic descriptions or textbook explanations.

        <section class="framework-card">

        <h1>{framework_name}</h1>

        ...

        </section>

        ============================================================

        {framework_prompt}
        """)

    # ------------------------------------------------------------------
    # Final Validation
    # ------------------------------------------------------------------

    prompt_sections.append("""
    FINAL VALIDATION

    Before returning the report verify that:

    ✓ Executive Dashboard has been generated.
    ✓ Executive Summary has been generated.
    ✓ Every requested framework has been generated.
    ✓ Framework order has been preserved.
    ✓ Strategic Recommendations have been generated.
    ✓ Every framework is wrapped inside 
    <section class="framework-card">

    ✓ Executive Summary uses
    <section class="summary-box">

    ✓ Dashboard uses
    <section class="dashboard">

    ✓ Recommendation section uses
    <section class="recommendation-box">

    Return ONLY the final HTML.
    Do not explain your work.
    Do not apologise.
    Do not add notes.
    End immediately after Recommendations.
    """)

    return "\n".join(prompt_sections)


if __name__ == "__main__":

    framework_ids = [
        "F1",
        "F5",
        "F13"
    ]

    prompt = build_report_prompt(
        "Microsoft",
        framework_ids
    )

    print(prompt)