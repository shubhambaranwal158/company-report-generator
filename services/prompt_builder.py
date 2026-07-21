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


def build_report_prompt(company: str, framework_ids: list[str]) -> str:
    """
    Builds one optimized master prompt for the complete report.
    """

    prompt_sections = []

    # ------------------------------------------------------------------
    # MASTER REPORT INSTRUCTIONS
    # ------------------------------------------------------------------

    prompt_sections.append(f"""
    You are a Senior Strategy Consultant at McKinsey, BCG or Bain.

    Prepare a professional Executive Intelligence Report for:

    COMPANY
    {company}

    OBJECTIVE

    Generate ONE cohesive executive report using ALL requested business frameworks.

    The report should read like a premium consulting deliverable rather than independent AI responses.

    GENERAL RULES

    • Maintain one consistent executive tone.
    • Avoid repeating insights across frameworks.
    • Focus on strategic insights rather than descriptive facts.
    • Use recent publicly available information wherever possible.
    • Avoid unsupported assumptions.
    • Keep insights concise and actionable.
    • Follow each framework prompt exactly.

    REPORT STYLE GUIDE

    REPORT DESIGN LANGUAGE

    This report should resemble a premium consulting deliverable.

    Design Principles:

    • Executive-friendly
    • Visually rich
    • Minimal text
    • High information density
    • Structured sections
    • Strong visual hierarchy

    Avoid:

    • Long paragraphs
    • Generic explanations
    • Text-heavy analysis
    • Repeated wording

    OUTPUT FORMAT

    Return ONLY semantic HTML.

    Allowed HTML tags:

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

    Do NOT generate:

    <html>
    <head>
    <body>
    <style>
    <script>
    <div>
    <span>

    Do NOT use inline CSS.

    REPORT STRUCTURE

    Generate the report EXACTLY in the following order.

    Do NOT skip any section.

    Complete each section before moving to the next.

    ==================================================
    SECTION 1
    ==================================================

    Generate ONLY the Executive Dashboard.

    The dashboard must contain:

    • Company Name
    • Industry
    • Headquarters
    • Region
    • Founded
    • Employee Count
    • Key Executives (Current CEO, Founder, CTO or other major leadership where publicly available)
    • Overall Position
    • Competitive Strength
    • Growth Outlook
    • Risk Level
    • Innovation Score (/10)
    • Digital Maturity (/10)
    • Overall Score (/100)

    Return it using:

    <section class="dashboard">

    <h1>Executive Dashboard</h1>

    <table class="dashboard-table">

    <tr>
    <th>Company Name</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Industry</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Headquarters</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Region</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Founded</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Key Executives</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Employees</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Overall Position</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Competitive Strength</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Growth Outlook</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Risk Level</th>
    <td>...</td>
    </tr>

    <tr>
    <th>Innovation</th>
    <td>.../10</td>
    </tr>

    <tr>
    <th>Digital Maturity</th>
    <td>.../10</td>
    </tr>

    <tr>
    <th>Overall Score</th>
    <td>.../100</td>
    </tr>

    </table>

    </section>

    ==================================================
    SECTION 2
    ==================================================

    Generate ONLY the Executive Summary.

    Return it as

    <section class="summary-box">

    <h1>Executive Summary</h1>

    <p>

    Write a concise Executive Summary (250–350 words).

    Structure it using the following subheadings:

    <h2>Business Overview</h2>

    <p>...</p>

    <h2>Key Findings</h2>

    <ul>
    <li>...</li>
    </ul>

    <h2>Strategic Outlook</h2>

    <p>...</p>

    </p>

    </section>

    ==================================================
    SECTION 3
    ==================================================

    Generate ALL requested frameworks.
    Do NOT skip any framework.
    For EVERY framework:
    Return

    <section class="framework-card">

    <h1>Actual Framework Name</h1>

    Framework output

    </section>

    Separate every framework using

    <hr>

    ==================================================
    SECTION 4
    ==================================================

    Generate Strategic Recommendations.

    Return

    <section class="recommendation-box">

    <h1>Strategic Recommendations</h1>

    <ul>

    <li>Recommendation 1</li>
    <li>Recommendation 2</li>
    <li>Recommendation 3</li>
    <li>Recommendation 4</li>
    <li>Recommendation 5</li>

    </ul>

    </section>

    <section class="references">

    <h1>Information Sources</h1>

    <ul>

    <li>Company website</li>
    <li>Annual reports</li>
    <li>Public investor presentations</li>
    <li>Industry reports</li>
    <li>Recent news where applicable</li>

    </ul>

    </section>

    After completing SECTION 5 stop generating.

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
        Generate this framework ONLY after the Executive Dashboard and Executive Summary have already been completed.
        Return the framework using

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