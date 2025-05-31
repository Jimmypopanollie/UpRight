# ─────────────────────────────────────────────────────────────────────────────
# UpRightApp.py — Simplified Streamlit‐Native Cards & CSS
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ──────────────────────────────────────────────────────────
# 1) PAGE CONFIG: Must be first Streamlit command
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UpRight", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────
# 2) MINIMAL CSS FOR “CARD” EFFECT
# ──────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Light gray background overall */
    body {
        background-color: #F5F7FA;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Add subtle shadow + rounded corners to containers */
    .card-container {
        background-color: #FFFFFF;
        border-radius: 8px;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        padding: 16px;
        margin-bottom: 24px;
    }
    /* Avatar style */
    .avatar-img {
        border-radius: 50%;
        width: 48px;
        height: 48px;
    }
    /* Reaction buttons spacing */
    .react-button {
        margin-right: 12px;
        cursor: pointer;
        font-size: 1.25rem;
    }
    /* Horizontal “moments” strip */
    .moment-container {
        display: flex;
        overflow-x: auto;
        gap: 12px;
        padding-bottom: 8px;
        margin-bottom: 24px;
    }
    .moment {
        min-width: 180px;
        height: 100px;
        background-color: #ECEFF4;
        border-radius: 8px;
        flex-shrink: 0;
        background-size: cover;
        background-position: center;
    }
    /* Hide scrollbar but still scroll */
    .moment-container::-webkit-scrollbar {
        height: 6px;
    }
    .moment-container::-webkit-scrollbar-thumb {
        background-color: #CBD5E0;
        border-radius: 3px;
    }
    @media (max-width: 600px) {
      .moment { min-width: 140px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ──────────────────────────────────────────────────────────
# 3) OPTIONAL TOAST ON REFRESH (works in newer Streamlit)
# ──────────────────────────────────────────────────────────
try:
    st.toast("UpRight App refreshed 🎯", icon="🚀")
except:
    pass

# ──────────────────────────────────────────────────────────
# 4) SIDEBAR NAVIGATION
# ──────────────────────────────────────────────────────────
st.sidebar.title("👋 Welcome to UpRight")
section = st.sidebar.radio(
    "Go to",
    ["Feed", "My Chart", "Explore", "Notifications"],
    index=0
)

# ──────────────────────────────────────────────────────────
# 5) DUMMY DATA FOR CHARTS & SPARKLINES
# ──────────────────────────────────────────────────────────
# Accent palette
ACCENT_GREEN  = "#10B981"
ACCENT_RED    = "#EF4444"
ACCENT_BLUE   = "#3B82F6"
ACCENT_YELLOW = "#FBBF24"

# Dummy bar/line data for main chart
df = pd.DataFrame({
    "Category": ["Income",     "Assets",    "Education", "Debt"],
    "Value":     [55200,       140000,      12,          3500],
    "Color":     [ACCENT_GREEN, ACCENT_BLUE, ACCENT_YELLOW, ACCENT_RED]
})

# Dummy history for sparklines
months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
income_history  = [45000, 47000, 49500, 51000, 52800, 55200]
debt_history    = [5000, 4800, 4600, 4200, 3800, 3500]
spark_income_df = pd.DataFrame({ "Month": months, "Income": income_history })
spark_debt_df   = pd.DataFrame({ "Month": months, "Debt": debt_history })

# ──────────────────────────────────────────────────────────
# 📲 FEED SECTION — Native Streamlit containers & columns
# ──────────────────────────────────────────────────────────
if section == "Feed":
    st.markdown("<h1>📲 UpRight Feed</h1>", unsafe_allow_html=True)

    # 5a) “Moments” strip at top
    st.markdown(
        """
        <div class="moment-container">
          <div class="moment" style="background-image: url(https://placehold.co/200x100/ff7f7f/333?text=Moment+1)"></div>
          <div class="moment" style="background-image: url(https://placehold.co/200x100/7fbfff/333?text=Moment+2)"></div>
          <div class="moment" style="background-image: url(https://placehold.co/200x100/7fff7f/333?text=Moment+3)"></div>
          <div class="moment" style="background-image: url(https://placehold.co/200x100/ffff7f/333?text=Moment+4)"></div>
          <div class="moment" style="background-image: url(https://placehold.co/200x100/dc7fff/333?text=Moment+5)"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 5b) Render 3 sample posts
    for i in range(3):
        username   = f"anon_user_{i+1}"
        avatar_url = "https://placehold.co/48x48"
        followers  = f"{(i+1)*750 + 250} followers"
        posted_on  = datetime.now().strftime("%b %d, %Y • %I:%M %p")

        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)

            # Header row: avatar + username/followers + timestamp
            header_col1, header_col2, header_col3 = st.columns([1, 6, 2], gap="small")
            with header_col1:
                st.markdown(f'<img src="{avatar_url}" class="avatar-img">', unsafe_allow_html=True)
            with header_col2:
                st.markdown(f"**@{username}**  \n<small style='color:#6B7280;'>{followers}</small>", unsafe_allow_html=True)
            with header_col3:
                st.markdown(f"<small style='color:#9CA3AF;'>{posted_on}</small>", unsafe_allow_html=True)

            st.markdown("---")  # divider

            # In‐post chart
            fig_feed = px.bar(
                df, x="Category", y="Value",
                color="Category", 
                color_discrete_sequence=df["Color"],
                template="none"
            )
            fig_feed.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=160
            )
            st.plotly_chart(fig_feed, use_container_width=True)

            # Footnotes: growth + reactions + comment
            st.markdown(
                f"""
                <p>Income Growth: <span style="color:{ACCENT_GREEN};">+22.4%</span>  
                • Debt Reduction: <span style="color:{ACCENT_RED};">-8.7%</span></p>
                <div>
                  <span class="react-button">🔥</span>
                  <span class="react-button">💡</span>
                  <span class="react-button">🙌</span>
                  <span class="react-button">💰</span>
                </div>
                <div style="margin-top: 8px;">
                  <input type="text" placeholder="Leave a comment…" 
                         style="width:100%; padding:8px; border-radius:4px; border:1px solid #CBD5E0;" />
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)  # close card-container

            st.markdown("")  # small blank between posts


# ──────────────────────────────────────────────────────────
# 📈 MY CHART SECTION — Native Streamlit layout + Sparklines
# ──────────────────────────────────────────────────────────
elif section == "My Chart":
    st.markdown("<h1>📈 UpRight: Your Life as a Chart</h1>", unsafe_allow_html=True)
    st.markdown("<p>Welcome to the UpRight Social Tracker!</p>", unsafe_allow_html=True)

    # 6a) Top Metrics & Sparklines
    colA, colB, colC, colD = st.columns([1, 1, 1, 2], gap="large")

    # Income Growth Card (with sparkline)
    with colA:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown(f"<h3>Income Growth</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:2rem; color:{ACCENT_GREEN}; margin:0;'>+22.4%</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.9rem; color:{ACCENT_GREEN}; margin:0;'>▲ 3.5%</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Inline sparkline below
        spark_fig_inc = px.line(
            spark_income_df, x="Month", y="Income",
            line_shape="spline", template="none", markers=False
        )
        spark_fig_inc.update_traces(line=dict(color=ACCENT_GREEN, width=2))
        spark_fig_inc.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(showgrid=False, visible=False),
            height=100,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(spark_fig_inc, use_container_width=True)

    # Debt Reduction Card (with sparkline)
    with colB:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown(f"<h3>Debt Reduction</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:2rem; color:{ACCENT_RED}; margin:0;'>-8.7%</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.9rem; color:{ACCENT_RED}; margin:0;'>▼ 1.1%</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        spark_fig_debt = px.line(
            spark_debt_df, x="Month", y="Debt",
            line_shape="spline", template="none", markers=False
        )
        spark_fig_debt.update_traces(line=dict(color=ACCENT_RED, width=2))
        spark_fig_debt.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(showgrid=False, visible=False),
            height=100,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(spark_fig_debt, use_container_width=True)

    # Chart Type Selector Card
    with colC:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown(f"<h3>Select Chart Type</h3>", unsafe_allow_html=True)
            # radio buttons beneath
            chart_type = st.radio("", ["Bar", "Line"], horizontal=True, key="chart_type_selector")
            st.markdown("</div>", unsafe_allow_html=True)

    # Time Range Selector Card
    with colD:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown(f"<h3>Time Range</h3>", unsafe_allow_html=True)
            time_range = st.selectbox("", ["1W", "1M", "1Y", "All"], key="time_range_selector")
            st.markdown("</div>", unsafe_allow_html=True)

    # 6b) Main Plotly Chart Below
    chart_choice = st.session_state.get("chart_type_selector", "Bar")
    if chart_choice == "Bar":
        fig2 = px.bar(
            df, x="Category", y="Value",
            color="Category", color_discrete_sequence=df["Color"],
            template="seaborn"
        )
    else:
        fig2 = px.line(
            df, x="Category", y="Value", template="seaborn"
        )
    st.plotly_chart(fig2, use_container_width=True)

    # 6c) Abstract Metrics at Bottom
    st.markdown("<h3>📚 Abstract Metrics</h3>", unsafe_allow_html=True)
    am_col1, am_col2 = st.columns(2, gap="large")

    with am_col1:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown("<p><strong>Books Read:</strong> 28</p>", unsafe_allow_html=True)
            st.markdown("<p><strong>Courses Completed:</strong> 5</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with am_col2:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown("<p><strong>Family Time Logged:</strong> 18 hrs/week</p>", unsafe_allow_html=True)
            st.markdown("<p><strong>Projects Finished:</strong> 3</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# 🔍 EXPLORE SECTION (placeholder)
# ──────────────────────────────────────────────────────────
elif section == "Explore":
    st.markdown("<h1>🔍 Explore Users</h1>", unsafe_allow_html=True)
    st.write("Coming soon: trending profiles, new milestones, and supporter leaderboard.")


# ──────────────────────────────────────────────────────────
# 🔔 NOTIFICATIONS SECTION (placeholder)
# ──────────────────────────────────────────────────────────
elif section == "Notifications":
    st.markdown("<h1>🔔 Notifications</h1>", unsafe_allow_html=True)
    st.write("Coming soon: support credits received, followers, and milestone badges.")
