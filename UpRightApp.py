# ─────────────────────────────────────────────────────────────────────────────
# UpRightApp.py — Coinbase-style UI + No Duplicate IDs
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────
# 1) PAGE CONFIGURATION: MUST be the FIRST Streamlit call
# ─────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UpRight",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────
# 2) GLOBAL CSS (Coinbase-ish) for “cards” and general layout
# ─────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* 2a) Background & default font */
    body {
        background-color: #F5F7FA;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 2b) Sidebar header styling */
    [data-testid="stSidebar"] .sidebar-content {
        background-color: #FFFFFF;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 1rem;
    }

    /* 2c) “Card” containers: white background, rounded corners, subtle shadow */
    .card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 24px;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.08);
    }

    /* 2d) Avatar style */
    .avatar {
        border-radius: 50%;
        width: 48px;
        height: 48px;
        object-fit: cover;
    }

    /* 2e) “Moments” bar at top: horizontal colored boxes */
    .moments-bar {
        display: flex;
        gap: 12px;
        overflow-x: auto;
        padding-bottom: 8px;
        margin-bottom: 24px;
    }
    .moment {
        flex-shrink: 0;
        min-width: 120px;
        height: 60px;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .moment:hover {
        opacity: 0.85;
    }

    /* 2f) Hide default scrollbar track, style thumb */
    .moments-bar::-webkit-scrollbar {
        height: 6px;
    }
    .moments-bar::-webkit-scrollbar-thumb {
        background-color: #CBD5E0;
        border-radius: 3px;
    }

    /* 2g) Reaction buttons styling */
    .reaction-container {
        display: flex;
        gap: 12px;
        margin-top: 8px;
    }
    .stButton>button {
        background-color: #E5F3FF;
        color: #0B69FF;
        border: none;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #D0EAFF;
    }

    /* 2h) Comment box styling override */
    input[type="text"].comment-input {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid #CBD5E0;
        border-radius: 6px;
        font-size: 0.95rem;
        margin-top: 8px;
    }
    input[type="text"].comment-input:focus {
        outline: none;
        border-color: #0B69FF;
        box-shadow: 0 0 0 2px rgba(11, 105, 255, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────
# 3) OPTIONAL: Toast when app loads (newer Streamlit only)
# ─────────────────────────────────────────────────────────────────────────
try:
    st.toast("UpRight has loaded 🚀", icon="🎉")
except:
    pass

# ─────────────────────────────────────────────────────────────────────────
# 4) SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────────────────
st.sidebar.markdown("# 👋 Welcome to UpRight")
section = st.sidebar.radio(
    "Go to",
    ["Feed", "My Chart", "Explore", "Notifications"],
    index=0,
)

# ─────────────────────────────────────────────────────────────────────────
# 5) DUMMY DATA (replace with real data later)
# ─────────────────────────────────────────────────────────────────────────
# Accent colors
ACCENT_GREEN  = "#16A34A"
ACCENT_RED    = "#DC2626"
ACCENT_BLUE   = "#0B69FF"
ACCENT_YELLOW = "#F59E0B"

# Main categories for bar chart
df_main = pd.DataFrame({
    "Category": ["Income",     "Assets",    "Education", "Debt"],
    "Value":     [55000,       140000,      12,          3500],
    "Color":     [ACCENT_GREEN, ACCENT_BLUE, ACCENT_YELLOW, ACCENT_RED],
})

# Sparkline history (six months)
months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
income_history  = [45000, 47000, 49500, 51000, 52800, 55000]
debt_history    = [5000, 4800, 4600, 4200, 3800, 3500]
spark_income_df = pd.DataFrame({"Month": months, "Income": income_history})
spark_debt_df   = pd.DataFrame({"Month": months, "Debt": debt_history})

# Dummy “Moments” (these would be replaced by real curated images/content)
moments = [
    {"label": "Moment 1", "color": "#EF4444"},
    {"label": "Moment 2", "color": "#3B82F6"},
    {"label": "Moment 3", "color": "#10B981"},
    {"label": "Moment 4", "color": "#F59E0B"},
    {"label": "Moment 5", "color": "#8B5CF6"},
]

# Dummy feed posts (replace with real database/API later)
dummy_posts = [
    {
        "username":   "anon_user_1",
        "followers":  "1 000 followers",
        "avatar_url": "https://placehold.co/48x48",
        "posted_on":  "May 31, 2025 • 06:45 PM",
        "income_pct": "+22.4%",   "income_delta": "+3.5%",
        "debt_pct":   "-8.7%",    "debt_delta": "-1.1%",
        "chart_key":  "post_chart_0",
    },
    {
        "username":   "anon_user_2",
        "followers":  "1 250 followers",
        "avatar_url": "https://placehold.co/48x48",
        "posted_on":  "May 31, 2025 • 06:50 PM",
        "income_pct": "+19.8%",   "income_delta": "+2.9%",
        "debt_pct":   "-10.2%",   "debt_delta": "-1.4%",
        "chart_key":  "post_chart_1",
    },
    {
        "username":   "anon_user_3",
        "followers":  "980 followers",
        "avatar_url": "https://placehold.co/48x48",
        "posted_on":  "May 31, 2025 • 06:55 PM",
        "income_pct": "+25.0%",   "income_delta": "+4.0%",
        "debt_pct":   "-7.3%",    "debt_delta": "-0.9%",
        "chart_key":  "post_chart_2",
    },
]

# ─────────────────────────────────────────────────────────────────────────
# 6) FEED SECTION
# ─────────────────────────────────────────────────────────────────────────
if section == "Feed":
    st.markdown("<h1>📱 UpRight Feed</h1>", unsafe_allow_html=True)

    # 6a) Moments Bar (horizontal scroll)
    st.markdown(
        '<div class="moments-bar">',
        unsafe_allow_html=True,
    )
    cols_m = st.columns(len(moments), gap="small")
    for idx, moment in enumerate(moments):
        label = moment["label"]
        color = moment["color"]
        with cols_m[idx]:
            if st.button(
                label,
                key=f"moment_btn_{idx}",
                help=f"View {label}",
                args=None,
                kwargs=None,
                # Inline CSS to color the background and white text
                unsafe_allow_html=True,
                # We embed the CSS style in the button label
                label_visibility="collapsed",
            ):
                # For now, this button does nothing except re-render the feed.
                # In a real app, you would set some filter in session_state.
                st.session_state["selected_moment"] = idx

        # Overwrite the default idx-button with our own styled HTML
        # (We cannot directly inject CSS into a st.button, so we fallback to Markdown)
        st.markdown(
            f"""
            <div style="
                background-color: {color};
                border-radius: 8px;
                height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
                font-weight: 600;
                color: #FFFFFF;
                cursor: pointer;
                " 
                onclick="document.querySelector('#moment_btn_{idx}').click();"
            >
                {label}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)  # close moments-bar

    # 6b) Render each post as a “card”
    for i, post in enumerate(dummy_posts):
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            # Header: avatar + username/followers + timestamp
            hcol1, hcol2, hcol3 = st.columns([1, 5, 3], gap="small")
            with hcol1:
                st.markdown(
                    f'<img src="{post["avatar_url"]}" class="avatar">',
                    unsafe_allow_html=True,
                )
            with hcol2:
                st.markdown(
                    f"""
                    <div style="display:flex; flex-direction:column; gap:4px;">
                      <span style="font-weight:600;">@{post["username"]}</span>
                      <span style="font-size:0.9rem; color:#6B7280;">{post["followers"]}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with hcol3:
                st.markdown(
                    f"<span style='font-size:0.9rem; color:#9CA3AF;'>{post['posted_on']}</span>",
                    unsafe_allow_html=True,
                )

            st.markdown("<hr style='border-color:#E5E7EB;'>", unsafe_allow_html=True)

            # In-post bar chart
            fig_feed = px.bar(
                df_main,
                x="Category",
                y="Value",
                color="Category",
                color_discrete_sequence=df_main["Color"],
                template="none",
            )
            fig_feed.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=180,
                xaxis=dict(showgrid=False, tickfont=dict(size=11)),
                yaxis=dict(showgrid=False, tickfont=dict(size=11)),
            )
            st.plotly_chart(
                fig_feed,
                use_container_width=True,
                key=post["chart_key"],  # unique key to avoid duplicate-ID errors
            )

            # Growth Stats line
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; margin-top:12px;">
                  <div>
                    <span style="font-size:1rem; color:{ACCENT_GREEN}; font-weight:600;">Income Growth: {post['income_pct']}</span>
                    <span style="font-size:0.9rem; color:{ACCENT_GREEN};"> ▲ {post['income_delta']}</span>
                  </div>
                  <div>
                    <span style="font-size:1rem; color:{ACCENT_RED}; font-weight:600;">Debt Reduct.: {post['debt_pct']}</span>
                    <span style="font-size:0.9rem; color:{ACCENT_RED};"> ▼ {post['debt_delta']}</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Reaction buttons (native Streamlit buttons styled via CSS above)
            rcol1, rcol2, rcol3, rcol4 = st.columns([1, 1, 1, 1], gap="small")
            with rcol1:
                if st.button("🔥", key=f"react_fire_{i}"):
                    pass  # In a real app, record that reaction somewhere
            with rcol2:
                if st.button("💡", key=f"react_idea_{i}"):
                    pass
            with rcol3:
                if st.button("🙌", key=f"react_praise_{i}"):
                    pass
            with rcol4:
                if st.button("💰", key=f"react_money_{i}"):
                    pass

            # Comment input (native input, styled via CSS)
            st.markdown(
                f"""
                <input 
                    type="text" 
                    placeholder="Leave a comment..." 
                    class="comment-input" 
                    id="comment_{i}"
                >
                """,
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)  # close card

# ─────────────────────────────────────────────────────────────────────────
# 7) “MY CHART” DASHBOARD SECTION
# ─────────────────────────────────────────────────────────────────────────
elif section == "My Chart":
    st.markdown("<h1>📈 UpRight: Your Life as a Chart</h1>", unsafe_allow_html=True)
    st.markdown("<p>Welcome to the UpRight Social Tracker!</p>", unsafe_allow_html=True)

    # 7a) Top‐row Cards: Income Growth & Debt Reduction (with Sparklines)
    colA, colB, colC, colD = st.columns([1, 1, 1, 2], gap="large")

    # Income Growth Card
    with colA:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>Income Growth</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:2rem; color:{ACCENT_GREEN}; margin:0;'>+22.4%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:0.9rem; color:{ACCENT_GREEN}; margin:0;'>▲ 3.5%</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Sparkline below
        spark_inc = px.line(
            spark_income_df,
            x="Month",
            y="Income",
            line_shape="spline",
            template="none",
            markers=False,
        )
        spark_inc.update_traces(line=dict(color=ACCENT_GREEN, width=2))
        spark_inc.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(showgrid=False, visible=False),
            height=90,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(spark_inc, use_container_width=True, key="spark_inc_chart")

    # Debt Reduction Card
    with colB:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>Debt Reduction</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:2rem; color:{ACCENT_RED}; margin:0;'>-8.7%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:0.9rem; color:{ACCENT_RED}; margin:0;'>▼ 1.1%</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Sparkline below
        spark_debt = px.line(
            spark_debt_df,
            x="Month",
            y="Debt",
            line_shape="spline",
            template="none",
            markers=False,
        )
        spark_debt.update_traces(line=dict(color=ACCENT_RED, width=2))
        spark_debt.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(showgrid=False, visible=False),
            height=90,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(spark_debt, use_container_width=True, key="spark_debt_chart")

    # Chart Type Selector Card
    with colC:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>Select Chart Type</h3>", unsafe_allow_html=True)
        chart_type = st.radio(
            "",
            ["Bar", "Line"],
            horizontal=True,
            key="mt_chart_type",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Time Range Selector Card
    with colD:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>Time Range</h3>", unsafe_allow_html=True)
        time_range = st.selectbox(
            "",
            ["1W", "1M", "1Y", "All"],
            index=3,
            key="mt_time_range",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # 7b) Main Chart Below
    if st.session_state.mt_chart_type == "Bar":
        fig_main = px.bar(
            df_main,
            x="Category",
            y="Value",
            color="Category",
            color_discrete_sequence=df_main["Color"],
            template="seaborn",
        )
    else:
        fig_main = px.line(
            df_main,
            x="Category",
            y="Value",
            template="seaborn",
        )
    st.plotly_chart(fig_main, use_container_width=True, key="main_mt_chart")

    # 7c) Abstract Metrics at Bottom (two cards side by side)
    st.markdown("<h3>📚 Abstract Metrics</h3>", unsafe_allow_html=True)
    am_col1, am_col2 = st.columns(2, gap="large")

    with am_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<p><strong>Books Read:</strong> 28</p>", unsafe_allow_html=True)
        st.markdown("<p><strong>Courses Completed:</strong> 5</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with am_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<p><strong>Family Time Logged:</strong> 18 hrs/week</p>", unsafe_allow_html=True)
        st.markdown("<p><strong>Projects Finished:</strong> 3</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
# 8) EXPLORE SECTION (Placeholder)
# ─────────────────────────────────────────────────────────────────────────
elif section == "Explore":
    st.markdown("<h1>🔍 Explore Users</h1>", unsafe_allow_html=True)
    st.write("Coming soon: trending profiles, new milestones, supporter leaderboard.")

# ─────────────────────────────────────────────────────────────────────────
# 9) NOTIFICATIONS SECTION (Placeholder)
# ─────────────────────────────────────────────────────────────────────────
elif section == "Notifications":
    st.markdown("<h1>🔔 Notifications</h1>", unsafe_allow_html=True)
    st.write("Coming soon: support credits, new followers, milestone badges.")
