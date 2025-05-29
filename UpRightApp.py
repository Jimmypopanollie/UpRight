import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# MUST be the first Streamlit command
st.set_page_config(page_title="UpRight", page_icon="📈", layout="centered")

# Safe to toast after page config
st.toast("UpRight App refreshed 🎯", icon="🚀")

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Feed", "My Chart", "Explore", "Notifications"])

# Dummy data
df = pd.DataFrame({
    "Category": ["Income", "Assets", "Education", "Debt"],
    "Value": [52000, 140000, 12, 3500],
    "Color": ["green", "blue", "yellow", "red"]
})

# -------------------------------
# 📲 FEED SECTION
# -------------------------------
if section == "Feed":
    st.title("📲 UpRight Feed")
    for i in range(3):
        st.image("https://placehold.co/48x48", width=48)
        st.markdown(f"**@anon_user{i+1}**")
        st.text("Posted on: " + datetime.now().strftime("%b %d, %Y"))
        fig = px.bar(df, x="Category", y="Value", color="Category", color_discrete_sequence=df["Color"])
        st.plotly_chart(fig, use_container_width=True)
        st.text("Income Growth: +22.4% • Debt Reduction: -8.7%")
        st.radio("React", ["🔥", "💡", "🙌", "💰"], key=f"react_{i}", horizontal=True)
        st.text_input("Leave a comment:", key=f"comment_{i}")
        st.markdown("---")

# -------------------------------
# 📈 DASHBOARD SECTION
# -------------------------------
elif section == "My Chart":
    st.title("📈 UpRight: Your Life as a Chart")
    st.write("Welcome to the UpRight Social Tracker!")

    chart_type = st.radio("Select chart type", ["Bar", "Line"], horizontal=True)
    time_range = st.selectbox("Time Range", ["1W", "1M", "1Y", "All"])

    col1, col2 = st.columns(2)
    col1.metric("Income Growth", "+22.4%", "+3.5%")
    col2
