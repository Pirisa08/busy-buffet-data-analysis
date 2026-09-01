# Busy Buffet Data Analysis
Data Analytics Assessment for **Hotel Amber 85**

This project analyzes the Busy Buffet dataset using Python and Streamlit.  
The objective is to validate staff comments, challenge management recommendations, and propose a practical solution based on the available data.

## Project Objectives
### Task 1 — Validate Staff Comments
Analyze the dataset to determine whether the following staff comments are supported by the data:

1. In-house guests have to wait for tables, while some walk-in guests leave after waiting too long.
2. The buffet is very busy every day of the week.
3. Walk-in customers sit for a very long time and reduce table availability.

Each comment is supported with:
- Data analysis
- Visualizations
- Key findings
- Verdict

### Task 2 — Challenge Recommended Actions
Evaluate the following proposed management actions and explain why they may not effectively solve the problem:

1. Reduce the current five-hour seating time.
2. Increase the buffet price to THB 259 every day.
3. Allow in-house guests to skip the queue.

### Task 3 — Recommendation
Recommend a practical solution based on the available data.

The proposed approach is a **peak-period seating-time policy**, applying a shorter seating limit only during high-demand periods rather than throughout the entire day.

## Key Findings

- In-house guests waited an average of **28.0 minutes**.
- Walk-in guests waited an average of **38.4 minutes**.
- There were **14 walk-away groups** in the dataset.
- Queue pressure was concentrated mainly on **14/3 and 15/3**.
- On 15/3, there were **54 queued groups**, the highest among the observed dates.
- Walk-in guests stayed longer than in-house guests on average.
- Only **10.6% of seated walk-in groups** stayed longer than 120 minutes.
- Only approximately **7.4% of all seated groups** stayed longer than 120 minutes.

## Dashboard
The Streamlit dashboard includes:

- Summary KPIs
- Waiting-time analysis
- Walk-away analysis
- Customer-volume analysis
- Meal-duration analysis
- Management-action evaluation
- Final recommendation

## Files
- `app.py` — Streamlit dashboard
- `requirements.txt` — Python dependencies
- `2026 Data Test1 Final - Busy Buffet Dataset.xlsx` — Dataset used in the analysis

## Tools Used
- Python
- Pandas
- Matplotlib
- Streamlit
- Google Colab

## How to Run Locally
Install the required packages:

```bash
pip install -r requirements.txt

Run the Streamlit application:

streamlit run app.py

Author

Pirisa Kitichai

Data Analytics Assessment — 2026
