import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Behavior Dashboard")

# -------- LOAD DATA --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "data.csv")
df = pd.read_csv(file_path)

# -------- SIDEBAR FILTERS (DECOMPOSITION LOGIC) --------
st.sidebar.header("Filters")

device = st.sidebar.selectbox("Device", ["All"] + list(df["Primary_Device"].unique()))
age = st.sidebar.selectbox("Age Group", ["All"] + list(df["Age_Band"].unique()))
day = st.sidebar.selectbox("Day Type", ["All"] + list(df["Day_Type"].unique()))
risk = st.sidebar.selectbox("Risk Level", ["All"] + list(df["Risk_Level"].unique()))

filtered_df = df.copy()

if device != "All":
    filtered_df = filtered_df[filtered_df["Primary_Device"] == device]

if age != "All":
    filtered_df = filtered_df[filtered_df["Age_Band"] == age]

if day != "All":
    filtered_df = filtered_df[filtered_df["Day_Type"] == day]

if risk != "All":
    filtered_df = filtered_df[filtered_df["Risk_Level"] == risk]

# -------- COLORS --------
colors = ["#D65DB1", "#FF6F61", "#B0BEC5", "#7F8C8D"]

# ===================================
# 📊 STACKED BAR (CORE BEHAVIOR)
# ===================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Device vs Risk Behavior")

    fig1 = px.histogram(
        filtered_df,
        x="Primary_Device",
        color="Risk_Level",
        barmode="stack",
        color_discrete_sequence=colors
    )

    fig1.update_layout(plot_bgcolor="#2F3E4E", paper_bgcolor="#2F3E4E", font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

# ===================================
# 🌞 SUNBURST (HIERARCHY)
# ===================================
with col2:
    st.subheader("Behavior Hierarchy")

    fig2 = px.sunburst(
        filtered_df,
        path=["Primary_Device", "Screen_Size_Type", "Risk_Level"],
        color="Risk_Level",
        color_discrete_sequence=colors
    )

    fig2.update_layout(plot_bgcolor="#2F3E4E", paper_bgcolor="#2F3E4E", font_color="white")
    st.plotly_chart(fig2, use_container_width=True)

# ===================================
# 📉 FUNNEL (INTENSITY BEHAVIOR)
# ===================================
col3, col4 = st.columns(2)

with col3:
    st.subheader("Screen Time Intensity")

    funnel_data = filtered_df["Screen_Time_Level"].value_counts().reset_index()
    funnel_data.columns = ["Stage", "Count"]

    fig3 = px.funnel(
        funnel_data,
        x="Count",
        y="Stage",
        color="Stage",
        color_discrete_sequence=colors
    )

    fig3.update_layout(plot_bgcolor="#2F3E4E", paper_bgcolor="#2F3E4E", font_color="white")
    st.plotly_chart(fig3, use_container_width=True)

# ===================================
# 📈 RIBBON (SIMULATED USING LINE)
# ===================================
with col4:
    st.subheader("Behavioral Flow (Age vs Usage)")

    fig4 = px.line(
        filtered_df,
        x="Age",
        y="Avg_Daily_Screen_Time_hr",
        color="Screen_Time_Level",
        color_discrete_sequence=colors
    )

    fig4.update_layout(plot_bgcolor="#2F3E4E", paper_bgcolor="#2F3E4E", font_color="white")
    st.plotly_chart(fig4, use_container_width=True)

# ===================================
# 🔍 DRILL-DOWN TABLE
# ===================================
st.subheader("Drill-down Behavioral Data")

selected_risk = st.selectbox(
    "Select Risk Level for Detailed View",
    ["All"] + list(filtered_df["Risk_Level"].unique())
)

if selected_risk != "All":
    table_df = filtered_df[filtered_df["Risk_Level"] == selected_risk]
else:
    table_df = filtered_df

st.dataframe(table_df)