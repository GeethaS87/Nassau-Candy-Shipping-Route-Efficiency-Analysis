"""
Nassau Candy Distributor — Shipping Route Efficiency Dashboard
==============================================================
Run:  streamlit run nassau_candy_dashboard.py
Deps: pip install streamlit pandas numpy plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy | Route Intelligence",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] { background: #0f1117; border-right: 1px solid #2a2a3a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #1a1f35 0%, #1e2640 100%);
    border: 1px solid #2d3561;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
}
.kpi-value { font-size: 2.1rem; font-weight: 700; color: #f59e0b; margin: 0; }
.kpi-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;
             letter-spacing: 1px; margin-top: 4px; }
.kpi-delta { font-size: 0.85rem; margin-top: 6px; }

/* Section headers */
.section-header {
    background: linear-gradient(90deg, #f59e0b22 0%, transparent 100%);
    border-left: 3px solid #f59e0b;
    padding: 8px 16px;
    margin: 24px 0 16px 0;
    border-radius: 0 6px 6px 0;
    font-weight: 600;
    font-size: 1.05rem;
    color: #1a1a2e;
}
/* Main content — force dark text everywhere outside sidebar,
   but NOT inside metric cards (value/label have their own rules below) */
.main .stMarkdown, .main p, .main label, .main .stText { color: #111111 !important; }
.main span:not([data-testid="stMetricValue"] span):not([data-testid="stMetricLabel"] span),
.main div:not([data-testid="stMetric"]):not([data-testid="stMetricValue"]):not([data-testid="stMetricLabel"]):not([data-testid="stMetricDelta"]) > p { color: #111111; }

/* Selectbox selected value & dropdown items */
.stSelectbox div[data-baseweb="select"] > div,
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox input { color: #111111 !important; font-weight: 500 !important; }

/* Dropdown open list */
[data-baseweb="menu"] li,
[data-baseweb="menu"] li span,
[data-baseweb="menu"] li div,
[data-baseweb="popover"] li,
[data-baseweb="popover"] span,
[data-baseweb="popover"] div { color: #111111 !important; }

/* Cards & table inline HTML text — st.markdown rendered divs */
.main [data-testid="stMarkdownContainer"] div,
.main [data-testid="stMarkdownContainer"] span,
.main [data-testid="stMarkdownContainer"] p { color: #111111 !important; }

/* Metric numbers & labels */
/* KPI metric colors handled by specific rules below */

/* General text in main area */
.block-container p, .block-container span,
.block-container div, .block-container label { color: #111111; }
/* Sidebar selectbox & input text visibility */
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background-color: #1e2640 !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stSelectbox span {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stSelectbox svg {
    fill: #e2e8f0 !important;
}
[data-testid="stSidebar"] input {
    color: #e2e8f0 !important;
    background-color: #1e2640 !important;
}
[data-testid="stSidebar"] .stDateInput > div > div {
    background-color: #1e2640 !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stDateInput input {
    background-color: #1e2640 !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] [data-baseweb="base-input"] {
    background-color: #1e2640 !important;
}

/* Reset (↺) buttons — subtle always, highlight on hover */
[data-testid="stSidebar"] div[data-testid="stButton"] button {
    background: #1e2640 !important;
    color: #6a7aaa !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 6px !important;
    box-shadow: none !important;
    font-size: 0.85rem !important;
    transition: background 0.2s, color 0.2s, border-color 0.2s !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
    background: #2d3561 !important;
    color: #e2e8f0 !important;
    border-color: rgba(255,255,255,0.45) !important;
}

/* Metric override */
[data-testid="stMetric"] {
    background: #1a1f35;
    border: 1px solid #2d3561;
    border-radius: 10px;
    padding: 14px !important;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * { color: #94a3b8 !important; font-size: 0.78rem !important; }
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] div,
[data-testid="stMetricValue"] span { color: #f59e0b !important; font-size: 1.6rem !important; }
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * { color: #94a3b8 !important; }

/* Tab labels */
[data-testid="stTabs"] button p { font-size: 1rem !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

# ── Lookup tables ─────────────────────────────────────────────────────────────
PRODUCT_FACTORY = {
    "Wonka Bar - Nutty Crunch Surprise":   "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows":           "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious":      "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate":          "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel":   "Wicked Choccy's",
    "Laffy Taffy":                         "Sugar Shack",
    "SweeTARTS":                           "Sugar Shack",
    "Nerds":                               "Sugar Shack",
    "Fun Dip":                             "Sugar Shack",
    "Fizzy Lifting Drinks":                "Sugar Shack",
    "Everlasting Gobstopper":              "Secret Factory",
    "Lickable Wallpaper":                  "Secret Factory",
    "Wonka Gum":                           "Secret Factory",
    "Hair Toffee":                         "The Other Factory",
    "Kazookles":                           "The Other Factory",
}

FACTORY_COORDS = {
    "Lot's O' Nuts":     {"lat": 32.881893, "lon": -111.768036, "state": "AZ"},
    "Wicked Choccy's":   {"lat": 32.076176, "lon":  -81.088371, "state": "GA"},
    "Sugar Shack":       {"lat": 44.500, "lon": -93.100, "state": "MN"},
    "Secret Factory":    {"lat": 41.446333, "lon":  -90.565487, "state": "IL"},
    "The Other Factory": {"lat": 35.117500, "lon":  -89.971107, "state": "TN"},
}

STATE_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC",
}

CANADA_ABBREV = {
    "Ontario": "ON", "Quebec": "QC", "Alberta": "AB",
    "British Columbia": "BC", "Manitoba": "MB",
    "Prince Edward Island": "PE", "New Brunswick": "NB",
    "Nova Scotia": "NS", "Newfoundland and Labrador": "NL",
    "Saskatchewan": "SK",
}
STATE_ABBREV.update(CANADA_ABBREV)

# US state centroids for proximity analysis
STATE_CENTROIDS = {
    "Alabama": (32.8, -86.8), "Alaska": (64.2, -153.4), "Arizona": (34.3, -111.1),
    "Arkansas": (34.8, -92.2), "California": (37.2, -119.5), "Colorado": (39.0, -105.5),
    "Connecticut": (41.6, -72.7), "Delaware": (39.0, -75.5), "Florida": (28.6, -82.4),
    "Georgia": (32.7, -83.4), "Hawaii": (20.3, -156.4), "Idaho": (44.4, -114.6),
    "Illinois": (40.0, -89.2), "Indiana": (39.9, -86.3), "Iowa": (42.1, -93.5),
    "Kansas": (38.5, -98.4), "Kentucky": (37.5, -85.3), "Louisiana": (31.2, -91.8),
    "Maine": (45.4, -69.2), "Maryland": (39.1, -76.8), "Massachusetts": (42.3, -71.8),
    "Michigan": (44.3, -85.4), "Minnesota": (46.4, -93.1), "Mississippi": (32.7, -89.7),
    "Missouri": (38.4, -92.5), "Montana": (47.0, -110.5), "Nebraska": (41.5, -99.9),
    "Nevada": (39.3, -116.6), "New Hampshire": (43.7, -71.6), "New Jersey": (40.1, -74.5),
    "New Mexico": (34.4, -106.1), "New York": (42.9, -75.6), "North Carolina": (35.5, -79.4),
    "North Dakota": (47.5, -100.5), "Ohio": (40.4, -82.7), "Oklahoma": (35.6, -97.5),
    "Oregon": (44.6, -122.1), "Pennsylvania": (40.9, -77.8), "Rhode Island": (41.7, -71.5),
    "South Carolina": (33.9, -80.9), "South Dakota": (44.4, -100.2), "Tennessee": (35.9, -86.4),
    "Texas": (31.5, -99.3), "Utah": (39.3, -111.1), "Vermont": (44.1, -72.7),
    "Virginia": (37.5, -78.9), "Washington": (47.4, -120.5), "West Virginia": (38.6, -80.6),
    "Wisconsin": (44.3, -89.8), "Wyoming": (43.0, -107.6), "District of Columbia": (38.9, -77.0),
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", family="Space Grotesk"),
    colorway=["#f59e0b", "#38bdf8", "#34d399", "#f87171", "#a78bfa", "#fb923c"],
)

# ── Data loader ───────────────────────────────────────────────────────────────
SHIP_MODE_PARAMS = {
    "Same Day":       (1, 0.3),
    "First Class":    (3, 1.0),
    "Second Class":   (5, 2.0),
    "Standard Class": (7, 3.0),
}

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)

    # The original Ship Date contains future-dated values (2026–2030) that are a
    # synthetic data artefact producing lead times of 900–1,600 days.
    # Ship Date is regenerated from Order Date using ship-mode-specific lead time
    # distributions matching EDA Cell 8 (fixed seed=42 for reproducibility).
    rng = np.random.default_rng(seed=42)

    def _generate_lead_time(ship_mode):
        mean, std = SHIP_MODE_PARAMS.get(ship_mode, (7, 3.0))
        return max(1, int(rng.normal(mean, std)))

    df["Lead Time"] = df["Ship Mode"].apply(_generate_lead_time)
    df["Ship Date"] = df["Order Date"] + pd.to_timedelta(df["Lead Time"], unit="D")

    df["Factory"]     = df["Product Name"].map(PRODUCT_FACTORY)
    df["Route"]       = df["Factory"] + " → " + df["State/Province"]
    df["RouteRegion"] = df["Factory"] + " → " + df["Region"]
    df["Month"]       = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"]        = df["Order Date"].dt.year
    df["State Code"]  = df["State/Province"].map(STATE_ABBREV)
    return df

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍬 Nassau Candy")
    st.markdown("<h3 style='margin-top:-0.8rem; padding-left:2.1rem;'>Route Intelligence</h3>", unsafe_allow_html=True)
    st.divider()

    import pathlib
    _script_dir = pathlib.Path(__file__).parent
    _candidates = (
        list(_script_dir.glob("Nassau Candy Distributor.csv")) +
        list(_script_dir.glob("Nassau_Candy_Distributor.csv")) +
        list(_script_dir.glob("*.csv"))
    )
    _default_path = str(_candidates[0]) if _candidates else "Nassau Candy Distributor.csv"

    DATA_PATH = st.text_input(
        "CSV file path",
        value=_default_path,
        help="Path to the Nassau Candy CSV file",
    )

    try:
        df_raw = load_data(DATA_PATH)
    except FileNotFoundError:
        st.error("CSV not found. Update the file path above.")
        st.stop()

    st.session_state.year_span = f"{df_raw['Order Date'].dt.year.min()}–{df_raw['Order Date'].dt.year.max()}"
    st.success(f"✓ {len(df_raw):,} orders loaded")
    st.divider()

    # ── Filters ───────────────────────────────────────────────────────────────
    st.markdown("<h3 style='margin-top:-1.5rem;'>🔧 Filters</h3>", unsafe_allow_html=True)

    min_date = df_raw["Order Date"].min().date()
    max_date = df_raw["Order Date"].max().date()

    # Key counters for per-filter reset (key increment forces widget re-render)
    for k, v in [("_date_key", 0), ("_region_key", 0), ("_ship_mode_key", 0), ("_factory_key", 0),
                 ("_threshold_key", 0), ("_timeline_key", 0)]:
        if k not in st.session_state:
            st.session_state[k] = v

    # ── Date Range ────────────────────────────────────────────────────────────
    _date_col, _date_reset = st.columns([4, 1])
    with _date_col:
        date_range = st.date_input(
            "Order Date Range",
            value=(min_date, max_date),
            key=f"filter_date_{st.session_state['_date_key']}",
        )
    with _date_reset:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("↺", key="reset_date"):
            st.session_state["_date_key"] += 1
            st.rerun()

    # Date warning in sidebar
    _sel_start, _sel_end = (date_range[0], date_range[1]) if len(date_range) == 2 else (min_date, max_date)
    _date_valid = _sel_start >= min_date and _sel_end <= max_date and _sel_start <= _sel_end
    _no_data_in_range = _date_valid and df_raw[
        (df_raw["Order Date"].dt.date >= _sel_start) &
        (df_raw["Order Date"].dt.date <= _sel_end)
    ].empty
    _warn_style = "background:#2a1a00;border:1px solid #f4a444;border-radius:6px;padding:8px 12px;color:#f4a444;font-size:0.75rem;margin-top:4px;"
    _partial = _sel_end > max_date and _sel_start <= max_date
    _before_start = _sel_end < min_date
    _after_end = _sel_start > max_date
    if _before_start or _after_end:
        st.markdown(f"<div style='{_warn_style}'>⚠️ No data available for this range. Data exists from {min_date} to {max_date}.</div>", unsafe_allow_html=True)
    elif _partial:
        st.markdown(f"<div style='{_warn_style}'>⚠️ No data after {max_date}. Showing up to {max_date}.</div>", unsafe_allow_html=True)
    elif _no_data_in_range:
        st.markdown(f"<div style='{_warn_style}'>⚠️ No data for this range. Data exists from {min_date} to {max_date}.</div>", unsafe_allow_html=True)

    region_options    = ["All"] + sorted(df_raw["Region"].unique().tolist())
    ship_mode_options = ["All"] + sorted(df_raw["Ship Mode"].unique().tolist())
    factory_options   = ["All"] + sorted(df_raw["Factory"].unique().tolist())

    # ── Region ────────────────────────────────────────────────────────────────
    _reg_col, _reg_reset = st.columns([4, 1])
    with _reg_col:
        region_sel = st.selectbox("Region", region_options,
                                  key=f"filter_region_{st.session_state['_region_key']}")
    with _reg_reset:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("↺", key="reset_region", help="Reset region filter"):
            st.session_state["_region_key"] += 1
            st.rerun()
    if st.session_state.get("_prev_region_sel") not in (None, "All") and region_sel == "All":
        st.session_state["_prev_region_sel"] = region_sel
        st.rerun()
    st.session_state["_prev_region_sel"] = region_sel

    # ── Ship Mode ─────────────────────────────────────────────────────────────
    _sm_col, _sm_reset = st.columns([4, 1])
    with _sm_col:
        ship_mode_sel = st.selectbox("Ship Mode", ship_mode_options,
                                     key=f"filter_ship_mode_{st.session_state['_ship_mode_key']}")
    with _sm_reset:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("↺", key="reset_ship_mode", help="Reset ship mode filter"):
            st.session_state["_ship_mode_key"] += 1
            st.rerun()
    if st.session_state.get("_prev_ship_mode_sel") not in (None, "All") and ship_mode_sel == "All":
        st.session_state["_prev_ship_mode_sel"] = ship_mode_sel
        st.rerun()
    st.session_state["_prev_ship_mode_sel"] = ship_mode_sel

    # ── Factory ───────────────────────────────────────────────────────────────
    _fac_col, _fac_reset = st.columns([4, 1])
    with _fac_col:
        factory_sel = st.selectbox("Factory", factory_options,
                                   key=f"filter_factory_{st.session_state['_factory_key']}")
    with _fac_reset:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("↺", key="reset_factory", help="Reset factory filter"):
            st.session_state["_factory_key"] += 1
            st.rerun()

    regions    = list(df_raw["Region"].unique())    if region_sel    == "All" else [region_sel]
    ship_modes = list(df_raw["Ship Mode"].unique()) if ship_mode_sel == "All" else [ship_mode_sel]
    factories  = list(df_raw["Factory"].unique())   if factory_sel   == "All" else [factory_sel]

    # ── Delay Threshold ───────────────────────────────────────────────────────
    _thr_col, _thr_reset = st.columns([4, 1])
    with _thr_col:
        delay_threshold = st.slider(
            "Delay Threshold (days)",
            min_value=1, max_value=30, value=7,
            key=f"filter_threshold_{st.session_state['_threshold_key']}",
            help="Shipments exceeding this are counted as 'delayed'",
        )
    with _thr_reset:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("↺", key="reset_threshold", help="Reset delay threshold"):
            st.session_state["_threshold_key"] += 1
            st.rerun()

    # ── Download All Reports — button only, zip built after data is ready ──────
    st.markdown("""
        <style>
        [data-testid="stSidebar"] [data-testid="stDownloadButton"] button {
            background-color: #1a1f35 !important;
            color: #e2e8f0 !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            opacity: 1 !important;
        }
        [data-testid="stSidebar"] [data-testid="stDownloadButton"] button:hover {
            background-color: #2d3561 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)
    _dl_all_reports_slot = st.empty()

    st.divider()

    if "year_span" in st.session_state:
        st.caption(f"Nassau Candy Distributor · {st.session_state.year_span}")
    else:
        st.caption("Nassau Candy Distributor")

# ── Apply filters ─────────────────────────────────────────────────────────────
start_date, end_date = (date_range[0], date_range[1]) if len(date_range) == 2 else (min_date, max_date)

_WARN_BANNER = "<div style='background:#fffde7;border:1px solid #f4a444;border-radius:6px;padding:12px 18px;color:#7a4f00;font-size:0.95rem;margin-bottom:1rem;'>⚠️ &nbsp; {msg}</div>"

# Show main page warning if date range is invalid (even if df is not empty)
if start_date > max_date or end_date < min_date:
    st.markdown(_WARN_BANNER.format(msg="No records found for the selected criteria. Consider revising the filter selections."), unsafe_allow_html=True)
    st.stop()
df = df_raw[
    (df_raw["Order Date"].dt.date >= start_date) &
    (df_raw["Order Date"].dt.date <= end_date)  &
    (df_raw["Region"].isin(regions))            &
    (df_raw["Ship Mode"].isin(ship_modes))      &
    (df_raw["Factory"].isin(factories))
].copy()

df["Is Delayed"] = df["Lead Time"] > delay_threshold

# Used for Factory Reach & Expansion Indicators — applies Date & Region filters only,
# unaffected by Ship Mode / Factory selections
df_dd = df_raw[
    (df_raw["Order Date"].dt.date >= start_date) &
    (df_raw["Order Date"].dt.date <= end_date)  &
    (df_raw["Region"].isin(regions))
].copy()

if df.empty:
    st.markdown(_WARN_BANNER.format(msg="No records found for the selected criteria. Consider revising the filter selections."), unsafe_allow_html=True)
    st.stop()

# ── Aggregations ───────────────────────────────────────────────────────────────
route_stats = (
    df.groupby("RouteRegion")
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
        Std_Dev=("Lead Time", "std"),
        Avg_Sales=("Sales", "mean"),
        Avg_Profit=("Gross Profit", "mean"),
    )
    .reset_index()
    .sort_values("Avg_Lead_Time")
)
route_stats["Std_Dev"] = route_stats["Std_Dev"].fillna(0).round(2)
lt_min = route_stats["Avg_Lead_Time"].min()
lt_max = route_stats["Avg_Lead_Time"].max()
route_stats["Efficiency_Score"] = (
    100 * (lt_max - route_stats["Avg_Lead_Time"]) / (lt_max - lt_min + 1e-9)
).round(1)

state_stats = (
    df.groupby(["State/Province", "State Code"])
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
        Total_Sales=("Sales", "sum"),
    )
    .reset_index()
)

# Unfiltered version — used to fix color-scale ranges so they don't shift with filters
df_raw["Is Delayed"] = df_raw["Lead Time"] > delay_threshold

# Unfiltered route stats — used by Top10/Bottom10 leaderboard so it stays
# constant regardless of Region / Ship Mode / Factory filter selections.
route_stats_all = (
    df_raw.groupby("RouteRegion")
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
        Std_Dev=("Lead Time", "std"),
        Avg_Sales=("Sales", "mean"),
        Avg_Profit=("Gross Profit", "mean"),
    )
    .reset_index()
    .sort_values("Avg_Lead_Time")
)
route_stats_all["Std_Dev"] = route_stats_all["Std_Dev"].fillna(0).round(2)
_ra_lt_min = route_stats_all["Avg_Lead_Time"].min()
_ra_lt_max = route_stats_all["Avg_Lead_Time"].max()
route_stats_all["Efficiency_Score"] = (
    100 * (_ra_lt_max - route_stats_all["Avg_Lead_Time"]) / (_ra_lt_max - _ra_lt_min + 1e-9)
).round(1)

state_stats_all = (
    df_raw.groupby(["State/Province", "State Code"])
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
        Total_Sales=("Sales", "sum"),
    )
    .reset_index()
)

# Region-only filtered version — used for Bottleneck / High Volume tables,
# unaffected by Ship Mode / Factory selections
df_dd["Is Delayed"] = df_dd["Lead Time"] > delay_threshold
state_stats_region = (
    df_dd.groupby(["State/Province", "State Code"])
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
        Total_Sales=("Sales", "sum"),
    )
    .reset_index()
)

ship_stats = (
    df.groupby("Ship Mode")
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
        Std_Lead_Time=("Lead Time", "std"),
    )
    .reset_index()
    .sort_values("Avg_Lead_Time")
)

factory_stats = (
    df.groupby("Factory")
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
    )
    .reset_index()
    .sort_values("Avg_Lead_Time")
)

# Unfiltered version — used to keep bubble size/color stable when a factory filter is applied
factory_stats_all = (
    df_raw.groupby("Factory")
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
    )
    .reset_index()
    .sort_values("Avg_Lead_Time")
)

monthly = (
    df.groupby("Month")
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
    )
    .reset_index()
)

# ── Full-portfolio factory assessment data (for assessment cards) ──────────────
_product_stats_all = (
    df_raw.groupby(["Product Name", "Factory"])
    .agg(Avg_Lead_Time=("Lead Time", "mean"), Shipments=("Lead Time", "count"))
    .reset_index()
)
_reach_rows_all = []
for _rf in df_raw["Factory"].unique():
    _rf_df    = df_raw[df_raw["Factory"] == _rf]
    _rf_stats = factory_stats_all[factory_stats_all["Factory"] == _rf].iloc[0]
    _reach_rows_all.append({
        "Factory": _rf,
        "States Served": _rf_df["State/Province"].nunique(),
        "Regions Served": _rf_df["Region"].nunique(),
        "Shipments": int(_rf_stats["Shipments"]),
        "Avg Lead Time": round(_rf_stats["Avg_Lead_Time"], 1),
        "Delay Rate": _rf_stats["Delay_Rate"],
    })
_reach_df_all = pd.DataFrame(_reach_rows_all).sort_values("States Served", ascending=False).reset_index(drop=True)

# ── Global export dataframes ───────────────────────────────────────────────────
_export_route_var = (
    df_raw.groupby("RouteRegion")
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Std_Dev=("Lead Time", "std"),
        Min_Lead_Time=("Lead Time", "min"),
        Max_Lead_Time=("Lead Time", "max"),
        Shipments=("Lead Time", "count"),
    )
    .reset_index()
    .sort_values("Std_Dev", ascending=False)
)
_export_route_var["Std_Dev"]       = _export_route_var["Std_Dev"].fillna(0).round(2)
_export_route_var["Avg_Lead_Time"] = _export_route_var["Avg_Lead_Time"].round(1)

_export_cost_df = (
    df.groupby("RouteRegion")
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Shipments=("Lead Time", "count"),
    )
    .reset_index()
)
_export_cost_df["Profit_Margin"] = (_export_cost_df["Total_Profit"] / _export_cost_df["Total_Sales"] * 100).round(1)
_export_cost_df["Avg_Lead_Time"] = _export_cost_df["Avg_Lead_Time"].round(1)

# ── Build zip for sidebar download button ─────────────────────────────────────
import zipfile, io as _io
_lb_cols_zip  = ["RouteRegion", "Efficiency_Score", "Avg_Lead_Time", "Delay_Rate", "Shipments"]
_cols_show_zip = ["Order ID", "Order Date", "Ship Date", "Lead Time",
                  "Factory", "State/Province", "Region", "Ship Mode",
                  "Product Name", "Sales", "Gross Profit", "Is Delayed"]
_zip_buf = _io.BytesIO()
def _zip_hav(lat1, lon1, lat2, lon2):
    import math
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))

_zip_underserved_rows = []
for _zu_state, (_zu_slat, _zu_slon) in STATE_CENTROIDS.items():
    _zu_s_data = state_stats_all[state_stats_all["State/Province"] == _zu_state]
    if _zu_s_data.empty:
        continue
    _zu_min_dist = min(_zip_hav(fc["lat"], fc["lon"], _zu_slat, _zu_slon) for fc in FACTORY_COORDS.values())
    _zu_sr = _zu_s_data.iloc[0]
    _zip_underserved_rows.append({
        "State": _zu_state,
        "Min Distance to Factory (mi)": round(_zu_min_dist, 0),
        "Avg Lead Time": round(_zu_sr["Avg_Lead_Time"], 1),
        "Delay Rate": _zu_sr["Delay_Rate"],
        "Shipments": int(_zu_sr["Shipments"]),
    })
_zip_underserved_df = pd.DataFrame(_zip_underserved_rows)
_zip_dist_thresh = _zip_underserved_df["Min Distance to Factory (mi)"].quantile(0.6)
_zip_lt_thresh   = _zip_underserved_df["Avg Lead Time"].quantile(0.6)
_zip_underserved_flagged = _zip_underserved_df[
    (_zip_underserved_df["Min Distance to Factory (mi)"] > _zip_dist_thresh) &
    (_zip_underserved_df["Avg Lead Time"] > _zip_lt_thresh)
].sort_values("Min Distance to Factory (mi)", ascending=False).reset_index(drop=True)

# ── Region Metrics Summary (Tab2) ───────────────────────────────────────────
_ZIP_CA_CODES = {"ON","QC","AB","BC","MB","PE","NB","NS","NL","SK"}
_zip_region_table = state_stats.copy()
_zip_region_table["Country"] = _zip_region_table["State Code"].apply(
    lambda c: "Canadian Province" if c in _ZIP_CA_CODES else "US State"
)
_zip_region_table = _zip_region_table.rename(columns={"State/Province": "Region"})[[
    "Country", "Region", "Avg_Lead_Time", "Delay_Rate", "Shipments", "Total_Sales"
]].sort_values("Shipments", ascending=False).reset_index(drop=True)
_zip_region_table.columns = ["Country", "Region", "Avg Lead Time (d)", "Delay Rate", "Shipments", "Total Sales ($)"]

# ── Factory Reach Index (Tab4) ───────────────────────────────────────────────
_zip_reach_rows = []
for _zf_factory in df["Factory"].unique():
    _zf_fdf = df[df["Factory"] == _zf_factory]
    _zf_f_stats = factory_stats[factory_stats["Factory"] == _zf_factory].iloc[0]
    _zip_reach_rows.append({
        "Factory": _zf_factory,
        "States Served": _zf_fdf["State/Province"].nunique(),
        "Regions Served": _zf_fdf["Region"].nunique(),
        "Shipments": int(_zf_f_stats["Shipments"]),
        "Avg Lead Time": round(_zf_f_stats["Avg_Lead_Time"], 1),
        "Delay Rate": _zf_f_stats["Delay_Rate"],
    })
_zip_reach_df = pd.DataFrame(_zip_reach_rows).sort_values("States Served", ascending=False).reset_index(drop=True)

# ── East vs West Coast Comparison (Tab2) ─────────────────────────────────────
_zip_WEST_STATES = ["California", "Oregon", "Washington", "Nevada", "Idaho",
                     "Montana", "Wyoming", "Colorado", "Utah", "Arizona", "New Mexico"]
_zip_EAST_STATES = ["New York", "Pennsylvania", "New Jersey", "Massachusetts",
                     "Connecticut", "Rhode Island", "New Hampshire", "Vermont",
                     "Maine", "Maryland", "Delaware", "Virginia", "North Carolina",
                     "South Carolina", "Georgia", "Florida"]
_zip_west_df = state_stats_all[state_stats_all["State/Province"].isin(_zip_WEST_STATES)]
_zip_east_df = state_stats_all[state_stats_all["State/Province"].isin(_zip_EAST_STATES)]
_zip_west_nearest_dist = np.mean([
    min(_zip_hav(fc["lat"], fc["lon"], STATE_CENTROIDS.get(s, (0, 0))[0], STATE_CENTROIDS.get(s, (0, 0))[1])
        for fc in FACTORY_COORDS.values())
    for s in _zip_WEST_STATES if s in STATE_CENTROIDS
])
_zip_east_nearest_dist = np.mean([
    min(_zip_hav(fc["lat"], fc["lon"], STATE_CENTROIDS.get(s, (0, 0))[0], STATE_CENTROIDS.get(s, (0, 0))[1])
        for fc in FACTORY_COORDS.values())
    for s in _zip_EAST_STATES if s in STATE_CENTROIDS
])
_zip_ew_compare = pd.DataFrame({
    "Metric": ["Avg Lead Time (d)", "Delay Rate (%)", "Avg Distance to Factory (mi)", "Total Shipments"],
    "West Coast": [
        round(_zip_west_df["Avg_Lead_Time"].mean(), 2),
        round(_zip_west_df["Delay_Rate"].mean() * 100, 1),
        round(_zip_west_nearest_dist, 0),
        int(_zip_west_df["Shipments"].sum()),
    ],
    "East Coast": [
        round(_zip_east_df["Avg_Lead_Time"].mean(), 2),
        round(_zip_east_df["Delay_Rate"].mean() * 100, 1),
        round(_zip_east_nearest_dist, 0),
        int(_zip_east_df["Shipments"].sum()),
    ],
})

# ── Order-Level Shipment Timeline (Tab5) — full, uncapped, all states/modes ──
_zip_order_timeline = df[_cols_show_zip].sort_values("Order Date").reset_index(drop=True)

# ── Division Performance Over Time (Tab5) ────────────────────────────────────
_zip_div_monthly = (
    df.groupby(["Month", "Division"])
    .agg(Avg_Lead_Time=("Lead Time", "mean"), Shipments=("Lead Time", "count"))
    .reset_index()
)

# ── Product-Level Lead Time (Tab4) — full table, all factories ──────────────
_zip_product_stats = (
    df.groupby(["Factory", "Product Name"])
    .agg(Avg_Lead_Time=("Lead Time", "mean"), Shipments=("Lead Time", "count"))
    .reset_index()
    .sort_values(["Factory", "Avg_Lead_Time"])
)

# ── Ship Mode × Region / Factory Heatmaps (Tab3) — full portfolio ───────────
_zip_smr_pivot = df_raw.pivot_table(
    index="Ship Mode", columns="Region", values="Lead Time", aggfunc="mean"
).round(1)
_zip_smf_pivot = df_raw.pivot_table(
    index="Ship Mode", columns="Factory", values="Is Delayed", aggfunc="mean"
).round(3)

# ── Network Coverage Deep Dive — Product Coverage, all states combined ──────
_zip_ca_centroids = {
    "Ontario": (51.2538, -85.3232), "Quebec": (53.0, -71.0),
    "Alberta": (53.9333, -116.5765), "British Columbia": (53.7267, -127.6476),
    "Manitoba": (53.7609, -98.8139), "Saskatchewan": (52.9399, -106.4509),
    "Nova Scotia": (44.6820, -63.7443), "New Brunswick": (46.5653, -66.4619),
    "Prince Edward Island": (46.5107, -63.4168), "Newfoundland and Labrador": (53.1355, -57.6604),
}
_zip_all_centroids = {**STATE_CENTROIDS, **_zip_ca_centroids}
_zip_coverage_rows = []
for _zc_state, (_zc_slat, _zc_slon) in _zip_all_centroids.items():
    _zc_sdf = df_dd[df_dd["State/Province"] == _zc_state]
    if _zc_sdf.empty:
        continue
    _zc_dists = {f: _zip_hav(fc["lat"], fc["lon"], _zc_slat, _zc_slon) for f, fc in FACTORY_COORDS.items()}
    _zc_nearest = min(_zc_dists, key=_zc_dists.get)
    _zc_nearest_can_make = {prod for prod, fac in PRODUCT_FACTORY.items() if fac == _zc_nearest}
    _zc_prod = (
        _zc_sdf.groupby(["Division", "Product Name", "Factory"])
        .size().reset_index(name="Orders")
        .sort_values(["Division", "Orders"], ascending=[True, False])
        .reset_index(drop=True)
    )
    _zc_total_orders = int(_zc_prod["Orders"].sum())
    for _, _zc_row in _zc_prod.iterrows():
        _zc_is_near = _zc_row["Factory"] == _zc_nearest
        _zc_is_gap  = _zc_row["Product Name"] not in _zc_nearest_can_make
        _zip_coverage_rows.append({
            "State/Province": _zc_state,
            "Product Name": _zc_row["Product Name"],
            "Division": _zc_row["Division"],
            "Orders": int(_zc_row["Orders"]),
            "Share": round(_zc_row["Orders"] / _zc_total_orders * 100, 1) if _zc_total_orders else 0,
            "Served By": _zc_row["Factory"],
            "Nearest Factory": _zc_nearest,
            "Coverage Status": "Network gap" if _zc_is_gap else "Covered",
        })
_zip_coverage_df = pd.DataFrame(_zip_coverage_rows)

_zip_exports = {
    "Tab1_Route_Efficiency/route_efficiency_table.csv":
        route_stats[["RouteRegion", "Shipments", "Delay_Rate", "Avg_Lead_Time", "Std_Dev", "Efficiency_Score"]].to_csv(index=False),
    "Tab1_Route_Efficiency/top10_efficient_routes.csv":
        route_stats_all.nlargest(10, "Efficiency_Score")[_lb_cols_zip].reset_index(drop=True).to_csv(index=True),
    "Tab1_Route_Efficiency/bottom10_efficient_routes.csv":
        route_stats_all.nsmallest(10, "Efficiency_Score")[_lb_cols_zip].reset_index(drop=True).to_csv(index=True),
    "Tab1_Route_Efficiency/route_variability_table.csv":
        _export_route_var.to_csv(index=False),
    "Tab1_Route_Efficiency/lead_time_vs_profit_margin.csv":
        _export_cost_df[["RouteRegion", "Avg_Lead_Time", "Profit_Margin", "Total_Sales", "Total_Profit", "Shipments"]].sort_values("Avg_Lead_Time").to_csv(index=False),
    "Tab2_Geographic_Coverage/state_stats.csv":
        state_stats.to_csv(index=False),
    "Tab2_Geographic_Coverage/top10_bottleneck_states.csv":
        state_stats_region.nlargest(10, "Avg_Lead_Time")[
            ["State/Province", "Shipments", "Avg_Lead_Time", "Delay_Rate"]
        ].reset_index(drop=True).to_csv(index=False),
    "Tab2_Geographic_Coverage/high_volume_high_delay_states.csv":
        state_stats_region[
            (state_stats_region["Shipments"] > state_stats_region["Shipments"].quantile(0.6)) &
            (state_stats_region["Delay_Rate"]  > state_stats_region["Delay_Rate"].quantile(0.6))
        ].sort_values("Delay_Rate", ascending=False)[
            ["State/Province", "Shipments", "Avg_Lead_Time", "Delay_Rate"]
        ].reset_index(drop=True).to_csv(index=False),
    "Tab2_Geographic_Coverage/underserved_regions.csv":
        _zip_underserved_flagged.to_csv(index=False),
    "Tab2_Geographic_Coverage/region_metrics_summary.csv":
        _zip_region_table.to_csv(index=False),
    "Tab2_Geographic_Coverage/network_coverage_product_detail_all_states.csv":
        _zip_coverage_df.to_csv(index=False),
    "Tab4_Factory_Intelligence/coast_exposure_east_vs_west.csv":
        _zip_ew_compare.to_csv(index=False),
    "Tab3_Ship_Mode/ship_mode_stats.csv":
        ship_stats.to_csv(index=False),
    "Tab3_Ship_Mode/ship_mode_x_region_avg_lead_time.csv":
        _zip_smr_pivot.to_csv(),
    "Tab3_Ship_Mode/ship_mode_x_factory_delay_rate.csv":
        _zip_smf_pivot.to_csv(),
    "Tab4_Factory_Intelligence/factory_stats.csv":
        factory_stats.to_csv(index=False),
    "Tab4_Factory_Intelligence/product_level_lead_time.csv":
        _zip_product_stats.to_csv(index=False),
    "Tab4_Factory_Intelligence/factory_reach_index.csv":
        _zip_reach_df.to_csv(index=False),
    "Tab5_Trends/monthly_trends.csv":
        monthly.to_csv(index=False),
    "Tab5_Trends/division_performance_over_time.csv":
        _zip_div_monthly.to_csv(index=False),
    "Tab5_Trends/order_level_shipment_timeline.csv":
        _zip_order_timeline.to_csv(index=False),
    "Tab5_Trends/raw_orders.csv":
        df[_cols_show_zip].sort_values("Lead Time", ascending=False).reset_index(drop=True).to_csv(index=False),
    "Tab5_Trends/shipment_volume_forecast.csv": (lambda: (
        lambda _fc: (
            lambda _x, _y, _coeffs: (
                lambda _future_x, _future_months, _resid_std: pd.DataFrame(
                    [{"Month": row["Month"], "Type": "Historical", "Shipments": int(row["Shipments"]),
                      "Trend": round(np.polyval(_coeffs, i), 1),
                      "Forecast": None, "Lower_Bound": None, "Upper_Bound": None}
                     for i, (_, row) in enumerate(_fc.iterrows())] +
                    [{"Month": _future_months[i], "Type": "Forecast", "Shipments": None,
                      "Trend": round(np.polyval(_coeffs, len(_fc) + i), 1),
                      "Forecast": round(np.polyval(_coeffs, len(_fc) + i), 1),
                      "Lower_Bound": round(np.polyval(_coeffs, len(_fc) + i) - _resid_std, 1),
                      "Upper_Bound": round(np.polyval(_coeffs, len(_fc) + i) + _resid_std, 1)}
                     for i in range(3)]
                ).to_csv(index=False)
            )(
                np.arange(len(_fc), len(_fc) + 3),
                [(pd.to_datetime(_fc["Month"].iloc[-1]) + pd.DateOffset(months=i+1)).strftime("%Y-%m") for i in range(3)],
                np.std(_y - np.polyval(_coeffs, _x))
            )
        )(np.arange(len(_fc)), _fc["Shipments"].values, np.polyfit(np.arange(len(_fc)), _fc["Shipments"].values, 1))
    )(df.groupby("Month").agg(Shipments=("Lead Time","count")).reset_index().sort_values("Month")))(),
    "Tab2_Geographic_Coverage/customer_segmentation_tiers.csv":
        (lambda s: (
            s.groupby(pd.cut(s["Sales"], bins=[-np.inf, s["Sales"].quantile(0.25), s["Sales"].quantile(0.75), np.inf],
                             labels=["Low Value","Medium Value","High Value"]), observed=True)
            .agg(Orders=("Sales","count"), Total_Revenue=("Sales","sum"),
                 Avg_Lead_Time=("Lead Time","mean"), Delay_Rate=("Is Delayed","mean"))
            .reset_index().rename(columns={"Sales":"Value_Tier"}).to_csv(index=False)
        ))(df),
}
with zipfile.ZipFile(_zip_buf, "w", zipfile.ZIP_DEFLATED) as _zf:
    for _fname, _data in _zip_exports.items():
        _zf.writestr(_fname, _data)
st.session_state["_reports_zip"] = _zip_buf.getvalue()

_dl_all_reports_slot.download_button(
    label="⬇️ Download All Reports (.zip)",
    data=st.session_state["_reports_zip"],
    file_name="nassau_candy_reports.zip",
    mime="application/zip",
    use_container_width=True,
    help="Downloads all tables organised by tab as CSV files in a zip folder",
    key="dl_all_reports"
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='color:#f59e0b; margin-bottom:0;'>🍬 Nassau Candy Distributor</h1>"
    "<p style='color:#475569; margin-top:-8px; font-size:1.05rem; padding-left:4.5rem;'>"
    "Factory-to-Customer Shipping Route Efficiency Dashboard</p>",
    unsafe_allow_html=True,
)
st.divider()

# ── KPI Row ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)
kpi_style = "background:#1a1f35;border:1px solid #2d3561;border-radius:10px;padding:16px;text-align:center;"

with k1:
    st.metric("Total Orders", f"{len(df):,}")
with k2:
    if region_sel != "All" and factory_sel != "All":
        _lt_note = "⚠️ Not region/factory-specific"
    elif region_sel != "All":
        _lt_note = "⚠️ Not region-specific"
    elif factory_sel != "All":
        _lt_note = "⚠️ Not factory-specific"
    else:
        _lt_note = None
    st.metric("Avg Lead Time", f"{df['Lead Time'].mean():.1f}d")
with k3:
    st.metric("Delay Rate", f"{df['Is Delayed'].mean()*100:.1f}%")
with k4:
    st.metric("Total Revenue", f"${df['Sales'].sum():,.0f}")
with k5:
    st.metric("Total Profit", f"${df['Gross Profit'].sum():,.0f}")
with k6:
    st.metric("Active Routes", f"{df['RouteRegion'].nunique()}")

# Note row — only k2 column gets the warning, others get empty space to preserve alignment
n1, n2, n3, n4, n5, n6 = st.columns(6)
with n2:
    if _lt_note:
        st.markdown(f"<div style='font-size:0.7rem;color:#f4a444;margin-top:-0.8rem;'>{_lt_note}</div>", unsafe_allow_html=True)

st.divider()

# ── Automated Alerts ───────────────────────────────────────────────────────────
_route_stats_all_alerts = (
    df_raw.groupby("RouteRegion")
    .agg(
        Shipments=("Lead Time", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delayed", "mean"),
    )
    .reset_index()
)
_lt_min_a = _route_stats_all_alerts["Avg_Lead_Time"].min()
_lt_max_a = _route_stats_all_alerts["Avg_Lead_Time"].max()
_route_stats_all_alerts["Efficiency_Score"] = (
    100 * (_lt_max_a - _route_stats_all_alerts["Avg_Lead_Time"]) / (_lt_max_a - _lt_min_a + 1e-9)
).round(1)

_network_delay_rate = df_raw["Is Delayed"].mean() * 100
_critical_routes    = _route_stats_all_alerts[_route_stats_all_alerts["Efficiency_Score"] == 0]
_high_delay_routes  = _route_stats_all_alerts[_route_stats_all_alerts["Delay_Rate"] > 0.40]

_alerts = []
if _network_delay_rate > 25:
    _alerts.append(
        f"🚨 <b>Network Delay Alert:</b> Overall delay rate is <b>{_network_delay_rate:.1f}%</b> — "
        f"exceeding the 25% alert threshold. Immediate review of high-delay lanes is recommended."
    )
if not _critical_routes.empty:
    _route_names = ", ".join(f"<b>{r}</b>" for r in _critical_routes["RouteRegion"].tolist())
    _alerts.append(
        f"⛔ <b>Critical Route(s):</b> {_route_names} — recorded an efficiency score of <b>0/100</b>. "
        f"These lanes represent the network's most urgent intervention priority."
    )
if not _high_delay_routes.empty:
    for _, _hr in _high_delay_routes.iterrows():
        _alerts.append(
            f"⚠️ <b>High Delay Route:</b> <b>{_hr['RouteRegion']}</b> has a delay rate of "
            f"<b>{_hr['Delay_Rate']:.1%}</b> — exceeding the 40% alert threshold."
        )

if _alerts:
    with st.expander(f"🔔 Network Alerts — {len(_alerts)} active", expanded=True):
        for _alert in _alerts:
            st.markdown(
                f"<div style='background:#fff7ed;border-left:4px solid #ea580c;"
                f"border-radius:6px;padding:10px 14px;margin-bottom:8px;"
                f"font-size:0.85rem;color:#1e293b;'>{_alert}</div>",
                unsafe_allow_html=True
            )

# TAB LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "📊 Route Efficiency",
    "🗺️ Geographic Coverage",
    "🚚 Ship Mode Analysis",
    "🏭 Factory Intelligence",
    "📈 Trends & Deep-Dive",
])

# ── TAB 1: Route Efficiency ────────────────────────────────────────────────────
with tabs[0]:
    st.markdown('<div class="section-header">Route Performance Leaderboard</div>', unsafe_allow_html=True)

    pivot_heat = df.pivot_table(
        index="Factory", columns="Region",
        values="Lead Time", aggfunc="mean"
    ).round(1)
    factories_list = pivot_heat.index.tolist()
    regions_list   = pivot_heat.columns.tolist()

    heat_z    = pivot_heat.values.tolist()
    heat_text = [[f"{v:.1f}d" if not pd.isna(v) else "" for v in row] for row in pivot_heat.values]

    fig_heat = go.Figure(data=go.Heatmap(
        z=heat_z,
        x=regions_list,
        y=factories_list,
        text=heat_text,
        texttemplate="%{text}",
        textfont={"size": 13, "color": "white"},
        colorscale=[[0,"#9ecae1"],[0.4,"#3182bd"],[1,"#08306b"]],
        zmin=3, zmax=9,
        colorbar=dict(title="Avg Lead Time (days)", ticksuffix="d", title_font=dict(color="#1a1a2e"), tickfont=dict(color="#1a1a2e")),
        hoverongaps=False,
        hovertemplate="<b>%{y} → %{x}</b><br>Avg Lead Time: %{z:.1f}d<extra></extra>",
    ))
    for _fi, _fac in enumerate(factories_list):
        for _ri, _reg in enumerate(regions_list):
            if pd.isna(pivot_heat.values[_fi][_ri]):
                fig_heat.add_annotation(
                    x=_reg, y=_fac, text="-", showarrow=False,
                    font=dict(size=15, color="#64748b")
                )
    fig_heat.update_layout(
        **PLOTLY_THEME,
        title="Factory × Region — Avg Lead Time Heatmap",
        height=340,
        xaxis=dict(title="", side="top", tickfont=dict(size=13, color="#1a1a2e")),
        yaxis=dict(title="", side="left", tickfont=dict(size=13, color="#1a1a2e")),
        margin=dict(l=160, r=40, t=100, b=20),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown('<div class="section-header">Efficiency Score vs Shipment Volume</div>', unsafe_allow_html=True)
    fig = px.scatter(
        route_stats,
        x="Shipments", y="Efficiency_Score",
        size="Shipments", color="Delay_Rate",
        hover_name="RouteRegion",
        hover_data={"Shipments": True, "Efficiency_Score": ":.1f", "Delay_Rate": ":.1%"},
        size_max=35,
        color_continuous_scale=[[0,"#00601a"],[0.3,"#31a354"],[0.6,"#fd8d3c"],[1,"#99000d"]],
        labels={"Efficiency_Score": "Efficiency Score (0-100)", "Delay_Rate": "Delay Rate"},
        title="Route Efficiency Score vs Volume (bubble size = volume, color = delay rate)",
    )
    fig.update_traces(marker=dict(sizemode="area", sizeref=2.*max(route_stats["Shipments"])/(35**2), sizemin=8))
    _dr_min = route_stats["Delay_Rate"].min()
    _dr_max = route_stats["Delay_Rate"].max()
    _dr_range = _dr_max - _dr_min
    if _dr_range < 0.05:  # narrow range — show actual values in title
        _cb_title = f"Delay Rate<br><span style='font-size:0.7em;color:#111;'>({_dr_min:.1%} – {_dr_max:.1%})</span>"
    else:
        _cb_title = "Delay Rate"
    fig.update_layout(
        **PLOTLY_THEME, height=440,
        xaxis=dict(tickfont=dict(color="#1a1a2e"), title_font=dict(color="#1a1a2e")),
        yaxis=dict(tickfont=dict(color="#1a1a2e"), title_font=dict(color="#1a1a2e")),
        coloraxis_colorbar=dict(title=_cb_title, title_font=dict(color="#1a1a2e"), tickfont=dict(color="#1a1a2e"), tickformat=".1%"),
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Full Route Efficiency Table"):
        route_stats_display = route_stats[["RouteRegion", "Shipments", "Delay_Rate", "Avg_Lead_Time", "Std_Dev", "Efficiency_Score"]]
        styled = (
            route_stats_display.style
                .background_gradient(subset=["Avg_Lead_Time"], cmap="Blues")
                .background_gradient(subset=["Efficiency_Score"], cmap="Blues_r")
                .background_gradient(subset=["Std_Dev"], cmap="Oranges")
                .format({"Avg_Lead_Time": "{:.1f}", "Delay_Rate": "{:.1%}", "Efficiency_Score": "{:.0f}", "Std_Dev": "{:.2f}"})
        )
        st.dataframe(styled, use_container_width=True)

    # ── Route Efficiency Leaderboard ──────────────────────────────────────────
    st.markdown('<div class="section-header">🏆 Route Efficiency Leaderboard — Top 10 & Bottom 10</div>', unsafe_allow_html=True)
    if region_sel != "All" or ship_mode_sel != "All" or factory_sel != "All":
        st.markdown(
            "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
            "📌 <i>Showing full portfolio — unaffected by Region / Ship Mode / Factory filter selections</i>"
            "</div>", unsafe_allow_html=True
        )

    _lb_cols  = ["RouteRegion", "Efficiency_Score", "Avg_Lead_Time", "Delay_Rate", "Shipments"]
    _top10    = route_stats_all.nlargest(10, "Efficiency_Score")[_lb_cols].reset_index(drop=True)
    _bot10    = route_stats_all.nsmallest(10, "Efficiency_Score")[_lb_cols].reset_index(drop=True)
    _top10.index  += 1
    _bot10.index  += 1

    _lb_col1, _lb_col2 = st.columns(2)
    with _lb_col1:
        st.markdown("<p style='font-size:0.95rem;font-weight:600;margin-bottom:6px;'>✅ Top 10 Most Efficient Routes</p>", unsafe_allow_html=True)
        st.dataframe(
            _top10.style
                .format({"Efficiency_Score": "{:.0f}", "Avg_Lead_Time": "{:.1f}d", "Delay_Rate": "{:.1%}", "Shipments": "{:,}"})
                .background_gradient(subset=["Efficiency_Score"], cmap="Greens"),
            use_container_width=True,
        )
    with _lb_col2:
        st.markdown("<p style='font-size:0.95rem;font-weight:600;margin-bottom:6px;'>⚠️ Bottom 10 Least Efficient Routes</p>", unsafe_allow_html=True)
        st.dataframe(
            _bot10.style
                .format({"Efficiency_Score": "{:.0f}", "Avg_Lead_Time": "{:.1f}d", "Delay_Rate": "{:.1%}", "Shipments": "{:,}"})
                .background_gradient(subset=["Efficiency_Score"], cmap="Reds_r"),
            use_container_width=True,
        )

    # ── Route-Level Lead Time Variability ─────────────────────────────────────
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📉 Lead Time Variability by Route</div>', unsafe_allow_html=True)
    if region_sel != "All" or ship_mode_sel != "All" or factory_sel != "All" or delay_threshold != 7:
        st.markdown(
            "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
            "📌 <i>Showing full portfolio — unaffected by Region / Ship Mode / Factory / Delay Threshold filter selections</i>"
            "</div>", unsafe_allow_html=True
        )

    fig_var = px.bar(
        _export_route_var.head(20),
        x="RouteRegion", y="Std_Dev",
        color="Std_Dev",
        color_continuous_scale=[[0,"#31a354"],[0.5,"#fd8d3c"],[1,"#99000d"]],
        labels={"Std_Dev": "Std Dev (days)", "RouteRegion": "Route"},
        title="Top 20 Routes by Lead Time Variability (Std Dev, days)",
        hover_data={"Avg_Lead_Time": ":.1f", "Min_Lead_Time": True, "Max_Lead_Time": True, "Shipments": True},
    )
    fig_var.update_layout(
        **PLOTLY_THEME, height=420,
        xaxis=dict(tickangle=-35, tickfont=dict(color="#1a1a2e"), title_font=dict(color="#1a1a2e")),
        yaxis=dict(tickfont=dict(color="#1a1a2e"), title_font=dict(color="#1a1a2e")),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_var, use_container_width=True)

    with st.expander("📋 Full Route Variability Table"):
        st.dataframe(
            _export_route_var.style
                .format({"Avg_Lead_Time": "{:.1f}", "Std_Dev": "{:.2f}", "Shipments": "{:,}"})
                .background_gradient(subset=["Std_Dev"], cmap="Reds"),
            use_container_width=True,
        )

    # ── Cost-Time Tradeoff ─────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">💰 Lead Time vs Profit Margin by Route</div>', unsafe_allow_html=True)

    _cost_df = (
        df.groupby("RouteRegion")
        .agg(
            Avg_Lead_Time=("Lead Time", "mean"),
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum"),
            Shipments=("Lead Time", "count"),
        )
        .reset_index()
    )
    _cost_df["Profit_Margin"]  = (_cost_df["Total_Profit"] / _cost_df["Total_Sales"] * 100).round(1)
    _cost_df["Avg_Lead_Time"]  = _cost_df["Avg_Lead_Time"].round(1)
    _cost_df["Sales_per_Ship"] = (_cost_df["Total_Sales"] / _cost_df["Shipments"]).round(0)

    fig_ct = px.scatter(
        _cost_df,
        x="Avg_Lead_Time", y="Profit_Margin",
        size="Shipments", color="Total_Sales",
        hover_name="RouteRegion",
        hover_data={"Avg_Lead_Time": ":.1f", "Profit_Margin": ":.1f", "Total_Sales": ":$,.0f", "Shipments": True},
        color_continuous_scale=[[0,"#6baed6"],[0.5,"#2171b5"],[1,"#08306b"]],
        labels={"Avg_Lead_Time": "Avg Lead Time (days)", "Profit_Margin": "Profit Margin (%)", "Total_Sales": "Total Sales ($)"},
        title="Lead Time vs Profit Margin by Route (bubble size = volume, color = revenue)",
    )
    fig_ct.update_layout(
        **PLOTLY_THEME, height=460,
        xaxis=dict(tickfont=dict(color="#1a1a2e"), title_font=dict(color="#1a1a2e")),
        yaxis=dict(tickfont=dict(color="#1a1a2e"), title_font=dict(color="#1a1a2e")),
        coloraxis_colorbar=dict(title="Total Sales ($)", title_font=dict(color="#1a1a2e"), tickfont=dict(color="#1a1a2e"), tickprefix="$", tickformat=",.0f"),
    )
    st.plotly_chart(fig_ct, use_container_width=True)

    with st.expander("📋 Full Lead Time vs Profit Margin Table"):
        st.dataframe(
            _cost_df[["RouteRegion", "Avg_Lead_Time", "Profit_Margin", "Total_Sales", "Total_Profit", "Shipments"]]
            .sort_values("Avg_Lead_Time")
            .style
            .format({"Avg_Lead_Time": "{:.1f}", "Profit_Margin": "{:.1f}%", "Total_Sales": "${:,.0f}", "Total_Profit": "${:,.0f}", "Shipments": "{:,}"})
            .background_gradient(subset=["Profit_Margin"], cmap="Greens")
            .background_gradient(subset=["Avg_Lead_Time"], cmap="Reds"),
            use_container_width=True,
        )
        _ct_export = _cost_df[["RouteRegion", "Avg_Lead_Time", "Profit_Margin", "Total_Sales", "Total_Profit", "Shipments"]].sort_values("Avg_Lead_Time")

    # ── Distance vs Lead Time Correlation ─────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-bottom:30px;">🧭 Distance vs Lead Time Correlation</div>', unsafe_allow_html=True)

    def _haversine(lat1, lon1, lat2, lon2):
        R = 3958.8  # miles
        φ1, φ2 = np.radians(lat1), np.radians(lat2)
        dφ = np.radians(lat2 - lat1)
        dλ = np.radians(lon2 - lon1)
        a = np.sin(dφ/2)**2 + np.cos(φ1)*np.cos(φ2)*np.sin(dλ/2)**2
        return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # Build per-order rows: one row per (state, factory) pair that actually has orders
    _dist_rows = []
    for _, row in df.iterrows():
        state = row["State/Province"]
        factory = row["Factory"]
        if state not in STATE_CENTROIDS or factory not in FACTORY_COORDS:
            continue
        slat, slon = STATE_CENTROIDS[state]
        fc = FACTORY_COORDS[factory]
        _dist = _haversine(fc["lat"], fc["lon"], slat, slon)

        # Find nearest factory for this state
        _nearest = min(FACTORY_COORDS.keys(),
                       key=lambda f: _haversine(FACTORY_COORDS[f]["lat"], FACTORY_COORDS[f]["lon"], slat, slon))
        _routing_type = "Nearest factory fulfilled" if factory == _nearest else "Non-nearest factory fulfilled"

        _dist_rows.append({
            "State": state,
            "Factory": factory,
            "Distance_mi": round(_dist, 0),
            "Lead_Time": row["Lead Time"],
            "Delayed": 1 if row.get("Delayed", False) else 0,
            "Routing": _routing_type,
        })

    _dist_df = pd.DataFrame(_dist_rows)

    if not _dist_df.empty:
        # Aggregate to state-factory level
        _agg = _dist_df.groupby(["State", "Factory", "Distance_mi", "Routing"]).agg(
            Avg_Lead_Time=("Lead_Time", "mean"),
            Shipments=("Lead_Time", "count"),
            Delay_Rate=("Delayed", "mean"),
        ).reset_index()

        _nearest_df = _agg[_agg["Routing"] == "Nearest factory fulfilled"]
        _nonnear_df = _agg[_agg["Routing"] == "Non-nearest factory fulfilled"]

        def _pearson(d):
            if len(d) < 2:
                return 0
            return d["Distance_mi"].corr(d["Avg_Lead_Time"])

        _r_nearest = _pearson(_nearest_df)
        _r_nonnear = _pearson(_nonnear_df)

        # ── Panel labels ──────────────────────────────────────────────────────
        _col_concept, _col_actual = st.columns(2)

        with _col_concept:
            st.markdown(
                "<div style='font-size:12px;font-weight:600;letter-spacing:0.07em;"
                "text-transform:uppercase;color:#1e293b;margin-bottom:0px;'>"
                "💡 Conceptual — what we'd expect if routing to nearest reduced lead time"
                "</div>", unsafe_allow_html=True
            )

        with _col_actual:
            st.markdown(
                "<div style='font-size:12px;font-weight:600;letter-spacing:0.07em;"
                "text-transform:uppercase;color:#1e293b;margin-bottom:0px;'>"
                "📊 Evidential — what the real data shows"
                "</div>", unsafe_allow_html=True
            )

        st.markdown("<div style='margin-top:-24px;'></div>", unsafe_allow_html=True)

        # ── CONCEPTUAL chart (simulated) ──────────────────────────────────────
        import random
        _rng = np.random.default_rng(42)

        # Simulate nearest: short distances, lower flat lead times
        _sim_n = 80
        _sim_near_dist  = _rng.uniform(80, 800, _sim_n)
        _sim_near_lt    = 3.8 + _rng.normal(0, 0.45, _sim_n)
        _sim_near_sz    = _rng.integers(4, 14, _sim_n).astype(float)

        # Simulate non-nearest: longer distances, rising lead time with distance
        _sim_nn = 120
        _sim_nn_dist = _rng.uniform(400, 2500, _sim_nn)
        _sim_nn_lt   = 4.2 + _sim_nn_dist * 0.0007 + _rng.normal(0, 0.5, _sim_nn)
        _sim_nn_sz   = _rng.integers(4, 14, _sim_nn).astype(float)

        fig_concept = go.Figure()

        # Nearest trace
        fig_concept.add_trace(go.Scatter(
            x=_sim_near_dist, y=_sim_near_lt,
            mode="markers", name="Nearest factory fulfilled",
            marker=dict(color="rgba(29,158,117,0.6)", size=_sim_near_sz, line=dict(width=0)),
            hoverinfo="skip",
        ))
        _mn, _bn = np.polyfit(_sim_near_dist, _sim_near_lt, 1)
        _xl = np.linspace(_sim_near_dist.min(), _sim_near_dist.max(), 100)
        fig_concept.add_trace(go.Scatter(
            x=_xl, y=_mn * _xl + _bn, mode="lines",
            line=dict(color="#0F6E56", width=2, dash="dash"), showlegend=False,
        ))

        # Non-nearest trace
        fig_concept.add_trace(go.Scatter(
            x=_sim_nn_dist, y=_sim_nn_lt,
            mode="markers", name="Non-nearest factory fulfilled",
            marker=dict(color="rgba(216,90,48,0.6)", size=_sim_nn_sz, line=dict(width=0)),
            hoverinfo="skip",
        ))
        _mnn, _bnn = np.polyfit(_sim_nn_dist, _sim_nn_lt, 1)
        _xl2 = np.linspace(_sim_nn_dist.min(), _sim_nn_dist.max(), 100)
        fig_concept.add_trace(go.Scatter(
            x=_xl2, y=_mnn * _xl2 + _bnn, mode="lines",
            line=dict(color="#993C1D", width=2, dash="dash"), showlegend=False,
        ))

        _r_concept_nn = float(np.corrcoef(_sim_nn_dist, _sim_nn_lt)[0, 1])
        fig_concept.update_layout(
            **PLOTLY_THEME, height=400,
            title=dict(text=f"If distance drove lead time — non-nearest r ≈ {_r_concept_nn:.2f} (rising slope)",
                       font=dict(size=12, color="#0f172a"), x=0),
            xaxis=dict(title=dict(text="Distance from factory (miles)", font=dict(color="#0f172a", size=12)),
                       color="#0f172a", tickfont=dict(color="#0f172a"),
                       gridcolor="rgba(200,200,200,0.3)", range=[0, 2600]),
            yaxis=dict(title=dict(text="Avg lead time (days)", font=dict(color="#0f172a", size=12)),
                       color="#0f172a", tickfont=dict(color="#0f172a"),
                       gridcolor="rgba(200,200,200,0.3)", range=[2, 8]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                        font=dict(size=11, color="#0f172a")),
            annotations=[dict(
                text="Simulated · not real data",
                xref="paper", yref="paper", x=0.99, y=0.01,
                xanchor="right", yanchor="bottom",
                font=dict(size=10, color="#64748b"), showarrow=False,
            )],
        )

        # ── EVIDENTIAL chart (real data) ──────────────────────────────────────
        fig_actual = go.Figure()

        _colors = {
            "Nearest factory fulfilled":     ("rgba(29,158,117,0.65)",  "#0F6E56"),
            "Non-nearest factory fulfilled": ("rgba(216,90,48,0.65)",   "#993C1D"),
        }
        for _rt, (_fill, _line_col) in _colors.items():
            _sub = _agg[_agg["Routing"] == _rt]
            if _sub.empty:
                continue
            fig_actual.add_trace(go.Scatter(
                x=_sub["Distance_mi"], y=_sub["Avg_Lead_Time"],
                mode="markers", name=_rt,
                marker=dict(color=_fill, size=np.sqrt(_sub["Shipments"]).clip(4, 18),
                            line=dict(width=0)),
                hovertemplate="<b>%{customdata[0]}</b><br>Factory: %{customdata[1]}<br>"
                              "Distance: %{x:,.0f} mi<br>Avg lead time: %{y:.1f}d<br>"
                              "Orders: %{customdata[2]}<extra></extra>",
                customdata=list(zip(_sub["State"], _sub["Factory"], _sub["Shipments"])),
            ))
            _x = _sub["Distance_mi"].values
            _y = _sub["Avg_Lead_Time"].values
            if len(_x) > 1:
                _m, _b = np.polyfit(_x, _y, 1)
                _xl = np.linspace(_x.min(), _x.max(), 100)
                fig_actual.add_trace(go.Scatter(
                    x=_xl, y=_m * _xl + _b, mode="lines",
                    line=dict(color=_line_col, width=2, dash="dash"), showlegend=False,
                ))

        fig_actual.update_layout(
            **PLOTLY_THEME, height=400,
            title=dict(
                text=f"Real data — nearest r = {_r_nearest:.2f}  |  non-nearest r = {_r_nonnear:.2f}  (both flat)",
                font=dict(size=12, color="#0f172a"), x=0,
            ),
            xaxis=dict(title=dict(text="Distance from factory (miles)", font=dict(color="#0f172a", size=12)),
                       color="#0f172a", tickfont=dict(color="#0f172a"),
                       gridcolor="rgba(200,200,200,0.3)", range=[0, 2600]),
            yaxis=dict(title=dict(text="Avg lead time (days)", font=dict(color="#0f172a", size=12)),
                       color="#0f172a", tickfont=dict(color="#0f172a"),
                       gridcolor="rgba(200,200,200,0.3)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                        font=dict(size=11, color="#0f172a")),
        )

        with _col_concept:
            st.plotly_chart(fig_concept, use_container_width=True)

        with _col_actual:
            st.plotly_chart(fig_actual, use_container_width=True)

        # ── Takeaway callout ──────────────────────────────────────────────────
        st.markdown(
            f"""<div style='font-size:0.82rem;color:#1e293b;line-height:1.7;padding:10px 16px;
            border-left:3px solid #cbd5e1;background:#eef2f7;border-radius:0 6px 6px 0;margin-top:4px;'>
            <b>What this comparison shows:</b> The real data shows both groups flat — nearest r = {_r_nearest:.2f},
            non-nearest r = {_r_nonnear:.2f} — suggesting the bottleneck lies in factory-level processing
            or scheduling, not geography. If routing to nearest factories reduced lead times, we'd expect
            to see the non-nearest group trend upward with distance (left panel).
            </div>""", unsafe_allow_html=True
        )
        st.markdown(
            "<div style='font-size:0.75rem;color:#1e293b;margin-top:14px;margin-bottom:36px;'>"
            "⚠️ Scope: US states only (49 states · 9,994 orders). "
            "Canadian provinces (10 provinces · 200 orders · 2% of total) are excluded — "
            "all factories are US-based and cross-border proximity distances would not reflect actual logistics constraints."
            "</div>", unsafe_allow_html=True
        )

        # ── Dumbbell chart: nearest vs non-nearest per state ─────────────────
        st.markdown(
            "<div style='font-size:12px;font-weight:600;letter-spacing:0.07em;"
            "text-transform:uppercase;color:#1e293b;margin-bottom:0px;'>"
            "📍 Nearest vs Non-nearest Factory — Distance & Lead Time by State"
            "</div>", unsafe_allow_html=True
        )

        st.markdown("<style>[data-testid='stPlotlyChart'] { margin-top: -2rem !important; }</style>", unsafe_allow_html=True)

        # Build one row per state — corrected inclusion logic:
        # Include: states where BOTH nearest AND non-nearest have fulfilled orders (any split).
        # Exclude: states where nearest has zero orders (no lead time baseline).
        # Exclude: states where no non-nearest orders exist (nothing to compare against).
        # Routing share (97/3 or 51/49) does NOT affect inclusion.
        _db_rows = []
        _excl_no_near_data = []

        for state, (slat, slon) in STATE_CENTROIDS.items():
            _state_orders = df[df["State/Province"] == state]
            if _state_orders.empty:
                continue

            _near_fac  = min(FACTORY_COORDS.keys(),
                             key=lambda f: _haversine(FACTORY_COORDS[f]["lat"], FACTORY_COORDS[f]["lon"], slat, slon))
            _near_dist = _haversine(FACTORY_COORDS[_near_fac]["lat"], FACTORY_COORDS[_near_fac]["lon"], slat, slon)

            _near_orders    = _state_orders[_state_orders["Factory"] == _near_fac]
            _nonnear_orders = _state_orders[_state_orders["Factory"] != _near_fac]

            if _near_orders.empty:
                _excl_no_near_data.append(state)
                continue
            if _nonnear_orders.empty:
                continue

            _near_lt    = _near_orders["Lead Time"].mean()
            _nonnear_lt = _nonnear_orders["Lead Time"].mean()

            if pd.isna(_near_lt) or pd.isna(_nonnear_lt):
                continue

            _actual_fac  = _nonnear_orders["Factory"].value_counts().idxmax()
            _actual_dist = _haversine(FACTORY_COORDS[_actual_fac]["lat"], FACTORY_COORDS[_actual_fac]["lon"], slat, slon)                            if _actual_fac in FACTORY_COORDS else _near_dist
            _near_pct    = round(len(_near_orders) / len(_state_orders) * 100)

            _db_rows.append({
                "State":          state,
                "Near_Factory":   _near_fac,
                "Near_Dist":      round(_near_dist, 0),
                "Near_LT":        round(_near_lt, 2),
                "Near_Pct":       _near_pct,
                "Actual_Factory": _actual_fac,
                "Actual_Dist":    round(_actual_dist, 0),
                "Nonnear_LT":     round(_nonnear_lt, 2),
                "Nonnear_Pct":    100 - _near_pct,
                "LT_Gap":         round(_nonnear_lt - _near_lt, 2),
            })

        _db_df = pd.DataFrame(_db_rows)

        if not _db_df.empty:
            _db_df = _db_df.sort_values("LT_Gap", ascending=True).reset_index(drop=True)
            _db_df_diff = _db_df.copy()

            fig_db = go.Figure()

            # Connector lines
            for _, r in _db_df_diff.iterrows():
                _line_col = "rgba(239,68,68,0.25)" if r["LT_Gap"] <= 0 else "rgba(203,213,225,0.5)"
                fig_db.add_trace(go.Scatter(
                    x=[r["Near_LT"], r["Nonnear_LT"]],
                    y=[r["State"], r["State"]],
                    mode="lines",
                    line=dict(color=_line_col, width=2),
                    showlegend=False, hoverinfo="skip",
                ))

            # Nearest factory dots (teal)
            fig_db.add_trace(go.Scatter(
                x=_db_df_diff["Near_LT"],
                y=_db_df_diff["State"],
                mode="markers",
                name="Nearest factory",
                marker=dict(color="rgba(29,158,117,0.85)", size=10, line=dict(width=0)),
                hovertemplate="<b>%{y}</b><br>Nearest: %{customdata[0]}<br>"
                              "Distance: %{customdata[1]:,.0f} mi<br>"
                              "Orders via nearest: %{customdata[2]}%<br>"
                              "Avg lead time: %{x:.1f}d<extra></extra>",
                customdata=list(zip(_db_df_diff["Near_Factory"], _db_df_diff["Near_Dist"], _db_df_diff["Near_Pct"])),
            ))

            # Non-nearest avg dots (coral)
            fig_db.add_trace(go.Scatter(
                x=_db_df_diff["Nonnear_LT"],
                y=_db_df_diff["State"],
                mode="markers",
                name="Non-nearest factory (avg)",
                marker=dict(color="rgba(216,90,48,0.85)", size=10, line=dict(width=0)),
                hovertemplate="<b>%{y}</b><br>Dominant non-nearest: %{customdata[0]}<br>"
                              "Distance: %{customdata[1]:,.0f} mi<br>"
                              "Orders via non-nearest: %{customdata[2]}%<br>"
                              "Avg lead time: %{x:.1f}d<extra></extra>",
                customdata=list(zip(_db_df_diff["Actual_Factory"], _db_df_diff["Actual_Dist"], _db_df_diff["Nonnear_Pct"])),
            ))

            # Highlight states where non-nearest is faster (red alarm)
            _alarm = _db_df_diff[_db_df_diff["LT_Gap"] <= 0]
            if not _alarm.empty:
                fig_db.add_trace(go.Scatter(
                    x=_alarm["Nonnear_LT"],
                    y=_alarm["State"],
                    mode="markers",
                    marker=dict(color="rgba(239,68,68,0.0)", size=18,
                                line=dict(color="rgba(239,68,68,0.7)", width=2)),
                    showlegend=False, hoverinfo="skip",
                    name="Non-nearest faster",
                ))

            _n_alarm = int((_db_df_diff["LT_Gap"] <= 0).sum())
            fig_db.update_layout(
                **PLOTLY_THEME,
                height=max(420, len(_db_df_diff) * 18 + 80),
                title=dict(
                    text=f"Lead time: nearest vs non-nearest factory — avg per state  ·  {len(_db_df_diff)} of 49 US states  ·  "
                         f"{_n_alarm} states where non-nearest is faster or equal",
                    font=dict(size=12, color="#0f172a"), x=0,
                ),
                xaxis=dict(title=dict(text="Avg lead time (days)", font=dict(color="#0f172a", size=12)), color="#0f172a", tickfont=dict(color="#0f172a"),
                           gridcolor="rgba(200,200,200,0.3)"),
                yaxis=dict(title="", color="#0f172a", tickfont=dict(size=10, color="#0f172a"),
                           gridcolor="rgba(200,200,200,0.15)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                            font=dict(size=11, color="#0f172a")),
            )
            st.plotly_chart(fig_db, use_container_width=True)

            # Callout
            _pct_alarm = round(_n_alarm / len(_db_df_diff) * 100)
            st.markdown(
                f"""<div style='font-size:0.82rem;color:#1e293b;line-height:1.7;padding:10px 16px;
                border-left:3px solid #ef4444;background:#fef2f2;border-radius:0 6px 6px 0;margin-top:4px;'>
                <b>Performance signal:</b> In {_n_alarm} states ({_pct_alarm}%), the non-nearest factory
                fulfils orders at the same speed or faster than the nearest factory — despite covering
                significantly more distance. This suggests the nearest factory's proximity advantage
                is not translating into faster delivery, pointing to factory-level processing or
                capacity constraints worth investigating.
                </div>""", unsafe_allow_html=True
            )
            _excl_list = ", ".join(sorted(_excl_no_near_data))
            st.markdown(
                f"""<div style='font-size:0.75rem;color:#334155;line-height:1.7;margin-top:8px;
                padding:8px 14px;background:#eef2f7;border-radius:6px;border:1px solid #cbd5e1;'>
                <b>{len(_excl_no_near_data)} of 49 US states excluded</b> — the nearest factory has
                no fulfilled orders in these states, so no lead time baseline exists for comparison.
                (<span style='color:#334155;'>{_excl_list}</span>)
                </div>""", unsafe_allow_html=True
            )
            st.markdown(
                "<div style='font-size:0.75rem;color:#1e293b;margin-top:14px;'>"
                "⚠️ Scope: US states only (49 states · 9,994 orders). "
                "Canadian provinces (10 provinces · 200 orders · 2% of total) are excluded — "
                "all factories are US-based and cross-border proximity distances would not reflect actual logistics constraints."
                "</div>", unsafe_allow_html=True
            )

    st.markdown("<div style='margin-top: 48px;'></div>", unsafe_allow_html=True)
    # ── Route Intelligence Assessment Cards ───────────────────────────────────
    st.markdown('<div class="section-header">Strategic Assessment</div>', unsafe_allow_html=True)

    _filters_active = (
        region_sel != "All" or
        ship_mode_sel != "All" or
        factory_sel != "All" or
        start_date != min_date or
        end_date != max_date
    )
    if _filters_active:
        st.markdown(
            "<p style='font-size:0.8rem; color:#b45309; margin: -8px 0 12px 0;'>"
            "📌 <i>Assessment reflects full portfolio — unaffected by filter selection</i></p>",
            unsafe_allow_html=True,
        )

    _top1        = route_stats.nlargest(1, "Efficiency_Score").iloc[0]
    _bottom1     = route_stats.nsmallest(1, "Efficiency_Score").iloc[0]
    _high_vol    = route_stats.nlargest(1, "Shipments").iloc[0]
    _high_delay  = route_stats.nlargest(1, "Delay_Rate").iloc[0]
    _score_spread = route_stats["Efficiency_Score"].max() - route_stats["Efficiency_Score"].min()
    _n_routes    = len(route_stats)
    _avg_lt      = route_stats["Avg_Lead_Time"].mean()

    _heat_stack  = pivot_heat.stack().reset_index()
    _heat_stack.columns = ["Factory", "Region", "AvgLT"]
    _heat_worst  = _heat_stack.loc[_heat_stack["AvgLT"].idxmax()]
    _heat_best   = _heat_stack.loc[_heat_stack["AvgLT"].idxmin()]

    _vol_q25           = route_stats["Shipments"].quantile(0.25)
    _low_vol_avg_score  = route_stats[route_stats["Shipments"] <= _vol_q25]["Efficiency_Score"].mean()
    _high_vol_avg_score = route_stats[route_stats["Shipments"] >  _vol_q25]["Efficiency_Score"].mean()
    _n_low_vol         = int((route_stats["Shipments"] <= _vol_q25).sum())

    _total_orders  = len(df)
    _total_revenue = df['Sales'].sum()
    _total_profit  = df['Gross Profit'].sum()
    _avg_lead_time = df['Lead Time'].mean()
    _delay_rate    = df['Is Delayed'].mean() * 100
    _active_routes = df['RouteRegion'].nunique()
    _margin_pct    = (_total_profit / _total_revenue * 100) if _total_revenue > 0 else 0

    _summary_html = f"""
    <style>
    .kpi-narrative-card {{
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #2563eb;
        border-radius: 8px;
        padding: 22px 28px;
        margin: 8px 0 28px 0;
        font-size: 0.875rem;
        color: #374151;
        line-height: 1.75;
    }}
    .kpi-narrative-title {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1rem;
        font-weight: 700;
        color: #1d4ed8;
        margin-bottom: 14px;
    }}
    .kpi-narrative-card p {{
        margin: 0 0 10px 0;
    }}
    .kpi-narrative-card p:last-child {{ margin-bottom: 0; }}
    .kpi-narrative-card b {{ color: #111827; }}
    </style>

    <div class="kpi-narrative-card">
      <div class="kpi-narrative-title">📊 Network Performance Summary</div>
      <p>
        The network processed <b>{_total_orders:,} orders</b> across <b>{_active_routes} active routes</b>,
        generating <b>${_total_revenue:,.0f} in revenue</b> and <b>${_total_profit:,.0f} in gross profit</b>
        — a margin of <b>{_margin_pct:.1f}%</b>. These headline numbers reflect a commercially healthy
        operation, but operational efficiency tells a more layered story.
      </p>
      <p>
        At an average lead time of <b>{_avg_lead_time:.1f} days</b>, fulfilment speed sits within a
        reasonable band for the network's ship mode mix — however, a <b>{_delay_rate:.1f}% delay rate</b>
        signals that nearly one in four shipments is breaching the threshold, a level that requires
        targeted intervention before it begins to impact service levels.
      </p>
      <p>
        The combination of strong revenue, a healthy margin, and an elevated delay rate points to
        a network that is financially productive but operationally uneven. Addressing delay
        concentration in underperforming lanes — without disrupting the high-volume routes that
        anchor revenue — represents the clearest path to improving overall network health.
      </p>
    </div>
    """
    st.markdown(_summary_html, unsafe_allow_html=True)

    # ── Proximity vs Performance card ─────────────────────────────────────────
    try:
        _prox_pct = round(_n_alarm / len(_db_df_diff) * 100)
        _prox_card_html = f"""
        <div class="kpi-narrative-card" style="border-left-color:#7c3aed;">
          <div class="kpi-narrative-title" style="color:#6d28d9;">🔍 The Proximity–Performance Divergence</div>
          <p>
            In <b>{_n_alarm} of {len(_db_df_diff)} states ({_prox_pct}%)</b>, non-nearest factories match
            or outperform nearest factories on average lead time — despite the added distance. Distance-to-lead-time
            correlations are near-zero for both groups (nearest r = 0.16, non-nearest r = −0.03), indicating
            that <b>operational execution, not geography, is the primary differentiator of fulfilment speed.</b>
          </p>
          <p>
            This has two compounding implications. First, <b>the nearest factory's proximity advantage is not translating into faster delivery</b> — pointing to factory-level processing or capacity constraints that, if addressed, represent the most immediate opportunity for lead time reduction.
            Second, <b>non-nearest factories are delivering at comparable speeds despite the added distance</b>
            — indicating that their operational practices are offsetting the geographic disadvantage. This suggests
            there is untapped potential in the network that, if systematically addressed, could drive meaningful
            lead time reductions across the board.
          </p>
        </div>
        """
        st.markdown(_prox_card_html, unsafe_allow_html=True)
    except Exception:
        pass

    _separately_sentence = (
        "" if _high_delay['RouteRegion'] == _bottom1['RouteRegion']
        else f"Separately, <b>{_high_delay['RouteRegion']}</b> carries the network's highest delay rate at "
             f"<b>{_high_delay['Delay_Rate']:.1%}</b> — the highest-priority route for immediate intervention."
    )

    _var_sorted = route_stats.sort_values("Std_Dev", ascending=False).reset_index(drop=True)
    _var_top    = _var_sorted.iloc[0]
    _var_second = _var_sorted.iloc[1]
    _var_third  = _var_sorted.iloc[2]

    _cards_html = f"""
    <style>
    .assess-grid {{
        display: flex;
        flex-direction: column;
        gap: 16px;
        margin: 8px 0 28px 0;
    }}
    .assess-card {{
        border-radius: 8px;
        padding: 20px 24px;
        border-left: 5px solid transparent;
    }}
    .assess-card.green  {{ background: #f0fdf4; border-left-color: #16a34a; }}
    .assess-card.red    {{ background: #fff7ed; border-left-color: #ea580c; }}
    .assess-card.blue   {{ background: #eff6ff; border-left-color: #2563eb; }}
    .assess-card.amber  {{ background: #fefce8; border-left-color: #ca8a04; }}
    .assess-head {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }}
    .assess-head-icon  {{ font-size: 1.1rem; }}
    .assess-head-title {{
        font-size: 1rem;
        font-weight: 700;
    }}
    .assess-card.green .assess-head-title {{ color: #15803d; }}
    .assess-card.red   .assess-head-title {{ color: #c2410c; }}
    .assess-card.blue  .assess-head-title {{ color: #1d4ed8; }}
    .assess-card.amber .assess-head-title {{ color: #a16207; }}
    .assess-para {{
        font-size: 0.875rem;
        color: #374151;
        line-height: 1.65;
        margin: 0 0 8px 0;
    }}
    .assess-para:last-child {{ margin-bottom: 0; }}
    .assess-para b {{ color: #111827; }}
    </style>

    <div class="assess-grid">

      <div class="assess-card blue">
        <div class="assess-head">
          <span class="assess-head-icon">🗺️</span>
          <span class="assess-head-title">Lead Time Gaps Across the Network</span>
        </div>
        <p class="assess-para">
          Delivery speed is far from uniform across the network. <b>{_heat_worst['Factory']} → {_heat_worst['Region']}</b> is
          the slowest lane at <b>{_heat_worst['AvgLT']:.1f} days</b>, while <b>{_heat_best['Factory']} → {_heat_best['Region']}</b>
          leads at <b>{_heat_best['AvgLT']:.1f} days</b> — a <b>{_heat_worst['AvgLT'] - _heat_best['AvgLT']:.1f}-day gap</b>
          between the two extremes within the same network.
        </p>
        <p class="assess-para">
          Critically, these disparities are lane-specific rather than factory-wide — the same factory can perform
          strongly in one region while lagging in another. The implication is clear: optimising carrier contracts and regional fulfilment capacity at the lane level
          will deliver more measurable gains than any factory-wide initiative.
        </p>
      </div>

      <div class="assess-card amber">
        <div class="assess-head">
          <span class="assess-head-icon">📊</span>
          <span class="assess-head-title">Volume Masks Efficiency Gaps</span>
        </div>
        <p class="assess-para">
          Shipment volume alone does not tell the full story — a closer look at route volume reveals a clear efficiency divide. The <b>{_n_low_vol}</b> lowest-volume
          routes average just <b>{_low_vol_avg_score:.0f}/100</b> in efficiency,
          compared to <b>{_high_vol_avg_score:.0f}/100</b> for higher-volume lanes. These low-volume routes
          also carry disproportionate delay risk — fragile lanes where even a small number of delayed
          shipments can materially spike the delay rate.
        </p>
        <p class="assess-para">
          High-volume routes, while more stable, are not without opportunity. The busiest lane,
          <b>{_high_vol['RouteRegion']}</b>, moves <b>{int(_high_vol['Shipments']):,} shipments</b> at an
          efficiency score of <b>{_high_vol['Efficiency_Score']:.0f}/100</b> — solid, but with clear headroom
          to improve. As the highest-volume lane in the network, even marginal performance improvements here would compound into significant gains overall.
        </p>
      </div>

      <div class="assess-card {'red' if _var_top['Std_Dev'] > 4 else 'amber'}">
        <div class="assess-head">
          <span class="assess-head-icon">📉</span>
          <span class="assess-head-title">Route Reliability — Beyond Average Lead Time</span>
        </div>
        <p class="assess-para">
          Average lead time provides an incomplete characterisation of route reliability.
          <b>{_var_top['RouteRegion']}</b> records a standard deviation of
          <b>{_var_top['Std_Dev']:.1f} days</b> — the highest across the network —
          reflecting substantial intra-route variability in individual shipment durations.
          This level of dispersion identifies the route as operationally unpredictable,
          independent of its mean lead time performance.
        </p>
        <p class="assess-para">
          The remaining routes exhibit considerably lower dispersion, with no other route exceeding
          <b>{_var_second['Std_Dev']:.1f} days</b> standard deviation — reinforcing that
          <b>{_var_top['RouteRegion']}</b> represents an isolated reliability concern
          rather than a network-wide pattern.
        </p>
      </div>

      <div class="assess-card green">
        <div class="assess-head">
          <span class="assess-head-icon">📋</span>
          <span class="assess-head-title">Network Performance Spread</span>
        </div>
        <p class="assess-para">
          Across <b>{_n_routes}</b> factory-region routes, efficiency scores span the complete efficiency range,
          set against a network average lead time of <b>{_avg_lt:.1f} days</b>. The range itself tells the
          story — there is no single network-wide problem, but rather a set of specific underperforming
          lanes pulling the average down. Targeted, lane-level intervention is the most effective course of action.
        </p>
        <p class="assess-para">
          <b>{_top1['RouteRegion']}</b> stands as the network's top-ranked route at
          <b>{_top1['Efficiency_Score']:.0f}/100</b> ({_top1['Avg_Lead_Time']:.1f}d avg,
          {_top1['Delay_Rate']:.1%} delay rate) — the benchmark against which carrier and ship-mode
          decisions should be measured.
          At the other end, <b>{_bottom1['RouteRegion']}</b> ranks lowest
          at <b>{_bottom1['Efficiency_Score']:.0f}/100</b> ({_bottom1['Avg_Lead_Time']:.1f}d,
          {_bottom1['Delay_Rate']:.1%} delay rate) and warrants immediate review.
        </p>
        {"<p class='assess-para'>" + _separately_sentence + "</p>" if _separately_sentence else ""}
      </div>

    </div>
    """
    st.markdown(_cards_html, unsafe_allow_html=True)

# ── TAB 2: Geographic Map ─────────────────────────────────────────────────────
with tabs[1]:
    map_metric = st.selectbox(
        "Metric",
        ["Avg_Lead_Time", "Delay_Rate", "Shipments", "Total_Sales"],
        format_func=lambda x: {
            "Avg_Lead_Time": "Avg Lead Time (days)",
            "Delay_Rate": "Delay Rate",
            "Shipments": "Shipment Volume",
            "Total_Sales": "Total Sales ($)",
        }[x],
    )

    label_map = {
        "Avg_Lead_Time": "Avg Lead Time",
        "Delay_Rate": "Delay Rate",
        "Shipments": "Shipments",
        "Total_Sales": "Total Sales",
    }

    st.markdown('<div class="section-header">Shipping Efficiency Heatmap</div>', unsafe_allow_html=True)

    if map_metric == "Avg_Lead_Time":
        color_scale = "Blues"
    elif map_metric == "Delay_Rate":
        color_scale = "RdYlGn_r"
    elif map_metric == "Shipments":
        color_scale = "Greens"
    else:  # Total_Sales
        color_scale = "Purples"

    CA_CODES = {"ON","QC","AB","BC","MB","PE","NB","NS","NL","SK"}
    PROVINCE_NAME_MAP = {
        "Ontario":"ON","Quebec":"QC","Alberta":"AB","British Columbia":"BC",
        "Manitoba":"MB","Prince Edward Island":"PE","New Brunswick":"NB",
        "Nova Scotia":"NS","Newfoundland and Labrador":"NL","Saskatchewan":"SK",
    }
    REVERSE_PROV = {v: k for k, v in PROVINCE_NAME_MAP.items()}

    us_stats = state_stats[~state_stats["State Code"].isin(CA_CODES)].copy()
    ca_stats = state_stats[state_stats["State Code"].isin(CA_CODES)].copy()
    ca_stats["Province_Name"] = ca_stats["State Code"].map(REVERSE_PROV)

    # Shared color range across both maps
    _all_vals = pd.concat([us_stats[map_metric], ca_stats[map_metric]]).dropna()
    _zmin, _zmax = _all_vals.min(), _all_vals.max()
    # Boost color intensity for volume/sales metrics so sparse regions are still visible
    if map_metric in ["Shipments", "Total_Sales"]:
        _zmin = max(0, _zmin - (_zmax - _zmin) * 0.7)
    # Avg Lead Time: use actual data minimum for natural color range
    elif map_metric == "Avg_Lead_Time":
        pass  # _zmin stays at actual data minimum

    _MAP_MARGIN = {"r": 0, "t": 10, "l": 10, "b": 0}
    _US_TITLE_PAD = {"t": 30}
    _COLORBAR   = dict(
        thickness=14, len=0.5, y=0.5, yanchor="middle", x=0.88,
        title=dict(side="right", font=dict(size=11), text=""),
        tickfont=dict(size=10),
    )

    map_col1, map_col2 = st.columns([6, 5])

    # ── US Map (left column) ──────────────────────────────────────────────────
    with map_col1:
        fig_us = px.choropleth(
            us_stats,
            locations="State Code",
            locationmode="USA-states",
            color=map_metric,
            hover_name="State/Province",
            hover_data={
                "Shipments": ":,",
                "Avg_Lead_Time": ":.1f",
                "Delay_Rate": ":.1%",
                "Total_Sales": ":$,.0f",
            },
            color_continuous_scale=color_scale,
            scope="usa",
            labels={map_metric: label_map[map_metric]},
        )
        fig_us.update_layout(
            **PLOTLY_THEME,
            title=dict(text=""),
            height=380,
            margin=_MAP_MARGIN,
            coloraxis_cmin=_zmin,
            coloraxis_cmax=_zmax,
            coloraxis_colorbar={**_COLORBAR, "title": dict(text=label_map[map_metric], side="right", font=dict(size=11)),
                                 **({"tickformat": ".0%"} if map_metric == "Delay_Rate" else {})},
            geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="#1a1f35", landcolor="#1e2640"),
        )
        st.plotly_chart(fig_us, use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            f"""<div style="text-align:center; margin-top:-60px; padding-bottom:8px; padding-right:140px;">
                <span style="background:#eef2ff; border-radius:6px; padding:6px 14px;
                    font-size:0.82rem; color:#374151; line-height:1.4;">
                    🗽 <b>{label_map[map_metric]} by US State</b>
                </span>
            </div>""",
            unsafe_allow_html=True,
        )

    # ── Canadian Province Map (right column) ──────────────────────────────────
    with map_col2:
        if ca_stats.empty:
            st.info("No Canadian province data available.")
        else:
            st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)
            import plotly.graph_objects as _go
            import plotly.colors as _pc
            _ca = ca_stats.copy().dropna(subset=[map_metric])
            _total_ship = _ca["Shipments"].sum()
            _labels  = ["Canada"] + _ca["Province_Name"].tolist()
            _parents = [""] + ["Canada"] * len(_ca)
            _values  = [0] + _ca["Shipments"].tolist()
            _norm = (_ca[map_metric] - _ca[map_metric].min()) / (_ca[map_metric].max() - _ca[map_metric].min() + 1e-9)
            _colors = ["rgba(0,0,0,0)"] + [
                _pc.sample_colorscale(color_scale, float(v))[0] for v in _norm
            ]
            # Per-tile text color: black for light backgrounds, white for dark
            _text_colors = ["white"] + [
                "black" if float(v) < 0.45 else "white" for v in _norm
            ]
            _customs = [
                [row["State/Province"], row["Shipments"], row["Shipments"]/_total_ship*100,
                 row["Avg_Lead_Time"], row["Delay_Rate"], row["Total_Sales"]]
                for _, row in _ca.iterrows()
            ]
            fig_ca = _go.Figure(_go.Treemap(
                labels=_labels,
                parents=_parents,
                values=_values,
                marker=dict(
                    colors=_colors,
                    line=dict(width=2, color="white"),
                    pad=dict(t=0, l=0, r=0, b=0),
                ),
                customdata=[[None]*6] + _customs,
                texttemplate="<b>%{label}</b><br>%{customdata[1]:,} shipments<br>%{customdata[2]:.1f}% of CA total",
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    f"{label_map[map_metric]}: %{{customdata[3]:.2f}}<br>"
                    "Shipments: %{customdata[1]:,}<br>"
                    "Delay Rate: %{customdata[4]:.1%}<br>"
                    "Total Sales: $%{customdata[5]:,.0f}<extra></extra>"
                ),
                textfont=dict(size=12, color=_text_colors),
                tiling=dict(pad=3),
                pathbar=dict(visible=False),
            ))
            fig_ca.update_traces(marker_depthfade=False, marker_line=dict(width=2, color="white"))
            import plotly.graph_objects as _pgo
            _cb_vals = list(__import__("numpy").linspace(_zmin, _zmax, 50))
            fig_ca.add_trace(_pgo.Scatter(
                x=[None]*50, y=[None]*50,
                mode="markers",
                marker=dict(
                    colorscale=color_scale,
                    color=_cb_vals,
                    cmin=_zmin, cmax=_zmax,
                    showscale=True,
                    colorbar=dict(
                        thickness=14, len=0.68, y=0.5, yanchor="middle",
                        title=dict(text=label_map[map_metric], side="right", font=dict(size=11, color="#1a1a2e")),
                        tickfont=dict(size=10, color="#1a1a2e"),
                        tickformat=".0%" if map_metric == "Delay_Rate" else "",
                        x=1.02,
                    ),
                ),
                showlegend=False,
            ))
            fig_ca.update_layout(
                **PLOTLY_THEME,
                title=dict(text=""),
                height=280,
                margin=dict(r=90, t=30, l=10, b=0),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
            )
            st.plotly_chart(fig_ca, use_container_width=True)
            st.markdown(
                f"""<div style="text-align:center; margin-top:4px; padding-right:80px;">
                    <span style="background:#eef2ff; border-radius:6px; padding:6px 14px;
                        font-size:0.82rem; color:#374151; line-height:1.4;">
                        🍁 <b>{label_map[map_metric]} by Canadian Province</b>
                    </span>
                </div>""",
                unsafe_allow_html=True,
            )

    # ── Insight banners below both maps ───────────────────────────────────────
    _us_top       = us_stats.nlargest(1, "Shipments").iloc[0]
    _us_top_pct   = _us_top["Shipments"] / us_stats["Shipments"].sum() * 100
    _ca_top       = ca_stats.nlargest(1, "Shipments").iloc[0] if not ca_stats.empty else None

    # ── Region Metrics Summary Table ──────────────────────────────────────────
    st.markdown('<div class="section-header">Region Metrics Summary</div>', unsafe_allow_html=True)

    _region_table = state_stats.copy()
    _region_table["Country"] = _region_table["State Code"].apply(
        lambda c: "🍁 Canadian Province" if c in CA_CODES else "🗽 US State"
    )
    _region_table = _region_table.rename(columns={"State/Province": "Region"})[[
        "Country", "Region", "Avg_Lead_Time", "Delay_Rate", "Shipments", "Total_Sales"
    ]].sort_values("Shipments", ascending=False).reset_index(drop=True)
    _region_table.columns = ["Country", "Region", "Avg Lead Time (d)", "Delay Rate", "Shipments", "Total Sales ($)"]

    _styled_region = (
        _region_table.style
        .format({
            "Avg Lead Time (d)": "{:.1f}",
            "Delay Rate": "{:.1%}",
            "Shipments": "{:,}",
            "Total Sales ($)": "${:,.0f}",
        })
        .background_gradient(subset=["Avg Lead Time (d)"], cmap="Blues",
                              vmin=state_stats_all["Avg_Lead_Time"].min(), vmax=state_stats_all["Avg_Lead_Time"].max())
        .background_gradient(subset=["Delay Rate"], cmap="RdYlGn_r",
                              vmin=state_stats_all["Delay_Rate"].min(), vmax=state_stats_all["Delay_Rate"].max())
        .background_gradient(subset=["Shipments"], cmap="Greens",
                              vmin=state_stats_all["Shipments"].min(), vmax=state_stats_all["Shipments"].max())
        .background_gradient(subset=["Total Sales ($)"], cmap="Purples",
                              vmin=state_stats_all["Total_Sales"].min(), vmax=state_stats_all["Total_Sales"].max())
    )
    st.dataframe(_styled_region, use_container_width=True, hide_index=True)

    # ── Nearest Factory per State ──────────────────────────────────────────────
    # ── Factory Shipment Volume Breakdown ─────────────────────────────────────
    st.markdown('<div class="section-header">🏭 Factory Shipment Volume Breakdown</div>', unsafe_allow_html=True)

    _fac_vol = (
        df.groupby("Factory")
        .agg(Shipments=("Order ID", "count"),
             Avg_Lead_Time=("Lead Time", "mean"),
             Delay_Rate=("Is Delayed", "mean"),
             Total_Sales=("Sales", "sum"))
        .reset_index()
        .sort_values("Shipments", ascending=False)
    )
    _fac_total = _fac_vol["Shipments"].sum()
    _fac_vol["Share (%)"] = (_fac_vol["Shipments"] / _fac_total * 100).round(1)

    _fv1, _fv2 = st.columns([1, 1])

    with _fv1:
        # Donut chart — shipment share
        # Pull small slices out more so they're visible; pull the tiniest slice even further
        _pulls = [
            0.25 if v < _fac_total * 0.005 else (0.12 if v < _fac_total * 0.05 else 0.03)
            for v in _fac_vol["Shipments"]
        ]
        _line_colors = "white"
        _line_widths = 1
        _fig_donut = go.Figure(go.Pie(
            labels=_fac_vol["Factory"],
            values=_fac_vol["Shipments"],
            hole=0.55,
            texttemplate="<b>%{label}</b><br>%{percent}",
            hovertemplate="<b>%{label}</b><br>Shipments: %{value:,}<br>Share: %{percent}<extra></extra>",
            marker=dict(colors=["#f4a444","#e05c5c","#5b8dee","#4caf91","#5b21b6"],
                        line=dict(color=_line_colors, width=_line_widths)),
            textfont=dict(size=10, color="#1a1a2e"),
            textposition="outside",
            pull=_pulls,
            domain=dict(x=[0.05, 0.95], y=[0.15, 0.95]),
        ))
        _fig_donut.update_layout(
            **PLOTLY_THEME,
            title=dict(text="Shipment Share by Factory", font=dict(size=13), x=0.03),
            height=420,
            margin=dict(t=50, b=20, l=80, r=80),
            showlegend=True,
            legend=dict(
                orientation="h", x=0.5, y=-0.05, xanchor="center", yanchor="top",
                font=dict(size=11, color="#1a1a2e"),
                bgcolor="rgba(0,0,0,0)",
            ),
            annotations=[dict(text=f"<b>{_fac_total:,}</b><br>total", x=0.5, y=0.5,
                              font=dict(size=13, color="#1a1a2e"), showarrow=False)],
        )
        # Show a compact label for the tiniest slice (Sugar Shack) instead of hiding it
        _fig_donut.update_traces(
            texttemplate=[
                "<b>%{label}</b> %{percent}" if v < _fac_total * 0.005 else "<b>%{label}</b><br>%{percent}"
                for v in _fac_vol["Shipments"]
            ],
            textfont=dict(size=[
                9 if v < _fac_total * 0.005 else 10 for v in _fac_vol["Shipments"]
            ]),
        )
        # Small slices shown in legend below
        st.plotly_chart(_fig_donut, use_container_width=True, config={"displayModeBar": False})

    with _fv2:
        # Grouped bar — shipments + avg lead time
        _fig_bar = go.Figure()
        _fig_bar.add_trace(go.Bar(
            x=_fac_vol["Factory"],
            y=_fac_vol["Shipments"],
            name="Shipments",
            marker_color="#f4a444",
            hovertemplate="<b>%{x}</b><br>Shipments: %{y:,}<extra></extra>",
            yaxis="y1",
        ))
        _fig_bar.add_trace(go.Scatter(
            x=_fac_vol["Factory"],
            y=_fac_vol["Avg_Lead_Time"],
            name="Avg Lead Time (days)",
            mode="lines+markers",
            marker=dict(size=8, color="#e05c5c"),
            line=dict(color="#e05c5c", width=2),
            hovertemplate="<b>%{x}</b><br>Avg Lead Time: %{y:.2f}d<extra></extra>",
            yaxis="y2",
        ))
        _fig_bar.update_layout(
            **PLOTLY_THEME,
            title=dict(text="Shipments vs Avg Lead Time per Factory", font=dict(size=13), x=0.03),
            height=400,
            margin=dict(t=50, b=80, l=10, r=50),
            yaxis=dict(title=dict(text="Shipments", font=dict(color="#f4a444")),
                       tickfont=dict(color="#1a1a2e"), dtick=1000),
            yaxis2=dict(title=dict(text="Avg Lead Time (days)", font=dict(color="#e05c5c")),
                        tickfont=dict(color="#1a1a2e"), overlaying="y", side="right",
                        showgrid=False),
            legend=dict(orientation="h", y=-0.38, x=0.5, xanchor="center", font=dict(color="#1a1a2e")),
            bargap=0.3,
        )
        st.plotly_chart(_fig_bar, use_container_width=True, config={"displayModeBar": False})

    # Summary insight banner
    _top_factory = _fac_vol.iloc[0]
    _top_share   = _top_factory["Share (%)"]
    _top_lt      = _top_factory["Avg_Lead_Time"]
    st.markdown(
        f"""<div style="background:#fff8ee; border-left:4px solid #f4a444; border-radius:6px;
            padding:14px 18px; font-size:0.85rem; color:#374151; margin-bottom:12px; line-height:1.6;">
            <span style="font-size:1rem;">⚠️</span>
            <b style="color:#b45309;">Volume Concentration Risk:</b>
            <b>{_top_factory['Factory']}</b> accounts for <b>{_top_share}%</b> of total shipments
            at an average lead time of <b>{_top_lt:.2f} days</b>. This level of dependency on a single
            facility creates supply chain vulnerability — any disruption at this factory would impact
            the majority of outbound orders.
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-header">📍 Factory Network — Nearest per State &amp; Locations</div>', unsafe_allow_html=True)

    _map_col1, _map_col2 = st.columns(2)

    def _hav(lat1, lon1, lat2, lon2):
        R = 3958.8
        φ1, φ2 = np.radians(lat1), np.radians(lat2)
        dφ, dλ = np.radians(lat2-lat1), np.radians(lon2-lon1)
        a = np.sin(dφ/2)**2 + np.cos(φ1)*np.cos(φ2)*np.sin(dλ/2)**2
        return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    # Build reverse map: factory → set of products it makes
    _FACTORY_PRODUCTS = {}
    for prod, fac in PRODUCT_FACTORY.items():
        _FACTORY_PRODUCTS.setdefault(fac, set()).add(prod)

    _nearest_rows = []
    for state, (slat, slon) in STATE_CENTROIDS.items():
        _s_data = state_stats[state_stats["State/Province"] == state]
        if _s_data.empty:
            continue
        _dists = {f: _hav(fc["lat"], fc["lon"], slat, slon) for f, fc in FACTORY_COORDS.items()}
        _nearest = min(_dists, key=_dists.get)
        # Most common factory actually serving this state
        _actual = df[df["State/Province"] == state]["Factory"].mode()
        _actual_factory = _actual.iloc[0] if not _actual.empty else "Unknown"

        # Mismatch reason logic
        if _nearest == _actual_factory:
            _mismatch = "✅ No"
            _reason = "—"
        else:
            _mismatch = "⚠️ Yes"
            # Top product ordered by this state
            _top_product = df[df["State/Province"] == state]["Product Name"].mode()
            if not _top_product.empty:
                _top_prod_name = _top_product.iloc[0]
                _required_factory = PRODUCT_FACTORY.get(_top_prod_name)
                # If nearest factory can't make the top product → product-driven
                if _required_factory and _required_factory != _nearest:
                    _reason = f"📦 Product-Driven (top product: {_top_prod_name.split(' - ')[-1] if ' - ' in _top_prod_name else _top_prod_name})"
                else:
                    _reason = "🔀 Route-Driven"
            else:
                _reason = "🔀 Route-Driven"

        _nearest_rows.append({
            "State": state,
            "State Code": STATE_ABBREV.get(state, ""),
            "Nearest Factory": _nearest,
            "Distance (mi)": round(_dists[_nearest], 0),
            "Actual Factory": _actual_factory,
            "Mismatch": _mismatch,
            "Mismatch Reason": _reason,
        })
    _nearest_df = pd.DataFrame(_nearest_rows)

    if True:
        with _map_col1:
        # Choropleth: nearest factory per state
            _color_map_f = {f: c for f, c in zip(
                list(FACTORY_COORDS.keys()),
                ["#f59e0b", "#38bdf8", "#34d399", "#f87171", "#a78bfa"]
            )}
            _nearest_df["Color"] = _nearest_df["Nearest Factory"].map(_color_map_f)
            fig_nearest = px.choropleth(
                _nearest_df, locations="State Code", locationmode="USA-states",
                color="Nearest Factory",
                hover_name="State",
                hover_data={"Distance (mi)": True, "Actual Factory": True, "Mismatch": True, "Mismatch Reason": True, "State Code": False},
                color_discrete_map=_color_map_f,
                scope="usa",
                title="Nearest Factory by Geographic Distance",
            )
            fig_nearest.update_layout(
                height=280,
                margin=dict(r=0, t=10, l=0, b=0),
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(color="#1a1a2e", family="Space Grotesk"),
                legend=dict(font=dict(color="#1a1a2e"), bgcolor="rgba(255,255,255,0.8)"),
                geo=dict(bgcolor="white", landcolor="#f1f5f9",
                lakecolor="#dbeafe", showlakes=True, showcoastlines=True,
                coastlinecolor="#94a3b8", subunitcolor="#cbd5e1", showsubunits=True),
            )
            st.markdown("<p style='font-size:14px;font-weight:600;color:#1a1a2e;margin-bottom:0;'>Nearest Factory by Geographic Distance</p>", unsafe_allow_html=True)
            st.plotly_chart(fig_nearest, use_container_width=True)

        with _map_col2:
            st.markdown("<p style='font-size:14px;font-weight:600;color:#1a1a2e;margin-bottom:0;'>Factory Locations — Shipment Volume &amp; Delay Rate</p>", unsafe_allow_html=True)
            st.markdown(
                "<div style='font-size:0.72rem;color:#475569;margin-bottom:4px;'>"
                "Bubble size = shipment volume &nbsp;·&nbsp; Color = delay rate (green = low · red = high)"
                "</div>", unsafe_allow_html=True
            )

            factory_map_data = pd.DataFrame([
                {
                    "Factory": name,
                    "lat": coords["lat"],
                    "lon": coords["lon"],
                    "Shipments": factory_stats_all.loc[factory_stats_all["Factory"] == name, "Shipments"].values[0]
                                 if name in factory_stats_all["Factory"].values else 0,
                    "Avg_Lead_Time": factory_stats_all.loc[factory_stats_all["Factory"] == name, "Avg_Lead_Time"].values[0]
                                     if name in factory_stats_all["Factory"].values else 0,
                    "Delay_Rate": factory_stats_all.loc[factory_stats_all["Factory"] == name, "Delay_Rate"].values[0]
                                  if name in factory_stats_all["Factory"].values else 0,
                    "Total_Sales": factory_stats_all.loc[factory_stats_all["Factory"] == name, "Total_Sales"].values[0]
                                   if name in factory_stats_all["Factory"].values else 0,
                }
                for name, coords in FACTORY_COORDS.items()
            ])

            import plotly.graph_objects as _fgo
            import plotly.colors as _fpc
            import numpy as _np

            # ── Balanced bubble sizing: sqrt scaling to compress extremes ────────────
            _ship_vals = factory_map_data["Shipments"].values.astype(float)
            _ship_sqrt = _np.sqrt(_ship_vals)
            _size_min, _size_max = 14, 36
            _ship_norm = (_ship_sqrt - _ship_sqrt.min()) / (_ship_sqrt.max() - _ship_sqrt.min() + 1e-9)
            factory_map_data["BubbleSize"] = _size_min + _ship_norm * (_size_max - _size_min)

            # ── Colorbar: use full 0–max range so gradient is distinguishable ────────
            _dr_min_cb = 0.0
            _dr_max_cb = factory_map_data["Delay_Rate"].max()
            _dr_range  = _dr_max_cb - factory_map_data["Delay_Rate"].min() + 1e-9

            fig_factories = _fgo.Figure()

            # ── Label offset direction per factory to avoid overlaps ─────────────────
            _label_pos = {
                "Lot's O' Nuts":    ("bottom center", 0,    -1.5),
                "Wicked Choccy's":  ("bottom center", 0,    -1.5),
                "Sugar Shack":      ("top center",    0,     1.5),
                "Secret Factory":   ("top center",    0,     1.5),
                "The Other Factory":("top center",    0,     1.5),
            }

            for _, row in factory_map_data.iterrows():
                _norm_dr = (row["Delay_Rate"] - factory_map_data["Delay_Rate"].min()) / _dr_range
                _color   = _fpc.sample_colorscale("RdYlGn_r", float(_norm_dr))[0]
                _lpos, _lax, _lay = _label_pos.get(row["Factory"], ("top center", 0, 0.8))

                _is_dimmed = (factory_sel != "All") and (row["Factory"] != factory_sel)
                _marker_opacity = 0.12 if _is_dimmed else 0.90
                _label_color = "#cbd5e1" if _is_dimmed else "#1a1a2e"

                # Main bubble
                fig_factories.add_trace(_fgo.Scattergeo(
                    lat=[row["lat"]],
                    lon=[row["lon"]],
                    mode="markers",
                    marker=dict(
                        size=row["BubbleSize"],
                        color=_color,
                        line=dict(width=2.5, color="white"),
                        opacity=_marker_opacity,
                    ),
                    hovertemplate=(
                        f"<b>🏭 {row['Factory']}</b><br>"
                        f"━━━━━━━━━━━━━━━━<br>"
                        f"📦 Shipments: <b>{int(row['Shipments']):,}</b><br>"
                        f"⏱ Avg Lead Time: <b>{row['Avg_Lead_Time']:.1f}d</b><br>"
                        f"⚠️ Delay Rate: <b>{row['Delay_Rate']:.1%}</b><br>"
                        f"💰 Total Sales: <b>${row['Total_Sales']:,.0f}</b>"
                        "<extra></extra>"
                    ),
                    showlegend=False,
                ))

                # Label as separate trace for better positioning
                fig_factories.add_trace(_fgo.Scattergeo(
                    lat=[row["lat"] + _lay * 1.2],
                    lon=[row["lon"] + _lax * 1.5],
                    mode="text",
                    text=[f"🏭 {row['Factory']}"],
                    textfont=dict(size=12, color=_label_color, family="Space Grotesk"),
                    hoverinfo="skip",
                    showlegend=False,
                ))

            # ── Colorbar trace (full 0–max range) ─────────────────────────────────────
            fig_factories.add_trace(_fgo.Scattergeo(
                lat=[None], lon=[None],
                mode="markers",
                marker=dict(
                    colorscale="RdYlGn_r",
                    color=[_dr_min_cb, _dr_max_cb],
                    cmin=_dr_min_cb, cmax=_dr_max_cb,
                    showscale=True,
                    colorbar=dict(
                        title=dict(text="Delay Rate", side="right", font=dict(size=11, color="#1a1a2e")),
                        tickformat=".0%",
                        tickfont=dict(size=10, color="#1a1a2e"),
                        thickness=14, len=0.55, x=1.01, y=0.6,
                    ),
                ),
                showlegend=False,
            ))

            fig_factories.update_layout(
                height=280,
                margin=dict(r=90, t=10, l=0, b=0),
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(color="#1a1a2e", family="Space Grotesk"),

                geo=dict(
                    scope="usa",
                    bgcolor="white",
                    lakecolor="#dbeafe",
                    landcolor="#f1f5f9",
                    showland=True,
                    showlakes=True,
                    showcoastlines=True,
                    coastlinecolor="#94a3b8",
                    countrycolor="#94a3b8",
                    showsubunits=True,
                    subunitcolor="#cbd5e1",
                    subunitwidth=1,
                    showrivers=True,
                    rivercolor="#dbeafe",
                    projection_type="albers usa",
                    lonaxis=dict(range=[-125, -66]),
                    lataxis=dict(range=[24, 50]),
                    framewidth=0,
                ),
            )
            st.plotly_chart(fig_factories, use_container_width=True, config={"displayModeBar": False})


    # ── Factory Reach & Gap Explorer ───────────────────────────────────────────
    st.markdown("<div style='margin-top:-120px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🏭 Factory Reach & Expansion Indicators</div>', unsafe_allow_html=True)
    if ship_mode_sel != "All" or factory_sel != "All" or delay_threshold != 7:
        st.markdown(
            "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
            "📌 <i>Showing full portfolio — unaffected by Ship Mode / Factory / Delay Threshold filter selections</i>"
            "</div>", unsafe_allow_html=True
        )
    st.markdown(
        """<div style='font-size:0.82rem;color:#1e293b;line-height:1.6;margin-bottom:16px;'>
        Select a state to see how its orders are fulfilled across factories — which <b>divisions</b>
        (Chocolate, Sugar, Other) reach the nearest factory, which are routed further away,
        and where <b>network gaps</b> signal an opportunity for factory expansion.
        </div>""", unsafe_allow_html=True
    )

    _ca_province_centroids = {
        "Ontario": (51.2538, -85.3232), "Quebec": (53.0, -71.0),
        "Alberta": (53.9333, -116.5765), "British Columbia": (53.7267, -127.6476),
        "Manitoba": (53.7609, -98.8139), "Saskatchewan": (52.9399, -106.4509),
        "Nova Scotia": (44.6820, -63.7443), "New Brunswick": (46.5653, -66.4619),
        "Prince Edward Island": (46.5107, -63.4168), "Newfoundland and Labrador": (53.1355, -57.6604),
    }
    _us_state_options  = sorted([s for s in STATE_CENTROIDS if not df_dd[df_dd["State/Province"] == s].empty])
    _ca_prov_options   = sorted([p for p in _ca_province_centroids if not df_dd[df_dd["State/Province"] == p].empty])
    _all_dd_options    = _us_state_options + (["─── Canadian Provinces ───"] if _ca_prov_options else []) + _ca_prov_options
    _dd_default_idx    = _all_dd_options.index("Michigan") if "Michigan" in _all_dd_options else 0
    _dd_state = st.selectbox("State / Province", _all_dd_options,
                              index=_dd_default_idx, key="division_drilldown_state")

    _is_ca = _dd_state in _ca_province_centroids
    _is_separator = _dd_state.startswith("───")

    if _is_separator:
        st.info("Please select a state or province from the list.")
        st.stop()

    if _is_ca:
        st.markdown(
            "<div style='font-size:0.78rem;color:#92400e;background:#fffbeb;border:1px solid #fcd34d;"
            "border-radius:6px;padding:8px 14px;margin-bottom:10px;'>"
            "🍁 <b>Cross-border routing</b> — nearest factory metric does not account for logistics constraints."
            "</div>", unsafe_allow_html=True
        )
        _dd_slat, _dd_slon = _ca_province_centroids[_dd_state]
    else:
        _dd_slat, _dd_slon = STATE_CENTROIDS[_dd_state]
    _dd_dists   = {f: _hav(fc["lat"], fc["lon"], _dd_slat, _dd_slon) for f, fc in FACTORY_COORDS.items()}
    _dd_nearest = min(_dd_dists, key=_dd_dists.get)
    _dd_sdf     = df_dd[df_dd["State/Province"] == _dd_state]
    _dd_actual  = _dd_sdf["Factory"].value_counts().idxmax() if not _dd_sdf.empty else _dd_nearest
    _dd_dist_diff    = round(_dd_dists[_dd_actual] - _dd_dists[_dd_nearest], 0)
    _dd_is_rerouted  = _dd_actual != _dd_nearest

    _dd_prod = (
        _dd_sdf.groupby(["Division", "Product Name", "Factory"])
        .size().reset_index(name="Orders")
        .sort_values(["Division", "Orders"], ascending=[True, False])
        .reset_index(drop=True)
    )
    _dd_total_orders     = int(_dd_prod["Orders"].sum())
    _dd_nearest_orders   = int(_dd_prod[_dd_prod["Factory"] == _dd_nearest]["Orders"].sum())
    _dd_non_nearest_orders = _dd_total_orders - _dd_nearest_orders
    _dd_nearest_pct      = round(_dd_nearest_orders / _dd_total_orders * 100) if _dd_total_orders else 0
    _dd_non_nearest_pct  = 100 - _dd_nearest_pct
    # Divisions nearest factory IS capable of (has products for)
    _dd_nearest_capable_prods = {prod for prod, fac in PRODUCT_FACTORY.items() if fac == _dd_nearest}
    _dd_nearest_divs = sorted(
        _dd_prod[_dd_prod["Product Name"].isin(_dd_nearest_capable_prods)]["Division"].unique().tolist()
    )
    # Divisions nearest factory CANNOT make — true capability gap
    _dd_non_nearest_divs = sorted(
        _dd_prod[~_dd_prod["Product Name"].isin(_dd_nearest_capable_prods)]["Division"].unique().tolist()
    )
    _dd_all_divs         = sorted(_dd_prod["Division"].unique().tolist())
    _dd_other_factories  = sorted(_dd_prod[_dd_prod["Factory"] != _dd_nearest]["Factory"].unique().tolist())

    if not _dd_is_rerouted:
        _dd_pct_label = f" ({_dd_nearest_pct}%)" if _dd_nearest_pct < 100 else ""
        _dd_badge = f"<span style='background:#C8DFB0;color:#1E4D08;font-size:12px;padding:3px 10px;border-radius:6px;font-weight:500;'>Nearest factory served{_dd_pct_label}</span>"
    elif _dd_dist_diff > 500:
        _dd_badge = "<span style='background:#F5C4B5;color:#5C1A08;font-size:12px;padding:3px 10px;border-radius:6px;font-weight:500;'>High route deviation</span>"
    else:
        _dd_badge = "<span style='background:#F5D9A8;color:#4A2800;font-size:12px;padding:3px 10px;border-radius:6px;font-weight:500;'>Suboptimal routing</span>"
    st.markdown(_dd_badge, unsafe_allow_html=True)

    _DIV_COLORS = {
        "Chocolate": ("#E8C9A0", "#4A2010"),
        "Sugar":     ("#FFD980", "#4A3000"),
        "Other":     ("#C0D4F8", "#0F2A5C"),
    }

    def _div_pill(div_name):
        bg, tc = _DIV_COLORS.get(div_name, ("#eee", "#333"))
        return f"<span style='background:{bg};color:{tc};font-size:10px;padding:2px 6px;border-radius:20px;white-space:nowrap;'>{div_name}</span>"

    _dd_c1, _dd_c2, _dd_c3, _dd_c4 = st.columns(4)

    with _dd_c1:
        if _is_ca:
            st.markdown(f"""<div style='background:#f1f5f9;border:1px solid #e2e8f0;border-radius:8px;padding:14px;height:160px;display:flex;flex-direction:column;justify-content:center;'>
                <div style='font-size:13px;color:#94a3b8;margin-bottom:6px;'>Nearest factory</div>
                <div style='font-size:11px;color:#94a3b8;font-style:italic;'>Not applicable for cross-border routing.</div>
            </div>""", unsafe_allow_html=True)
        else:
            _near_pills = " ".join([_div_pill(d) for d in _dd_nearest_divs]) or "<span style='color:#0a0a0a;font-size:11px;'>None via nearest</span>"
            st.markdown(f"""<div style='background:#FDFCFA;border:1px solid #e2e8f0;border-radius:8px;padding:14px;height:160px;display:flex;flex-direction:column;'>
                <div style='font-size:13px;color:#0a0a0a;margin-bottom:2px;'>Nearest factory</div>
                <div style='font-size:22px;font-weight:700;margin-bottom:2px;color:#0a0a0a;'>{_dd_nearest_pct}%</div>
                <div style='font-size:12px;color:#085041;font-weight:600;margin-bottom:10px;'>{_dd_nearest}</div>
                <div style='font-size:11px;color:#0a0a0a;margin-bottom:5px;'>Divisions handled</div>
                <div style='display:flex;flex-wrap:wrap;gap:4px;'>{_near_pills}</div>
            </div>""", unsafe_allow_html=True)

    with _dd_c2:
        _nonnear_pills  = " ".join([_div_pill(d) for d in _dd_non_nearest_divs]) or "<span style='color:#0a0a0a;font-size:11px;'>No dependency</span>"
        _nonnear_label  = ", ".join(_dd_other_factories) if _dd_other_factories else "—"
        _nonnear_font = "10px" if len(_nonnear_label) > 40 else "12px"
        st.markdown(f"""<div style='background:#FDFCFA;border:1px solid #e2e8f0;border-radius:8px;padding:14px;height:160px;display:flex;flex-direction:column;'>
            <div style='font-size:13px;color:#0a0a0a;margin-bottom:2px;'>Non-nearest factory</div>
            <div style='font-size:22px;font-weight:700;margin-bottom:2px;color:#0a0a0a;'>{_dd_non_nearest_pct}%</div>
            <div style='font-size:{_nonnear_font};color:#712B13;font-weight:600;margin-bottom:10px;'>{_nonnear_label}</div>
            <div style='font-size:11px;color:#0a0a0a;margin-bottom:5px;'>Divisions handled</div>
            <div style='display:flex;flex-wrap:wrap;gap:4px;'>{_nonnear_pills}</div>
        </div>""", unsafe_allow_html=True)

    with _dd_c3:
        if _dd_nearest_pct == 100:
            _extra_mi = "Optimal routing"
            _extra_mi_color = "#3B6D11"
        elif _dd_dist_diff <= 0:
            _extra_mi = f"Partial routing ({_dd_nearest_pct}% nearest)"
            _extra_mi_color = "#633806"
        else:
            _extra_mi = f"+{int(_dd_dist_diff)} mi deviation"
            _extra_mi_color = "#712B13"
        st.markdown(f"""<div style='background:#FDFCFA;border:1px solid #e2e8f0;border-radius:8px;padding:14px;height:160px;display:flex;flex-direction:column;'>
            <div style='font-size:13px;color:#0a0a0a;margin-bottom:2px;'>Total orders</div>
            <div style='font-size:22px;font-weight:700;margin-bottom:2px;color:#0a0a0a;'>{_dd_total_orders:,}</div>
            <div style='font-size:12px;color:{_extra_mi_color};font-weight:500;margin-top:4px;'>{_extra_mi}</div>
        </div>""", unsafe_allow_html=True)

    with _dd_c4:
        st.markdown(f"""<div style='background:#FDFCFA;border:1px solid #e2e8f0;border-radius:8px;padding:14px;height:160px;display:flex;flex-direction:column;'>
            <div style='font-size:13px;color:#0a0a0a;margin-bottom:2px;'>Routes to non-nearest</div>
            <div style='font-size:22px;font-weight:700;margin-bottom:2px;color:#0a0a0a;'>{_dd_non_nearest_orders:,}</div>
            <div style='font-size:12px;color:#0a0a0a;'>of {_dd_total_orders:,} total orders</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # Products the nearest factory is capable of making
    _dd_nearest_can_make = {prod for prod, fac in PRODUCT_FACTORY.items() if fac == _dd_nearest}

    # Build product table rows
    _dd_rows_html = ""
    for _ri, _rrow in _dd_prod.iterrows():
        _is_near = _rrow["Factory"] == _dd_nearest
        # Gap = product is NOT made by nearest factory (nearest lacks capability for this product)
        _nearest_can_make_this = _rrow["Product Name"] in _dd_nearest_can_make
        _is_gap  = not _nearest_can_make_this
        _rpct    = round(_rrow["Orders"] / _dd_total_orders * 100) if _dd_total_orders else 0
        _rbg     = "#FEFEFE" if _ri % 2 == 0 else "#FDFCFA"
        _dbg, _dtc = _DIV_COLORS.get(_rrow["Division"], ("#eee", "#333"))
        _dtag    = f"<span style='background:{_dbg};color:{_dtc};font-size:11px;padding:2px 8px;border-radius:20px;'>{_rrow['Division']}</span>"
        _stag    = (
            f"<span style='background:#E8F5F0;color:#085041;font-size:11px;padding:2px 8px;border-radius:20px;'>{_rrow['Factory']}</span>"
            if _is_near else
            f"<span style='background:#F5C4B5;color:#5C1A08;font-size:11px;padding:2px 8px;border-radius:20px;'>{_rrow['Factory']}</span>"
        )
        _gtag    = (
            f"<span style='background:#F5D9A8;color:#4A2800;font-size:11px;padding:2px 8px;border-radius:20px;'>Network gap</span>"
            if _is_gap else
            f"<span style='background:#C8DFB0;color:#1E4D08;font-size:11px;padding:2px 8px;border-radius:20px;'>Covered ✓</span>"
        )
        _dd_rows_html += f"""
        <div style='display:grid;grid-template-columns:1.6fr 1fr 60px 60px 1.4fr 1.2fr;
                     padding:8px 14px;background:{_rbg};font-size:12px;align-items:center;
                     border-bottom:0.5px solid #eee;'>
          <span style='color:#0a0a0a;'>{_rrow['Product Name']}</span>
          <span>{_dtag}</span>
          <span style='text-align:right;color:#0a0a0a;'>{int(_rrow['Orders'])}</span>
          <span style='text-align:right;color:#0a0a0a;'>{_rpct}%</span>
          <span style='text-align:center;'>{_stag}</span>
          <span style='text-align:center;'>{_gtag}</span>
        </div>"""

    _dd_table_header = (
        "<div style='border:0.5px solid #ddd;border-radius:10px;overflow:hidden;margin-bottom:16px;'>"
        "<div style='display:grid;grid-template-columns:1.6fr 1fr 60px 60px 1.4fr 1.2fr;"
        "background:#FDFCFA;padding:8px 14px;font-size:12px;color:#0a0a0a;font-weight:500;'>"
        "<span>Product name</span><span>Division</span>"
        "<span style='text-align:right;'>Orders</span>"
        "<span style='text-align:right;'>Share</span>"
        "<span style='text-align:center;'>Served by</span>"
        "<span style='text-align:center;'>Coverage status</span>"
        "</div>"
    )
    _dd_table_full = _dd_table_header + _dd_rows_html + "</div>"
    st.markdown(_dd_table_full, unsafe_allow_html=True)

    # ── Network-wide routing summary ──────────────────────────────────────────
    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

    _net_nearest_only = _net_both = _net_non_nearest_only = 0
    _net_covered = _net_gap = _net_total_orders = 0
    _net_high_deviation = _net_suboptimal = 0

    for _s in [s for s in STATE_CENTROIDS if not df_dd[df_dd["State/Province"] == s].empty]:
        _s_lat, _s_lon = STATE_CENTROIDS[_s]
        _s_nearest = min(FACTORY_COORDS, key=lambda f: _hav(FACTORY_COORDS[f]["lat"], FACTORY_COORDS[f]["lon"], _s_lat, _s_lon))
        _s_nearest_dist = _hav(FACTORY_COORDS[_s_nearest]["lat"], FACTORY_COORDS[_s_nearest]["lon"], _s_lat, _s_lon)
        _s_df = df_dd[df_dd["State/Province"] == _s]
        _s_factories = set(_s_df["Factory"].unique())
        _s_nearest_can_make = {prod for prod, fac in PRODUCT_FACTORY.items() if fac == _s_nearest}
        _s_modal_factory = _s_df["Factory"].mode()[0] if not _s_df.empty else _s_nearest
        _s_is_rerouted = _s_modal_factory != _s_nearest

        if _s_factories == {_s_nearest}:
            _net_nearest_only += 1
        elif _s_nearest not in _s_factories:
            _net_non_nearest_only += 1
        else:
            _net_both += 1

        if _s_is_rerouted and _s_modal_factory in FACTORY_COORDS:
            _s_actual_dist = _hav(FACTORY_COORDS[_s_modal_factory]["lat"], FACTORY_COORDS[_s_modal_factory]["lon"], _s_lat, _s_lon)
            _s_diff = _s_actual_dist - _s_nearest_dist
            if _s_diff > 500:
                _net_high_deviation += 1
            else:
                _net_suboptimal += 1

        for _, _row in _s_df.iterrows():
            _net_total_orders += 1
            if _row["Product Name"] in _s_nearest_can_make:
                _net_covered += 1
            else:
                _net_gap += 1

    _net_covered_pct = round(_net_covered / _net_total_orders * 100) if _net_total_orders else 0
    _net_gap_pct     = 100 - _net_covered_pct
    _net_total_states = _net_nearest_only + _net_both + _net_non_nearest_only

    _sum_col1, _sum_col2 = st.columns([3, 2])

    with _sum_col1:
        st.markdown(
            f"<div style='font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;"
            f"color:#334155;margin-bottom:14px;'>📊 State Routing Classification — {_net_total_states} US States</div>",
            unsafe_allow_html=True
        )

        _routing_items = [
            ("Nearest only",      _net_nearest_only,     "#0ea5e9", "#0c4a6e"),
            ("Served by both",    _net_both,             "#7c3aed", "#3b0764"),
            ("Non-nearest only",  _net_non_nearest_only, "#f59e0b", "#78350f"),
        ]
        _deviation_items = [
            ("High route deviation", _net_high_deviation, "#ef4444", "#7f1d1d"),
            ("Suboptimal routing",   _net_suboptimal,     "#fb923c", "#7c2d12"),
        ]
        _bar_rows_html = ""
        for _lbl, _val, _bar_col, _txt_col in _routing_items:
            _pct = round(_val / _net_total_states * 100) if _net_total_states else 0
            _bar_rows_html += f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
              <div style="width:150px;font-size:13px;color:var(--color-text-primary);white-space:nowrap;">{_lbl}</div>
              <div style="flex:1;max-width:260px;background:#cbd5e1;border-radius:999px;height:10px;overflow:hidden;">
                <div style="width:{_pct}%;background:{_bar_col};height:100%;border-radius:999px;transition:width 0.4s ease;"></div>
              </div>
              <div style="width:28px;font-size:13px;font-weight:700;color:var(--color-text-primary);text-align:right;">{_val}</div>
              <div style="width:44px;font-size:13px;font-weight:700;color:{_txt_col};text-align:right;">{_pct}%</div>
            </div>"""

        _bar_rows_html += "<div style='border-top:1px dashed #e2e8f0;margin:10px 0 14px;'></div>"

        for _lbl, _val, _bar_col, _txt_col in _deviation_items:
            _pct = round(_val / _net_total_states * 100) if _net_total_states else 0
            _bar_rows_html += f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
              <div style="width:150px;font-size:13px;color:var(--color-text-primary);white-space:nowrap;">{_lbl}</div>
              <div style="flex:1;max-width:260px;background:#cbd5e1;border-radius:999px;height:10px;overflow:hidden;">
                <div style="width:{_pct}%;background:{_bar_col};height:100%;border-radius:999px;transition:width 0.4s ease;"></div>
              </div>
              <div style="width:28px;font-size:13px;font-weight:700;color:var(--color-text-primary);text-align:right;">{_val}</div>
              <div style="width:44px;font-size:13px;font-weight:700;color:{_txt_col};text-align:right;">{_pct}%</div>
            </div>"""

        st.markdown(
            f"<div style='padding:4px 0 8px;'>{_bar_rows_html}</div>",
            unsafe_allow_html=True
        )

    with _sum_col2:
        st.markdown(
            "<div style='font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;"
            "color:#334155;margin-bottom:10px;'>🎯 Order Coverage vs Network Gap</div>",
            unsafe_allow_html=True
        )
        import plotly.graph_objects as _go_sum
        fig_donut = _go_sum.Figure(_go_sum.Pie(
            labels=["Covered orders", "Network gap"],
            values=[_net_covered, _net_gap],
            hole=0.58,
            marker=dict(colors=["#7CB87A", "#E8A838"]),
            textinfo="none",
            hovertemplate="%{label}: %{value:,} orders (%{percent})<extra></extra>",
            sort=False,
        ))
        fig_donut.add_annotation(
            text=f"<b>{_net_gap_pct}%</b><br>gap",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="#4A2800"),
            align="center",
        )
        fig_donut.update_layout(
            **PLOTLY_THEME, height=220,
            margin=dict(t=40, b=0, l=0, r=0),
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=-0.05,
                        xanchor="left", x=0, font=dict(size=11)),
        )
        st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
        st.plotly_chart(fig_donut, use_container_width=True)

    # ── Network Coverage Deep Dive ─────────────────────────────────────────────
    st.markdown('<div class="section-header">📊 Network Coverage Deep Dive</div>', unsafe_allow_html=True)
    if delay_threshold != 7:
        st.markdown(
            "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
            "📌 <i>Showing full portfolio — unaffected by Delay Threshold filter selections</i>"
            "</div>", unsafe_allow_html=True
        )

    _ncd_col3, _ncd_col4 = st.columns(2)

    with _ncd_col3:
        st.markdown(
            "<div style=\"font-size:12px;font-weight:600;letter-spacing:0.07em;"
            "text-transform:uppercase;color:#1e293b;margin-bottom:8px;\">"
            "🏭 Factory Reach — States & Provinces Covered per Division</div>",
            unsafe_allow_html=True
        )
        _hm_rows = []
        for _f in FACTORY_COORDS:
            _f_df = df[df["Factory"] == _f]
            for _div in ["Chocolate", "Sugar", "Other"]:
                if "Division" in _f_df.columns:
                    _div_df = _f_df[_f_df["Division"] == _div]
                else:
                    _div_df = pd.DataFrame()
                _states_covered = int(_div_df["State/Province"].nunique()) if not _div_df.empty else 0
                _hm_rows.append({"Factory": _f, "Division": _div, "States": _states_covered})

        _hm_df = pd.DataFrame(_hm_rows)
        _hm_pivot = _hm_df.pivot(index="Factory", columns="Division", values="States").fillna(0)

        # Total unique states across entire dataset
        _total_states_all = int(df["State/Province"].nunique())
        # Build customdata: [factory_home_state, total_states_all, pct_of_total]
        _cd = []
        for _f in list(_hm_pivot.index):
            _row = []
            for _div in list(_hm_pivot.columns):
                _val = int(_hm_pivot.loc[_f, _div])
                _pct = round(_val / _total_states_all * 100) if _val > 0 else 0
                _home = FACTORY_COORDS[_f]["state"]
                _row.append([_home, _total_states_all, _pct])
            _cd.append(_row)

        import plotly.graph_objects as _go_hm
        fig_hm = _go_hm.Figure(_go_hm.Heatmap(
            z=_hm_pivot.values,
            x=list(_hm_pivot.columns),
            y=list(_hm_pivot.index),
            colorscale=[[0, "#f1f5f9"], [0.5, "#7dd3fc"], [1, "#0369a1"]],
            text=_hm_pivot.values.astype(int),
            texttemplate="",
            textfont=dict(size=12),
            showscale=True,
            colorbar=dict(title="States/Prov.", thickness=12, len=0.8),
            customdata=_cd,
            hovertemplate=(
                "<b>%{y}</b> (%{customdata[0]}) — %{x} division<br>"
                "States covered: <b>%{z} of %{customdata[1]} (%{customdata[2]}%)</b>"
                "<extra></extra>"
            ),
        ))
        # Overlay white text on dark cells, dark on light
        _thresh = _hm_pivot.values.max() * 0.5
        for i, row in enumerate(_hm_pivot.values):
            for j, val in enumerate(row):
                fig_hm.add_annotation(
                    x=list(_hm_pivot.columns)[j], y=list(_hm_pivot.index)[i],
                    text=str(int(val)),
                    font=dict(size=12, color="white" if val > _thresh else "#1e293b"),
                    showarrow=False,
                )
        fig_hm.update_layout(
            **PLOTLY_THEME, height=340, margin=dict(t=40, b=10, l=0, r=60),
            xaxis=dict(title="", tickfont=dict(size=12, color="#1e293b"),
                       linecolor="#1e293b", tickcolor="#1e293b"),
            yaxis=dict(title="", tickfont=dict(size=11, color="#1e293b"),
                       linecolor="#1e293b", tickcolor="#1e293b", autorange="reversed"),
        )
        fig_hm.update_traces(
            colorbar=dict(title=dict(text="States/Prov.", font=dict(color="#1e293b")),
                          tickfont=dict(color="#1e293b"), thickness=12, len=0.8),
            textfont=dict(size=12, color="#1e293b"),
        )
        st.plotly_chart(fig_hm, use_container_width=True)

    # _ncd_col4 intentionally left empty — heatmap rendered full-width below
    with _ncd_col4:
        st.markdown(
            "<div style=\"font-size:12px;font-weight:600;letter-spacing:0.07em;"
            "text-transform:uppercase;color:#1e293b;margin-bottom:8px;\">"
            "📍 Nearest vs Actual Factory Distance — by State</div>",
            unsafe_allow_html=True
        )
        _all_regions_sc = {**STATE_CENTROIDS, **_ca_province_centroids}
        _sc_rows = []
        for _s, (_s_lat, _s_lon) in _all_regions_sc.items():
            _s_df = df[df["State/Province"] == _s]
            if _s_df.empty:
                continue
            _s_nearest_factory = min(FACTORY_COORDS, key=lambda f: _hav(FACTORY_COORDS[f]["lat"], FACTORY_COORDS[f]["lon"], _s_lat, _s_lon))
            _s_nearest_dist = _hav(FACTORY_COORDS[_s_nearest_factory]["lat"], FACTORY_COORDS[_s_nearest_factory]["lon"], _s_lat, _s_lon)
            _s_actual_factory = _s_df["Factory"].mode()[0]
            if _s_actual_factory not in FACTORY_COORDS:
                continue
            _s_actual_dist = _hav(FACTORY_COORDS[_s_actual_factory]["lat"], FACTORY_COORDS[_s_actual_factory]["lon"], _s_lat, _s_lon)
            _sc_rows.append({
                "State": _s,
                "Nearest_dist": round(_s_nearest_dist, 0),
                "Actual_dist": round(_s_actual_dist, 0),
                "Shipments": len(_s_df),
                "Is_nearest": _s_actual_factory == _s_nearest_factory,
            })
        _sc_df = pd.DataFrame(_sc_rows)
        _sc_nearest = _sc_df[_sc_df["Is_nearest"]]
        _sc_non     = _sc_df[~_sc_df["Is_nearest"]]

        import plotly.graph_objects as _go_sc
        _sc_max = int(_sc_df[["Nearest_dist","Actual_dist"]].max().max() * 1.08)
        fig_sc = _go_sc.Figure()
        fig_sc.add_trace(_go_sc.Scatter(
            x=_sc_nearest["Nearest_dist"], y=_sc_nearest["Actual_dist"],
            mode="markers", name="Nearest routed",
            marker=dict(color="#34d399", size=(_sc_nearest["Shipments"] / _sc_df["Shipments"].max() * 22 + 6).round(1),
                        opacity=0.8, line=dict(width=0.5, color="#0f6e56")),
            text=_sc_nearest["State"],
            hovertemplate="<b>%{text}</b><br>Nearest: %{x:,} mi<br>Actual: %{y:,} mi<extra></extra>",
        ))
        fig_sc.add_trace(_go_sc.Scatter(
            x=_sc_non["Nearest_dist"], y=_sc_non["Actual_dist"],
            mode="markers", name="Non-nearest routed",
            marker=dict(color="#7c3aed", size=(_sc_non["Shipments"] / _sc_df["Shipments"].max() * 22 + 6).round(1),
                        opacity=0.7, symbol="triangle-up", line=dict(width=0.5, color="#4c1d95")),
            text=_sc_non["State"],
            hovertemplate="<b>%{text}</b><br>Nearest: %{x:,} mi<br>Actual: %{y:,} mi<extra></extra>",
        ))
        fig_sc.add_shape(type="line", x0=0, y0=0, x1=_sc_max, y1=_sc_max,
                         line=dict(color="#ef4444", width=1.5, dash="dash"))
        fig_sc.add_trace(_go_sc.Scatter(
            x=[None], y=[None], mode="lines", name="Nearest = Actual (reference)",
            line=dict(color="#ef4444", width=1.5, dash="dash"), showlegend=True,
        ))
        fig_sc.update_layout(
            **PLOTLY_THEME, height=360, margin=dict(t=10, b=90, l=0, r=0),
            xaxis=dict(title="Nearest factory (mi)", range=[0, _sc_max],
                       tickfont=dict(size=10, color="#1e293b"),
                       title_font=dict(color="#1e293b"),
                       linecolor="#1e293b", tickcolor="#1e293b", gridcolor="#e2e8f0"),
            yaxis=dict(title="Actual factory (mi)", range=[0, _sc_max],
                       tickfont=dict(size=10, color="#1e293b"),
                       title_font=dict(color="#1e293b"),
                       linecolor="#1e293b", tickcolor="#1e293b", gridcolor="#e2e8f0"),
            legend=dict(orientation="h", yanchor="top", y=-0.24, xanchor="center", x=0.5,
                        font=dict(size=10, color="#1e293b")),
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    # ── Factory Expansion Opportunity ──────────────────────────────────────────
    st.markdown('<div class="section-header">🚀 Factory Expansion Opportunity — States Served vs Reachable</div>', unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:0.82rem;color:#475569;margin-bottom:8px;'>"
        "Compares how many states each factory currently serves against how many it could reach within a given distance threshold. "
        "The gap represents untapped distribution potential — states within range that the factory does not currently serve."
        "</div>", unsafe_allow_html=True
    )

    st.markdown(
        "<div style='border:1.5px dashed #a78bfa;border-radius:8px;background:#f5f3ff;"
        "padding:7px 12px;font-size:11.5px;color:#5b21b6;line-height:1.5;margin-bottom:12px;'>"
        "💡 Conceptual projection — assumes routing to nearest factory reduces lead time proportionally to distance saved."
        "</div>",
        unsafe_allow_html=True
    )

    if region_sel != "All" or ship_mode_sel != "All" or delay_threshold != 7:
        st.markdown(
            "<div style='display:inline-flex;align-items:center;gap:6px;background:#f8fafc;"
            "border:1px solid #cbd5e1;border-radius:6px;padding:5px 11px;"
            "font-size:11.5px;color:#475569;margin-bottom:12px;'>"
            "📌 <i>Showing full portfolio — unaffected by Region / Ship Mode / Delay Threshold filter selections</i>"
            "</div>",
            unsafe_allow_html=True
        )

    _reach_threshold = st.slider(
        "Distance threshold (miles)", min_value=300, max_value=2000,
        value=800, step=100, key="expansion_threshold",
        help="States within this distance from the factory are considered 'reachable'"
    )

    _exp_rows = []
    _all_regions_exp = {**STATE_CENTROIDS, **_ca_province_centroids}
    for _f, _fc in FACTORY_COORDS.items():
        _f_lat, _f_lon = _fc["lat"], _fc["lon"]
        _currently_serving = set(df_raw[df_raw["Factory"] == _f]["State/Province"].unique())
        _reachable = {
            s for s, (slat, slon) in _all_regions_exp.items()
            if _hav(_f_lat, _f_lon, slat, slon) <= _reach_threshold
        }
        _gap_states = _reachable - _currently_serving
        _exp_rows.append({
            "Factory": _f,
            "Currently Serving": len(_currently_serving),
            "Reachable (not serving)": len(_gap_states),
            "Total Reachable": len(_reachable),
        })

    _exp_df = pd.DataFrame(_exp_rows).sort_values("Currently Serving", ascending=True)

    # Per-bar colors: dim non-selected factories when factory filter is active
    def _exp_bar_color(factory, base_color, dim_color):
        if factory_sel == "All":
            return [base_color] * len(_exp_df)
        return [base_color if f == factory_sel else dim_color for f in _exp_df["Factory"]]

    _dark_colors  = _exp_bar_color(factory_sel, "#6d28d9", "#e2e8f0")
    _light_colors = _exp_bar_color(factory_sel, "#c4b5fd", "#f1f5f9")
    _label_colors = [
        ("#16a34a" if v == 0 else "#7c3aed") if (factory_sel == "All" or f == factory_sel) else "#cbd5e1"
        for f, v in zip(_exp_df["Factory"], _exp_df["Reachable (not serving)"])
    ]

    import plotly.graph_objects as _go_exp
    fig_exp = _go_exp.Figure()
    fig_exp.add_trace(_go_exp.Bar(
        y=_exp_df["Factory"], x=_exp_df["Currently Serving"],
        name="Currently serving", orientation="h",
        marker_color=_dark_colors,
        text=_exp_df.apply(lambda r: str(r["Currently Serving"]) if r["Reachable (not serving)"] > 0 else "", axis=1),
        textposition="inside", textfont=dict(size=11, color="white"),
        customdata=_exp_df[["Total Reachable", "Reachable (not serving)"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Currently serving: <b>%{x} states/provinces</b><br>"
            "Total reachable within threshold: <b>%{customdata[0]}</b><br>"
            "Untapped (reachable, not serving): <b>%{customdata[1]}</b>"
            "<extra></extra>"
        ),
    ))
    _exp_gap_text = _exp_df["Reachable (not serving)"].apply(lambda v: f"+{v} gap" if v > 0 else "✓ Full coverage")

    fig_exp.add_trace(_go_exp.Bar(
        y=_exp_df["Factory"], x=_exp_df["Reachable (not serving)"],
        name="Reachable within threshold (not serving)", orientation="h",
        marker_color=_light_colors,
        text=None,
        customdata=_exp_df[["Currently Serving", "Total Reachable"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Untapped states/provinces: <b>%{x}</b><br>"
            "Currently serving: <b>%{customdata[0]}</b><br>"
            "Total reachable within threshold: <b>%{customdata[1]}</b>"
            "<extra></extra>"
        ),
    ))
    # overlay invisible scatter to apply per-bar text colors
    fig_exp.add_trace(_go_exp.Scatter(
        x=[_exp_df["Currently Serving"].iloc[i] + _exp_df["Reachable (not serving)"].iloc[i] + 2
           for i in range(len(_exp_df))],
        y=_exp_df["Factory"],
        mode="text",
        text=_exp_gap_text,
        textfont=dict(size=11, color=_label_colors),
        textposition="middle right",
        showlegend=False,
        hoverinfo="skip",
    ))
    fig_exp.update_layout(
        **PLOTLY_THEME, height=360, barmode="stack",
        margin=dict(t=40, b=10, l=0, r=100),
        xaxis=dict(title="Number of states / provinces", range=[0, 80],
                   tickfont=dict(size=11, color="#0f172a"), gridcolor="#f1f5f9"),
        yaxis=dict(title="", tickfont=dict(size=11, color="#0f172a")),
        showlegend=False,
    )
    st.plotly_chart(fig_exp, use_container_width=True)
    st.markdown(
        "<div style='display:flex;align-items:center;justify-content:center;gap:24px;margin-top:-12px;margin-bottom:16px;flex-wrap:wrap;'>"
        "<span style='display:flex;align-items:center;gap:6px;font-size:12px;color:#0f172a;'>"
        "<span style='width:14px;height:14px;border-radius:3px;background:#c4b5fd;display:inline-block;'></span>"
        "Reachable within threshold (not serving)</span>"
        "<span style='display:flex;align-items:center;gap:6px;font-size:12px;color:#0f172a;'>"
        "<span style='width:14px;height:14px;border-radius:3px;background:#6d28d9;display:inline-block;'></span>"
        "Currently serving</span>"
        f"<span style='font-size:11px;color:#94a3b8;'>· Gap = states/provinces within {_reach_threshold} mi not currently served</span>"
        "</div>",
        unsafe_allow_html=True
    )

    # ── Underserved Regions ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔴 Underserved Regions (Far from all factories + High Lead Time)</div>', unsafe_allow_html=True)
    if ship_mode_sel != "All" or factory_sel != "All":
        st.markdown(
            "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
            "📌 <i>Showing full portfolio — unaffected by Ship Mode / Factory filter selections</i>"
            "</div>", unsafe_allow_html=True
        )

    _underserved_rows = []
    for state, (slat, slon) in STATE_CENTROIDS.items():
        _s_data = state_stats_all[state_stats_all["State/Province"] == state]
        if _s_data.empty:
            continue
        _min_dist = min(_hav(fc["lat"], fc["lon"], slat, slon) for fc in FACTORY_COORDS.values())
        _sr = _s_data.iloc[0]
        _underserved_rows.append({
            "State": state,
            "State Code": STATE_ABBREV.get(state, ""),
            "Min Distance to Factory (mi)": round(_min_dist, 0),
            "Avg Lead Time": round(_sr["Avg_Lead_Time"], 1),
            "Delay Rate": _sr["Delay_Rate"],
            "Shipments": int(_sr["Shipments"]),
        })
    _underserved_df = pd.DataFrame(_underserved_rows)
    # Thresholds always from full portfolio — unaffected by filters
    _dist_thresh = _underserved_df["Min Distance to Factory (mi)"].quantile(0.6)
    _lt_thresh   = _underserved_df["Avg Lead Time"].quantile(0.6)
    _underserved_flagged = _underserved_df[
        (_underserved_df["Min Distance to Factory (mi)"] > _dist_thresh) &
        (_underserved_df["Avg Lead Time"] > _lt_thresh)
    ].sort_values("Min Distance to Factory (mi)", ascending=False).reset_index(drop=True)
    # Apply region filter: only show states present in the filtered dataset
    if region_sel != "All":
        _visible_states = set(state_stats["State/Province"].tolist())
        _underserved_flagged = _underserved_flagged[
            _underserved_flagged["State"].isin(_visible_states)
        ].reset_index(drop=True)
    _uc1, _uc2 = st.columns([2, 3])
    with _uc1:
        st.markdown(f"**{len(_underserved_flagged)} states** are both far from all factories (>{_dist_thresh:,.0f} mi) and have above-average lead times (>{_lt_thresh:.1f}d), representing the highest-priority gaps in current network coverage.")
        _und_df = _underserved_flagged[["State", "Min Distance to Factory (mi)", "Avg Lead Time", "Delay Rate", "Shipments"]].reset_index(drop=True)
        _und_style = _und_df.style.format({
            "Min Distance to Factory (mi)": "{:,.0f}", "Avg Lead Time": "{:.1f}", "Shipments": "{:,}",
        }) \
        .format({"Delay Rate": lambda v: "—"},
                subset=pd.IndexSlice[_und_df["Shipments"] <= 2, ["Delay Rate"]]) \
        .format({"Delay Rate": "{:.1%}"},
                subset=pd.IndexSlice[_und_df["Shipments"] > 2, ["Delay Rate"]])
        if _und_df.empty:
            st.markdown(
                "<div style='padding:12px 16px;color:#94a3b8;font-size:13px;border:1px solid #e2e8f0;"
                "border-radius:6px;text-align:center;'>No records found for the selected filter.</div>",
                unsafe_allow_html=True
            )
        else:
            st.dataframe(_und_style, use_container_width=True, hide_index=True)
            if (_und_df["Shipments"] <= 2).any():
                st.markdown("<p style='font-size:0.8rem; color:#334155; margin: 2px 0 12px 0;'>ⓘ '—' shown where 2 or fewer shipments exist — delay rate not meaningful for such a small sample.</p>", unsafe_allow_html=True)
    with _uc2:
        fig_under = px.scatter_geo(
            _underserved_df, lat=_underserved_df["State"].map(lambda s: STATE_CENTROIDS.get(s, (0,0))[0]),
            lon=_underserved_df["State"].map(lambda s: STATE_CENTROIDS.get(s, (0,0))[1]),
            size="Min Distance to Factory (mi)",
            color="Avg Lead Time",
            hover_name="State",
            hover_data={"Avg Lead Time": True, "Min Distance to Factory (mi)": ":,.0f", "Delay Rate": ":.1%"},
            color_continuous_scale="Reds",
            scope="usa",
            title="State remoteness vs Lead Time (bubble = distance to nearest factory)",
        )
        fig_under.update_layout(height=340, margin=dict(r=0,t=40,l=0,b=0),
            paper_bgcolor="white",
            geo=dict(bgcolor="white", landcolor="#f1f5f9", lakecolor="#dbeafe",
                showlakes=True, showcoastlines=True, coastlinecolor="#94a3b8",
                subunitcolor="#cbd5e1", showsubunits=True,
                domain=dict(y=[0, 0.85])),
            coloraxis_colorbar=dict(title="Avg Lead Time", title_font=dict(color="#1a1a2e"),
                tickfont=dict(color="#1a1a2e")),
            font=dict(color="#1a1a2e"))
        st.plotly_chart(fig_under, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">Top 10 Bottleneck States</div>', unsafe_allow_html=True)
        if ship_mode_sel != "All" or factory_sel != "All":
            st.markdown(
                "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
                "📌 Showing full portfolio — unaffected by Ship Mode / Factory filter selections"
                "</div>", unsafe_allow_html=True
            )
        bottlenecks = state_stats_region.nlargest(10, "Avg_Lead_Time")[
            ["State/Province", "Shipments", "Avg_Lead_Time", "Delay_Rate"]
        ].reset_index(drop=True)
        _bn_style = bottlenecks.style.format({
            "Avg_Lead_Time": "{:.1f}d",
            "Shipments": "{:,}",
        }) \
        .format({"Delay_Rate": lambda v: "—"},
                subset=pd.IndexSlice[bottlenecks["Shipments"] <= 2, ["Delay_Rate"]]) \
        .format({"Delay_Rate": "{:.1%}"},
                subset=pd.IndexSlice[bottlenecks["Shipments"] > 2, ["Delay_Rate"]])
        st.dataframe(_bn_style, use_container_width=True, hide_index=True)
        if (bottlenecks["Shipments"] <= 2).any():
            st.markdown("<p style='font-size:0.8rem; color:#334155; margin: 2px 0 12px 0;'>ⓘ '—' shown where 2 or fewer shipments exist — delay rate not meaningful for such a small sample.</p>", unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="section-header">High Volume + High Delay States</div>', unsafe_allow_html=True)
        if ship_mode_sel != "All" or factory_sel != "All":
            st.markdown(
                "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
                "📌 Showing full portfolio — unaffected by Ship Mode / Factory filter selections"
                "</div>", unsafe_allow_html=True
            )
        congested = state_stats_region[
            (state_stats_region["Shipments"] > state_stats_region["Shipments"].quantile(0.6)) &
            (state_stats_region["Delay_Rate"]  > state_stats_region["Delay_Rate"].quantile(0.6))
        ].sort_values("Delay_Rate", ascending=False)[
            ["State/Province", "Shipments", "Avg_Lead_Time", "Delay_Rate"]
        ].reset_index(drop=True)
        st.dataframe(
            congested.style.format({
                "Avg_Lead_Time": "{:.1f}d",
                "Delay_Rate": "{:.1%}",
                "Shipments": "{:,}",
            }),
            use_container_width=True, hide_index=True,
        )

    # ── Customer Segmentation ──────────────────────────────────────────────────
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">👥 Customer Segmentation — Order Value Tiers</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#475569;margin:-8px 0 12px 0;'>"
        "Orders segmented into High, Medium, and Low value tiers based on Sales percentiles. "
        "Tier thresholds: High (&gt; 75th percentile), Medium (25th–75th), Low (&lt; 25th percentile).</p>",
        unsafe_allow_html=True
    )

    _seg_df = df.copy()
    _p25 = _seg_df["Sales"].quantile(0.25)
    _p75 = _seg_df["Sales"].quantile(0.75)
    _seg_df["Value_Tier"] = pd.cut(
        _seg_df["Sales"],
        bins=[-np.inf, _p25, _p75, np.inf],
        labels=["Low Value", "Medium Value", "High Value"]
    )
    _tier_summary = (
        _seg_df.groupby("Value_Tier", observed=True)
        .agg(
            Orders=("Sales", "count"),
            Total_Revenue=("Sales", "sum"),
            Avg_Sales=("Sales", "mean"),
            Avg_Lead_Time=("Lead Time", "mean"),
            Delay_Rate=("Is Delayed", "mean"),
            Total_Profit=("Gross Profit", "sum"),
        )
        .reset_index()
    )
    _tier_summary["Profit_Margin"] = (_tier_summary["Total_Profit"] / _tier_summary["Total_Revenue"] * 100).round(1)
    _tier_summary["Revenue_Share"] = (_tier_summary["Total_Revenue"] / _tier_summary["Total_Revenue"].sum() * 100).round(1)

    _seg_col1, _seg_col2 = st.columns(2)
    with _seg_col1:
        fig_tier_rev = px.bar(
            _tier_summary, x="Value_Tier", y="Total_Revenue",
            color="Value_Tier",
            color_discrete_map={"High Value": "#16a34a", "Medium Value": "#f59e0b", "Low Value": "#ef4444"},
            text="Revenue_Share",
            labels={"Total_Revenue": "Total Revenue ($)", "Value_Tier": "Tier"},
            title="Revenue by Order Value Tier",
        )
        fig_tier_rev.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                                   hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>")
        fig_tier_rev.update_layout(
            **{**PLOTLY_THEME, "font": dict(color="#1e293b", family="Space Grotesk")},
            height=350, showlegend=False,
            xaxis=dict(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b")),
            yaxis=dict(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b")),
        )
        st.plotly_chart(fig_tier_rev, use_container_width=True)

    with _seg_col2:
        fig_tier_lt = px.bar(
            _tier_summary, x="Value_Tier", y="Avg_Lead_Time",
            color="Value_Tier",
            color_discrete_map={"High Value": "#16a34a", "Medium Value": "#f59e0b", "Low Value": "#ef4444"},
            labels={"Avg_Lead_Time": "Avg Lead Time (days)", "Value_Tier": "Tier"},
            title="Avg Lead Time by Order Value Tier",
        )
        fig_tier_lt.update_traces(hovertemplate="<b>%{x}</b><br>Avg Lead Time: %{y:.1f}d<extra></extra>")
        fig_tier_lt.update_layout(
            **{**PLOTLY_THEME, "font": dict(color="#1e293b", family="Space Grotesk")},
            height=350, showlegend=False,
            xaxis=dict(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b")),
            yaxis=dict(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b")),
        )
        st.plotly_chart(fig_tier_lt, use_container_width=True)

    _tier_region = (
        _seg_df.groupby(["Region", "Value_Tier"], observed=True)
        .agg(Orders=("Sales", "count"), Revenue=("Sales", "sum"))
        .reset_index()
    )
    fig_tier_region = px.bar(
        _tier_region, x="Region", y="Orders",
        color="Value_Tier",
        color_discrete_map={"High Value": "#16a34a", "Medium Value": "#f59e0b", "Low Value": "#ef4444"},
        barmode="stack",
        labels={"Orders": "Order Count", "Value_Tier": "Tier"},
        title="Order Volume by Region and Value Tier",
        hover_data={"Revenue": ":$,.0f"},
    )
    fig_tier_region.update_layout(
        **{**PLOTLY_THEME, "font": dict(color="#1e293b", family="Space Grotesk")},
        height=380,
        legend=dict(font=dict(color="#1e293b"), title_text="Value Tier"),
        xaxis=dict(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b")),
        yaxis=dict(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b")),
    )
    st.plotly_chart(fig_tier_region, use_container_width=True)

    with st.expander("📋 Full Tier Summary Table"):
        st.dataframe(
            _tier_summary[["Value_Tier", "Orders", "Total_Revenue", "Avg_Sales",
                           "Revenue_Share", "Profit_Margin", "Avg_Lead_Time", "Delay_Rate"]]
            .style
            .format({
                "Total_Revenue": "${:,.0f}", "Avg_Sales": "${:,.2f}",
                "Revenue_Share": "{:.1f}%", "Profit_Margin": "{:.1f}%",
                "Avg_Lead_Time": "{:.1f}d", "Delay_Rate": "{:.1%}", "Orders": "{:,}"
            })
            .background_gradient(subset=["Revenue_Share"], cmap="Greens", vmin=0, vmax=100)
            .background_gradient(subset=["Delay_Rate"], cmap="Reds", vmin=0, vmax=1),
            use_container_width=True,
        )

    # ── Geographic Network Assessment ──────────────────────────────────────
    st.markdown("<div style='margin-top: 48px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Geographic Network Assessment</div>', unsafe_allow_html=True)

    try:
        _rm = state_stats.copy()
        _rm_top_rev = _rm.nlargest(1, "Total_Sales").iloc[0]
        _rm_high_delay = _rm.nlargest(1, "Delay_Rate").iloc[0]
        _rm_low_delay = _rm[_rm["Shipments"] >= 10].nsmallest(1, "Delay_Rate").iloc[0]
        _rm_high_lt = _rm.nlargest(1, "Avg_Lead_Time").iloc[0]

        _geo_cards_html = f"""
        <div class="assess-grid">
          <div class="assess-card blue">
            <div class="assess-head">
              <span class="assess-head-icon">🌎</span>
              <span class="assess-head-title">Regional Performance Spread</span>
            </div>
            <p class="assess-para">
              Revenue and operational performance are unevenly distributed across regions.
              <b>{_rm_top_rev['State/Province']}</b> leads in total sales at <b>${_rm_top_rev['Total_Sales']:,.0f}</b>
              with a <b>{_rm_top_rev['Delay_Rate']:.1%}</b> delay rate — a high-volume region that remains broadly
              stable despite its scale.
            </p>
            <p class="assess-para">
              At the other end, <b>{_rm_high_delay['State/Province']}</b> records the network's highest delay rate at
              <b>{_rm_high_delay['Delay_Rate']:.1%}</b>, while <b>{_rm_high_lt['State/Province']}</b> has the longest
              average lead time at <b>{_rm_high_lt['Avg_Lead_Time']:.1f} days</b>. By contrast,
              <b>{_rm_low_delay['State/Province']}</b> shows a notably lower delay rate of
              <b>{_rm_low_delay['Delay_Rate']:.1%}</b>, suggesting that low delay rates are achievable even with
              limited shipment volume — though with only <b>{int(_rm_low_delay['Shipments'])} shipments</b>, this
              isn't yet a statistically robust benchmark. Overall, the spread between regions suggests that delay
              and lead-time issues are concentrated in specific areas rather than reflecting a uniform,
              network-wide pattern.
            </p>
          </div>
        </div>
        """
        st.markdown(_geo_cards_html, unsafe_allow_html=True)
    except Exception:
        pass

    # ── Factory Concentration & Network Routing cards ────────────────────────
    try:
        _second_factory = _fac_vol.iloc[1]
        _fac_cards_html = f"""
        <div class="assess-grid">
          <div class="assess-card amber">
            <div class="assess-head">
              <span class="assess-head-icon">🏭</span>
              <span class="assess-head-title">Factory Volume Concentration</span>
            </div>
            <p class="assess-para">
              Shipment volume is heavily concentrated in just two facilities. <b>{_top_factory['Factory']}</b>
              handles <b>{_top_share}%</b> of total shipments at an average lead time of <b>{_top_lt:.2f} days</b>,
              while <b>{_second_factory['Factory']}</b> accounts for a further <b>{_second_factory['Share (%)']}%</b>.
              Together, these two factories handle the large majority of the network's volume, while the
              remaining factories each handle under 3% — a concentration that creates supply chain
              vulnerability if either top facility faces disruption.
            </p>
            <p class="assess-para">
              On the map, <b>{_top_factory['Factory']}</b> and <b>{_second_factory['Factory']}</b> also carry the
              largest bubble sizes (shipment volume), with delay rates that remain within acceptable bounds —
              indicating that the concentration itself — rather than underperformance at these sites —
              represents the primary structural risk requiring attention.
            </p>
          </div>

          <div class="assess-card red">
            <div class="assess-head">
              <span class="assess-head-icon">🧭</span>
              <span class="assess-head-title">Routing &amp; Coverage Gaps</span>
            </div>
            <p class="assess-para">
              Across <b>{_net_total_states}</b> US states, none are served exclusively
              by their nearest factory, while <b>{_net_both}</b> states are served by both nearest and non-nearest
              factories, and <b>{_net_non_nearest_only}</b> states are served entirely by a non-nearest factory.
              This means the large majority of states have at least some orders routed away from their
              geographically closest facility.
            </p>
            <p class="assess-para">
              Of these, <b>{_net_high_deviation}</b> states show <b>high route deviation</b> (over 500 miles
              beyond the nearest-factory distance) and <b>{_net_suboptimal}</b> show milder suboptimal routing.
              At the order level, only <b>{_net_covered_pct}%</b> of orders are fulfilled by a factory capable
              of producing that product nearest to the customer — leaving a <b>{_net_gap_pct}%</b> network gap.
              This distance-based gap warrants further operational review. Distance to the nearest factory
              shows a weak correlation with lead time across the network (r ≈ 0.16); closing this gap
              would reduce shipping distance, while delivery speed improvements would need independent
              evaluation.
            </p>
          </div>
        </div>
        """
        st.markdown(_fac_cards_html, unsafe_allow_html=True)
    except Exception:
        pass

    try:
        _full_cov = _exp_df[_exp_df["Reachable (not serving)"] == 0]["Factory"].tolist()
        _gap_sorted = _exp_df[_exp_df["Reachable (not serving)"] > 0].sort_values(
            "Reachable (not serving)", ascending=False)
        _top_gap_factory = _gap_sorted.iloc[0]
        _bn_top = bottlenecks.iloc[0]
        _top_underserved = _underserved_flagged.iloc[0] if len(_underserved_flagged) else None
        _cong_top = congested.iloc[0] if len(congested) else None

        _ncd_card_html = f"""
        <div class="assess-grid">
          <div class="assess-card amber">
            <div class="assess-head">
              <span class="assess-head-icon">📊</span>
              <span class="assess-head-title">Coverage Concentration &amp; Reroute Distances</span>
            </div>
            <p class="assess-para">
              State and provincial coverage is heavily concentrated in the <b>Chocolate</b> division, where
              <b>Lot's O' Nuts</b> and <b>Wicked Choccy's</b> each cover <b>57</b> states/provinces — full
              network reach for that division. The <b>Sugar</b> division, by contrast, is served by just two
              factories with limited overlap, and the <b>Other</b> division sits in between, split mainly
              between Secret Factory and The Other Factory.
            </p>
            <p class="assess-para">
              The nearest-vs-actual factory distance comparison shows a large cluster of <b>non-nearest routed</b>
              states sitting well above the reference line — in several cases, orders travel <b>1,000–1,500
              miles farther</b> than necessary to reach a non-nearest factory. <b>Nearest-routed</b> states, in
              contrast, cluster tightly along the reference line, confirming that distance-driven inefficiency
              is concentrated in a specific subset of states rather than spread evenly across the network.
            </p>
          </div>

          <div class="assess-card red">
            <div class="assess-head">
              <span class="assess-head-icon">🚀</span>
              <span class="assess-head-title">Expansion Gaps &amp; Persistent Bottlenecks</span>
            </div>
            <p class="assess-para">
              At an 800-mile threshold, <b>{", ".join(_full_cov)}</b> already achieve full coverage of reachable
              states, while <b>{_top_gap_factory['Factory']}</b> has the largest untapped opportunity — an
              additional <b>{int(_top_gap_factory['Reachable (not serving)'])}</b> states/provinces fall within
              range but are not currently served, out of <b>{int(_top_gap_factory['Total Reachable'])}</b>
              reachable in total. Closing even part of this gap could meaningfully extend the network's
              effective footprint without requiring new factory locations.
            </p>
            <p class="assess-para">
              At the state level, <b>{_bn_top['State/Province']}</b> is the network's leading bottleneck at
              <b>{_bn_top['Avg_Lead_Time']:.1f} days</b> average lead time"""
        if _cong_top is not None:
            _ncd_card_html += f""", while <b>{_cong_top['State/Province']}</b> combines both high shipment
              volume (<b>{int(_cong_top['Shipments']):,}</b> shipments) and an elevated <b>{_cong_top['Delay_Rate']:.1%}</b>
              delay rate — making it a higher-impact target for intervention than smaller, low-volume
              bottleneck states"""
        if _top_underserved is not None:
            _ncd_card_html += f""". <b>{_top_underserved['State']}</b> is the most acute case of an
              underserved region, sitting <b>{_top_underserved['Min Distance to Factory (mi)']:,.0f} miles</b>
              from its nearest factory with a <b>{_top_underserved['Avg Lead Time']:.1f}-day</b> average
              lead time"""
        _ncd_card_html += """. Together, these patterns identify a small number of states that would
              benefit most from operational intervention.
            </p>
          </div>
        </div>
        """
        st.markdown(_ncd_card_html, unsafe_allow_html=True)

        # ── Order Value Segmentation assessment card ───────────────────────
        _high_tier = _tier_summary[_tier_summary["Value_Tier"] == "High Value"].iloc[0]
        _low_tier  = _tier_summary[_tier_summary["Value_Tier"] == "Low Value"].iloc[0]
        _seg_card_html = f"""
        <div class="assess-grid">
          <div class="assess-card blue">
            <div class="assess-head">
              <span class="assess-head-icon">👥</span>
              <span class="assess-head-title">Order Value Segmentation — Network Profile</span>
            </div>
            <p class="assess-para">
              High-value orders (above <b>${_p75:,.2f}</b> per order) account for
              <b>{_high_tier['Revenue_Share']:.1f}%</b> of total network revenue across
              <b>{_high_tier['Orders']:,}</b> orders, with an average profit margin of
              <b>{_high_tier['Profit_Margin']:.1f}%</b> and an average lead time of
              <b>{_high_tier['Avg_Lead_Time']:.1f} days</b>.
              Low-value orders (below <b>${_p25:,.2f}</b>) contribute
              <b>{_low_tier['Revenue_Share']:.1f}%</b> of revenue at a
              <b>{_low_tier['Delay_Rate']:.1%}</b> delay rate —
              {'comparable to' if abs(_high_tier['Delay_Rate'] - _low_tier['Delay_Rate']) < 0.03 else 'diverging from'}
              the <b>{_high_tier['Delay_Rate']:.1%}</b> recorded for high-value orders.
              This indicates that fulfilment reliability does not vary materially by order value tier,
              and delay risk is distributed broadly rather than concentrated in any single segment.
            </p>
          </div>
        </div>
        """
        st.markdown(_seg_card_html, unsafe_allow_html=True)
    except Exception:
        pass


# ── TAB 3: Ship Mode Analysis ──────────────────────────────────────────────────
with tabs[2]:
    # Semantic palette: low delay = cool blue, high delay = warm red/amber
    _SHIP_MODE_COLORS = {
        "Same Day":      "#3b82f6",  # clean blue      – 0% delay, fastest
        "First Class":   "#60a5fa",  # soft blue       – low delay
        "Second Class":  "#f59e0b",  # amber           – moderate delay (5.5%)
        "Standard Class":"#ef4444",  # professional red – high delay (36.9%)
    }

    st.markdown('<div class="section-header">Ship Mode Performance Comparison</div>', unsafe_allow_html=True)
    if delay_threshold != 7:
        st.markdown("<p style='font-size:0.8rem; color:#b45309; margin: -8px 0 12px 0;'>📌 <i>Avg lead time is unaffected by the Delay Threshold filter</i></p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        fig = px.bar(
            ship_stats, x="Ship Mode", y="Avg_Lead_Time",
            color="Ship Mode", text=ship_stats["Avg_Lead_Time"].round(1).astype(str) + "d",
            title="Average Lead Time by Ship Mode",
            labels={"Avg_Lead_Time": "Days"},
            color_discrete_map=_SHIP_MODE_COLORS,
        )
        fig.update_layout(**PLOTLY_THEME, showlegend=False, height=360)
        fig.update_xaxes(tickfont=dict(color="#334155", size=11), title_font=dict(color="#334155", size=12))
        fig.update_yaxes(tickfont=dict(color="#334155", size=11), title_font=dict(color="#334155", size=12))
        fig.update_traces(textfont=dict(color=["#1e3a5f", "white", "white", "white"]))
        if delay_threshold != 7:
            fig.update_traces(marker_opacity=0.35, textfont=dict(color=["#94a3b8", "#94a3b8", "#94a3b8", "#94a3b8"]))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(
            ship_stats, x="Ship Mode", y="Delay_Rate",
            color="Ship Mode",
            text=(ship_stats["Delay_Rate"] * 100).round(1).astype(str) + "%",
            title="Delay Rate by Ship Mode",
            labels={"Delay_Rate": "Rate"},
            color_discrete_map=_SHIP_MODE_COLORS,
        )
        fig.update_layout(**PLOTLY_THEME, showlegend=False, height=360)
        fig.update_xaxes(tickfont=dict(color="#334155", size=11), title_font=dict(color="#334155", size=12))
        fig.update_yaxes(tickformat=".0%", tickfont=dict(color="#334155", size=11), title_font=dict(color="#334155", size=12))
        fig.update_traces(textfont=dict(color=["#1e3a5f", "white", "white", "white"]))
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        fig = px.bar(
            ship_stats, x="Ship Mode", y="Shipments",
            color="Ship Mode",
            text=ship_stats["Shipments"].apply(lambda x: f"{x:,}"),
            title="Volume by Ship Mode",
            labels={"Shipments": "Orders"},
            color_discrete_map=_SHIP_MODE_COLORS,
        )
        fig.update_layout(**PLOTLY_THEME, showlegend=False, height=360)
        fig.update_xaxes(tickfont=dict(color="#334155", size=11), title_font=dict(color="#334155", size=12))
        fig.update_yaxes(tickfont=dict(color="#334155", size=11), title_font=dict(color="#334155", size=12))
        # Same Day bar is light blue — darken its label for legibility
        fig.update_traces(textfont=dict(color=["#1e3a5f", "white", "white", "white"]))
        st.plotly_chart(fig, use_container_width=True)

    # ── Lead Time Variability chart ─────────────────────────────────────────────
    st.markdown('<div class="section-header">Lead Time Variability by Ship Mode</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#334155; margin: 2px 0 12px 0;'>Standard deviation of lead time — higher values indicate less consistent delivery.</p>", unsafe_allow_html=True)
    if delay_threshold != 7:
        st.markdown("<p style='font-size:0.8rem; color:#b45309; margin: -8px 0 12px 0;'>📌 <i>Showing full portfolio — unaffected by the Delay Threshold filter</i></p>", unsafe_allow_html=True)
    fig_std = px.bar(
        ship_stats.sort_values("Avg_Lead_Time"),
        x="Ship Mode", y="Std_Lead_Time",
        color="Ship Mode",
        text=ship_stats.sort_values("Avg_Lead_Time")["Std_Lead_Time"].round(1).astype(str) + "d",
        title="Lead Time Std Deviation by Ship Mode",
        labels={"Std_Lead_Time": "Std Dev (days)"},
        color_discrete_map=_SHIP_MODE_COLORS,
    )
    fig_std.update_layout(**PLOTLY_THEME, showlegend=False, height=360)
    fig_std.update_xaxes(tickfont=dict(color="#334155", size=11), title_font=dict(color="#334155", size=12))
    fig_std.update_yaxes(tickfont=dict(color="#334155", size=11), title_font=dict(color="#334155", size=12))
    fig_std.update_traces(textfont=dict(color=["#1e3a5f", "white", "white", "white"]))
    st.plotly_chart(fig_std, use_container_width=True)

    st.markdown('<div class="section-header">Lead Time Distribution by Ship Mode</div>', unsafe_allow_html=True)
    if delay_threshold != 7:
        st.markdown("<p style='font-size:0.8rem; color:#b45309; margin: -8px 0 12px 0;'>📌 <i>Showing full portfolio — unaffected by the Delay Threshold filter</i></p>", unsafe_allow_html=True)
    fig_box = px.box(
        df, x="Ship Mode", y="Lead Time",
        color="Ship Mode",
        points="outliers",
        title="Lead Time Distribution (Box Plot)",
        labels={"Lead Time": "Lead Time (days)"},
        color_discrete_map=_SHIP_MODE_COLORS,
    )
    fig_box.update_layout(
        **PLOTLY_THEME, height=420, showlegend=False, yaxis_range=[0, 20],
        xaxis=dict(tickfont=dict(color="#334155", size=12), title_font=dict(color="#334155", size=13)),
        yaxis=dict(tickfont=dict(color="#334155", size=12), title_font=dict(color="#334155", size=13)),
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<div class="section-header">Ship Mode × Region Heatmap</div>', unsafe_allow_html=True)
    if delay_threshold != 7:
        st.markdown("<p style='font-size:0.8rem; color:#b45309; margin: -8px 0 12px 0;'>📌 <i>Showing full portfolio — unaffected by the Delay Threshold filter</i></p>", unsafe_allow_html=True)
    pivot = df.pivot_table(
        index="Ship Mode", columns="Region",
        values="Lead Time", aggfunc="mean"
    ).round(1)
    # Pin color scale to full-portfolio range so filters don't rescale colors
    _pivot_full = df_raw.pivot_table(
        index="Ship Mode", columns="Region",
        values="Lead Time", aggfunc="mean"
    )
    _heat_zmin = float(_pivot_full.values.min())
    _heat_zmax = float(_pivot_full.values.max())

    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale="RdYlGn_r",
        zmin=_heat_zmin,
        zmax=_heat_zmax,
        text=[["—" if (v != v) else f"{v:.1f}d" for v in row] for row in pivot.values],
        texttemplate="%{text}",
        textfont={"size": 13},
        colorbar=dict(title="Avg Lead Time (days)", tickfont=dict(color="#334155", size=11), title_font=dict(color="#334155", size=12)),
    ))
    fig_heat.update_layout(
        **PLOTLY_THEME,
        title="Avg Lead Time (days) — Ship Mode × Region",
        height=380,
        xaxis=dict(tickfont=dict(color="#334155", size=12)),
        yaxis=dict(tickfont=dict(color="#334155", size=12)),
        coloraxis_colorbar=dict(
            tickfont=dict(color="#334155", size=11),
            title=dict(font=dict(color="#334155", size=12)),
        ),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Delay Rate: Ship Mode × Factory Heatmap ──────────────────────────────────
    st.markdown('<div class="section-header">Ship Mode × Factory Heatmap</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#334155; margin: 2px 0 12px 0;'>Delay rate (%) by ship mode and factory — identifies which factories drive Standard Class delays.</p>", unsafe_allow_html=True)

    _pivot_dr = df.pivot_table(
        index="Ship Mode", columns="Factory",
        values="Is Delayed", aggfunc="mean"
    ).round(3)
    _pivot_dr_full = df_raw.pivot_table(
        index="Ship Mode", columns="Factory",
        values="Is Delayed", aggfunc="mean"
    )
    _dr_zmin = 0.0
    _dr_zmax = float(_pivot_dr_full.values[~np.isnan(_pivot_dr_full.values)].max())

    fig_heat_dr = go.Figure(data=go.Heatmap(
        z=_pivot_dr.values,
        x=_pivot_dr.columns.tolist(),
        y=_pivot_dr.index.tolist(),
        colorscale="RdYlGn_r",
        zmin=_dr_zmin,
        zmax=_dr_zmax,
        text=[["—" if (v != v) else f"{v*100:.1f}%" for v in row] for row in _pivot_dr.values],
        texttemplate="%{text}",
        textfont={"size": 12},
        colorbar=dict(
            title="Delay Rate",
            tickformat=".0%",
            tickfont=dict(color="#334155", size=11),
            title_font=dict(color="#334155", size=12),
        ),
    ))
    fig_heat_dr.update_layout(
        **PLOTLY_THEME,
        title="Delay Rate (%) — Ship Mode × Factory",
        height=380,
        xaxis=dict(tickfont=dict(color="#334155", size=12)),
        yaxis=dict(tickfont=dict(color="#334155", size=12)),
    )
    st.plotly_chart(fig_heat_dr, use_container_width=True)

    # ── Ship Mode Assessment Cards ──────────────────────────────────────────────
    st.markdown('<div class="section-header">Ship Mode Risk & Efficiency Breakdown</div>', unsafe_allow_html=True)
    if region_sel != "All" or ship_mode_sel != "All" or factory_sel != "All" or delay_threshold != 7:
        st.markdown("<p style='font-size:0.8rem; color:#b45309; margin: -8px 0 12px 0;'>📌 <i>Assessment reflects full portfolio — unaffected by filter selections</i></p>", unsafe_allow_html=True)

    # Stats computed from df_raw (full portfolio) at a FIXED delay threshold — this card is
    # meant to be a static, always-on-screen assessment, so it must not move when the user
    # adjusts the Region / Ship Mode / Factory / Delay Threshold filters.
    _CARD_FIXED_THRESHOLD = 7
    _df_card_fixed = df_raw[["Ship Mode", "Lead Time"]].copy()
    _df_card_fixed["Is Delayed"] = _df_card_fixed["Lead Time"] > _CARD_FIXED_THRESHOLD
    _raw_ship_stats = (
        _df_card_fixed.groupby("Ship Mode")
        .agg(
            Shipments=("Lead Time", "count"),
            Avg_Lead_Time=("Lead Time", "mean"),
            Delay_Rate=("Is Delayed", "mean"),
        )
        .reset_index()
    )
    _sc_delay = _raw_ship_stats.loc[_raw_ship_stats["Ship Mode"] == "Standard Class", "Delay_Rate"].values
    _sc_delay_pct = f"{_sc_delay[0]*100:.1f}%" if len(_sc_delay) else "N/A"
    _sc_lt = _raw_ship_stats.loc[_raw_ship_stats["Ship Mode"] == "Standard Class", "Avg_Lead_Time"].values
    _sc_lt_val = f"{_sc_lt[0]:.1f}" if len(_sc_lt) else "N/A"
    _sc_vol = _raw_ship_stats.loc[_raw_ship_stats["Ship Mode"] == "Standard Class", "Shipments"].values
    _sc_vol_val = f"{int(_sc_vol[0]):,}" if len(_sc_vol) else "N/A"
    _total_vol = _raw_ship_stats["Shipments"].sum()
    _sc_vol_share = f"{(_sc_vol[0]/_total_vol*100):.0f}%" if len(_sc_vol) else "N/A"
    _sd_lt = _raw_ship_stats.loc[_raw_ship_stats["Ship Mode"] == "Same Day", "Avg_Lead_Time"].values
    _sd_lt_val = f"{_sd_lt[0]:.1f}" if len(_sd_lt) else "N/A"
    _fc_delay = _raw_ship_stats.loc[_raw_ship_stats["Ship Mode"] == "First Class", "Delay_Rate"].values
    _fc_delay_pct = f"{_fc_delay[0]*100:.1f}%" if len(_fc_delay) else "N/A"
    _2c_delay = _raw_ship_stats.loc[_raw_ship_stats["Ship Mode"] == "Second Class", "Delay_Rate"].values
    _2c_delay_pct = f"{_2c_delay[0]*100:.1f}%" if len(_2c_delay) else "N/A"

    _sm_cards_html = f"""
    <div class="assess-grid">

      <div class="assess-card red">
        <div class="assess-head">
          <span class="assess-head-icon">⚠️</span>
          <span class="assess-head-title">Standard Class: High Volume, High Risk</span>
        </div>
        <p class="assess-para">
          <b>Standard Class</b> accounts for <b>{_sc_vol_val} shipments</b> — <b>{_sc_vol_share}</b> of all orders —
          yet records the network's highest delay rate at <b>{_sc_delay_pct}</b> and an average lead time of
          <b>{_sc_lt_val} days</b>. In absolute terms, this translates to approximately
          <b>{int(float(_sc_vol[0]) * float(_sc_delay[0])):,} delayed shipments</b> attributable to this mode alone —
          the single largest concentration of delivery risk across the network.
        </p>
        <p class="assess-para">
          The scale of Standard Class exposure means that even a modest reduction in its delay rate would
          produce outsized improvements to overall network performance. Given that faster modes demonstrate
          delay rates at or near zero, the performance gap is not a network-wide constraint — it is
          mode-specific, and concentrated in the highest-volume segment.
        </p>
      </div>

      <div class="assess-card blue">
        <div class="assess-head">
          <span class="assess-head-icon">⚡</span>
          <span class="assess-head-title">Premium Mode Capacity: Strong Performance, Limited Reach</span>
        </div>
        <p class="assess-para">
          The faster modes establish that reliable, low-delay delivery is achievable within the existing
          network. <b>Same Day</b> achieves a <b>{_sd_lt_val}-day</b> average lead time, <b>First Class</b>
          maintains the lowest delay rate of the four modes at <b>{_fc_delay_pct}</b>, and <b>Second Class</b>
          holds at <b>{_2c_delay_pct}</b> — all materially below Standard Class. The performance differential
          between Standard Class and First Class delay rates stands at
          <b>{round(float(_sc_delay[0]) * 100 - float(_fc_delay[0]) * 100, 1)} percentage points</b>.
        </p>
        <p class="assess-para">
          Despite this, Same Day and First Class together account for only
          <b>{int(_raw_ship_stats.loc[_raw_ship_stats["Ship Mode"].isin(["Same Day", "First Class"]), "Shipments"].sum()):,} shipments</b> —
          <b>{round(_raw_ship_stats.loc[_raw_ship_stats["Ship Mode"].isin(["Same Day", "First Class"]), "Shipments"].sum() / _total_vol * 100, 1)}%</b>
          of total volume — while Standard Class alone handles <b>{_sc_vol_val}</b>. The data does not point
          to a capability deficit; it points to a routing allocation imbalance. A review of order assignment
          logic — particularly for orders currently defaulting to Standard Class — is where the most
          measurable gains are likely to be found.
        </p>
      </div>

      <div class="assess-card amber">
        <div class="assess-head">
          <span class="assess-head-icon">🗺️</span>
          <span class="assess-head-title">Regional Variation Persists Across All Modes</span>
        </div>
        <p class="assess-para">
          The Ship Mode × Region heatmap shows that lead times are broadly consistent across regions
          within each mode — Standard Class averages 6.5–6.6 days regardless of region, and Same Day
          holds at 1.0 day everywhere it operates. This uniformity indicates that ship mode selection,
          not regional routing, is the primary driver of lead time outcomes.
        </p>
        <p class="assess-para">
          The sparse coverage visible in the heatmap — particularly for Same Day and First Class — is more
          accurately attributable to low overall adoption of premium modes rather than a geographic service gap.
          Same Day accounts for just 5.4% of total shipments, and its limited heatmap presence reflects
          constrained demand rather than absent network capability. The more actionable implication is that
          a significant portion of orders currently routed through Standard Class may be candidates for
          reassignment to faster modes, which the network demonstrably supports where utilised.
        </p>
      </div>

    </div>
    """
    st.markdown(_sm_cards_html, unsafe_allow_html=True)


# ── TAB 4: Factory Intelligence ────────────────────────────────────────────────
with tabs[3]:
    _top_col1, _top_col2 = st.columns(2)

    with _top_col1:
        st.markdown('<div class="section-header">Product-Level Lead Time</div>', unsafe_allow_html=True)
        product_stats = (
            df.groupby(["Factory", "Product Name"])
            .agg(Avg_Lead_Time=("Lead Time", "mean"), Shipments=("Lead Time", "count"))
            .reset_index()
            .sort_values("Avg_Lead_Time")
        )
        selected_factory = st.selectbox("Select factory", sorted(df["Factory"].unique()))
        pf = product_stats[product_stats["Factory"] == selected_factory]
        fig_prod = px.bar(
            pf.sort_values("Avg_Lead_Time"),
            x="Avg_Lead_Time", y="Product Name",
            orientation="h", color="Avg_Lead_Time",
            color_continuous_scale=[(0, "#93c5fd"), (1, "#1e3a5f")],
            text=pf.sort_values("Avg_Lead_Time")["Avg_Lead_Time"].round(1).astype(str) + "d",
            title=f"Product Lead Times — {selected_factory}",
        )
        fig_prod.update_layout(
            **PLOTLY_THEME, showlegend=False, height=370,
            xaxis=dict(title=dict(text="Avg_Lead_Time", font=dict(color="#1a1a2e")),
                       tickfont=dict(color="#1a1a2e")),
            yaxis=dict(title=dict(text="Product Name", font=dict(color="#1a1a2e")),
                       tickfont=dict(color="#1a1a2e")),
        )
        fig_prod.update_coloraxes(showscale=False)
        st.plotly_chart(fig_prod, use_container_width=True)

    with _top_col2:
        st.markdown('<div class="section-header">Factory Revenue & Profit</div>', unsafe_allow_html=True)
        fig_rev = px.bar(
            factory_stats,
            x="Factory", y=["Total_Sales", "Total_Profit"],
            barmode="group",
            title="Total Sales vs Gross Profit by Factory",
            labels={"value": "Amount ($)", "variable": "Metric"},
            color_discrete_map={"Total_Sales": "#38bdf8", "Total_Profit": "#34d399"},
        )
        fig_rev.update_layout(
            **PLOTLY_THEME, height=460,
            xaxis=dict(title=dict(text="Factory", font=dict(color="#1a1a2e")),
                       tickfont=dict(color="#1a1a2e")),
            yaxis=dict(title=dict(text="Amount ($)", font=dict(color="#1a1a2e")),
                       tickfont=dict(color="#1a1a2e")),
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    # ── Factory Reach Index ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🌐 Factory Reach Index</div>', unsafe_allow_html=True)

    _reach_rows = []
    for factory in df["Factory"].unique():
        _fdf = df[df["Factory"] == factory]
        _states_served = _fdf["State/Province"].nunique()
        _regions_served = _fdf["Region"].nunique()
        _f_stats = factory_stats[factory_stats["Factory"] == factory].iloc[0]
        _reach_rows.append({
            "Factory": factory,
            "States Served": _states_served,
            "Regions Served": _regions_served,
            "Shipments": int(_f_stats["Shipments"]),
            "Avg Lead Time": round(_f_stats["Avg_Lead_Time"], 1),
            "Delay Rate": _f_stats["Delay_Rate"],
        })
    _reach_df = pd.DataFrame(_reach_rows).sort_values("States Served", ascending=False)

    # Color scale domain anchored to df_dd (Date + Region filtered, but immune to the Factory
    # filter) so selecting a factory doesn't collapse Delay Rate / States Served coloring to a
    # meaningless single-point scale. Delay Threshold / Region / Date filters still apply correctly.
    _reach_stats_anchor = (
        df_dd.groupby("Factory")
        .agg(Delay_Rate=("Is Delayed", "mean"), States=("State/Province", "nunique"))
    )
    _reach_delay_min, _reach_delay_max = _reach_stats_anchor["Delay_Rate"].min(), _reach_stats_anchor["Delay_Rate"].max()
    _reach_states_min, _reach_states_max = _reach_stats_anchor["States"].min(), _reach_stats_anchor["States"].max()

    _ri1, _ri2 = st.columns(2)
    with _ri1:
        fig_reach = px.bar(
            _reach_df, x="Factory", y="States Served",
            color="Delay Rate", color_continuous_scale="RdYlGn_r",
            range_color=[_reach_delay_min, _reach_delay_max],
            text="States Served",
            title="States Served per Factory (wide reach + high delay = systemic risk)",
        )
        fig_reach.update_layout(**PLOTLY_THEME, height=360, showlegend=False,
            coloraxis_colorbar=dict(title="Delay Rate", tickformat=".0%",
                title_font=dict(color="#1a1a2e"), tickfont=dict(color="#1a1a2e")))
        st.plotly_chart(fig_reach, use_container_width=True)
    with _ri2:
        st.markdown("**Factory Reach Summary**")
        st.dataframe(
            _reach_df.style.format({
                "Shipments": "{:,}", "Avg Lead Time": "{:.1f}",
                "Delay Rate": "{:.1%}",
            }).background_gradient(subset=["States Served"], cmap="Blues",
                                    vmin=_reach_states_min, vmax=_reach_states_max)
              .background_gradient(subset=["Delay Rate"], cmap="RdYlGn_r",
                                    vmin=_reach_delay_min, vmax=_reach_delay_max),
            use_container_width=True, hide_index=True,
        )

    # ── Factory Clustering Risk ────────────────────────────────────────────────
    st.markdown('<div class="section-header">⚠️ Factory Clustering Risk</div>', unsafe_allow_html=True)
    if region_sel != "All" or ship_mode_sel != "All" or delay_threshold != 7:
        st.markdown(
            "<div style='text-align:left; color:#6b7280; font-size:0.78rem; margin:0 0 14px;'>"
            "📌 <i>Showing full portfolio — unaffected by Region / Ship Mode / Delay Threshold filter selections</i></div>",
            unsafe_allow_html=True,
        )

    def _hav2(lat1, lon1, lat2, lon2):
        R = 3958.8
        φ1, φ2 = np.radians(lat1), np.radians(lat2)
        dφ, dλ = np.radians(lat2-lat1), np.radians(lon2-lon1)
        a = np.sin(dφ/2)**2 + np.cos(φ1)*np.cos(φ2)*np.sin(dλ/2)**2
        return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    _factories = list(FACTORY_COORDS.keys())
    _dist_matrix = pd.DataFrame(index=_factories, columns=_factories, dtype=float)
    for f1 in _factories:
        for f2 in _factories:
            if f1 == f2:
                _dist_matrix.loc[f1, f2] = 0
            else:
                _dist_matrix.loc[f1, f2] = round(_hav2(
                    FACTORY_COORDS[f1]["lat"], FACTORY_COORDS[f1]["lon"],
                    FACTORY_COORDS[f2]["lat"], FACTORY_COORDS[f2]["lon"]
                ), 0)

    _cl1, _cl2 = st.columns([3, 2])
    with _cl1:
        st.markdown("**Factory-to-Factory Distance Matrix** (red = close = clustering risk)")
        fig_cluster = go.Figure(data=go.Heatmap(
            z=_dist_matrix.values,
            x=_factories, y=_factories,
            colorscale="RdYlGn",
            text=[[f"{int(v):,} mi" if v > 0 else "—" for v in row] for row in _dist_matrix.values],
            texttemplate="%{text}",
            textfont={"size": 11, "color": "#1a1a2e"},
            colorbar=dict(title="Distance (mi)", title_font=dict(color="#1a1a2e"), tickfont=dict(color="#1a1a2e")),
            hovertemplate="<b>%{y} ↔ %{x}</b><br>Distance: %{z:,.0f} mi<extra></extra>",
        ))
        fig_cluster.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            font=dict(color="#1a1a2e", family="Space Grotesk"),
            height=360,
            xaxis=dict(tickfont=dict(color="#1a1a2e")),
            yaxis=dict(tickfont=dict(color="#1a1a2e")),
            margin=dict(l=160, r=40, t=20, b=20),
        )
        st.plotly_chart(fig_cluster, use_container_width=True)
    with _cl2:
        _CLUSTER_THRESH = 600  # miles
        _clustered = [(f1, f2, int(_dist_matrix.loc[f1, f2]))
                      for i, f1 in enumerate(_factories)
                      for j, f2 in enumerate(_factories)
                      if i < j and _dist_matrix.loc[f1, f2] < _CLUSTER_THRESH]
        st.markdown(f"**Clustering threshold: < {_CLUSTER_THRESH:,} miles**")
        if _clustered:
            st.warning(f"⚠️ {len(_clustered)} factory pair(s) are within {_CLUSTER_THRESH:,} mi — a regional disruption could affect multiple factories simultaneously.")
            for f1, f2, d in sorted(_clustered, key=lambda x: x[2]):
                st.markdown(f"- **{f1}** ↔ **{f2}**: {d:,} mi")
        else:
            st.success("✅ No factories are dangerously close to each other.")
        # Total shipments at risk from midwest cluster
        _midwest = ["Sugar Shack", "Secret Factory", "The Other Factory"]
        _midwest_ship = factory_stats[factory_stats["Factory"].isin(_midwest)]["Shipments"].sum()
        _total_ship = factory_stats["Shipments"].sum()
        st.metric("Shipments at risk from midwest cluster",
                  f"{_midwest_ship:,} ({_midwest_ship/_total_ship:.0%} of total)")

    # ── Coast Exposure to Central Factory Cluster ─────────────────────────────
    st.markdown('<div class="section-header">🗺️ Coast Exposure to Central Factory Cluster</div>', unsafe_allow_html=True)
    if region_sel != "All" or ship_mode_sel != "All" or factory_sel != "All":
        st.markdown(
            "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
            "📌 <i>Showing full portfolio — unaffected by Region / Ship Mode / Factory filter selections</i>"
            "</div>", unsafe_allow_html=True
        )

    _WEST_STATES  = ["California", "Oregon", "Washington", "Nevada", "Idaho",
                     "Montana", "Wyoming", "Colorado", "Utah", "Arizona", "New Mexico"]
    _EAST_STATES  = ["New York", "Pennsylvania", "New Jersey", "Massachusetts",
                     "Connecticut", "Rhode Island", "New Hampshire", "Vermont",
                     "Maine", "Maryland", "Delaware", "Virginia", "North Carolina",
                     "South Carolina", "Georgia", "Florida"]

    _west_df = state_stats_all[state_stats_all["State/Province"].isin(_WEST_STATES)]
    _east_df = state_stats_all[state_stats_all["State/Province"].isin(_EAST_STATES)]

    _ew1, _ew2, _ew3 = st.columns(3)
    with _ew1:
        st.metric("West Coast Shipments", f"{_west_df['Shipments'].sum():,}",
                  delta=f"{_west_df['Shipments'].sum() / state_stats_all['Shipments'].sum():.0%} of total")
    with _ew2:
        st.metric("East Coast Shipments", f"{_east_df['Shipments'].sum():,}",
                  delta=f"{_east_df['Shipments'].sum() / state_stats_all['Shipments'].sum():.0%} of total")
    with _ew3:
        _west_nearest_dist = np.mean([
            min(_hav2(fc["lat"], fc["lon"],
                      STATE_CENTROIDS.get(s, (0,0))[0],
                      STATE_CENTROIDS.get(s, (0,0))[1])
                for fc in FACTORY_COORDS.values())
            for s in _WEST_STATES if s in STATE_CENTROIDS
        ])
        _east_nearest_dist = np.mean([
            min(_hav2(fc["lat"], fc["lon"],
                      STATE_CENTROIDS.get(s, (0,0))[0],
                      STATE_CENTROIDS.get(s, (0,0))[1])
                for fc in FACTORY_COORDS.values())
            for s in _EAST_STATES if s in STATE_CENTROIDS
        ])
        _avg_coast_dist = (_west_nearest_dist + _east_nearest_dist) / 2
        st.metric("Avg Distance to Nearest Factory",
                  f"{_avg_coast_dist:,.0f} mi",
                  delta=f"W: {_west_nearest_dist:,.0f} mi · E: {_east_nearest_dist:,.0f} mi")

    _ew_compare = pd.DataFrame({
        "Metric": ["Avg Lead Time (d)", "Delay Rate (%)", "Avg Distance to Factory (mi)", "Total Shipments"],
        "West Coast": [
            round(_west_df["Avg_Lead_Time"].mean(), 2),
            round(_west_df["Delay_Rate"].mean() * 100, 1),
            round(_west_nearest_dist, 0),
            int(_west_df["Shipments"].sum()),
        ],
        "East Coast": [
            round(_east_df["Avg_Lead_Time"].mean(), 2),
            round(_east_df["Delay_Rate"].mean() * 100, 1),
            round(_east_nearest_dist, 0),
            int(_east_df["Shipments"].sum()),
        ],
    })
    st.dataframe(_ew_compare, use_container_width=True, hide_index=True)

    # Longitude scatter: factory coverage vs customer density
    _all_state_lons = [(s, STATE_CENTROIDS[s][1], state_stats_all[state_stats_all["State/Province"]==s]["Shipments"].values[0])
                       for s in STATE_CENTROIDS if not state_stats_all[state_stats_all["State/Province"]==s].empty]
    _factory_lons   = [(f, FACTORY_COORDS[f]["lon"]) for f in FACTORY_COORDS]
    fig_ew = go.Figure()
    fig_ew.add_trace(go.Scatter(
        x=[l for _, l, _ in _all_state_lons],
        y=[s for _, _, s in _all_state_lons],
        mode="markers", name="States (shipment volume)",
        marker=dict(size=10, color="#38bdf8", opacity=0.7),
        text=[s for s, _, _ in _all_state_lons],
        hovertemplate="<b>%{text}</b><br>Longitude: %{x:.1f}°<br>Shipments: %{y:,}<extra></extra>",
    ))
    # Colored vlines per factory with legend entries
    _max_y = max(s for _, _, s in _all_state_lons)
    _factory_colors = {
        "Lot's O' Nuts":    "#cc0000",
        "Sugar Shack":      "#e07b00",
        "Secret Factory":   "#6a0572",
        "The Other Factory":"#1a7a2e",
        "Wicked Choccy's":  "#cc8800",
    }
    for fname, flon in _factory_lons:
        fig_ew.add_trace(go.Scatter(
            x=[flon, flon], y=[0, _max_y],
            mode="lines",
            line=dict(color=_factory_colors[fname], width=1.5, dash="dash"),
            name=fname, showlegend=True,
            hovertemplate=f"<b>{fname}</b><br>Longitude: {flon:.1f}°<extra></extra>",
        ))
    fig_ew.update_layout(
        **PLOTLY_THEME, height=320, margin=dict(l=70, r=160, t=40, b=60),
        title="Shipment Volume by Longitude — factory lines show geographic coverage gaps",
        xaxis=dict(title="Longitude (°W)", tickformat=".0f",
                   tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b"),
                   showline=False, gridcolor="#e2e8f0", zeroline=False),
        yaxis=dict(title="Shipments", tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b"),
                   showline=False, gridcolor="#e2e8f0", zeroline=False, rangemode="tozero",
                   range=[-80, _max_y * 1.05]),
    )
    st.plotly_chart(fig_ew, use_container_width=True)

    # ── Factory Network Assessment ─────────────────────────────────────────────
    st.markdown("<div style='margin-top: 48px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Factory Network Assessment</div>', unsafe_allow_html=True)
    if region_sel != "All" or ship_mode_sel != "All" or factory_sel != "All" or delay_threshold != 7:
        st.markdown(
            "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
            "📌 <i>Assessment reflects full portfolio — unaffected by filter selections</i>"
            "</div>", unsafe_allow_html=True
        )

    try:
        _fa_rev_sorted  = factory_stats_all.sort_values("Total_Sales", ascending=False).reset_index(drop=True)
        _fa_top_rev     = _fa_rev_sorted.iloc[0]
        _fa_second_rev  = _fa_rev_sorted.iloc[1]
        _fa_rev_share   = (_fa_top_rev["Total_Sales"] + _fa_second_rev["Total_Sales"]) / factory_stats_all["Total_Sales"].sum() * 100
        _fa_top_reach   = _reach_df_all[_reach_df_all["Factory"] == _fa_top_rev["Factory"]].iloc[0]
        _fa_second_reach = _reach_df_all[_reach_df_all["Factory"] == _fa_second_rev["Factory"]].iloc[0]
        _fa_low_reach   = _reach_df_all.nsmallest(1, "States Served").iloc[0]

        _fa_card1_html = f"""
        <div class="assess-grid">
          <div class="assess-card blue">
            <div class="assess-head">
              <span class="assess-head-icon">🏭</span>
              <span class="assess-head-title">Revenue and Reach: A Shared Concentration Risk</span>
            </div>
            <p class="assess-para">
              <b>{_fa_top_rev['Factory']}</b> and <b>{_fa_second_rev['Factory']}</b> together account for
              <b>{_fa_rev_share:.0f}%</b> of network revenue and also lead the network in geographic footprint,
              serving <b>{int(_fa_top_reach['States Served'])}</b> and
              <b>{int(_fa_second_reach['States Served'])}</b> states/provinces respectively. This indicates that
              revenue scale and geographic reach are mutually reinforcing at the top of the network.
            </p>
            <p class="assess-para">
              By contrast, <b>{_fa_low_reach['Factory']}</b> serves only <b>{int(_fa_low_reach['States Served'])}</b>
              states and records the network's longest average lead time at
              <b>{_fa_low_reach['Avg Lead Time']:.1f} days</b>. This combination of constrained reach and
              extended fulfilment time identifies the facility as a priority focus for targeted performance
              remediation or a deliberate reassessment of its role within the network.
            </p>
          </div>
        </div>
        """
        st.markdown(_fa_card1_html, unsafe_allow_html=True)
    except Exception:
        pass

    try:
        _fa_pl_max  = _product_stats_all.loc[_product_stats_all["Avg_Lead_Time"].idxmax()]
        _fa_pl_min  = _product_stats_all.loc[_product_stats_all["Avg_Lead_Time"].idxmin()]
        _fa_pl_spread = _fa_pl_max["Avg_Lead_Time"] - _fa_pl_min["Avg_Lead_Time"]
        _fa_worst_factory = factory_stats_all.loc[factory_stats_all["Avg_Lead_Time"].idxmax()]

        _fa_pl_title = "Facility-Level Lead Time Variance"
        _fa_pl_same_factory = _fa_pl_min["Factory"] == _fa_pl_max["Factory"]
        if _fa_pl_same_factory:
            _fa_pl_note = (
                f"Notably, both extremes occur at the same facility — <b>{_fa_pl_min['Factory']}</b> — "
                f"indicating that this network-wide spread is concentrated within a single factory rather "
                f"than distributed evenly across the network."
            )
        else:
            _fa_pl_note = (
                "This modest spread suggests that product type plays a limited role in determining lead "
                "time relative to other factors, such as the factory handling the order."
            )

        _fa_card2_html = f"""
        <div class="assess-grid">
          <div class="assess-card green">
            <div class="assess-head">
              <span class="assess-head-icon">📦</span>
              <span class="assess-head-title">{_fa_pl_title}</span>
            </div>
            <p class="assess-para">
              Across all factory-product combinations, average lead time ranges from
              <b>{_fa_pl_min['Avg_Lead_Time']:.1f} days</b> (<b>{_fa_pl_min['Product Name']}</b> at
              {_fa_pl_min['Factory']}) to <b>{_fa_pl_max['Avg_Lead_Time']:.1f} days</b>
              (<b>{_fa_pl_max['Product Name']}</b> at {_fa_pl_max['Factory']}), a network-wide spread of
              <b>{_fa_pl_spread:.1f} days</b>. {_fa_pl_note}
            </p>
            <p class="assess-para">
              <b>{_fa_worst_factory['Factory']}</b> records the network's highest overall average lead time at
              <b>{_fa_worst_factory['Avg_Lead_Time']:.1f} days</b> across its product mix. Targeted operational
              improvements at this facility represent the more direct lever for narrowing this gap.
            </p>
          </div>
        </div>
        """
        st.markdown(_fa_card2_html, unsafe_allow_html=True)
    except Exception:
        pass

    try:
        _fa_cluster_n   = len(_clustered)
        _fa_midwest_pct = _midwest_ship / _total_ship * 100
        _fa_west_lt     = _west_df["Avg_Lead_Time"].mean()
        _fa_east_lt     = _east_df["Avg_Lead_Time"].mean()

        _fa_card3_html = f"""
        <div class="assess-grid">
          <div class="assess-card red">
            <div class="assess-head">
              <span class="assess-head-icon">⚠️</span>
              <span class="assess-head-title">Geographic Concentration Risk</span>
            </div>
            <p class="assess-para">
              <b>{_fa_cluster_n} factory pair(s)</b> fall within the 600-mile clustering threshold, with the
              Midwest cluster — Sugar Shack, Secret Factory, and The Other Factory — handling
              <b>{_fa_midwest_pct:.0f}%</b> of total network shipments directly. A single regional disruption
              could therefore affect multiple facilities simultaneously.
            </p>
            <p class="assess-para">
              West Coast (<b>{_fa_west_lt:.2f}d</b>) and East Coast (<b>{_fa_east_lt:.2f}d</b>) shipments
              currently achieve comparable lead times despite all five factories sitting in a narrow central
              band — meaning neither coast is served by a geographically distinct facility that could act as
              a fallback if the Midwest cluster were disrupted.
            </p>
          </div>
        </div>
        """
        st.markdown(_fa_card3_html, unsafe_allow_html=True)
    except Exception:
        pass

# ── TAB 5: Trends & Deep-Dive ──────────────────────────────────────────────────
with tabs[4]:
    st.markdown('<div class="section-header">Monthly Shipping Trends</div>', unsafe_allow_html=True)

    fig_trend = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08)
    fig_trend.add_trace(
        go.Scatter(x=monthly["Month"], y=monthly["Avg_Lead_Time"],
                   mode="lines+markers", name="Avg Lead Time",
                   line=dict(color="#f59e0b", width=2),
                   fill="tozeroy", fillcolor="rgba(245,158,11,0.1)",
                   hovertemplate="%{x}<br>Avg Lead Time: <b>%{y:.1f} days</b><extra></extra>"),
        row=1, col=1,
    )
    fig_trend.add_trace(
        go.Bar(x=monthly["Month"], y=monthly["Delay_Rate"] * 100,
               name="Delay Rate (%)", marker_color="#f87171",
               hovertemplate="%{x}<br>Delay Rate: <b>%{y:.1f}%</b><extra></extra>"),
        row=2, col=1,
    )
    fig_trend.update_layout(
        **{**PLOTLY_THEME, "font": dict(color="#1e293b", family="Space Grotesk")},
        title="Monthly Lead Time & Delay Rate",
        height=520,
        showlegend=True,
        legend=dict(font=dict(color="#1e293b")),
    )
    fig_trend.update_yaxes(title_text="Lead Time (days)", row=1,
                            tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b"))
    fig_trend.update_yaxes(title_text="Delay Rate (%)", row=2,
                            tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b"))
    fig_trend.update_xaxes(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b"))
    st.plotly_chart(fig_trend, use_container_width=True)

    # ── Assessment card: Monthly Trends ────────────────────────────────────────
    _peak_delay_row  = monthly.loc[monthly["Delay_Rate"].idxmax()]
    _low_delay_row   = monthly.loc[monthly["Delay_Rate"].idxmin()]
    _peak_lt_row     = monthly.loc[monthly["Avg_Lead_Time"].idxmax()]
    _low_lt_row      = monthly.loc[monthly["Avg_Lead_Time"].idxmin()]
    _avg_delay_rate  = monthly["Delay_Rate"].mean() * 100
    _avg_lt_overall  = monthly["Avg_Lead_Time"].mean()
    _lt_range        = monthly["Avg_Lead_Time"].max() - monthly["Avg_Lead_Time"].min()
    _peak_delay_pct  = _peak_delay_row["Delay_Rate"] * 100
    _low_delay_pct   = _low_delay_row["Delay_Rate"] * 100
    _fmt_mo = lambda s: pd.to_datetime(s).strftime("%b %Y")
    _peak_delay_mo   = _fmt_mo(_peak_delay_row["Month"])
    _low_delay_mo    = _fmt_mo(_low_delay_row["Month"])
    _peak_lt_mo      = _fmt_mo(_peak_lt_row["Month"])
    _low_lt_mo       = _fmt_mo(_low_lt_row["Month"])

    _trend_card_html = f"""
    <div class="assess-grid">
      <div class="assess-card {'amber' if _avg_delay_rate > 22 else 'blue'}">
        <div class="assess-head">
          <span class="assess-head-icon">📊</span>
          <span class="assess-head-title">Monthly Shipping Performance — Network Overview</span>
        </div>
        <p class="assess-para">
          Network-wide average lead time of <b>{_avg_lt_overall:.1f} days</b> held within a
          <b>{_lt_range:.1f}-day range</b> over the review period
          (high: <b>{_peak_lt_row['Avg_Lead_Time']:.1f} days</b>, {_peak_lt_mo};
          low: <b>{_low_lt_row['Avg_Lead_Time']:.1f} days</b>, {_low_lt_mo}),
          with no evidence of sustained directional movement.
          Monthly delay incidence averaged <b>{_avg_delay_rate:.1f}%</b>, spanning
          <b>{_low_delay_pct:.1f}%</b> ({_low_delay_mo}) to <b>{_peak_delay_pct:.1f}%</b> ({_peak_delay_mo}).
          The stability of both metrics is indicative of a persistent, underlying constraint within the network rather than a discrete or seasonal event.
        </p>
      </div>
    </div>
    """
    st.markdown(_trend_card_html, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

    # ── Step 14: Correlation Matrix ────────────────────────────────────────────
    st.markdown('<div class="section-header">🔗 Cross-Variable Correlation Matrix</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#475569;margin:-8px 0 12px 0;'>"
        "Correlation matrix across key numeric variables — Lead Time, Sales, Units, Gross Profit, and Cost. "
        "Validates relationships identified across earlier analytical steps.</p>",
        unsafe_allow_html=True
    )

    _corr_df = df[["Lead Time", "Sales", "Units", "Gross Profit", "Cost"]].corr().round(2)
    _corr_labels = _corr_df.columns.tolist()

    fig_corr = go.Figure(data=go.Heatmap(
        z=_corr_df.values,
        x=_corr_labels, y=_corr_labels,
        colorscale="RdBu_r",
        zmin=-1, zmax=1,
        text=[[f"{v:.2f}" for v in row] for row in _corr_df.values],
        texttemplate="%{text}",
        textfont={"size": 12},
        colorbar=dict(
            title="Correlation",
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["-1.00", "-0.50", "0.00", "0.50", "1.00"],
            title_font=dict(color="#1e293b"),
            tickfont=dict(color="#1e293b"),
        ),
        hovertemplate="<b>%{y} × %{x}</b><br>Correlation: <b>%{z:.2f}</b><extra></extra>",
    ))
    fig_corr.update_layout(
        **{**PLOTLY_THEME, "font": dict(color="#1e293b", family="Space Grotesk")},
        height=420,
        title=dict(text="Correlation Matrix — Key Variables", font=dict(size=13, color="#1e293b"), x=0),
        xaxis=dict(tickfont=dict(color="#1e293b", size=11)),
        yaxis=dict(tickfont=dict(color="#1e293b", size=11), autorange="reversed"),
        margin=dict(t=50, b=40, l=100, r=60),
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # ── Correlation Matrix Assessment Card ─────────────────────────────────────
    _lt_sales_corr    = round(_corr_df.loc["Lead Time", "Sales"], 2)
    _sales_gp_corr    = round(_corr_df.loc["Sales", "Gross Profit"], 2)
    _sales_cost_corr  = round(_corr_df.loc["Sales", "Cost"], 2)

    _corr_card_html = f"""
    <div class="assess-grid">
      <div class="assess-card amber">
        <div class="assess-head">
          <span class="assess-head-icon">🔗</span>
          <span class="assess-head-title">Cross-Variable Correlation — Validation Summary</span>
        </div>
        <p class="assess-para">
          Lead Time records a near-zero correlation of <b>{_lt_sales_corr:.2f}</b> with Sales —
          and equivalently with Units, Gross Profit, and Cost — confirming that fulfilment speed
          has no bearing on order financial size. This holds across all financial dimensions
          simultaneously, cross-validating findings from the Order Value Tier and Lead Time
          vs Profit Margin analyses. Sales and Gross Profit exhibit a near-perfect correlation
          of <b>{_sales_gp_corr:.2f}</b>, indicating that revenue growth translates proportionally
          into profit — consistent with a structurally sound distribution model. Sales and Cost
          are similarly tightly linked at <b>{_sales_cost_corr:.2f}</b>, reflecting a volume-driven
          cost structure. Lead Time sits entirely outside this financial cluster — it is an
          independent operational variable, confirming that fulfilment performance is governed
          by logistics and routing factors rather than the financial characteristics of
          individual orders.
        </p>
      </div>
    </div>
    """
    st.markdown(_corr_card_html, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

    # ── Sales Forecasting ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📈 Shipment Volume Forecast — 3-Month Outlook</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#475569;margin:-8px 0 12px 0;'>"
        "Historical monthly shipment volumes with a linear trend projection for the next 3 months. "
        "Shaded band indicates the forecast confidence range (±1 std dev of residuals).</p>",
        unsafe_allow_html=True
    )

    _fc_monthly = (
        df.groupby("Month")
        .agg(Shipments=("Lead Time", "count"))
        .reset_index()
        .sort_values("Month")
    )
    _fc_x = np.arange(len(_fc_monthly))
    _fc_y = _fc_monthly["Shipments"].values
    _fc_coeffs = np.polyfit(_fc_x, _fc_y, 1)
    _fc_trend  = np.polyval(_fc_coeffs, _fc_x)
    _fc_resid_std = np.std(_fc_y - _fc_trend)

    # Generate 3 future months
    _last_month = pd.to_datetime(_fc_monthly["Month"].iloc[-1])
    _future_months = [(_last_month + pd.DateOffset(months=i+1)).strftime("%Y-%m") for i in range(3)]
    _future_x = np.arange(len(_fc_monthly), len(_fc_monthly) + 3)
    _future_y = np.polyval(_fc_coeffs, _future_x)

    _all_x_labels = list(_fc_monthly["Month"]) + _future_months
    _all_trend_y  = np.polyval(_fc_coeffs, np.arange(len(_all_x_labels)))

    fig_fc = go.Figure()
    # Historical bars
    fig_fc.add_trace(go.Bar(
        x=_fc_monthly["Month"], y=_fc_monthly["Shipments"],
        name="Historical Shipments", marker_color="#60a5fa",
        hovertemplate="%{x}<br>Shipments: <b>%{y:,}</b><extra></extra>"
    ))
    # Trend line (full)
    fig_fc.add_trace(go.Scatter(
        x=_all_x_labels, y=_all_trend_y,
        mode="lines", name="Trend Line",
        line=dict(color="#f59e0b", width=2, dash="dot"),
        hovertemplate="%{x}<br>Trend: <b>%{y:.0f}</b><extra></extra>"
    ))
    # Forecast bars
    fig_fc.add_trace(go.Bar(
        x=_future_months, y=_future_y,
        name="Forecast", marker_color="#a78bfa",
        hovertemplate="%{x}<br>Forecast: <b>%{y:.0f}</b><extra></extra>"
    ))
    # Confidence band
    fig_fc.add_trace(go.Scatter(
        x=_future_months + _future_months[::-1],
        y=list(_future_y + _fc_resid_std) + list((_future_y - _fc_resid_std)[::-1]),
        fill="toself", fillcolor="rgba(167,139,250,0.2)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Confidence Range", showlegend=True,
        hoverinfo="skip"
    ))
    # Divider annotation between historical and forecast
    _last_x_idx = len(_fc_monthly) - 1
    fig_fc.add_annotation(
        x=_fc_monthly["Month"].iloc[-1], y=1, yref="paper",
        text="◀ Historical | Forecast ▶",
        showarrow=False, font=dict(color="#94a3b8", size=11),
        xanchor="center", yanchor="bottom"
    )
    fig_fc.update_layout(
        **{**PLOTLY_THEME, "font": dict(color="#1e293b", family="Space Grotesk")},
        height=420, barmode="overlay",
        legend=dict(font=dict(color="#1e293b")),
        xaxis=dict(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b")),
        yaxis=dict(title="Shipments", tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b")),
    )
    st.plotly_chart(fig_fc, use_container_width=True)

    # Forecast assessment card
    _fc_direction = "upward" if _fc_coeffs[0] > 0 else "downward"
    _fc_change    = abs(_fc_coeffs[0])
    _fc_card_html = f"""
    <div class="assess-grid">
      <div class="assess-card {'green' if _fc_coeffs[0] > 0 else 'amber'}">
        <div class="assess-head">
          <span class="assess-head-icon">📈</span>
          <span class="assess-head-title">Shipment Volume Trend — Forward Outlook</span>
        </div>
        <p class="assess-para">
          Historical shipment volumes exhibit a <b>{_fc_direction} trend</b> of approximately
          <b>{_fc_change:.1f} shipments per month</b>. Based on this trajectory, the 3-month
          forecast projects volumes of <b>{_future_y[0]:.0f}</b>, <b>{_future_y[1]:.0f}</b>,
          and <b>{_future_y[2]:.0f}</b> shipments respectively.
          This projection is derived from a linear trend model and should be interpreted as a
          directional indicator rather than a precise prediction — actual volumes may vary
          with seasonal patterns, order mix, or operational changes.
        </p>
      </div>
    </div>
    """
    st.markdown(_fc_card_html, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Order-Level Shipment Timeline</div>', unsafe_allow_html=True)

    # Auto-follow the sidebar Region filter: whenever it changes, re-key the
    # State widget so its options/default refresh to match the new region
    # (and snap back to the full state list when Region is reset to "All").
    if st.session_state.get("_prev_timeline_region") != region_sel:
        st.session_state["_timeline_state_key"] = st.session_state.get("_timeline_state_key", 0) + 1
        st.session_state["_prev_timeline_region"] = region_sel

    # Auto-follow the sidebar Ship Mode filter: whenever it changes, re-key the
    # widget below so its default snaps to the new sidebar value (user can still
    # override it manually afterward, until the sidebar changes again).
    if st.session_state.get("_prev_timeline_ship_mode") != ship_mode_sel:
        st.session_state["_timeline_mode_key"] = st.session_state.get("_timeline_mode_key", 0) + 1
        st.session_state["_prev_timeline_ship_mode"] = ship_mode_sel

    col_f1, col_f2 = st.columns([3, 3])
    with col_f1:
        _timeline_state_options = sorted(
            df_raw[df_raw["Region"] == region_sel]["State/Province"].unique()
            if region_sel != "All" else df_raw["State/Province"].unique()
        )
        state_sel = st.selectbox("State", _timeline_state_options, index=0,
                                 key=f"timeline_state_{st.session_state.get('_timeline_state_key', 0)}")
    with col_f2:
        _timeline_mode_options = sorted(df_raw["Ship Mode"].unique())
        _default_mode = ship_mode_sel if ship_mode_sel in _timeline_mode_options else _timeline_mode_options[0]
        mode_sel  = st.selectbox("Ship Mode", _timeline_mode_options,
                                 index=_timeline_mode_options.index(_default_mode),
                                 key=f"timeline_mode_{st.session_state.get('_timeline_mode_key', 0)}")

    sample_df = (
        df[(df["State/Province"] == state_sel) & (df["Ship Mode"] == mode_sel)]
        .sort_values("Order Date")
        .tail(100)
    )

    if sample_df.empty:
        st.info("No orders match this combination.")
    elif len(sample_df) < 5:
        st.markdown(
            "<div style='font-size:0.78rem;color:#92400e;margin-bottom:6px;'>"
            f"📌 {mode_sel} shipments are limited in volume for this state — "
            "try a broader Ship Mode for a fuller timeline"
            "</div>", unsafe_allow_html=True
        )
    else:
        fig_tl = px.scatter(
            sample_df,
            x="Order Date", y="Lead Time",
            color="Factory",
            hover_data=["Product Name", "Ship Mode", "Sales"],
            title=f"Shipment Lead Times — {state_sel} | {mode_sel} (cap: 100 orders)",
        )
        fig_tl.add_hline(y=delay_threshold, line_dash="dash",
                         line_color="orange",
                         annotation_text=f"Delay threshold ({delay_threshold}d)",
                         annotation_position="top left")
        fig_tl.update_layout(
            **{**PLOTLY_THEME, "font": dict(color="#1e293b", family="Space Grotesk")},
            height=420,
            legend=dict(font=dict(color="#1e293b")),
        )
        fig_tl.update_xaxes(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b"))
        fig_tl.update_yaxes(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b"))
        st.plotly_chart(fig_tl, use_container_width=True)

        # ── Assessment card: Order-Level Timeline ──────────────────────────────
        _tl_avg_lt      = sample_df["Lead Time"].mean()
        _tl_max_lt      = sample_df["Lead Time"].max()
        _tl_min_lt      = sample_df["Lead Time"].min()
        _tl_n_delayed   = (sample_df["Lead Time"] > delay_threshold).sum()
        _tl_delay_rate  = _tl_n_delayed / len(sample_df) * 100
        _tl_n           = len(sample_df)
        _tl_factories   = sample_df["Factory"].nunique()
        _tl_color       = "red" if _tl_delay_rate > 25 else ("amber" if _tl_delay_rate > 10 else "green")

        _tl_card_html = f"""
        <div class="assess-grid">
          <div class="assess-card {_tl_color}">
            <div class="assess-head">
              <span class="assess-head-icon">📦</span>
              <span class="assess-head-title">Shipment Profile — {state_sel} | {mode_sel}</span>
            </div>
            <p class="assess-para">
              The {_tl_n} most recent orders for this state–mode combination record an average lead time of
              <b>{_tl_avg_lt:.1f} days</b> (range: <b>{_tl_min_lt}–{_tl_max_lt} days</b>), fulfilled across
              <b>{_tl_factories}</b> {'factory' if _tl_factories == 1 else 'factories'}.
              Of these, <b>{_tl_n_delayed} of {_tl_n}</b> shipments ({_tl_delay_rate:.1f}%) exceeded the
              <b>{delay_threshold}-day</b> delay threshold —
              {'indicating negligible delay exposure for this combination.' if _tl_delay_rate == 0
               else 'reflecting moderate delay exposure; recurrence warrants monitoring.' if _tl_delay_rate <= 15
               else 'representing an elevated delay incidence relative to the threshold.'}
            </p>
          </div>
        </div>
        """
        st.markdown(_tl_card_html, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    if delay_threshold != 7:
        st.markdown(
            "<p style='font-size:0.8rem; color:#b45309; margin: -8px 0 12px 0;'>"
            "📌 <i>Showing full portfolio — unaffected by the Delay Threshold filter</i></p>",
            unsafe_allow_html=True
        )
    st.markdown('<div class="section-header">Division Performance Over Time</div>', unsafe_allow_html=True)
    div_monthly = (
        df.groupby(["Month", "Division"])
        .agg(Avg_Lead_Time=("Lead Time", "mean"), Shipments=("Lead Time", "count"))
        .reset_index()
    )
    fig_div = px.line(
        div_monthly, x="Month", y="Avg_Lead_Time",
        color="Division", markers=True,
        title="Average Lead Time by Division Over Time",
    )
    fig_div.update_traces(
        hovertemplate="%{fullData.name}<br>%{x}<br>Avg Lead Time: <b>%{y:.1f} days</b><extra></extra>"
    )
    fig_div.update_layout(
        **{**PLOTLY_THEME, "font": dict(color="#1e293b", family="Space Grotesk")},
        height=400,
        legend=dict(font=dict(color="#1e293b")),
    )
    fig_div.update_xaxes(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b"))
    fig_div.update_yaxes(tickfont=dict(color="#1e293b"), title_font=dict(color="#1e293b"))
    st.plotly_chart(fig_div, use_container_width=True)

    # ── Assessment card: Division Performance ──────────────────────────────────
    _div_summary = (
        div_monthly.groupby("Division")
        .agg(Avg_LT=("Avg_Lead_Time", "mean"), Max_LT=("Avg_Lead_Time", "max"))
        .reset_index()
        .sort_values("Avg_LT", ascending=False)
    )
    _div_worst  = _div_summary.iloc[0]
    _div_best   = _div_summary.iloc[-1]
    _div_spread = _div_worst["Avg_LT"] - _div_best["Avg_LT"]
    _div_color  = "red" if _div_spread > 2 else ("amber" if _div_spread > 1 else "green")

    _sugar_rows = div_monthly[div_monthly["Division"] == "Sugar"]
    _sugar_note = ""
    if not _sugar_rows.empty:
        _sugar_peak = _sugar_rows.loc[_sugar_rows["Avg_Lead_Time"].idxmax()]
        _sugar_note = (f" The <b>Sugar</b> division recorded its peak at "
                       f"<b>{_sugar_peak['Avg_Lead_Time']:.1f} days</b> in "
                       f"<b>{pd.to_datetime(_sugar_peak['Month']).strftime('%b %Y')}</b>, "
                       f"the highest single-month average across all divisions.")

    _div_card_html = f"""
    <div class="assess-grid">
      <div class="assess-card {_div_color}">
        <div class="assess-head">
          <span class="assess-head-icon">🍫</span>
          <span class="assess-head-title">Division-Level Lead Time Divergence</span>
        </div>
        <p class="assess-para">
          Lead time performance varies materially across divisions.
          <b>{_div_worst['Division']}</b> records the highest average at
          <b>{_div_worst['Avg_LT']:.1f} days</b>, while <b>{_div_best['Division']}</b>
          leads at <b>{_div_best['Avg_LT']:.1f} days</b> —
          a <b>{_div_spread:.1f}-day spread</b> between the highest and lowest-performing divisions.{_sugar_note}
        </p>
        <p class="assess-para">
          {'This narrow spread indicates broadly consistent cross-division fulfilment.' if _div_spread <= 1
           else "Sugar's elevated lead time is consistent with the broader network finding that fulfilment performance is driven primarily by factory and ship mode assignment rather than division-level characteristics."}
        </p>
      </div>
    </div>
    """
    st.markdown(_div_card_html, unsafe_allow_html=True)

    with st.expander("📊 Raw Order Data Explorer"):
        cols_show = ["Order ID", "Order Date", "Ship Date", "Lead Time",
                     "Factory", "State/Province", "Region", "Ship Mode",
                     "Product Name", "Sales", "Gross Profit", "Is Delayed"]
        _raw_export = df[cols_show].sort_values("Lead Time", ascending=False).reset_index(drop=True)
        st.dataframe(_raw_export, use_container_width=True)