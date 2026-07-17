from pathlib import Path

import pandas as pd
import streamlit as st

from eda import render_dashboard

st.set_page_config(page_title="Dataset Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dataset Dashboard")
st.caption("Upload a CSV file to explore its data, quality, and trends.")

default_file = Path(__file__).with_name("data.csv")
uploaded_file = st.sidebar.file_uploader("Upload your dataset (CSV)", type="csv")

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        source = uploaded_file.name
    elif default_file.exists():
        df = pd.read_csv(default_file)
        source = default_file.name
    else:
        st.info("Upload a CSV file from the sidebar, or save it as `data.csv` beside app.py.")
        st.stop()
except (pd.errors.ParserError, UnicodeDecodeError) as error:
    st.error(f"The file could not be read as a CSV: {error}")
    st.stop()

st.sidebar.success(f"Loaded: {source}")
render_dashboard(df)
