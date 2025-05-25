import streamlit as st
import pandas as pd
import os

DTYPE_OPTIONS = ["int64", "float64", "object"]


def show_data_preview(df):
    st.write(":blue-background[Data Preview:]")
    st.write(df.head())
    st.write(
        f":blue-background[Shape:] :orange-background[Rows: {df.shape[0]}]  :orange-background[Columns: {df.shape[1]}]"
    )


def show_columns_info(df):
    st.write(":blue-background[Columns Information:]")
    st.write("You can also edit the data type of column/s here.")
    null_counts = df.isnull().sum()
    info_df = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Null Rows": null_counts
    })
    edited_dtype_df = st.data_editor(
        info_df,
        column_config={
            "Data Type": st.column_config.SelectboxColumn(
                "Data Type",
                options=DTYPE_OPTIONS
            )
        },
        disabled=["Column Name", "Null Rows"],
        hide_index=True,
        key="dtype_editor"
    )
    return edited_dtype_df


def apply_dtype_changes(df, edited_dtype_df):
    for row in edited_dtype_df.itertuples(index=False):
        col, new_dtype = row[0], row[1]
        current_dtype = str(df[col].dtype)
        if new_dtype != current_dtype:
            try:
                df[col] = df[col].astype(new_dtype)
                st.success(f"Changed {col} to {new_dtype}")
            except Exception as e:
                st.error(f"Could not convert {col} to {new_dtype}: {e}")


def load_uploaded_file(uploaded_file):
    file_name = uploaded_file.name.lower()
    if file_name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif file_name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(uploaded_file)
    else:
        st.error("Please upload a valid CSV or Excel file.")
        return None


def load_sample_data():
    sample_data_dir = "sample_data"
    files = [f for f in os.listdir(
        sample_data_dir) if f.endswith(('.csv', '.xlsx', '.xls'))]
    if not files:
        st.warning("No sample data files found.")
        return None

    info = """
    DATA FROM KAGGLE: \n
    ph_school_enrollment.csv: https://www.kaggle.com/datasets/raiblaze/philippines-school-enrollment-data \n
    ph_shs_table_strand.csv: https://www.kaggle.com/datasets/raiblaze/philippines-school-enrollment-data \n

    """
    selected_file = st.selectbox(
        "Select a sample data file", files, index=0, help=info)
    sample_path = os.path.join(sample_data_dir, selected_file)
    return sample_path


def load_data():
    st.write(":blue-background[Load Data:]")

    uploaded_file = st.file_uploader(
        "Choose your CSV or Excel File",
        type=["csv", "xlsx", "xls"],
        on_change=lambda: st.session_state.__setitem__('transformed', False)
    )

    sample_data = load_sample_data()

    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame()

    if st.session_state.get("transformed", False):
        df = st.session_state
        st.session_state.transformed = False
    elif uploaded_file is not None and not st.session_state.get("transformed", False):
        df = load_uploaded_file(uploaded_file)
        if df is not None:
            st.session_state.df = df
    elif st.session_state.df.empty and not st.session_state.get("transformed", False):
        df = pd.read_csv(sample_data)
        st.session_state.df = df

    df = st.session_state.df
    st.session_state.transformed = False

    if not df.empty:
        show_data_preview(df)
        edited_dtype_df = show_columns_info(df)
        apply_dtype_changes(df, edited_dtype_df)
        st.session_state.df = df
