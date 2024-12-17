import requests
from bs4 import BeautifulSoup

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

    url = url_map.get(location)
    identifier = identifier_map.get(location)

    if not url or not identifier:
        return None

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        rows = soup.find_all("tr")
        for row in rows:
            cells = row.find_all("td", class_="tdLeft")
            if cells and cells[0].text.strip() == identifier:
                return float(cells[3].text.strip().replace(',', ''))
    except Exception as e:
        print(f"Error fetching price for {location}: {e}")
        return None

def fetch_lmp(location):
    """Fetch the LMP value for a given location."""
    url = "https://www.ercot.com/content/cdr/html/current_np6788.html"
    identifier_map = {
        "PHR": "BAC_RN_ALL",
        "Wharton": "TGS_GT01",
        "Ector": "RN_ECEC_HOLT"
    }

    identifier = identifier_map.get(location)
    if not identifier:
        return 0.0

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        rows = soup.find_all("tr")
        for row in rows:
            cells = row.find_all("td", class_="tdLeft")
            if cells and cells[0].text.strip() == identifier:
                return float(cells[1].text.strip())
    except Exception as e:
        print(f"Error fetching LMP for {location}: {e}")
        return 0.0
