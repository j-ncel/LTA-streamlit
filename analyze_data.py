import streamlit as st
import pandas as pd
import plotly.express as px


def show_summary_statistics(df):
    st.write("Summary Statistics")
    summary_stats = df.describe()
    st.dataframe(summary_stats)


def select_chart_options(df):
    left_col, right_col = st.columns([1, 1])
    x_axis = left_col.selectbox("Select X-axis", df.columns.tolist())
    y_axis = right_col.selectbox(
        "Select Y-axis", df.select_dtypes(include=['float64', 'int64']).columns.tolist())
    chart_type = left_col.pills(
        "Select Chart Type",
        ["Line Chart", "Bar Chart", "Box Plot", "Scatter Chart"], default="Line Chart"
    )
    color_col = right_col.selectbox(
        "Group by (optional)", ["None"] + df.columns.tolist())
    return x_axis, y_axis, chart_type, color_col


def create_interactive_chart(df, x_axis, y_axis, chart_type, color_col):
    color_arg = None if color_col == "None" else color_col
    fig = None

    if chart_type == "Line Chart":
        plot_df = df.sort_values(
            by=x_axis) if pd.api.types.is_numeric_dtype(df[x_axis]) else df
        fig = px.line(
            plot_df, x=x_axis, y=y_axis, color=color_arg, markers=True,
            title=f"Line Chart: {y_axis} vs {x_axis}"
        )
    elif chart_type == "Bar Chart":
        agg_cols = [x_axis]
        if color_arg:
            agg_cols.append(color_arg)
        grouped = df.groupby(agg_cols, dropna=False)[
            y_axis].mean().reset_index()
        fig = px.bar(
            grouped, x=x_axis, y=y_axis, color=color_arg, barmode="group",
            title=f"Bar Chart: Mean {y_axis} by {x_axis}" +
            (f" and {color_arg}" if color_arg else "")
        )
    elif chart_type == "Box Plot":
        fig = px.box(df, x=x_axis, y=y_axis, color=color_arg,
                     title=f"Box Plot: {y_axis} vs {x_axis}")
    elif chart_type == "Scatter Chart":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_arg,
                         title=f"Scatter Chart: {y_axis} vs {x_axis}")

    if fig is not None:
        fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis, height=500)
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Invalid chart type selected.")


def show_correlation_heatmap(df):
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(
            corr_matrix, text_auto=".2f", color_continuous_scale='RdBu',
            zmin=-1, zmax=1, aspect="auto"
        )
        fig.update_layout(height=500)
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Need at least 2 numeric columns to create a correlation heatmap")


def show_histograms(df):
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        hist_container = st.container(border=True)
        for i in range(0, len(numeric_cols), 3):
            cols = hist_container.columns(3)
            for j, col in enumerate(numeric_cols[i:i+3]):
                with cols[j]:
                    fig = px.histogram(df, x=col, nbins=30,
                                       template='simple_white')
                    fig.update_layout(
                        height=200, showlegend=False,
                        margin=dict(t=10, l=10, r=10, b=10)
                    )
                    st.write(f"Histogram for **{col}**")
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No numeric columns available for histogram visualization")


def analyze_data(df):
    st.write(":blue-background[Analyze Data:]")
    if df.empty:
        st.info("No data available.")
        return

    show_summary_statistics(df)

    st.write(":blue-background[Create Interactive Chart]")
    try:
        x_axis, y_axis, chart_type, color_col = select_chart_options(df)
        create_interactive_chart(df, x_axis, y_axis, chart_type, color_col)
    except Exception as e:
        st.error(f"Cannot create chart  Error: {str(e)}")

    st.write(":blue-background[Correlation Heatmap]")
    show_correlation_heatmap(df)

    st.write(":blue-background[Distribution of Numeric Columns]")
    show_histograms(df)
