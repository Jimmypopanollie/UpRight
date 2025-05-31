# UpRightApp.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ──────────────────────────────────────────────────────────
# 1) PAGE CONFIG: Must be the first Streamlit command
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UpRight", 
    page_icon="📈", 
    layout="wide",           # use "wide" now that we have more CSS
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────
# 2) INJECT CUSTOM CSS
#    - cards
#    - avatars 
#    - horizontal scroller
#    - sidebar width
#    - fonts/colors
# ──────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ---------- GLOBAL ---------- */
    body {
        background-color: #F5F7FA;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .css-18gvkmn {
        /* remove default padding Streamlit adds around wide-layout pages */
        padding: 1rem 2rem;
    }
    /* ---------- SIDEBAR WIDTH ---------- */
    [data-testid="stSidebar"] > div:first-child {
        width: 280px;
    }
    /* ---------- CARD STYLING ---------- */
    .card {
        background-color: #FFFFFF;
        border-radius: 8px;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        margin-bottom: 1.5rem;
    }
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .avatar {
        border-radius: 50%;
        width: 48px;
        height: 48px;
        object-fit: cover;
        margin-right: 0.75rem;
    }
    .username {
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0;
    }
    .follower {
        font-size: 0.875rem;
        color: #6B7280;
    }
    .posted-time {
        font-size: 0.875rem;
        color: #9CA3AF;
        margin-left: auto;
    }
    .card-body {
        margin-top: 0.5rem;
    }
    /* ---------- HORIZONTAL SCROLLER FOR MOMENTS ---------- */
    .moment-container {
        display: flex;
        overflow-x: auto;
        gap: 1rem;
        padding-bottom: 0.5rem;
    }
    .moment {
        min-width: 200px;
        height: 120px;
        background-color: #ECEFF4;
        border-radius: 8px;
        flex-shrink: 0;
        background-size: cover;
        background-position: center;
    }
    /* Hide scrollbar visually but allow scroll */
    .moment-container::-webkit-scrollbar {
        height: 6px;
    }
    .moment-container::-webkit-scrollbar-thumb {
        background-color: #CBD5E0;
        border-radius: 3px;
    }
    /* ---------- BUTTON STYLING ---------- */
    .react-buttons > input[type="radio"] + label {
        margin-right: 0.75rem;
        cursor: pointer;
        font-size: 1.25rem;
    }
    /* Streamlit's default radio is hidden; we style via label */
    input[type="radio"] { display: none; }
    input[type="radio"]:checked + label {
        background-color: #E2E8F0;
        border-radius: 4px;
        padding: 0.25rem 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ──────────────────────────────────────────────────────────
# 3) TOAST ON REFRESH (optional)
# ──────────────────────────────────────────────────────────
try:
    st.toast("UpRight App refreshed 🎯", icon="🚀")
except:
    # If running on older Streamlit where st.toast doesn't exist, ignore
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
# 5) DUMMY DATA (for charts)
# ──────────────────────────────────────────────────────────
df = pd.DataFrame({
    "Category": ["Income",    "Assets",   "Education", "Debt"],
    "Value":     [52000,      140000,     12,          3500],
    "Color":     ["green",    "blue",     "gold",      "red"]
})


# ──────────────────────────────────────────────────────────
# 📲 FEED SECTION: Instagram-style feed with cards + avatars
# ──────────────────────────────────────────────────────────
if section == "Feed":
    st.markdown("<h1>📲 UpRight Feed</h1>", unsafe_allow_html=True)

    # Example: a row of “moments” at the top (horizontally scrollable)
    st.markdown("<div class='moment-container'>"
                "<div class='moment' style='background-image: url(https://placehold.co/200x120/ff7f7f/333?text=Moment+1)'></div>"
                "<div class='moment' style='background-image: url(https://placehold.co/200x120/7fbfff/333?text=Moment+2)'></div>"
                "<div class='moment' style='background-image: url(https://placehold.co/200x120/7fff7f/333?text=Moment+3)'></div>"
                "<div class='moment' style='background-image: url(https://placehold.co/200x120/ffff7f/333?text=Moment+4)'></div>"
                "<div class='moment' style='background-image: url(https://placehold.co/200x120/dc7fff/333?text=Moment+5)'></div>"
                "</div>",
                unsafe_allow_html=True)

    # Show 3 dummy posts
    for i in range(3):
        username = f"anon_user_{i+1}"
        avatar_url = "https://placehold.co/48x48"  # replace with real avatar URL if you have
        followers = f"{1000 + i*250} followers"
        posted_on = datetime.now().strftime("%b %d, %Y • %I:%M %p")

        # Wrap each post in a .card
        post_md = f"""
        <div class='card'>
            <div class='card-header'>
                <img src='{avatar_url}' class='avatar' />
                <div>
                    <p class='username'>@{username}</p>
                    <p class='follower'>{followers}</p>
                </div>
                <p class='posted-time'>{posted_on}</p>
            </div>
            <div class='card-body'>
                <!-- Chart inside the post -->
                {{}}
                <p>Income Growth: <span style='color: #16A34A;'>+22.4%</span> • Debt Reduction: <span style='color: #DC2626;'>-8.7%</span></p>
                <div class='react-buttons'>
                    <input type='radio' id='fire_{i}'     name='react_{i}' value='🔥'><label for='fire_{i}'>🔥</label>
                    <input type='radio' id='idea_{i}'     name='react_{i}' value='💡'><label for='idea_{i}'>💡</label>
                    <input type='radio' id='praise_{i}'   name='react_{i}' value='🙌'><label for='praise_{i}'>🙌</label>
                    <input type='radio' id='money_{i}'    name='react_{i}' value='💰'><label for='money_{i}'>💰</label>
                </div>
                <div style='margin-top: 0.75rem;'>
                    <input type='text' placeholder='Leave a comment...' style='width: 100%; padding: 0.5rem; border-radius: 4px; border: 1px solid #CBD5E0;' />
                </div>
            </div>
        </div>
        """
        # Plotly chart for this post
        fig = px.bar(
            df, x="Category", y="Value", 
            color="Category", 
            color_discrete_sequence=df["Color"],
            template="simple_white"
        )
        # Render the chart and capture its HTML with st.plotly_chart → to_html
        # NOTE: st.plotly_chart → we can't directly inject a figure into our HTML string. 
        #       Instead, we render the figure below the markdown card-body placeholder.
        st.markdown(post_md.format(""), unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("")  # small blank line between posts


# ──────────────────────────────────────────────────────────
# 📈 MY CHART SECTION: Coinbase-style dashboard cards + metrics
# ──────────────────────────────────────────────────────────
elif section == "My Chart":
    st.markdown("<h1>📈 UpRight: Your Life as a Chart</h1>", unsafe_allow_html=True)
    st.markdown("<p>Welcome to the UpRight Social Tracker!</p>", unsafe_allow_html=True)

    # Top row of metric-cards
    colA, colB, colC, colD = st.columns([1, 1, 1, 2], gap="large")

    with colA:
        st.markdown(
            """
            <div class='card'>
                <h3 style='margin-bottom: 0.25rem;'>Income Growth</h3>
                <p style='font-size: 2rem; color: #16A34A; margin: 0;'>+22.4%</p>
                <p style='font-size: 0.9rem; color: #10B981;'>▲ 3.5%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with colB:
        st.markdown(
            """
            <div class='card'>
                <h3 style='margin-bottom: 0.25rem;'>Debt Reduction</h3>
                <p style='font-size: 2rem; color: #DC2626; margin: 0;'>-8.7%</p>
                <p style='font-size: 0.9rem; color: #F87171;'>▼ 1.1%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with colC:
        st.markdown(
            """
            <div class='card' style='text-align: center;'>
                <h3 style='margin-bottom: 0.5rem;'>Select Chart Type</h3>
                {}
            </div>
            """.format(
                st.radio(
                    "", ["Bar", "Line"], 
                    horizontal=True, key="chart_type_selector"
                )
            ),
            unsafe_allow_html=True
        )

    with colD:
        st.markdown(
            """
            <div class='card' style='text-align: center;'>
                <h3 style='margin-bottom: 0.5rem;'>Time Range</h3>
                {}
            </div>
            """.format(
                st.selectbox(
                    "", ["1W", "1M", "1Y", "All"], key="time_range_selector"
                )
            ),
            unsafe_allow_html=True
        )

    # Rebuild the figure based on radio selection
    chart_choice = st.session_state.get("chart_type_selector", "Bar")
    if chart_choice == "Bar":
        fig2 = px.bar(
            df, x="Category", y="Value", 
            color="Category", 
            color_discrete_sequence=df["Color"],
            template="seaborn"
        )
    else:
        fig2 = px.line(
            df, x="Category", y="Value", 
            template="seaborn"
        )

    st.plotly_chart(fig2, use_container_width=True)

    # Abstract Metrics Section in two columns
    st.markdown("<h3>📚 Abstract Metrics</h3>", unsafe_allow_html=True)
    am_col1, am_col2 = st.columns(2, gap="large")
    with am_col1:
        st.markdown("""
            <div class='card'>
                <p><strong>Books Read:</strong> 28</p>
                <p><strong>Courses Completed:</strong> 5</p>
            </div>
        """, unsafe_allow_html=True)
    with am_col2:
        st.markdown("""
            <div class='card'>
                <p><strong>Family Time Logged:</strong> 18 hrs/week</p>
                <p><strong>Projects Finished:</strong> 3</p>
            </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# 🔍 EXPLORE SECTION (placeholder for future)
# ──────────────────────────────────────────────────────────
elif section == "Explore":
    st.markdown("<h1>🔍 Explore Users</h1>", unsafe_allow_html=True)
    st.markdown("<p>Coming soon: trending profiles, new milestones, and supporter leaderboard.</p>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# 🔔 NOTIFICATIONS SECTION (placeholder for future)
# ──────────────────────────────────────────────────────────
elif section == "Notifications":
    st.markdown("<h1>🔔 Notifications</h1>", unsafe_allow_html=True)
    st.markdown("<p>Coming soon: support credits received, followers, and milestone badges.</p>", unsafe_allow_html=True)
