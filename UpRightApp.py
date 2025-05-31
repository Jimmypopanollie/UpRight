# ─────────────────────────────────────────────────────────────────────────────
# UpRightApp.py
#
# A refined, complete Streamlit app that mimics a Coinbase-like “Feed” page,
# plus your existing “My Chart,” “Explore,” and “Notifications” sections.
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# 0) PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UpRight", 
    page_icon="📈", 
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# 1) CSS & BASIC STYLES
# ─────────────────────────────────────────────────────────────────────────────
# We inject a style block at the top so all classes below take effect.
# Feel free to tweak colors, paddings, and fonts to your preference.
st.markdown(
    """
    <style>
    /* ───── Hide default Streamlit menu/border on top ───── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ───── Sidebar Heading ───── */
    .sidebar .sidebar-content {
      padding-top: 1.5rem;
    }
    .sidebar .sidebar-content h1 {
      font-size: 1.6rem;
      font-weight: 700;
      margin-bottom: 1rem;
    }

    /* ───── Moments Bar Container ───── */
    .moments-bar {
      display: flex;
      flex-wrap: nowrap;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
      overflow-x: auto;
      padding-bottom: 0.5rem;
    }
    .moments-bar::-webkit-scrollbar {
      height: 6px;
    }
    .moments-bar::-webkit-scrollbar-thumb {
      background: #CBD5E0;
      border-radius: 3px;
    }

    /* ───── Each “Moment” Box ───── */
    .moment {
      flex: 0 0 auto;
      padding: 1rem 1.25rem;
      border-radius: 0.5rem;
      font-weight: 600;
      font-size: 1rem;
      color: #111827;
      cursor: pointer;
      transition: opacity 0.2s ease;
      min-width: 120px;
      text-align: center;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .moment:hover {
      opacity: 0.85;
    }

    /* ───── Feed “Card” ───── */
    .card {
      background-color: #FFFFFF;
      border: 1px solid #E5E7EB;
      border-radius: 0.75rem;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.25rem;
      box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* ───── Avatar Circle ───── */
    .avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      object-fit: cover;
      border: 2px solid #E5E7EB;
    }

    /* ───── Reaction Buttons (native Streamlit buttons) ───── */
    /* We’ll simply style the <button> that Streamlit renders. */
    button.stButton {
      margin: 0;
      padding: 0.5rem;
      font-size: 1.125rem;
      border-radius: 0.375rem;
      border: 1px solid transparent;
      background-color: #F3F4F6;
      transition: background-color 0.15s ease;
    }
    button.stButton:hover {
      background-color: #E5E7EB;
    }

    /* ───── Comment Input (pure HTML <input>) ───── */
    .comment-input {
      width: 100%;
      padding: 0.5rem 0.75rem;
      margin-top: 0.75rem;
      border: 1px solid #CBD5E0;
      border-radius: 0.375rem;
      font-size: 0.95rem;
      color: #374151;
    }
    .comment-input:focus {
      outline: none;
      border-color: #3B82F6;
      box-shadow: 0 0 0 3px rgba(59,130,246,0.2);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 2) CONSTANTS & DUMMY DATA
# ─────────────────────────────────────────────────────────────────────────────

# (A) Accent colors for “growth” text:
ACCENT_GREEN = "#16A34A"  # green‐600
ACCENT_RED   = "#DC2626"  # red‐600

# (B) The DataFrame underlying every bar chart in the Feed:
df_main = pd.DataFrame({
    "Category": ["Income", "Assets", "Education", "Debt"],
    "Value":    [52000, 140000, 12, 3500],
    "Color":    ["green", "blue", "yellow", "red"],
})

# (C) A list of “moments” to show in the top bar of the Feed.
#     In a real app, you might fetch these from a database or API.
moments = [
    {"label": "Moment 1", "color": "#FCA5A5"},  # red‐300
    {"label": "Moment 2", "color": "#93C5FD"},  # blue‐300
    {"label": "Moment 3", "color": "#86EFAC"},  # green‐300
    {"label": "Moment 4", "color": "#FEF9C3"},  # yellow‐300
    {"label": "Moment 5", "color": "#E9D5FF"},  # purple‐300
]

# (D) Dummy “feed” posts. Each entry becomes one “card” in the Feed.
#     The “chart_key” must be unique for each Plotly chart to avoid duplicate IDs.
dummy_posts = [
    {
        "avatar_url":  "https://placehold.co/48x48", 
        "username":    "anon_user_1",
        "followers":   "1,000 followers",
        "posted_on":   "May 31, 2025 • 06:45 PM",
        "income_pct":  "+22.4%",
        "income_delta":"+3.5%",
        "debt_pct":    "-8.7%",
        "debt_delta":  "-1.1%",
        "chart_key":   "chart_0",
    },
    {
        "avatar_url":  "https://placehold.co/48x48", 
        "username":    "anon_user_2",
        "followers":   "1,250 followers",
        "posted_on":   "May 31, 2025 • 07:15 PM",
        "income_pct":  "+18.9%",
        "income_delta":"+2.8%",
        "debt_pct":    "-5.3%",
        "debt_delta":  "-0.5%",
        "chart_key":   "chart_1",
    },
    {
        "avatar_url":  "https://placehold.co/48x48", 
        "username":    "anon_user_3",
        "followers":   "980 followers",
        "posted_on":   "May 31, 2025 • 07:42 PM",
        "income_pct":  "+10.2%",
        "income_delta":"+1.1%",
        "debt_pct":    "-2.0%",
        "debt_delta":  "-0.2%",
        "chart_key":   "chart_2",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 3) SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.markdown("<h1>👋 Welcome to<br>UpRight</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<small style='color:#6B7280;'>Go to</small>", unsafe_allow_html=True)
section = st.sidebar.radio(
    label="",
    options=["Feed", "My Chart", "Explore", "Notifications"],
    index=0,
    label_visibility="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# 4) FEED SECTION (WITH “MOMENTS” BAR + CARDS)
# ─────────────────────────────────────────────────────────────────────────────
if section == "Feed":
    # Title
    st.markdown("<h1>📱 UpRight Feed</h1>", unsafe_allow_html=True)

    # -- 4a) Pure‐HTML Moments Bar (no st.button) --
    if "selected_moment" not in st.session_state:
        st.session_state.selected_moment = None

    # Build HTML for each moment box. When clicked, it issues a postMessage with {type:"CUSTOM_EVENT", midx: <idx>}.
    moments_html = ""
    for idx, moment in enumerate(moments):
        label = moment["label"]
        bgcol = moment["color"]
        moments_html += f"""
            <div
              class="moment"
              style="background-color: {bgcol};"
              onclick="window.parent.postMessage(
                {{ 'type': 'CUSTOM_EVENT', 'midx': {idx} }}, '*'
              );"
            >
              {label}
            </div>
        """

    # Wrap them in a horizontal flex container
    st.markdown(f'<div class="moments-bar">{moments_html}</div>', unsafe_allow_html=True)

    # Register a dummy query params call so Streamlit’s front-end will catch our postMessage
    _ = st.experimental_get_query_params()
    # If the front-end just posted a CUSTOM_EVENT with midx, Streamlit sees it here:
    qp = st.experimental_get_query_params()
    if qp and "midx" in qp:
        try:
            sel_idx = int(qp["midx"][0])
            st.session_state.selected_moment = sel_idx
        except:
            pass

    # Optional: show which moment is selected
    if st.session_state.selected_moment is not None:
        sel = st.session_state.selected_moment
        sel_label = moments[sel]["label"]
        st.markdown(
            f"<p style='font-size:0.9rem; color:#6B7280;'>"
            f"Showing posts for <strong>{sel_label}</strong>.</p>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -- 4b) Render each dummy post as a “card” --
    for i, post in enumerate(dummy_posts):
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            # Header: Avatar + username/followers + timestamp
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

            # Divider
            st.markdown("<hr style='border-color:#E5E7EB;'>", unsafe_allow_html=True)

            # In-Post Bar Chart (unique key per post)
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
            st.plotly_chart(fig_feed, use_container_width=True, key=post["chart_key"])

            # Growth Stats
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; margin-top:12px;">
                  <div>
                    <span style="font-size:1rem; color:{ACCENT_GREEN}; font-weight:600;">Income Growth: {post['income_pct']}</span>
                    <span style="font-size:0.9rem; color:{ACCENT_GREEN};"> ▲ {post['income_delta']}</span>
                  </div>
                  <div>
                    <span style="font-size:1rem; color:{ACCENT_RED}; font-weight:600;">Debt Reduction: {post['debt_pct']}</span>
                    <span style="font-size:0.9rem; color:{ACCENT_RED};"> ▼ {post['debt_delta']}</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Reaction Buttons (each as a native Streamlit button with a unique key)
            rcol1, rcol2, rcol3, rcol4 = st.columns([1, 1, 1, 1], gap="small")
            with rcol1:
                if st.button("🔥", key=f"react_fire_{i}"):
                    pass
            with rcol2:
                if st.button("💡", key=f"react_idea_{i}"):
                    pass
            with rcol3:
                if st.button("🙌", key=f"react_praise_{i}"):
                    pass
            with rcol4:
                if st.button("💰", key=f"react_money_{i}"):
                    pass

            # Comment Input (pure HTML <input>, identified by id="comment_i")
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

            # Close the card
            st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 5) “My Chart” (Dashboard) SECTION
# ─────────────────────────────────────────────────────────────────────────────
elif section == "My Chart":
    st.markdown("<h1>📈 UpRight: Your Life as a Chart</h1>", unsafe_allow_html=True)
    st.write("Welcome to the UpRight Social Tracker!")

    # Chart type & time-range selectors
    chart_type = st.radio("Select chart type", ["Bar", "Line"], horizontal=True)
    time_range = st.selectbox("Time Range", ["1W", "1M", "1Y", "All"])

    col1, col2 = st.columns(2)
    col1.metric("Income Growth", "+22.4%", "+3.5%")
    col2.metric("Debt Reduction", "-8.7%", "-1.1%")

    # Show either a Bar or Line chart
    if chart_type == "Bar":
        fig2 = px.bar(
            df_main, 
            x="Category", 
            y="Value", 
            color="Category", 
            color_discrete_sequence=df_main["Color"],
        )
    else:
        fig2 = px.line(df_main, x="Category", y="Value")

    st.plotly_chart(fig2, use_container_width=True)

    # Abstract Metrics
    st.subheader("📚 Abstract Metrics")
    st.markdown("""
    - Books Read: 28  
    - Courses Completed: 5  
    - Family Time Logged: 18 hrs/week  
    - Projects Finished: 3  
    """)


# ─────────────────────────────────────────────────────────────────────────────
# 6) EXPLORE SECTION
# ─────────────────────────────────────────────────────────────────────────────
elif section == "Explore":
    st.markdown("<h1>🔍 Explore Users</h1>", unsafe_allow_html=True)
    st.markdown("Coming soon: trending profiles, new milestones, and supporter leaderboard.")


# ─────────────────────────────────────────────────────────────────────────────
# 7) NOTIFICATIONS SECTION
# ─────────────────────────────────────────────────────────────────────────────
elif section == "Notifications":
    st.markdown("<h1>🔔 Notifications</h1>", unsafe_allow_html=True)
    st.markdown("Coming soon: support credits received, followers, and milestone badges.")
