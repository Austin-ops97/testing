import streamlit as st
from utils.weather import fetch_and_update_data

def dashboard(selected_locations):
    """Displays the Dashboard with vertical cards and horizontal content."""
    st.markdown("<h1>Energy Dashboard</h1>", unsafe_allow_html=True)

    # Fetch Data
    data = fetch_and_update_data(selected_locations)

    # Vertical Layout Wrapper
    st.markdown('<div class="main">', unsafe_allow_html=True)

    for location, info in data.items():
        # Each card container
        st.markdown(f"""
        <div class="location-container">
            <h2>{location}</h2>
            <div class="metrics">
                <div>
                    <div class="metric-title">Price</div>
                    <div class="metric-value">${info["Price"]}</div>
                </div>
                <div>
                    <div class="metric-title">Temperature</div>
                    <div class="metric-value">{info["Temperature"]}</div>
                </div>
                <div>
                    <div class="metric-title">Condition</div>
                    <div class="metric-value">{info["Condition"]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Close Wrapper
    st.markdown('</div>', unsafe_allow_html=True)
