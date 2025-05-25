import streamlit as st
import pandas as pd


def handle_missing_values(df):
    """Handles missing values in the DataFrame"""
    st.write("Handle Missing Values")
    missing_cols = df.columns[df.isnull().any()].tolist()
    if not missing_cols:
        st.info("No missing values detected.")
        return df

    if st.button("Drop all missing values"):
        df = df.dropna()

    selected_col = st.selectbox(
        "Select column with missing values", missing_cols)

    action = st.pills(
        "How to handle?",
        ["Drop rows", "Forward Fill", "Backward Fill",
            "Fill Mean", "Fill Median", "Fill Mode"]
    )

    if action == "Forward Fill":
        df[selected_col] = df[selected_col].fillna(method="ffill")
        st.success(
            f"Filled missing values in {selected_col} with previous value forward.")
    elif action == "Backward Fill":
        df[selected_col] = df[selected_col].fillna(method="bfill")
        st.success(
            f"Filled missing values in {selected_col} with next valid value.")
    elif action == "Drop rows":
        df = df.dropna(subset=[selected_col])
        st.success(f"Dropped rows with missing values in {selected_col}")
    elif action == "Fill Mean":
        if pd.api.types.is_numeric_dtype(df[selected_col]):
            df[selected_col] = df[selected_col].fillna(df[selected_col].mean())
            st.success(
                f"Filled missing values in {selected_col} with the Mean value.")
        else:
            st.error("Mean can only be used for numeric columns.")

    elif action == "Fill Median":
        if pd.api.types.is_numeric_dtype(df[selected_col]):
            df[selected_col] = df[selected_col].fillna(
                df[selected_col].median())
            st.success(
                f"Filled missing values in {selected_col} with the Median value.")
        else:
            st.error("Median can only be used for numeric columns.")
    elif action == "Fill Mode":
        mode_value = df[selected_col].mode(
        ).iloc[0] if not df[selected_col].mode().empty else None
        df[selected_col] = df[selected_col].fillna(mode_value)
        st.success(
            f"Filled missing values in {selected_col} with the Mode value.")

    st.session_state.transformed = True
    return df


def show_null_info(df):
    """Displays null value information and column details."""
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()
    if total_nulls > 0:
        st.warning(f"You have {total_nulls} null values in the dataset.")
    else:
        st.info(f"You have {total_nulls} null values in the dataset.")

    st.dataframe(
        pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes,
            "Null Rows": null_counts
        }),
        hide_index=True
    )
    st.info(
        f"Shape: :orange-background[{df.shape[0]} Rows] :orange-background[{df.shape[1]} Columns]")


def download_transformed_data(df):
    """Provides a download button for the transformed DataFrame."""
    if df.empty:
        st.warning("No data available to download.")
        return
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Transformed Data as CSV",
        data=csv,
        file_name="transformed_data.csv",
        mime="text/csv"
    )


def transform_data(df):
    """Main function to transform data."""
    st.write(":blue-background[Transform Data]")
    if df.empty:
        st.warning("No data to transform.")
        return

    df = handle_missing_values(df)
    st.session_state.df = df

    show_null_info(df)
    download_transformed_data(df)
