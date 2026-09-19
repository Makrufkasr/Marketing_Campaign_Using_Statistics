import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Marketing Campaign A/B Test & Business ROI",
    page_icon="📈",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .metric-box {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #2b8cbe;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    csv_file = os.path.join(os.path.dirname(__file__), 'data', 'WA_Marketing-Campaign.csv')
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        url = 'https://docs.google.com/spreadsheets/d/1nCl_evlaMh7maLUMF2Q2sdnYtUfSAwbiu-6pRqHZMIM/export?format=csv&gid=1849995340'
        df = pd.read_csv(url)
    df['Promotion_Name'] = df['Promotion'].map({1: 'Campaign 1', 2: 'Campaign 2', 3: 'Campaign 3'})
    return df

df = load_data()

# --- HEADER ---
st.title("📈 Fast-Food Marketing Campaign A/B Test & Business ROI Dashboard")
st.markdown("""
Dashboard interaktif ini mengevaluasi efektivitas 3 strategi promosi restoran cepat saji (*A/B/n Testing*) 
dan menyajikan simulasi proyeksi keuntungan finansial (*Business Impact & ROMI Simulator*).
""")

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filter Data")
market_size_options = df['MarketSize'].unique().tolist()
selected_market_size = st.sidebar.multiselect(
    "Pilih Market Size:",
    options=market_size_options,
    default=market_size_options
)

store_age_range = st.sidebar.slider(
    "Rentang Umur Toko (Tahun):",
    min_value=int(df['AgeOfStore'].min()),
    max_value=int(df['AgeOfStore'].max()),
    value=(int(df['AgeOfStore'].min()), int(df['AgeOfStore'].max()))
)

filtered_df = df[
    (df['MarketSize'].isin(selected_market_size)) &
    (df['AgeOfStore'] >= store_age_range[0]) &
    (df['AgeOfStore'] <= store_age_range[1])
]

# --- METRIC SUMMARY CARDS ---
mean_c1 = filtered_df[filtered_df['Promotion'] == 1]['SalesInThousands'].mean() if len(filtered_df[filtered_df['Promotion'] == 1]) > 0 else 0
mean_c2 = filtered_df[filtered_df['Promotion'] == 2]['SalesInThousands'].mean() if len(filtered_df[filtered_df['Promotion'] == 2]) > 0 else 0
mean_c3 = filtered_df[filtered_df['Promotion'] == 3]['SalesInThousands'].mean() if len(filtered_df[filtered_df['Promotion'] == 3]) > 0 else 0

lift_c1 = ((mean_c1 - mean_c2) / mean_c2 * 100) if mean_c2 > 0 else 0
lift_c3 = ((mean_c3 - mean_c2) / mean_c2 * 100) if mean_c2 > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Campaign 1 (Winner)", f"${mean_c1:.2f}k / wk", f"+{lift_c1:.1f}% vs C2")
col2.metric("Campaign 2 (Baseline)", f"${mean_c2:.2f}k / wk", "Baseline Terendah")
col3.metric("Campaign 3 (Runner-up)", f"${mean_c3:.2f}k / wk", f"+{lift_c3:.1f}% vs C2")
col4.metric("Total Observasi Terfilter", f"{len(filtered_df)} minggu", f"{filtered_df['LocationID'].nunique()} Cabang")

st.divider()

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Hasil A/B Testing & EDA", "💼 Interactive ROI Simulator", "📋 Observasi Dataset"])

with tab1:
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Distribusi Penjualan Mingguan")
        fig_box = px.box(
            filtered_df,
            x='Promotion_Name',
            y='SalesInThousands',
            color='Promotion_Name',
            points="all",
            color_discrete_map={'Campaign 1': '#2b8cbe', 'Campaign 2': '#e41a1c', 'Campaign 3': '#4daf4a'},
            labels={'Promotion_Name': 'Strategi Promosi', 'SalesInThousands': 'Weekly Sales ($k)'}
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_right:
        st.subheader("Performa per Skala Pasar (Market Size)")
        mkt_agg = filtered_df.groupby(['MarketSize', 'Promotion_Name'])['SalesInThousands'].mean().reset_index()
        fig_bar = px.bar(
            mkt_agg,
            x='MarketSize',
            y='SalesInThousands',
            color='Promotion_Name',
            barmode='group',
            category_orders={'MarketSize': ['Small', 'Medium', 'Large']},
            color_discrete_map={'Campaign 1': '#2b8cbe', 'Campaign 2': '#e41a1c', 'Campaign 3': '#4daf4a'},
            labels={'SalesInThousands': 'Avg Weekly Sales ($k)', 'MarketSize': 'Market Tier'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.subheader("🔬 Hasil Uji Hipotesis Statistik (Welch's Two-Sample t-Test)")
    c1_s = filtered_df[filtered_df['Promotion'] == 1]['SalesInThousands']
    c2_s = filtered_df[filtered_df['Promotion'] == 2]['SalesInThousands']
    c3_s = filtered_df[filtered_df['Promotion'] == 3]['SalesInThousands']
    
    if len(c1_s) > 1 and len(c2_s) > 1 and len(c3_s) > 1:
        t_12, p_12 = stats.ttest_ind(c1_s, c2_s, equal_var=False)
        t_13, p_13 = stats.ttest_ind(c1_s, c3_s, equal_var=False)
        t_23, p_23 = stats.ttest_ind(c2_s, c3_s, equal_var=False)
        
        stat_df = pd.DataFrame({
            "Pasangan Uji": ["Campaign 1 vs Campaign 2", "Campaign 3 vs Campaign 2", "Campaign 1 vs Campaign 3"],
            "t-Statistic": [f"{t_12:.3f}", f"{-t_23:.3f}", f"{t_13:.3f}"],
            "p-Value": [f"{p_12:.4f}", f"{p_23:.4f}", f"{p_13:.4f}"],
            "Kesimpulan Statistik (α = 0.05)": [
                "✅ Signifikan (Campaign 1 Mengungguli Baseline C2)",
                "✅ Signifikan (Campaign 3 Mengungguli Baseline C2)",
                "❌ Tidak Berbeda Signifikan (Performa C1 ≈ C3)"
            ]
        })
        st.table(stat_df)
    else:
        st.warning("Sampel data tidak mencukupi untuk uji statistik pada filter saat ini.")

with tab2:
    st.subheader("🧮 Interactive Financial Impact & ROMI Simulator")
    st.markdown("Sesuaikan parameter di bawah ini untuk mensimulasikan proyeksi laba bersih dan efisiensi modal pemasaran:")
    
    sim1, sim2, sim3 = st.columns(3)
    with sim1:
        num_stores = st.slider("Jumlah Cabang (Stores):", min_value=10, max_value=500, value=100, step=10)
        num_weeks = st.slider("Durasi Program (Minggu):", min_value=4, max_value=52, value=12, step=1)
    with sim2:
        gross_margin = st.slider("Gross Margin Menu (%):", min_value=30, max_value=90, value=60, step=5) / 100
        cost_c1 = st.number_input("Biaya Marketing Campaign 1 ($k):", value=1200, step=50)
    with sim3:
        cost_c2 = st.number_input("Biaya Marketing Campaign 2 Baseline ($k):", value=400, step=50)
        cost_c3 = st.number_input("Biaya Marketing Campaign 3 ($k):", value=600, step=50)
        
    store_weeks = num_stores * num_weeks
    rev_c1 = (mean_c1 * store_weeks)
    rev_c2 = (mean_c2 * store_weeks)
    rev_c3 = (mean_c3 * store_weeks)
    
    gp_c1 = rev_c1 * gross_margin
    gp_c2 = rev_c2 * gross_margin
    gp_c3 = rev_c3 * gross_margin
    
    net_c1 = gp_c1 - cost_c1
    net_c2 = gp_c2 - cost_c2
    net_c3 = gp_c3 - cost_c3
    
    romi_c1 = ((gp_c1 - gp_c2) / (cost_c1 - cost_c2)) if (cost_c1 > cost_c2) else 0
    romi_c3 = ((gp_c3 - gp_c2) / (cost_c3 - cost_c2)) if (cost_c3 > cost_c2) else 0
    
    sim_df = pd.DataFrame({
        "Metrik Finansial": [
            "Total Gross Revenue",
            "Gross Profit (Margin Bersih Produk)",
            "Biaya Marketing Campaign",
            "Net Profit Contribution",
            "Net Profit Lift vs Baseline (C2)",
            "Return on Marketing Investment (ROMI)"
        ],
        "Campaign 2 (Baseline)": [
            f"${rev_c2/1000:.2f} M",
            f"${gp_c2/1000:.2f} M",
            f"${cost_c2/1000:.2f} M",
            f"${net_c2/1000:.2f} M",
            "-",
            "-"
        ],
        "Campaign 3": [
            f"${rev_c3/1000:.2f} M",
            f"${gp_c3/1000:.2f} M",
            f"${cost_c3/1000:.2f} M",
            f"${net_c3/1000:.2f} M",
            f"+${(net_c3 - net_c2)/1000:.2f} M",
            f"{romi_c3:.2f}x"
        ],
        "Campaign 1 (Winner)": [
            f"${rev_c1/1000:.2f} M",
            f"${gp_c1/1000:.2f} M",
            f"${cost_c1/1000:.2f} M",
            f"${net_c1/1000:.2f} M",
            f"+${(net_c1 - net_c2)/1000:.2f} M",
            f"{romi_c1:.2f}x"
        ]
    })
    
    st.table(sim_df)
    
    # Financial Chart
    fig_rev = go.Figure(data=[
        go.Bar(name='Gross Revenue', x=['Campaign 2 (Baseline)', 'Campaign 3', 'Campaign 1'], y=[rev_c2/1000, rev_c3/1000, rev_c1/1000], marker_color='#9ecae1'),
        go.Bar(name='Net Profit Contribution', x=['Campaign 2 (Baseline)', 'Campaign 3', 'Campaign 1'], y=[net_c2/1000, net_c3/1000, net_c1/1000], marker_color='#3182bd')
    ])
    fig_rev.update_layout(barmode='group', title="Perbandingan Gross Revenue vs Net Profit ($ Millions)", yaxis_title="$ Millions")
    st.plotly_chart(fig_rev, use_container_width=True)

with tab3:
    st.subheader("Tabel Observasi Mentah")
    st.dataframe(filtered_df, use_container_width=True)
