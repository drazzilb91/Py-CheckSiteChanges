import requests
import time

def get_page_content():
    url = "https://canadasoccer.com/wp-admin/admin-ajax.php"
    params = {
        "action": "get_referees",
        "langCode": "en",
        "year": "",
        "month": "",
        "search-text": "",
        "_": int(time.time()) # The _ parameter looks like a timestamp, so we'll generate it based on the current time
    }
    response = requests.get(url, params=params)
    return response.json() # Parse the response as JSON

previous_latest_date: str | None = None

def check_for_changes():
    global previous_latest_date
    data = get_page_content()['data']
    latest_date = max(item['0'] for item in data) if data else None
    if latest_date != previous_latest_date:
        print("New games detected!")
        previous_latest_date = latest_date

def monitor_website(delay_in_seconds=3600):
    while True:
        check_for_changes()
        time.sleep(delay_in_seconds)

monitor_website()

