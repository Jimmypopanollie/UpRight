import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION (must be first Streamlit command)
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UpRight",
    page_icon="🤖",
    layout="wide",
)

# ──────────────────────────────────────────────────────────────────────────────
# THEME CSS INJECTION: Primary colors (red, blue, yellow) + accent green
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ---------- Typography & Background ---------- */
    body {
        background-color: #F9FAFB;
        color: #1F2937;
        font-family: "Segoe UI", sans-serif;
    }
    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    /* ---------- Buttons ---------- */
    .stButton>button {
        background-color: #3B82F6;  /* Blue primary */
        color: white;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        color: #FFFFFF;
    }
    /* ---------- Input fields ---------- */
    input[type="text"], input[type="number"], textarea {
        border: 1px solid #D1D5DB !important;
        border-radius: 4px !important;
        padding: 0.5rem !important;
    }
    /* ---------- Metrics ---------- */
    .stMetricValue {
        color: #10B981;  /* Accent green for positive by default */
        font-size: 2rem;
        font-weight: 700;
    }
    /* ---------- Section Headers ---------- */
    h1, h2, h3, h4, h5 {
        color: #111827;
    }
    /* ---------- Profile Picture ---------- */
    .profile-avatar {
        border-radius: 50%;
        border: 2px solid #10B981;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ──────────────────────────────────────────────────────────────────────────────
if "profile_created" not in st.session_state:
    st.session_state.profile_created = False

if "profile" not in st.session_state:
    st.session_state.profile = {
        "username": "",
        "full_name": "",
        "photo_url": None,  # will store URL or None
    }

if "indicators" not in st.session_state:
    # store main indicators and abstract metrics
    st.session_state.indicators = {
        "income": 0.0,
        "assets": 0.0,
        "debt": 0.0,
        "net_worth": 0.0,
        "accolades": "",
        "books_read": 0,
        "courses_completed": 0,
        "family_time": 0.0,  # hours/week
        "projects_finished": 0,
    }

# ──────────────────────────────────────────────────────────────────────────────
# DEFAULT ROBOT AVATAR (iStock‐style)
# ──────────────────────────────────────────────────────────────────────────────
DEFAULT_AVATAR_URL = "https://placehold.co/100x100?text=🤖&bg=10B981&fg=FFFFFF"

# ──────────────────────────────────────────────────────────────────────────────
# PROFILE CREATION FORM
# ──────────────────────────────────────────────────────────────────────────────
def show_profile_creation():
    st.title("Welcome to UpRight")
    st.write("Let's create your profile to get started!")
    st.markdown("---")

    with st.form(key="profile_form"):
        col1, col2 = st.columns((1, 2), gap="large")
        with col1:
            st.markdown("**Upload a Profile Photo**")
            photo_uploader = st.file_uploader(
                "Choose an image (JPG/PNG)", type=["jpg", "png"], accept_multiple_files=False
            )
            if photo_uploader is not None:
                # Display the uploaded image
                photo_bytes = photo_uploader.read()
                st.image(photo_bytes, caption="Your Uploaded Photo", width=100, use_column_width=False)
                # We'll temporarily store this photo in session_state as bytes
                st.session_state.profile["photo_url"] = photo_bytes
        with col2:
            st.text_input(
                "Username",
                key="profile_username",
                placeholder="e.g., john_doe",
            )
            st.text_input(
                "Full Name",
                key="profile_full_name",
                placeholder="e.g., John Doe",
            )
            st.text_area(
                "Short Bio / Accolades",
                key="profile_accolades",
                help="Share a few lines about yourself or your accolades",
                placeholder="I’m a finance enthusiast, avid reader, and life‐long learner..."
            )
        submitted = st.form_submit_button(label="Create Profile", type="primary")
        if submitted:
            # Validate inputs
            if st.session_state.profile_username.strip() == "" or st.session_state.profile_full_name.strip() == "":
                st.error("Username and Full Name cannot be empty.")
            else:
                # Save profile information
                st.session_state.profile["username"] = st.session_state.profile_username.strip()
                st.session_state.profile["full_name"] = st.session_state.profile_full_name.strip()
                # If user didn't upload a photo, use default
                if st.session_state.profile.get("photo_url") is None:
                    st.session_state.profile["photo_url"] = DEFAULT_AVATAR_URL
                # Save accolades
                st.session_state.indicators["accolades"] = st.session_state.profile_accolades
                st.session_state.profile_created = True
                st.success("Profile created successfully! Welcome aboard 🎉")
                st.experimental_rerun()


# ──────────────────────────────────────────────────────────────────────────────
# PROFILE EDIT FORM
# ──────────────────────────────────────────────────────────────────────────────
def show_profile_edit():
    st.title("Edit Your Profile")
    st.markdown("---")

    with st.form(key="edit_profile_form"):
        col1, col2 = st.columns((1, 2), gap="large")
        with col1:
            st.markdown("**Change Profile Photo**")
            photo_uploader = st.file_uploader(
                "Upload a new image (JPG/PNG)", type=["jpg", "png"], accept_multiple_files=False
            )
            if photo_uploader is not None:
                photo_bytes = photo_uploader.read()
                st.image(photo_bytes, caption="Preview", width=100, use_column_width=False)
        with col2:
            new_username = st.text_input(
                "Username",
                value=st.session_state.profile["username"],
                placeholder="e.g., john_doe",
                key="edit_username",
            )
            new_full_name = st.text_input(
                "Full Name",
                value=st.session_state.profile["full_name"],
                placeholder="e.g., John Doe",
                key="edit_full_name",
            )
            new_accolades = st.text_area(
                "Short Bio / Accolades",
                value=st.session_state.indicators["accolades"],
                help="Share a few lines about yourself or your accolades",
                key="edit_accolades",
            )
        submitted = st.form_submit_button(label="Save Changes", type="primary")
        if submitted:
            if new_username.strip() == "" or new_full_name.strip() == "":
                st.error("Username and Full Name cannot be empty.")
            else:
                st.session_state.profile["username"] = new_username.strip()
                st.session_state.profile["full_name"] = new_full_name.strip()
                st.session_state.indicators["accolades"] = new_accolades.strip()
                if photo_uploader is not None:
                    st.session_state.profile["photo_url"] = photo_bytes
                st.success("Profile updated successfully!")
                st.experimental_rerun()


# ──────────────────────────────────────────────────────────────────────────────
# NAVIGATION: Build sidebar with profile summary + section selection
# ──────────────────────────────────────────────────────────────────────────────
def show_sidebar_nav():
    profile = st.session_state.profile
    avatar = profile["photo_url"]
    if isinstance(avatar, (bytes, bytearray)):
        st.sidebar.image(avatar, width=80, use_column_width=False, caption=None, output_format="PNG", className="profile-avatar")
    else:
        # If avatar is a URL
        st.sidebar.image(avatar, width=80, use_column_width=False, caption=None, className="profile-avatar")

    st.sidebar.markdown(f"**{profile['full_name']}**")
    st.sidebar.markdown(f"@{profile['username']}")
    st.sidebar.markdown("---")

    choice = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Edit Profile", "Feed", "Explore", "Notifications"],
        index=0,
    )
    return choice


# ──────────────────────────────────────────────────────────────────────────────
# DASHBOARD (“My Chart”) SECTION
# ──────────────────────────────────────────────────────────────────────────────
def show_dashboard():
    st.title("📊 Dashboard")
    st.markdown("---")
    st.write("Update your main indicators below, then view your life as a chart.")

    with st.form(key="indicators_form"):
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            income_val = st.number_input(
                "📈 Income",
                min_value=0.0,
                format="%.2f",
                value=st.session_state.indicators["income"],
                key="income_input",
            )
            assets_val = st.number_input(
                "💼 Assets",
                min_value=0.0,
                format="%.2f",
                value=st.session_state.indicators["assets"],
                key="assets_input",
            )
            debt_val = st.number_input(
                "💳 Debt",
                min_value=0.0,
                format="%.2f",
                value=st.session_state.indicators["debt"],
                key="debt_input",
            )
        with col2:
            net_worth_val = st.number_input(
                "🪙 Net Worth",
                min_value=0.0,
                format="%.2f",
                value=st.session_state.indicators["net_worth"],
                key="networth_input",
            )
            books_read_val = st.number_input(
                "📚 Books Read",
                min_value=0,
                value=st.session_state.indicators["books_read"],
                step=1,
                key="books_input",
            )
            courses_val = st.number_input(
                "🎓 Courses Completed",
                min_value=0,
                value=st.session_state.indicators["courses_completed"],
                step=1,
                key="courses_input",
            )
        with col3:
            family_time_val = st.number_input(
                "👪 Family Time (hrs/week)",
                min_value=0.0,
                format="%.1f",
                value=st.session_state.indicators["family_time"],
                key="family_input",
            )
            projects_val = st.number_input(
                "🚀 Projects Finished",
                min_value=0,
                value=st.session_state.indicators["projects_finished"],
                step=1,
                key="projects_input",
            )
            accolades_val = st.text_area(
                "🏆 Accolades / Short Bio",
                value=st.session_state.indicators["accolades"],
                key="accolades_input",
                help="Share new accomplishments or notes",
            )

        submitted = st.form_submit_button(label="Save Indicators", type="primary")
        if submitted:
            # Update session state with new values
            st.session_state.indicators["income"] = income_val
            st.session_state.indicators["assets"] = assets_val
            st.session_state.indicators["debt"] = debt_val
            st.session_state.indicators["net_worth"] = net_worth_val
            st.session_state.indicators["books_read"] = books_read_val
            st.session_state.indicators["courses_completed"] = courses_val
            st.session_state.indicators["family_time"] = family_time_val
            st.session_state.indicators["projects_finished"] = projects_val
            st.session_state.indicators["accolades"] = accolades_val
            st.success("Indicators saved!")
            st.experimental_rerun()

    st.markdown("---")
    st.subheader("📈 Your Life as a Chart")

    # Build a DataFrame from session_state.indicators
    data = {
        "Category": ["Income", "Assets", "Debt", "Net Worth", "Books Read", "Courses", "Family Time", "Projects"],
        "Value": [
            st.session_state.indicators["income"],
            st.session_state.indicators["assets"],
            st.session_state.indicators["debt"],
            st.session_state.indicators["net_worth"],
            st.session_state.indicators["books_read"],
            st.session_state.indicators["courses_completed"],
            st.session_state.indicators["family_time"],
            st.session_state.indicators["projects_finished"],
        ],
    }
    chart_df = pd.DataFrame(data)

    # Default to Line chart (index=1)
    chart_type = st.radio(
        "Select chart style:",
        ["Bar", "Line"],
        index=1,
        horizontal=True,
        key="dashboard_chart_type",
    )

    if chart_type == "Bar":
        fig = px.bar(
            chart_df,
            x="Category",
            y="Value",
            color="Category",
            color_discrete_sequence=["#EF4444", "#3B82F6", "#FACC15", "#10B981", "#3B82F6", "#EF4444", "#10B981", "#FACC15"],
            height=450,
        )
    else:
        fig = px.line(
            chart_df,
            x="Category",
            y="Value",
            markers=True,
            color_discrete_sequence=["#10B981"],
            height=450,
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=20),
        xaxis_title=None,
        yaxis_title="Value",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#F9FAFB",
        font=dict(color="#1F2937"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Display "Abstract Metrics" summary below the chart
    st.markdown("---")
    st.subheader("📋 Summary of Abstract Metrics")
    st.write(f"**Accolades / Bio:** {st.session_state.indicators['accolades']}")
    col_a, col_b, col_c = st.columns(3, gap="large")
    with col_a:
        st.metric(label="Books Read", value=st.session_state.indicators["books_read"])
    with col_b:
        st.metric(label="Courses Completed", value=st.session_state.indicators["courses_completed"])
    with col_c:
        st.metric(label="Family Time (hrs/week)", value=f"{st.session_state.indicators['family_time']:.1f}")

    st.markdown("---")
    st.write("🚀 Keep these numbers up to date to see your progress grow over time!")

# ──────────────────────────────────────────────────────────────────────────────
# FEED SECTION (Placeholder / Minimal Implementation)
# ──────────────────────────────────────────────────────────────────────────────
def show_feed():
    st.title("📱 UpRight Feed")
    st.markdown("---")
    st.write("Your personal feed will appear here soon! For now, feel free to snap a screenshot of your Dashboard chart and share it to social media.")
    st.write("Stay tuned: we’re building a full social experience—moments, reactions, comments—just like your favorite apps.")

# ──────────────────────────────────────────────────────────────────────────────
# EXPLORE SECTION (Placeholder)
# ──────────────────────────────────────────────────────────────────────────────
def show_explore():
    st.title("🔍 Explore")
    st.markdown("---")
    st.write("Discover trending profiles and connect with other UpRight users. Coming soon!")

# ──────────────────────────────────────────────────────────────────────────────
# NOTIFICATIONS SECTION (Placeholder)
# ──────────────────────────────────────────────────────────────────────────────
def show_notifications():
    st.title("🔔 Notifications")
    st.markdown("---")
    st.write("You will see notifications here when someone interacts with your feed or follows you. Coming soon!")

# ──────────────────────────────────────────────────────────────────────────────
# MAIN APP LOGIC
# ──────────────────────────────────────────────────────────────────────────────

if not st.session_state.profile_created:
    # If the user has not created a profile yet, show the creation form
    show_profile_creation()
else:
    # Once profile is created, show sidebar + chosen section
    choice = show_sidebar_nav()

    if choice == "Dashboard":
        show_dashboard()
    elif choice == "Edit Profile":
        show_profile_edit()
    elif choice == "Feed":
        show_feed()
    elif choice == "Explore":
        show_explore()
    elif choice == "Notifications":
        show_notifications()
