
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Busy Buffet Data Analysis",
    page_icon="🍽️",
    layout="wide"
)


# =========================
# Dashboard Styling
# =========================

st.markdown("""
<style>

/* Main page width */
.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* Main title */
h1 {
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
    margin-bottom: 0.4rem !important;
}

/* Task titles */
h2 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    margin-top: 3rem !important;
    margin-bottom: 1.2rem !important;
}

/* Comment / Action titles */
h3 {
    font-size: 1.45rem !important;
    font-weight: 650 !important;
    margin-top: 2.2rem !important;
    margin-bottom: 1rem !important;
}

/* Normal text */
p, li {
    font-size: 1rem !important;
    line-height: 1.65 !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.04);
}

/* Metric value */
div[data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
}

/* Success message */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Captions under graphs */
div[data-testid="stCaptionContainer"] {
    text-align: center;
    font-size: 0.85rem;
    color: #777;
    margin-top: -0.4rem;
    margin-bottom: 1.8rem;
}

/* Center matplotlib charts and limit size */
div[data-testid="stImage"] {
    text-align: center;
}

div[data-testid="stImage"] img {
    max-width: 780px;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
}

/* Horizontal lines */
hr {
    margin-top: 2.5rem;
    margin-bottom: 2.5rem;
    border-color: #eeeeee;
}

/* Reduce top menu visual weight */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Lists */
ul, ol {
    padding-left: 1.4rem;
}

</style>
""", unsafe_allow_html=True)


st.title("🍽️ Busy Buffet Data Analysis")

st.markdown("""
### Hotel Amber 85
**Data Analytics Assessment · 2026**

Prepared by **Pirisa Kitichai**
""")

st.markdown("---")

st.header("Overview")

st.write("""
This dashboard analyzes the Busy Buffet dataset to:

1. Validate the three staff comments.
2. Challenge the three management actions.
3. Recommend a practical solution based on the available data.
""")

# =========================
# Load and Prepare Dataset
# =========================

file_path = "2026 Data Test1 Final - Busy Buffet Dataset.xlsx"

sheet_to_date = {
    '133': '13/3',
    '143': '14/3',
    '153': '15/3',
    '173': '17/3',
    '183': '18/3'
}

all_data = []

for sheet, date in sheet_to_date.items():
    df = pd.read_excel(file_path, sheet_name=sheet)
    df['date'] = date
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)

data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Clean time columns
time_cols = ['queue_start', 'queue_end', 'meal_start', 'meal_end']

for col in time_cols:
    data[col] = pd.to_datetime(
        data[col].astype(str),
        errors='coerce'
    )

# Calculate waiting and meal duration
data['wait_minutes'] = (
    data['queue_end'] - data['queue_start']
).dt.total_seconds() / 60

data['meal_minutes'] = (
    data['meal_end'] - data['meal_start']
).dt.total_seconds() / 60

# Create flags
data['walk_away'] = (
    data['queue_start'].notna()
    & data['meal_start'].isna()
)

data['waited'] = (
    data['queue_start'].notna()
    & data['queue_end'].notna()
)

data['direct_seating'] = (
    data['meal_start'].notna()
    & data['queue_start'].isna()
)

# Daily summary
daily_summary = (
    data.groupby('date')
    .agg(
        total_groups=('service_no.', 'count'),
        total_pax=('pax', 'sum'),
        queued_groups=('waited', 'sum'),
        walk_away_groups=('walk_away', 'sum')
    )
    .reset_index()
)

st.success("Dataset loaded successfully")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(data))
col2.metric("Total Pax", int(data['pax'].sum()))
col3.metric("Queued Groups", int(data['waited'].sum()))
col4.metric("Walk-away Groups", int(data['walk_away'].sum()))

st.markdown("---")

# =========================
# TASK 1
# =========================

st.header("Task 1 — Validate Staff Comments")

# -------------------------
# Comment 1
# -------------------------

st.subheader("Comment 1: Waiting Time and Walk-away")

st.markdown("**Staff Claim**")
st.write(
    "In-house guests have to wait for tables, while walk-in guests may wait too long and leave the queue."
)

st.markdown("**Key Findings**")

st.write("""
- In-house average waiting time: **28.0 minutes**
- Walk-in average waiting time: **38.4 minutes**
- Total walk-away groups: **14**
- On 15/3, average waiting time increased to **30.7 minutes** for in-house guests and **46.8 minutes** for walk-in guests.
""")

# Figure 1
wait_daily = (
    data[data['wait_minutes'].notna()]
    .groupby(['date', 'Guest_type'])['wait_minutes']
    .mean()
    .unstack()
)

fig1, ax1 = plt.subplots(figsize=(7,4))

wait_daily.plot(
    kind='bar',
    ax=ax1
)

ax1.set_title(
    'Task 1 — Comment 1: Average Waiting Time by Date and Guest Type',
    fontweight='bold', fontsize=13, pad=14
)

ax1.set_xlabel('Date')
ax1.set_ylabel('Average Waiting Time (minutes)')
ax1.tick_params(axis='x', rotation=0)

st.pyplot(fig1)

st.caption("Average Waiting Time by Date and Guest Type")

# Figure 2
walkaway_summary = (
    data[data['walk_away']]
    .groupby(['date', 'Guest_type'])
    .size()
    .reset_index(name='walk_away_groups')
)

walkaway_plot = (
    walkaway_summary
    .pivot(
        index='date',
        columns='Guest_type',
        values='walk_away_groups'
    )
    .fillna(0)
)

fig2, ax2 = plt.subplots(figsize=(7,4))

walkaway_plot.plot(
    kind='bar',
    ax=ax2
)

ax2.set_title(
    'Task 1 — Comment 1: Walk-away Groups by Date and Guest Type',
    fontweight='bold', fontsize=13, pad=14
)

ax2.set_xlabel('Date')
ax2.set_ylabel('Number of Walk-away Groups')
ax2.tick_params(axis='x', rotation=0)

st.pyplot(fig2)

st.caption("Walk-away Groups by Date and Guest Type")

st.markdown("**Verdict: Partially True**")

st.write("""
The data confirms that both guest types experienced waiting times and that some queued guests left before being seated. However, the dataset does not directly measure customer satisfaction, so the word “unhappy” cannot be proven from the available data alone.
""")

st.markdown("---")

# -------------------------
# Comment 2
# -------------------------

st.subheader("Comment 2: We are very busy every day of the week.")

st.markdown("**Staff Claim**")
st.write(
    "The buffet is very busy every day and may be impossible to sustain."
)

st.markdown("**Key Findings**")

st.write("""
- 13/3: **57 groups, 102 pax, 0 queued groups**
- 14/3: **81 groups, 154 pax, 19 queued groups, 1 walk-away group**
- 15/3: **86 groups, 166 pax, 54 queued groups, 13 walk-away groups**
- 17/3: **70 groups, 118 pax, 0 queued groups**
- 18/3: **70 groups, 122 pax, 0 queued groups**
""")

# Figure 3
fig3, ax3 = plt.subplots(figsize=(7,4))

ax3.bar(
    daily_summary['date'],
    daily_summary['total_pax']
)

ax3.set_title(
    'Task 1 — Comment 2: Total Pax by Date',
    fontweight='bold', fontsize=13, pad=14
)

ax3.set_xlabel('Date')
ax3.set_ylabel('Total Pax')

st.pyplot(fig3)

st.caption("Total Pax by Date")

# Figure 4
fig4, ax4 = plt.subplots(figsize=(7,4))

ax4.bar(
    daily_summary['date'],
    daily_summary['queued_groups']
)

ax4.set_title(
    'Task 1 — Comment 2: Queued Groups by Date',
    fontweight='bold', fontsize=13, pad=14
)

ax4.set_xlabel('Date')
ax4.set_ylabel('Number of Queued Groups')

st.pyplot(fig4)

st.caption("Queued Groups by Date")

st.markdown("**Verdict: False / Exaggerated**")

st.write("""
Customer volume and queue pressure varied significantly across the observed dates. 
15/3 was the busiest day with **166 pax and 54 queued groups**, while 14/3 had 
**154 pax and 19 queued groups**. In contrast, 13/3, 17/3, and 18/3 had no recorded 
queued groups.

The restaurant was therefore not equally busy every day; operational congestion 
was concentrated mainly on 14/3 and especially 15/3.
""")

st.markdown("---")

# -------------------------
# Comment 3
# -------------------------

st.subheader("Comment 3: Walk-in customers sit the whole day.")

st.markdown("**Staff Claim**")
st.write(
    "Walk-in guests sit for a very long time and reduce table availability for in-house guests."
)

st.markdown("**Key Findings**")

st.write("""
- Average meal duration for Walk-in guests: **72.8 minutes**
- Average meal duration for In-house guests: **45.3 minutes**
- Only **21 of 199 seated Walk-in groups (10.6%)** stayed longer than 120 minutes
""")

# Figure 5
meal_avg = (
    data[data['meal_minutes'].notna()]
    .groupby('Guest_type')['meal_minutes']
    .mean()
)

fig5, ax5 = plt.subplots(figsize=(7,4))

meal_avg.plot(
    kind='bar',
    ax=ax5
)

ax5.set_title(
    'Task 1 — Comment 3: Average Meal Duration by Guest Type',
    fontweight='bold', fontsize=13, pad=14
)

ax5.set_xlabel('Guest Type')
ax5.set_ylabel('Average Meal Duration (minutes)')
ax5.tick_params(axis='x', rotation=0)

st.pyplot(fig5)

st.caption("Average Meal Duration by Guest Type")


# Figure 6
walkin_meals = data[
    (data['Guest_type'] == 'Walk in')
    & (data['meal_minutes'].notna())
]['meal_minutes']

fig6, ax6 = plt.subplots(figsize=(7,4))

ax6.hist(
    walkin_meals,
    bins=15
)

ax6.axvline(
    120,
    linestyle='--',
    label='120 minutes'
)

ax6.set_title(
    'Task 1 — Comment 3: Walk-in Meal Duration Distribution',
    fontweight='bold', fontsize=13, pad=14
)

ax6.set_xlabel('Meal Duration (minutes)')
ax6.set_ylabel('Number of Groups')
ax6.legend()

st.pyplot(fig6)

st.caption("Walk-in Meal Duration Distribution")

st.metric(
    "Walk-in groups staying longer than 120 minutes",
    "10.6%",
    "21 of 199 seated groups"
)

st.markdown("**Verdict: Partially True**")

st.write("""
Walk-in guests stayed longer than in-house guests on average. However, only 
**10.6%** of seated walk-in groups stayed longer than 120 minutes.

Therefore, the statement that walk-in guests “sit the whole day” is exaggerated 
and does not represent the majority of walk-in customers.
""")

st.markdown("---")

# =========================
# TASK 2
# =========================

st.header("Task 2 — Challenge Recommended Actions")

# -------------------------
# Action 1
# -------------------------

st.subheader("Action 1: Reduce Seating Time")

st.markdown("**Management Proposal**")
st.write(
    "Reduce the current five-hour seating time."
)

st.markdown("**Why It May Not Work**")

st.write("""
Only a small proportion of seated groups stayed for extended periods.

Approximately:
- **7.4%** stayed longer than 120 minutes
- **1.1%** stayed longer than 180 minutes
- only around **0.3%** exceeded 300 minutes

Because almost all guests already leave well before the five-hour limit,
reducing the maximum seating time would affect only a small minority of customers
and may not address the main cause of congestion during peak periods.
""")

# Prepare duration threshold data
seated = data[data['meal_minutes'].notna()].copy()

duration_thresholds = pd.DataFrame({
    'threshold': ['> 120 min', '> 180 min', '> 300 min'],
    'groups': [
        (seated['meal_minutes'] > 120).sum(),
        (seated['meal_minutes'] > 180).sum(),
        (seated['meal_minutes'] > 300).sum()
    ]
})

duration_thresholds['percentage'] = (
    duration_thresholds['groups'] / len(seated) * 100
).round(1)

# Figure 7
fig7, ax7 = plt.subplots(figsize=(7,4))

ax7.bar(
    duration_thresholds['threshold'],
    duration_thresholds['percentage']
)

ax7.set_title(
    'Task 2 — Action 1: Share of Guests Exceeding Seating Duration Thresholds',
    fontweight='bold', fontsize=13, pad=14
)

ax7.set_xlabel('Meal Duration Threshold')
ax7.set_ylabel('Percentage of Seated Groups')

st.pyplot(fig7)

st.caption(
    "Share of Guests Exceeding Seating Duration Thresholds"
)

st.markdown("**Key KPI**")
st.write(
    ">120 min ≈ **7.4%** | >180 min ≈ **1.1%** | >300 min ≈ **0.3%**"
)

st.markdown("**Verdict: Weak as a standalone solution**")

st.write("""
The existing five-hour limit is not binding for most customers.
A modest reduction in the seating limit is therefore unlikely to solve
the peak-period queue problem by itself.
""")

st.markdown("---")

# -------------------------
# Action 2
# -------------------------

st.subheader("Action 2: Increase Price to THB 259 Every Day")

st.markdown("**Management Proposal**")
st.write(
    "Increase the buffet price to THB 259 every day."
)

st.markdown("**Why It May Not Work**")

st.write("""
The dataset contains no historical observations at the proposed **THB 259** price,
so the effect of the price increase on customer demand cannot be estimated directly.

A higher price may reduce demand, but the available data cannot show:
- how much demand would decrease
- whether the decrease would be enough to solve the queue problem
- whether the price increase would unnecessarily affect lower-demand days
""")

# Figure 8
fig8, ax8 = plt.subplots(figsize=(7,4))

ax8.bar(
    daily_summary['date'],
    daily_summary['total_pax']
)

ax8.set_title(
    'Task 2 — Action 2: Customer Volume by Date',
    fontweight='bold', fontsize=13, pad=14
)

ax8.set_xlabel('Date')
ax8.set_ylabel('Total Pax')

st.pyplot(fig8)

st.caption("Customer Volume by Date")


# Figure 9
fig9, ax9 = plt.subplots(figsize=(7,4))

ax9.bar(
    daily_summary['date'],
    daily_summary['total_groups']
)

ax9.set_title(
    'Task 2 — Action 2: Total Groups by Date',
    fontweight='bold', fontsize=13, pad=14
)

ax9.set_xlabel('Date')
ax9.set_ylabel('Total Groups')

st.pyplot(fig9)

st.caption("Total Groups by Date")

st.markdown("**Data Limitation**")
st.write(
    "No price-elasticity or before/after pricing data is available in the dataset."
)

st.markdown("**Verdict: Not supported by the current dataset**")

st.write("""
Customer demand varies by date, but the dataset does not provide evidence that
raising the buffet price to THB 259 would reduce demand by an appropriate amount.

Therefore, a permanent price increase cannot be justified as a reliable
queue-management solution using the available data.
""")

st.markdown("---")

# -------------------------
# Action 3
# -------------------------

st.subheader("Action 3: Queue Skipping for In-house Guests")

st.markdown("**Management Proposal**")
st.write(
    "Allow in-house guests to skip the queue."
)

st.markdown("**Why It May Not Work**")

st.write("""
Queue priority may improve the experience for in-house guests,
but it does not increase the number of available tables.

Walk-in guests already wait longer on average than in-house guests.
Giving in-house guests priority may therefore push walk-in guests
further back in the queue and potentially increase walk-away behavior.
""")

# Figure 10
avg_wait = (
    data[data['wait_minutes'].notna()]
    .groupby('Guest_type')['wait_minutes']
    .mean()
)

fig10, ax10 = plt.subplots(figsize=(7,4))

avg_wait.plot(
    kind='bar',
    ax=ax10
)

ax10.set_title(
    'Task 2 — Action 3: Waiting Time by Guest Type',
    fontweight='bold', fontsize=13, pad=14
)

ax10.set_xlabel('Guest Type')
ax10.set_ylabel('Average Waiting Time (minutes)')
ax10.tick_params(axis='x', rotation=0)

st.pyplot(fig10)

st.caption("Waiting Time by Guest Type")


# Figure 11
walkaway_by_type = (
    data[data['walk_away']]
    .groupby('Guest_type')
    .size()
)

fig11, ax11 = plt.subplots(figsize=(7,4))

walkaway_by_type.plot(
    kind='bar',
    ax=ax11
)

ax11.set_title(
    'Task 2 — Action 3: Walk-away Groups by Guest Type',
    fontweight='bold', fontsize=13, pad=14
)

ax11.set_xlabel('Guest Type')
ax11.set_ylabel('Number of Walk-away Groups')
ax11.tick_params(axis='x', rotation=0)

st.pyplot(fig11)

st.caption("Walk-away Groups by Guest Type")

st.markdown("**Key Findings**")

st.write("""
- In-house average waiting time: **28.0 minutes**
- Walk-in average waiting time: **38.4 minutes**
- Walk-away behavior was observed for both guest types
""")

st.markdown("**Verdict: Not a complete solution**")

st.write("""
Queue skipping redistributes waiting time rather than solving the
underlying seating-capacity constraint.

It may improve the experience for in-house guests, but it could worsen
the experience for walk-in guests who already have longer waiting times.
""")

st.markdown("---")

# =========================
# TASK 3
# =========================

st.header("Task 3 — Extra Recommendation")

st.subheader("Recommendation: Peak-period Seating Limit")

st.markdown("**Recommended Action**")

st.write("""
Apply a **90–120 minute seating limit only during peak periods**,
rather than reducing the seating time for all guests throughout the day.
""")

st.markdown("**Why This May Work**")

st.write("""
The data suggests that queue pressure is concentrated on specific
high-demand dates rather than occurring equally every day.

At the same time, only a small proportion of seated groups stayed
for very long periods.

A peak-period seating limit could therefore improve table turnover
when capacity is constrained, while avoiding unnecessary restrictions
during quieter periods.
""")

# Figure 12
fig12, ax12 = plt.subplots(figsize=(7,4))

ax12.bar(
    duration_thresholds['threshold'],
    duration_thresholds['percentage']
)

ax12.set_title(
    'Task 3 — Recommendation: Meal Duration Thresholds',
    fontweight='bold', fontsize=13, pad=14
)

ax12.set_xlabel('Meal Duration Threshold')
ax12.set_ylabel('Percentage of Seated Groups')

st.pyplot(fig12)

st.caption("Meal Duration Thresholds")


# Figure 13
fig13, ax13 = plt.subplots(figsize=(7,4))

ax13.bar(
    daily_summary['date'],
    daily_summary['queued_groups']
)

ax13.set_title(
    'Task 3 — Recommendation: Queue Pressure by Date',
    fontweight='bold', fontsize=13, pad=14
)

ax13.set_xlabel('Date')
ax13.set_ylabel('Number of Queued Groups')

st.pyplot(fig13)

st.caption("Queue Pressure by Date")

st.markdown("**Supporting Evidence**")

st.write("""
- Only about **7.4%** of seated groups stayed longer than 120 minutes
- Only about **1.1%** stayed longer than 180 minutes
- Queue pressure was concentrated mainly on **14/3 and 15/3**
- **15/3** had the highest recorded queue pressure with **54 queued groups**
""")

st.markdown("**Personal Reasoning**")

st.write("""
From a customer-experience perspective, a fixed short seating limit
throughout the entire breakfast period may feel unnecessarily restrictive.

Applying the limit only when queues are building creates a better balance
between operational efficiency, table turnover, and guest comfort.
""")

st.markdown(
    "**Recommendation Verdict: Most practical option among the proposed actions**"
)

st.markdown("---")

st.caption(
    "Busy Buffet Data Analysis — Hotel Amber 85 | Pirisa Kitichai"
)
