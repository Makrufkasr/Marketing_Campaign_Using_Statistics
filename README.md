# Fast-Food Marketing Campaign Optimization via A/B Testing & Financial ROI Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![SciPy](https://img.shields.io/badge/SciPy-Statistical%20Testing-8CAAE6.svg)](https://scipy.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Makrufkasr/Marketing_Campaign_Using_Statistics/blob/main/Marketing_Campaigns_Using_Statistics_.ipynb)

---

## 1. Problem Statement & Business Context

### Background & Business Problem
A nationwide fast-food chain planned to introduce a new menu item across its store network. In a highly competitive retail food market, launching a new product without empirical marketing data poses significant financial risks, including misallocated promotional budgets, suboptimal customer reach, and lost revenue opportunities.

To determine the most commercially viable marketing strategy, management designed a controlled A/B/n experiment testing **three distinct promotional campaigns (Campaign 1, Campaign 2, and Campaign 3)** across randomly selected market locations.

### Core Business Questions
1. **Primary Decision**: Which promotional campaign generates the greatest statistical and commercial lift in sales?
2. **Market Segmentation**: Does campaign effectiveness vary across different market tiers (*Small*, *Medium*, *Large*) or store age profiles?
3. **Financial Impact**: What is the projected net profit lift and Return on Marketing Investment (ROMI) under full-scale national rollout?

### Experiment Scope & Dataset Parameters
- **Locations Tested**: 137 individual store locations
- **Test Duration**: 4 consecutive weeks per location (total 548 store-week observations)
- **Market Segments**: Small (60 records), Medium (320 records), and Large (168 records)
- **Primary KPI**: Weekly Sales Revenue (recorded in thousands of USD, `$k`)

### Methodology & Analytical Framework
1. **A/B/n Randomized Controlled Trial (RCT) Design**:
   - Random allocation of 137 store branches into 3 independent treatment cohorts (Promotion 1: 172 observations, Promotion 2: 188 observations, Promotion 3: 188 observations).
2. **Data Cleansing & Sanity Check**:
   - Verification of zero missing values, zero duplicated records, and validation of feature data types.
   - Verification of treatment balance across *Market Size* and *Age of Store* to prevent selection bias.
3. **Exploratory Data Analysis (EDA)**:
   - Distributional analysis of sales variation using box plots and mean comparisons across campaign variations and market tiers.
4. **Inferential Hypothesis Testing**:
   - **Welch’s Two-Sample Independent t-Test** (`equal_var=False`): Formulated with $H_0: \mu_A = \mu_B$ vs $H_1: \mu_A \neq \mu_B$ at significance threshold $\alpha = 0.05$ to account for unequal group variances.
5. **Business Impact & Financial Modeling**:
   - Conversion of statistical sales lift into financial projections across 100 stores over 1 Quarter (12 weeks), accounting for a 60% gross profit margin, campaign expenditures, net profit lift, and Return on Marketing Investment (ROMI).

---

## 2. Executive Summary & Key Findings

1. **Campaign 1 and Campaign 3 Delivered Superior Sales Performance**:
   - Campaign 1 achieved the highest average weekly sales at **$58.10k** per store.
   - Campaign 3 followed closely with an average of **$55.36k** per store.
2. **Campaign 2 Significantly Underperformed**:
   - Campaign 2 generated only **$47.33k** per store-week, lagging behind the winning campaigns.
3. **Hypothesis Testing Results (Welch's Two-Sample t-Test, $\alpha = 0.05$)**:
   - **Campaign 1 vs Campaign 2**: +22.8% sales lift ($p < 0.001$), statistically significant.
   - **Campaign 3 vs Campaign 2**: +17.0% sales lift ($p < 0.001$), statistically significant.
   - **Campaign 1 vs Campaign 3**: Difference of $2.73k/week was not statistically significant ($p = 0.121$).

---

## 3. Visualizations & Statistical Evaluation

![Sales Distribution](assets/sales_distribution.png)

### Summary of Experiment Results

| Campaign Group | Sample Size ($n$) | Avg Sales / Week ($'000) | Std Deviation | vs Campaign 2 (Sales Lift) | Statistical Significance ($\alpha = 0.05$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Promotion 1** | 172 | **$58.10k** | 16.55 | **+22.8%** | Significant ($p = 0.000$) |
| **Promotion 2** | 188 | **$47.33k** | 15.11 | Baseline | Baseline |
| **Promotion 3** | 188 | **$55.36k** | 16.77 | **+17.0%** | Significant ($p = 0.000$) |

> **Head-to-Head Comparison (Promotion 1 vs Promotion 3)**: $t = 1.556$, $p = 0.121$. The null hypothesis cannot be rejected; both campaigns are statistically comparable in revenue generation.

---

## 4. Market Size Performance Breakdown

![Market Size Performance](assets/market_size_performance.png)

- **Large Market Tier**: Demonstrated the strongest revenue response, with Campaign 1 averaging **$72.8k/wk** and Campaign 3 averaging **$77.2k/wk**.
- **Medium & Small Market Tiers**: Campaign 1 and Campaign 3 consistently outperformed Campaign 2 across all store maturity brackets.

---

## 5. Business Impact & Financial ROI Simulation

To demonstrate real-world financial implications, a commercial rollout simulation was conducted across **100 stores** over **1 Quarter (12 weeks = 1,200 store-weeks)**:

![Business Impact Simulation](assets/business_impact.png)

### Commercial Simulation Assumptions
- **Rollout Scale**: 100 Stores
- **Campaign Horizon**: 12 Weeks (1 Quarter)
- **Menu Gross Profit Margin**: 60%
- **Estimated Marketing Investment**:
  - Campaign 1 (Omnichannel Media & Broad Digital Reach): $1,200,000 ($1.2M)
  - Campaign 2 (Standard Baseline Promotion): $400,000 ($0.4M)
  - Campaign 3 (In-Store Merchandising & Localized Digital): $600,000 ($0.6M)

### Financial Model Projection (1 Quarter)

| Financial Metric | Campaign 2 (Baseline) | Campaign 3 | Campaign 1 (Winner) | Delta (C1 vs Baseline) |
| :--- | :---: | :---: | :---: | :---: |
| **Average Weekly Sales per Store** | $47.33k | $55.36k | **$58.10k** | **+$10.77k (+22.8%)** |
| **Total Gross Revenue** | $56.80M | $66.43M | **$69.72M** | **+$12.92M** |
| **Gross Profit (60% Margin)** | $34.08M | $39.86M | **$41.83M** | **+$7.75M** |
| **Marketing Campaign Expenditure** | $0.40M | $0.60M | **$1.20M** | +$0.80M |
| **Net Profit Contribution** | $33.68M | $39.26M | **$40.63M** | **+$6.95M** |
| **Incremental ROMI (vs Baseline)** | - | **9.63x** | **6.46x** | - |

---

## 6. Strategic Recommendations & Decision Matrix

| Priority | Action Item | Business Rationale |
| :---: | :--- | :--- |
| **1** | **Immediately Decommission Campaign 2** | Eliminates an ongoing opportunity loss of **~$10.77k per store-week** compared to Campaign 1. |
| **2** | **Profit Maximization Scenario: Deploy Campaign 1** | Generates the highest absolute bottom-line expansion (**+$6.95M net profit lift per quarter**) under full-scale rollout. |
| **3** | **Budget-Constrained Scenario: Deploy Campaign 3** | Provides superior capital efficiency with a **9.63x ROMI** while requiring 50% less marketing expenditure than Campaign 1. |
| **4** | **Prioritize Large Market Branches** | Target the highest concentration of marketing spend in Large Market locations to capture the highest sales response. |

---

## Author
- **Makruf Kasr**
- [LinkedIn Profile](https://www.linkedin.com/) • [GitHub Repository](https://github.com/Makrufkasr/Marketing_Campaign_Using_Statistics)
