import streamlit as st

st.set_page_config(page_title="UpRight App", layout="centered")
st.title("UpRight App")

st.write("Welcome to the UpRight Social Tracker!")



import streamlit as st
import pandas as pd
import plotly.express as px

# App Config
st.set_page_config(page_title="UpRight", page_icon="📈", layout="centered")
st.title("📈 UpRight: Your Life as a Chart")

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["My Chart", "Explore", "Notifications"])

# Dummy data for charts
df = pd.DataFrame({
    "Category": ["Income", "Assets", "Education", "Debt"],
    "Value": [52000, 140000, 12, 3500],
    "Color": ["green", "blue", "yellow", "red"]
})

# My Chart Section
if section == "My Chart":
    st.subheader("📊 Personal Growth Overview")
    col1, col2 = st.columns(2)
    col1.metric("Income Growth", "+22.4%", "+3.5%")
    col2.metric("Debt Reduction", "-8.7%", "-1.1%")

    fig = px.bar(df, x="Category", y="Value", color="Category",
                 color_discrete_map={"Income":"green", "Assets":"blue", "Education":"yellow", "Debt":"red"})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.write("### 📘 Abstract Metrics")
    st.write("- Books Read: 28")
    st.write("- Certifications Completed: 3")
    st.write("- Projects Launched: 6")
    st.write("- Family Time Tracked: 162 hrs")

# Explore Section
elif section == "Explore":
    st.subheader("🌍 Explore Profiles")
    profiles = [
        {"name": "@EcoChloe", "title": "Sustainable Designer", "vibes": "🌱 Design / Impact"},
        {"name": "@ByteSmith", "title": "Indie Developer", "vibes": "💻 Code / Web3"},
        {"name": "@NovaFlux", "title": "Crypto Creator", "vibes": "🧬 AI / Crypto"}
    ]

    for profile in profiles:
        st.markdown(f"**{profile['name']}** — {profile['title']}  ")
        st.caption(profile['vibes'])
        st.button(f"Support {profile['name']}", key=profile['name'])
        st.markdown("---")

# Notifications Section
elif section == "Notifications":
    st.subheader("🔔 Notifications")
    notifications = [
        "AlexRobot invested 250 Support Credits in you!",
        "Janelle commented on your income chart.",
        "Mateo followed your anonymous profile.",
        "You hit a milestone: 10 projects completed!"
    ]

    for note in notifications:
        st.success(note)


