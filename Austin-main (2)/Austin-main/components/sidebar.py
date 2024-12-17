import streamlit as st

def render_sidebar():
    """Renders the sidebar with settings."""
    if "selected_locations" not in st.session_state:
        st.session_state.selected_locations = ["PHR", "Wharton", "Ector"]
    if "refresh_rate" not in st.session_state:
        st.session_state.refresh_rate = 30

    # Sidebar header
    st.sidebar.markdown("<h2 style='text-align: center;'>Settings</h2>", unsafe_allow_html=True)

    # Location selection
    selected_locations = st.sidebar.multiselect(
        "Select Locations:",
        options=["PHR", "Wharton", "Ector"],
        default=st.session_state.selected_locations
    )
    st.session_state.selected_locations = selected_locations

    # Refresh rate selection
    refresh_rate = st.sidebar.slider(
        "Refresh Rate (seconds):",
        min_value=15,
        max_value=60,
        value=st.session_state.refresh_rate
    )
    st.session_state.refresh_rate = refresh_rate

    return selected_locations, refresh_rate
