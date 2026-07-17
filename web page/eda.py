import pandas as pd
import plotly.express as px
import streamlit as st


def render_dashboard(df: pd.DataFrame) -> None:
    """Render an interactive exploratory dashboard for any CSV dataset."""
    df = df.copy()
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

    with st.sidebar:
        st.subheader("Filters")
        filter_column = st.selectbox("Filter a column", ["No filter"] + categorical_columns)
        if filter_column != "No filter":
            values = sorted(df[filter_column].dropna().astype(str).unique().tolist())
            selected_values = st.multiselect("Select values", values, default=values)
            df = df[df[filter_column].astype(str).isin(selected_values)]

    total_missing = int(df.isna().sum().sum())
    left, middle_left, middle_right, right = st.columns(4)
    left.metric("Rows", f"{len(df):,}")
    middle_left.metric("Columns", len(df.columns))
    middle_right.metric("Missing values", f"{total_missing:,}")
    right.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")

    overview_tab, analysis_tab, relationship_tab, quality_tab = st.tabs(
        ["Overview", "Column analysis", "Relationships", "Data quality"]
    )

    with overview_tab:
        st.subheader("Dataset preview")
        st.dataframe(df, use_container_width=True, height=340)
        st.subheader("Summary statistics")
        if numeric_columns:
            st.dataframe(df[numeric_columns].describe().T, use_container_width=True)
        else:
            st.info("This dataset has no numeric columns to summarize.")

    with analysis_tab:
        column = st.selectbox("Choose a column", df.columns, key="univariate_column")
        if column in numeric_columns:
            chart_left, chart_right = st.columns(2)
            with chart_left:
                bins = st.slider("Histogram bins", 5, 100, 30)
                st.plotly_chart(px.histogram(df, x=column, nbins=bins, title=f"Distribution of {column}"), use_container_width=True)
            with chart_right:
                st.plotly_chart(px.box(df, y=column, title=f"Box plot of {column}"), use_container_width=True)
        else:
            counts = df[column].fillna("Missing").astype(str).value_counts().head(20).reset_index()
            counts.columns = [column, "Count"]
            st.plotly_chart(px.bar(counts, x=column, y="Count", title=f"Top values in {column}"), use_container_width=True)

    with relationship_tab:
        if len(numeric_columns) >= 2:
            x_axis, y_axis = st.columns(2)
            x = x_axis.selectbox("X-axis", numeric_columns, key="x_axis")
            y = y_axis.selectbox("Y-axis", numeric_columns, index=min(1, len(numeric_columns) - 1), key="y_axis")
            color_options = ["No color"] + categorical_columns
            color = st.selectbox("Color by", color_options)
            st.plotly_chart(
                px.scatter(df, x=x, y=y, color=None if color == "No color" else color, title=f"{y} vs {x}"),
                use_container_width=True,
            )
            st.subheader("Correlation matrix")
            correlation = df[numeric_columns].corr()
            st.plotly_chart(px.imshow(correlation, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1), use_container_width=True)
        else:
            st.info("At least two numeric columns are needed for relationship analysis.")

    with quality_tab:
        st.subheader("Missing values by column")
        missing = df.isna().sum().sort_values(ascending=False).reset_index()
        missing.columns = ["Column", "Missing values"]
        st.dataframe(missing, use_container_width=True)
        st.subheader("Data types")
        types = df.dtypes.astype(str).reset_index()
        types.columns = ["Column", "Data type"]
        st.dataframe(types, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download filtered data", csv, "filtered_dataset.csv", "text/csv")
