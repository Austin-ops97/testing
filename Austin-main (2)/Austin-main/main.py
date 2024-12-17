import streamlit as st
from components.sidebar import render_sidebar
from components.dashboard import dashboard
from components.custom_css import apply_custom_css

def main():
    # Apply global CSS
    apply_custom_css()

    # Sidebar settings
    selected_locations, refresh_rate = render_sidebar()

    # Dashboard rendering
    dashboard(selected_locations)

if __name__ == "__main__":
    st.set_page_config(page_title="Energy Dashboard", layout="wide")
    main()
