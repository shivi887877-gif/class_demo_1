"""Data-loading and empty-state helpers for the Streamlit application."""

from pathlib import Path
from typing import BinaryIO

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="Loading dataset...")
def load_csv(source: str | Path | BinaryIO) -> pd.DataFrame:
    """Load a CSV and remove fully empty rows and columns."""
    data = pd.read_csv(source)
    return data.dropna(axis=0, how="all").dropna(axis=1, how="all")


def render_welcome() -> None:
    """Explain how to provide data when the project CSV is unavailable."""
    st.info("Upload a CSV from the sidebar to begin exploring your used-cars data.")
    st.markdown("""
    ### How to use this dashboard

    1. Place `Cars_cleaned.csv` beside this app, or upload a CSV in the sidebar.
    2. Use the filters to narrow categorical fields such as brand or fuel type.
    3. Explore the data summary and download the filtered results.
    """)
