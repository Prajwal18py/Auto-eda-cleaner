# 📊 Auto EDA & Data Cleaning Tool

A powerful, interactive web application built with **Streamlit** that streamlines the Data Science workflow. This tool allows users to upload datasets, perform comprehensive Exploratory Data Analysis (EDA), apply advanced data cleaning techniques (including ML-based outlier detection), and download the processed data.

## 🚀 Features

### 1. 📋 Data Overview

* **Instant Preview:** View the head of your dataset immediately after upload.
* **Metadata:** Automatically generate column data types, non-null counts, and unique value counts.
* **Missing Value Analysis:** Get a summarized report of missing data percentages per column.

### 2. 🧹 Advanced Data Cleaning

* **⚡ Auto-Clean Mode:** A one-click solution that removes duplicates and intelligently fills missing values (median for numbers, mode for categories).
* **Handling Missing Values:**
* Drop rows.
* Impute with Mean, Median, or Mode.
* Fill with a specific custom value.


* **Duplicate Removal:** Detect and remove duplicate rows instantly.
* **Outlier Detection & Removal:**
* **IQR Method:** Standard statistical method for outlier removal.
* **Isolation Forest:** Machine Learning algorithm (Unsupervised) to detect anomalies in complex distributions.



### 3. 📊 Exploratory Data Analysis (EDA)

* **Statistical Summary:** detailed descriptive statistics (mean, std, min, max, percentiles).
* **Interactive Visualizations:**
* **Distributions:** Histograms with interactive tooltips.
* **Box Plots:** For spotting outliers visually.
* **Correlation Heatmap:** Visualize relationships between numeric variables.
* **Categorical Counts:** Bar charts for top appearing categories.



### 4. 💾 Export

* **Comparison Metrics:** See how many rows were removed during cleaning.
* **Download:** Export the final cleaned dataset as a `.csv` file.

---

## 📂 Project Structure

To ensure the imports work correctly, organize your files as follows:

```text
auto-eda-tool/
│
├── app.py                 # The main Streamlit application
├── requirements.txt       # List of dependencies
└── utils/
    ├── __init__.py        # Empty file to make utils a Python package
    ├── data_cleaner.py    # Contains the cleaning logic functions
    └── eda_functions.py   # Contains the plotting and stats functions

```

---

## 🛠️ Installation & Setup

1. **Clone the repository** (or create the folder structure above):
```bash
mkdir auto-eda-tool
cd auto-eda-tool

```


2. **Create a virtual environment** (Recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```


3. **Install dependencies**:
Create a `requirements.txt` file with the contents below, then run:
```bash
pip install -r requirements.txt

```


**`requirements.txt` content:**
```text
streamlit
pandas
numpy
scikit-learn
plotly

```


4. **Run the application**:
```bash
streamlit run app.py

```



---

## 📖 Usage Guide

1. **Upload:** Use the sidebar to upload a CSV file.
2. **Overview Tab:** Check the "Missing Values Summary" to see what needs fixing.
3. **Cleaning Tab:**
* Use **"Auto Clean"** for a quick fix.
* Or, go step-by-step: Pick a strategy for missing values -> Remove duplicates -> Select a column to strip outliers.
* *Note:* The app uses Session State, so you can perform multiple cleaning actions in sequence.


4. **EDA Tab:** Select specific columns to visualize their distribution or check the heatmap for correlations.
5. **Download Tab:** Review the final row count and download your clean dataset.

---

## 🧰 Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Machine Learning:** [Scikit-learn](https://scikit-learn.org/) (SimpleImputer, LabelEncoder, StandardScaler, IsolationForest)
* **Visualization:** [Plotly Express](https://plotly.com/python/)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

---

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).