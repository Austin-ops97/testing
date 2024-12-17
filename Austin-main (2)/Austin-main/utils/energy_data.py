from datetime import datetime, timedelta
from utils.weather import (
    get_current_temperature_phr,
    get_current_temperature_wharton,
    get_current_temperature_ector,
    get_current_condition_phr,
    get_current_condition_wharton,
    get_current_condition_ector,
)
from utils.graphs import create_trend_graph

# ==================== PRICE FETCHING FUNCTION ====================
def fetch_price(location):
    """Fetch the price for a specific location."""
    url_map = {
        "PHR": "https://www.ercot.com/content/cdr/html/current_np6788.html",
        "Wharton": "https://www.ercot.com/content/cdr/html/current_np6788.html",
        "Ector": "https://www.ercot.com/content/cdr/html/current_np6788.html"
    }
    identifier_map = {
        "PHR": "BAC_RN_ALL",
        "Wharton": "TGS_GT01",
        "Ector": "RN_ECEC_HOLT"
    }

    try:
        # Get the correct URL and identifier for the location
        url = url_map.get(location, "")
        identifier = identifier_map.get(location, "")

        if not url or not identifier:
            st.warning(f"URL or identifier missing for {location}.")
            return None

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Scrape price data from the table
        rows = soup.find_all("tr")
        for row in rows:
            cells = row.find_all("td", class_="tdLeft")
            if cells and cells[0].text.strip() == identifier:
                price_text = cells[3].text.strip().replace(',', '')
                try:
                    price = float(price_text)
                    return price
                except ValueError:
                    st.warning(f"Invalid price format for {location}: {price_text}")
        st.warning(f"No price data found for {location}.")
    except Exception as e:
        st.warning(f"Error fetching price for {location}: {e}")
    return None  # Return None to indicate missing data

# ==================== LMP FETCHING FUNCTION ====================
def fetch_lmp(location):
    """Fetch the LMP value for a given location."""
    url = "https://www.ercot.com/content/cdr/html/current_np6788.html"
    identifier_map = {
        "PHR": "BAC_RN_ALL",
        "Wharton": "TGS_GT01",
        "Ector": "RN_ECEC_HOLT"
    }

    try:
        identifier = identifier_map.get(location, "")
        if not identifier:
            raise ValueError(f"Unknown location: {location}")

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        rows = soup.find_all("tr")
        for row in rows:
            cells = row.find_all("td", class_="tdLeft")
            if cells and cells[0].text.strip() == identifier:
                lmp = cells[1].text.strip()  # Extract the LMP value
                try:
                    return float(lmp)
                except ValueError:
                    st.warning(f"Invalid LMP format for {location}: {lmp}")
        st.warning(f"No LMP data found for {location}.")
    except Exception as e:
        st.warning(f"Error fetching LMP for {location}: {e}")
    return 0.0

def fetch_weather_data(location, temp_func, cond_func):
    """Fetches weather data for a given location."""
    try:
        temp = temp_func()
        cond = cond_func()
    except Exception as e:
        temp, cond = "Error", "Error"
        print(f"Error fetching weather for {location}: {e}")
    return temp, cond

def fetch_and_update_data(selected_locations):
    """Fetches and updates weather and price data."""
    current_time = datetime.now()
    one_hour_ago = current_time - timedelta(hours=1)

    data = {}

    location_funcs = {
        "PHR": (get_current_temperature_phr, get_current_condition_phr),
        "Wharton": (get_current_temperature_wharton, get_current_condition_wharton),
        "Ector": (get_current_temperature_ector, get_current_condition_ector),
    }

    for location in selected_locations:
        temp_func, cond_func = location_funcs.get(location, (lambda: "N/A", lambda: "N/A"))

        # Fetch weather data
        temp, cond = fetch_weather_data(location, temp_func, cond_func)

        # Mock price and LMP data (replace with actual fetching logic)
        current_price = 100.0  # Replace with fetch_price(location)
        lmp = 95.0  # Replace with fetch_lmp(location)

        # Generate price history (replace with actual data if available)
        price_history = [
            (one_hour_ago + timedelta(minutes=i * 10), current_price + i)
            for i in range(6)
        ]

        # Calculate percentage change
        initial_price = price_history[0][1]
        percent_change = (
            ((current_price - initial_price) / initial_price) * 100
            if initial_price
            else 0.0
        )

        # Determine arrow and color for price change
        arrow = "↑" if percent_change > 0 else ("↓" if percent_change < 0 else "")
        color = "#00e676" if percent_change > 0 else (
            "#ff1744" if percent_change < 0 else "#ffffff"
        )

        # Calculate Adder
        adder = max(0.0, current_price - lmp)
        adder_color = "#00e676" if adder > 0 else "#ffffff"

        # Create trend graph
        graph_path = create_trend_graph(location, price_history)

        # Assign data
        data[location] = {
            "Price": f"{current_price:.2f}",
            "Change": f"{percent_change:+.2f}% {arrow}",
            "Change_Color": color,
            "Temperature": f"🌡️ {temp}",
            "Condition": f"{cond}",
            "LMP": f"${lmp:.2f}",
            "LMP_Color": "#ffffff",
            "Adder": f"${adder:.2f}" if adder != 0 else "0.0",
            "Adder_Color": adder_color,
            "Trend_Graph_Path": graph_path,
        }

    return data
