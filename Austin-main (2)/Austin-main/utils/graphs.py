import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

# Ensure the directory exists for saving trend graphs
TREND_GRAPH_DIR = "resources/trend_graphs"
os.makedirs(TREND_GRAPH_DIR, exist_ok=True)

def create_trend_graph(location, price_history):
    """
    Create a trend graph image for the given location and return its file path.

    Args:
        location (str): The name of the location (e.g., "PHR", "Wharton").
        price_history (list): A list of tuples containing (timestamp, price).
                              Example: [(datetime1, 25.0), (datetime2, 30.0), ...]

    Returns:
        str: The file path to the generated graph image, or None if not enough data.
    """
    try:
        if not price_history:
            print(f"[Error] No price history available for {location}. Cannot create graph.")
            return None

        # Limit to the last 10 points and pad if necessary
        price_history_copy = price_history[-10:]
        while len(price_history_copy) < 10:
            last_timestamp = price_history_copy[0][0] if price_history_copy else datetime.now()
            price_history_copy.insert(0, (last_timestamp - timedelta(minutes=1), 0.0))

        timestamps, prices = zip(*price_history_copy)

        if len(prices) < 2:
            print(f"[Warning] Insufficient data for {location}. Cannot create graph.")
            return None

        plt.figure(figsize=(1.5, 0.75), dpi=100)
        plt.plot(range(len(prices)), prices, color="red", linewidth=2, marker='o', markersize=0)

        for i in range(1, len(prices)):
            color = "green" if prices[i] > prices[i - 1] else "red"
            plt.plot([i - 1, i], [prices[i - 1], prices[i]], color=color, linewidth=2)

        plt.axis("off")
        plt.tight_layout()

        graph_path = os.path.join(TREND_GRAPH_DIR, f"{location}_trend.png")
        plt.savefig(graph_path, bbox_inches="tight", pad_inches=0, transparent=True)
        plt.close()

        print(f"[Success] Trend graph created for {location}: {graph_path}")
        return graph_path
    except Exception as e:
        print(f"[Error] Failed to create trend graph for {location}: {e}")
        return None
