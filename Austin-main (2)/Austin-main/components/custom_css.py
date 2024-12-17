import streamlit as st

def apply_custom_css():
    """Applies custom CSS for vertical cards with gaps and horizontal content."""
    st.markdown(
        """
        <style>
        /* Overall App Background */
        body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Vertical Cards Layout */
        .main {
            display: flex;
            flex-direction: column; /* Cards stacked vertically */
            gap: 20px; /* Gap between cards */
            padding: 20px;
        }

        /* Location Container Styling */
        .location-container {
            background-color: #1e1e1e; /* Dark gray background */
            border-radius: 16px; /* Rounded corners */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            padding: 20px; /* Inner spacing */
            margin: 10px 0; /* Add margin to create spacing between cards */
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        /* Hover Effect */
        .location-container:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.6);
        }

        /* Horizontal Metrics Layout */
        .metrics {
            display: flex;
            justify-content: space-around; /* Distribute content evenly */
            align-items: center;
            gap: 20px; /* Gap between metrics */
            text-align: center;
        }

        /* Metric Titles */
        .metric-title {
            font-size: 14px;
            color: #b0b0b0;
            text-transform: uppercase;
            margin-bottom: 5px;
        }

        /* Metric Values */
        .metric-value {
            font-size: 20px;
            color: #ffffff;
            font-weight: bold;
        }

        /* Dashboard Title Styling */
        h1 {
            text-align: center;
            color: #ffffff;
            font-size: 36px;
            margin-bottom: 20px;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .metrics {
                flex-direction: column; /* Stack metrics vertically on small screens */
                gap: 10px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
