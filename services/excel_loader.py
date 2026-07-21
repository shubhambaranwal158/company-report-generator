import pandas as pd
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FRAMEWORK_FILE = os.path.join(
    BASE_DIR,
    "config",
    "Framework_Intelligence.xlsx"
)

MAPPING_FILE = os.path.join(
    BASE_DIR,
    "config",
    "Persona_Report_Mapping.xlsx"
)

@st.cache_data
def load_framework_library() -> pd.DataFrame:
    """
    Load the Framework Intelligence Excel file.
    """
    return pd.read_excel(FRAMEWORK_FILE)

@st.cache_data
def load_mapping() -> pd.DataFrame:
    """
    Load Persona-Report-Framework Mapping.
    """
    return pd.read_excel(MAPPING_FILE)

def get_personas() -> list:

    mapping_df = load_mapping()

    personas = sorted(mapping_df["Persona"].dropna().unique())

    return personas

def get_reports(persona: str) -> list:

    mapping_df = load_mapping()

    reports = mapping_df[
        mapping_df["Persona"] == persona
    ]["Report Name"].unique()

    return sorted(reports)

def get_frameworks_for_report(persona: str, report: str) -> list:

    mapping_df = load_mapping()

    frameworks = (
    mapping_df[
        (mapping_df["Persona"] == persona)
        &
        (mapping_df["Report Name"] == report)
    ]["Framework"]
    .dropna()
    .tolist())
    return frameworks

def get_framework_details(framework_id: str) -> dict | None:

    framework_df = load_framework_library()

    framework = framework_df[
    framework_df["#"].astype(str).str.strip() == framework_id
    ]

    if framework.empty:
        return None

    return framework.iloc[0].to_dict()

def get_framework_names(persona: str, report: str) -> list:

    framework_ids = get_frameworks_for_report(
        persona,
        report
    )

    framework_df = load_framework_library()

    framework_names = []

    for framework_id in framework_ids:

        framework = framework_df[
            framework_df["#"].astype(str).str.strip() == framework_id
        ]

        if not framework.empty:

            framework_names.append(
                framework.iloc[0]["Framework Name"]
            )

    return framework_names


if __name__ == "__main__":

    print("Personas")
    print(get_personas())

    print("\nReports")
    print(get_reports("Leadership"))

    print("\nFramework IDs")
    print(
        get_frameworks_for_report(
            "Leadership",
            "Corporate Strategy & Company Health"
        )
    )

    print("\nFramework Details")
    print(get_framework_details("F37"))

    print("\nFramework Names")
    print(
        get_framework_names(
            "Leadership",
            "Corporate Strategy & Company Health"
        )
    )