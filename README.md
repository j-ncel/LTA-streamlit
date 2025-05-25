# **Load-Transform-Analyze (LTA) Streamlit App**  

## **Overview**
The **Load-Transform-Analyze App** is a **Streamlit-based** data analysis tool designed for easy dataset handling. It allows users to load, clean, and visualize data interactively.

## **Features**
### 🔹 **Load Data**
🔸Upload CSV or Excel files.
🔸Load sample datasets.
🔸Preview loaded data, including the first rows and the shape of the DataFrame.
🔸Edit column data types using a data editor.

### 🔹 **Transform Data**
🔸Handle missing values using various methods such as dropping rows, forward fill, backward fill, mean imputation, median imputation, and mode imputation.
🔸Download the transformed data as a CSV file.

### 🔹 **Analyze Data**
🔸Generate summary statistics for numeric columns.
🔸Create interactive charts, including line charts, bar charts, box plots, and scatter charts, with customizable X and Y axes and optional color grouping. 
🔸Display a correlation heatmap for numeric columns.
🔸Show histograms for the distribution of numeric columns.

## **📊 Sample Data**
This app includes publicly available datasets from Kaggle as sample datasets: 
- [`ph_school_enrollment.csv`](https://www.kaggle.com/datasets/raiblaze/philippines-school-enrollment-data)  
- [`ph_shs_table_strand.csv`](https://www.kaggle.com/datasets/raiblaze/philippines-school-enrollment-data)  
- [`screentime_analysis_jan_2025.csv`](https://www.kaggle.com/datasets/flaviamonique/screetime-analysis-jan2025)  

To install dependencies:
```bash
pip install -r requirements.txt
```

To run the app:
```bash
streamlit run main.py
```

### Contributing
Contributions are wellcome! Feel free to fork the repository, make changes and submit a pull request.

