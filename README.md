# Nassau Candy Distributor — Shipping Route Efficiency Analysis

> Exploratory data analysis and interactive Streamlit dashboard for factory-to-customer shipping route efficiency at Nassau Candy Distributor.

> 📄 **Published Research:** [Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor: A Data-Driven Logistics Intelligence Study](https://www.aijfr.com/papers/2026/4/6846.pdf) — *Advanced International Journal for Research (AIJFR), Volume 7, Issue 4, July–August 2026*

> 📊 **Project Presentation:** [Nassau Candy Route Efficiency Analysis — Methodology & Findings](./Nassau_Candy_Route_Efficiency_Methodology.pptx)

> 🚀 **Live Dashboard:** [ncd-shipping-route-efficiency-dashboard.streamlit.app](https://ncd-shipping-route-efficiency-dashboard.streamlit.app/)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Research Publication](#research-publication)
- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Analytical Methodology](#analytical-methodology)
- [Dashboard Modules](#dashboard-modules)
- [Key Metrics & KPIs](#key-metrics--kpis)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Key Findings](#key-findings)
- [Recommendations](#recommendations)
- [Live Demo](#live-demo)
- [Presentation](#presentation)
- [Author](#author)

---

## Project Overview

Nassau Candy Distributor ships confectionery products from 5 regional factories to customers across the United States and Canada. Although the organisation maintains detailed order and shipment records, logistics decisions have historically been made without route-level efficiency intelligence — leaving questions about which factory-to-customer lanes are reliable, which experience frequent delays, and where geographic bottlenecks exist largely unanswered.

This project transforms raw order and shipment data into route-level operational intelligence through a full EDA pipeline and a five-tab interactive Streamlit dashboard.

---

## Research Publication

This project has been peer-reviewed and published in the **Advanced International Journal for Research (AIJFR)**.

| Field | Details |
|---|---|
| **Title** | Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor: A Data-Driven Logistics Intelligence Study |
| **Author** | Geetha S |
| **Journal** | Advanced International Journal for Research (AIJFR) |
| **E-ISSN** | 3048-7641 |
| **Impact Factor** | 9.11 |
| **Volume / Issue** | Volume 7, Issue 4 (July–August 2026) |
| **Full Paper** | [https://www.aijfr.com/papers/2026/4/6846.pdf](https://www.aijfr.com/papers/2026/4/6846.pdf) |

**Abstract:** This study undertakes an exploratory data analysis of 10,194 orders spanning January 2024 to December 2025, covering 5 factories, 4 customer regions, and 15 products across 3 product divisions. Shipping Lead Time is computed as the interval between order date and ship date, and an Efficiency Score, a Delay Rate, and a Route Volume metric are derived for each factory-region lane. Findings indicate that the network records a mean lead time of 5.22 days and an overall delay rate of 23.2% against a 7-day threshold, with Standard Class shipping responsible for the substantial majority of delay incidents despite carrying 60% of total order volume. Route-level analysis identifies Sugar Shack's connection to the Gulf region as the network's least efficient lane, while geographic analysis reveals that proximity to a factory does not reliably predict shipping speed. A Streamlit-based interactive dashboard was developed to operationalise these findings for ongoing monitoring, and the study concludes with 5 data-supported recommendations.

---

## Problem Statement

The organisation currently lacks visibility into:

- Which factory-to-customer routes are consistently efficient
- Which routes experience frequent delays
- How shipping performance varies by region, state, and shipping mode
- Where operational bottlenecks exist geographically

Without this visibility, logistics optimisation remains reactive rather than data-driven.

---

## Dataset

| Field | Description |
|---|---|
| Row ID / Order ID | Unique row and order identifiers |
| Order Date / Ship Date | Date the order was placed and the date it was shipped |
| Ship Mode | Shipping method (Same Day, First Class, Second Class, Standard Class) |
| Customer ID, City, State/Province, Postal Code | Customer geographic identifiers |
| Country/Region | Country (US or Canada) and customer region |
| Region | Sales region: Interior, Atlantic, Gulf, Pacific |
| Division, Product ID, Product Name | Product classification and identifiers |
| Sales, Units, Gross Profit, Cost | Order-level financial and quantity metrics |

**Dataset summary:**

- **Total orders:** 10,194
- **Factories:** 5 — Lot's O' Nuts (Arizona), Wicked Choccy's (Georgia), Sugar Shack (North Dakota), Secret Factory (Iowa), The Other Factory (Tennessee)
- **Customer regions:** 4 (Interior, Atlantic, Gulf, Pacific)
- **Unique products:** 15, across 3 divisions (Chocolate, Sugar, Other)
- **Order date range:** January 2024 – December 2025
- **Market coverage:** United States and Canada

> **Note on Ship Date reconstruction:** the source Ship Date column contained future-dated artefacts (2026–2030) producing implausible lead times. Ship Date was regenerated from Order Date using realistic, ship-mode-specific lead-time distributions (Same Day: mean 1 day; First Class: mean 3 days; Second Class: mean 5 days; Standard Class: mean 7 days) under a fixed random seed for reproducibility. Product-to-factory assignment follows a fixed mapping: Lot's O' Nuts and Wicked Choccy's exclusively produce Chocolate division items, Sugar Shack is the principal producer of Sugar division items, and Secret Factory / The Other Factory supplement the Sugar and Other divisions.

---

## Project Structure

```
Nassau-Candy-Shipping-Route-Efficiency-Analysis/
│
├── Nassau_Candy_Distributor.csv      # Source dataset
├── nassau_candy_eda.ipynb            # Full exploratory data analysis notebook
├── nassau_candy_dashboard.py         # Streamlit dashboard (single-file, 5-tab app)
├── eda_outputs/                      # Exported charts/tables from the EDA notebook
└── requirements.txt                  # Python dependencies
```

---

## Analytical Methodology

### 1. Data Cleaning & Validation
Order Date and Ship Date fields were parsed and validated for consistency, geographic fields were standardised, and the dataset was checked for missing values — none were found across the 10,194 records.

### 2. Feature Engineering
Shipping Lead Time was computed in days as Ship Date minus Order Date. Each shipment was flagged as delayed if its lead time exceeded 7 days, the fixed delivery-window benchmark used throughout the analysis. Shipments were grouped by factory-to-region and factory-to-state/province pairings, and by ship mode.

### 3. Route Definition & Aggregation
Each route is defined as a Factory-to-Customer-Region pairing, yielding 20 distinct factory-region lanes. For each route, total shipment volume, average lead time, and lead-time standard deviation were calculated.

### 4. Efficiency Benchmarking
Routes were rank-ordered by average lead time, and an Efficiency Score was computed on a 0-to-100 scale, normalised such that a score of 100 corresponds to the network's shortest average lead time. Top 10 and bottom 10 routes were identified.

### 5. Geographic Bottleneck Analysis
State- and province-level average lead time and delay rate were computed to identify congestion-prone states. A distance-based proximity analysis compared each state's geographically nearest factory against the factory that actually fulfilled the majority of its orders.

---

## Dashboard Modules

The Streamlit dashboard consists of five interactive tabs, all sharing a unified sidebar filter system (Date Range, Region, Ship Mode, Factory, Delay Threshold).

| Tab | Description |
|---|---|
| 📊 Route Efficiency | Route Performance Leaderboard heatmap; Efficiency Score vs Shipment Volume scatter; Top 10/Bottom 10 Route Leaderboard; Lead Time Variability by Route; Lead Time vs Profit Margin scatter; Distance vs Lead Time Correlation; Strategic Assessment cards |
| 🗺️ Geographic Coverage | Shipping efficiency choropleth; Region Metrics Summary; Factory Shipment Volume Breakdown; Factory Network map; Factory Reach & Expansion Indicators; Underserved Regions; Top 10 Bottleneck States; High Volume + High Delay States; Customer Segmentation by Order Value; Geographic Network Assessment cards |
| 🚚 Ship Mode Analysis | Ship Mode Performance Comparison; Lead Time Variability & Distribution by Ship Mode; Ship Mode × Region and × Factory heatmaps; Ship Mode Risk & Efficiency Breakdown |
| 🏭 Factory Intelligence | Product-Level Lead Time; Factory Revenue & Profit; Factory Reach Index; Factory Clustering Risk heatmap; Coast Exposure to Central Factory Cluster; Factory Network Assessment cards |
| 📈 Trends & Deep-Dive | Monthly Shipping Trends; Cross-Variable Correlation Matrix; 3-Month Shipment Volume Forecast; Order-Level Shipment Timeline; Division Performance Over Time |

### Dashboard Sidebar Filters
All five tabs respond to five unified filters:
- **Order Date Range**
- **Region**
- **Ship Mode**
- **Factory**
- **Delay Threshold** — configurable slider (default 7 days)

---

## Key Metrics & KPIs

| KPI | Formula | Purpose |
|---|---|---|
| Shipping Lead Time | Ship Date − Order Date | Core unit of measure for every downstream KPI |
| Average Lead Time | Mean shipping duration per route, factory, or ship mode | Primary efficiency benchmark |
| Route Volume | Number of orders per factory-region route | Identifies high-traffic lanes warranting priority |
| Delay Frequency | % of shipments exceeding the 7-day threshold | Direct measure of operational risk per route/mode |
| Route Efficiency Score | Normalised lead-time performance, 0 to 100 | Enables fair cross-route comparison at any volume |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Core Language | Python 3.x |
| Data Wrangling | Pandas |
| Numerical Computing | NumPy |
| Visualisation | Plotly (Express, Graph Objects, Subplots) |
| Dashboard Framework | Streamlit |
| Exploratory Analysis | Jupyter Notebook |

---

## Getting Started

### Prerequisites

Python 3.8 or higher is required.

### Installation

```bash
# Clone the repository
git clone https://github.com/GeethaS87/Nassau-Candy-Shipping-Route-Efficiency-Analysis.git
cd Nassau-Candy-Shipping-Route-Efficiency-Analysis

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run nassau_candy_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`.

### Running the EDA Notebook

```bash
jupyter notebook nassau_candy_eda.ipynb
```

### Requirements

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.26.0
plotly>=5.18.0
```

---

## Key Findings

1. **Standard Class is the dominant driver of network-wide delay.** It carries 60% of total shipment volume (6,120 shipments) and records a 36.9% delay rate — its 6.53-day mean lead time sits close enough to the 7-day threshold that ordinary variability pushes a large share of orders into delay. Same Day and First Class, by contrast, record zero recorded delays.
2. **Sugar Shack is the network's clearest outlier.** Despite accounting for only 0.3% of total network shipment volume, it records both the longest average lead time (6.09 days) and the highest delay rate (33%) of any factory, and serves the fewest states in the network (15).
3. **Sugar Shack → Gulf is the single highest-risk route.** At 8.25 days average lead time and a 50% delay rate, it is also the most variable lane (std. dev. ≈ 5.91 days) — a doubly elevated reliability risk.
4. **Geographic proximity does not reliably predict shipping speed.** Distance to the nearest factory shows only a weak correlation with average lead time (r ≈ 0.16), and in 54% of comparable states, the non-nearest factory fulfils orders at the same speed or faster than the geographically nearest one.
5. **8 states are congestion hotspots** — combining high shipment volume with elevated delay rates — led by Texas (985 shipments, 26% delay), Pennsylvania (587 shipments, 25% delay), and Washington (506 shipments, 25% delay).
6. **Regional performance is uniform; factory and mode performance are not.** Average lead times across Pacific, Gulf, Atlantic, and Interior range narrowly between 5.15 and 5.34 days, indicating that shipping performance is driven primarily by ship-mode composition rather than geography itself.
7. **Order value is not a driver of fulfilment speed.** Lead time and delay rate are effectively flat across High, Medium, and Low value order tiers.
8. **Lead time is financially uncorrelated.** Lead time records a near-zero correlation (r ≈ 0.02) with sales, units, gross profit, and cost, confirming that shipping speed is governed by operational factors, not order value.

---

## Recommendations

1. **Address Standard Class delay concentration** as the primary network-wide risk — review order-to-mode assignment logic to shift eligible orders to Second or First Class.
2. **Prioritise Sugar Shack's Standard Class performance** for operational review, with its Gulf connection as the top priority and its Atlantic connection as secondary.
3. **Investigate the unrealised proximity advantage** at nearest factories via a factory-level processing audit.
4. **Target congestion hotspot states** for operational review, led by Texas, Pennsylvania, and Washington.
5. **Evaluate factory capability expansion** to address concentration risk, given Lot's O' Nuts and Wicked Choccy's dominant share of Chocolate-division shipments and the central-US clustering of the remaining three factories.

---

## Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ncd-shipping-route-efficiency-dashboard.streamlit.app/)

> Click the badge above or visit: [https://ncd-shipping-route-efficiency-dashboard.streamlit.app/](https://ncd-shipping-route-efficiency-dashboard.streamlit.app/)

---

## Presentation

📊 The project methodology, analytical approach, and key findings are documented in the accompanying PowerPoint presentation:

**[Nassau Candy Route Efficiency Analysis — Methodology & Findings](./Nassau_Candy_Route_Efficiency_Methodology.pptx)**

The presentation covers:
- Project background and problem statement
- Analytical methodology and KPI framework
- Ship mode, route, factory, and geographic findings
- Dashboard architecture walkthrough
- Recommendations and conclusion

---

## Author

**Geetha S**
- GitHub: [@GeehaS87](https://github.com/GeehaS87)
- Published: [AIJFR Volume 7, Issue 4 (July–August 2026)](https://www.aijfr.com/papers/2026/4/6846.pdf)

---

*This project was developed as part of a data analytics internship focused on factory-to-customer logistics intelligence for a national confectionery distributor. The findings and methodology have been peer-reviewed and published in the Advanced International Journal for Research (AIJFR), E-ISSN: 3048-7641.*
