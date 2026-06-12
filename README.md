# Netflix Data Analysis: 45-Day Professional Internship Project

Welcome to the **Netflix Data Analysis Project** workspace! This project is structured as a professional, corporate-ready 45-day internship curriculum. Over the course of this project, you will load, clean, analyze, visualize, and extract data-driven business insights from Netflix's extensive catalog.

---

## 📁 Workspace Structure

```
project1/
├── data/
│   ├── netflix_titles.csv              # Raw titles dataset
│   └── netflix_titles_cleaned.csv      # Cleaned and processed dataset
├── notebooks/
│   ├── 01_data_cleaning.ipynb          # Day 1–10: Data parsing & pipeline execution
│   ├── 02_exploratory_analysis.ipynb   # Day 11–30: Univariate & Bivariate EDA
│   └── 03_advanced_insights.ipynb      # Day 31–42: Multivalue explosions, text & temporal trends
├── src/
│   ├── __init__.py                     # Package marker
│   ├── data_cleaner.py                 # Modular script containing ETL logic
│   └── visualization_theme.py          # Custom styling theme for Seaborn/Matplotlib
├── README.md                           # Project documentation
└── requirements.txt                    # Project dependencies
```

---

## 🛠️ Installation & Setup

1. **Verify Python Installation**: Make sure Python 3.9+ is installed on your system.
2. **Install Dependencies**: Open your terminal in the `project1` root directory and install packages using:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Notebooks**: Launch Jupyter Notebook or VS Code Jupyter Extension:
   ```bash
   jupyter notebook
   ```
   Open the files in `notebooks/` in sequential order:
   - Run [01_data_cleaning.ipynb](file:///c:/Users/yaswa/OneDrive/Desktop/internprograms/project1/notebooks/01_data_cleaning.ipynb) to clean the raw data.
   - Run [02_exploratory_analysis.ipynb](file:///c:/Users/yaswa/OneDrive/Desktop/internprograms/project1/notebooks/02_exploratory_analysis.ipynb) to inspect primary variables and distributions.
   - Run [03_advanced_insights.ipynb](file:///c:/Users/yaswa/OneDrive/Desktop/internprograms/project1/notebooks/03_advanced_insights.ipynb) for advanced temporal, genre, and text analysis.

---

## 📈 Key Research Insights Summary

Here are the primary corporate findings extracted from the dataset:

*   **Content Composition**: Approximately **69.6%** of Netflix's catalog consists of Movies, while **30.4%** consists of TV Shows.
*   **Release Timing**: Over **50%** of Netflix content is added on **Fridays**, matching the company's release strategy targeting weekend binge-watching.
*   **Seasonality**: Content additions peak during the late fall and early winter months (October, November, December, January), with December leading as the top month for uploads.
*   **Retention/Renewal Profile**: Nearly **68%** of TV Shows on the platform only run for **1 Season**, highlighting a strategic focus on miniseries or high-turnover trial runs before committing to multi-season renewals.
*   **Narrative Focus**: Text analysis on description content shows that dramas, thrillers, and family-centric themes dominate descriptions, emphasizing keywords like *love, life, family, world, school, secrets, murder*.

---

## 🧑‍💻 Technical Highlights
*   **ETL Engineering**: Misplaced duration/rating discrepancies are resolved automatically inside `src/data_cleaner.py`.
*   **Custom Corporate Styling**: Charts are standardized with professional typography, appropriate spacing, and Netflix brand HSL color mappings using `src/visualization_theme.py`.
*   **Data Multi-explosion**: Comma-separated listing fields (such as `country` or `listed_in`) are exploded dynamically to represent country and genre frequencies accurately without skew.
