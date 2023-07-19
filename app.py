import streamlit as st
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import datetime
import requests
import time
import json

st.title('Canada Soccer Referee Assignments Watcher')

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
    st.write("Latest match appointment date:", latest_date)
    if (latest_date != previous_latest_date) & (previous_latest_date is not None):
        st.write("New games detected!")
        previous_latest_date = latest_date
    
    return data


# If you have a JSON file saved locally, you can use this function to load it   
# def load_json():
#     with open('SampleReturnedData.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)
#         return data

def generateTable(data):

    # Only the first 10 rows
    # df = pd.DataFrame(data['data'][:10])
    df = pd.DataFrame(data)

    # Drop the "href" column
    df = df.drop(columns=["href"])

    # Set column labels to "Date", "Referee", "Assistant Referee(s)", "Fourth Official", "Match", "Comepetition"
    df.columns = ["Date", "Referee", "Assistant Referee(s)", "Fourth Official", "Match", "Comepetition"]

    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Keep only items where the date is in the future
    df = df[df["Date"] > pd.to_datetime('today')]
    # df = df[df["Date"] > pd.to_datetime('today') - pd.Timedelta(days=3)]

    # Convert the 'Date' column from datetime to date for display purposes
    df['Date'] = df['Date'].dt.date


    # Clean up the Referee column by removing the html around the person's name
    df["Referee"] = df["Referee"].str.replace(r"<.*?>", "", regex=True, case=False)

    # Replace </p> tags with newline characters, then remove the rest of the HTML tags
    df["Assistant Referee(s)"] = df["Assistant Referee(s)"].str.replace("</p>", "\n", regex=False, case=False)
    df["Assistant Referee(s)"] = df["Assistant Referee(s)"].str.replace(r"<.*?>", "", regex=True, case=False)

    df["Fourth Official"] = df["Fourth Official"].str.replace(r"<.*?>", "", regex=True, case=False)

    return df


def main(delay_in_seconds=3600):
    # while True:
        with st.spinner("Checking for changes..."):
            data = check_for_changes()

        # Get current time
        now = datetime.datetime.now()
        st.write('Last updated at: ', now)
        # Calculate next update time
        next_update = now + datetime.timedelta(seconds=3600)

        # Display next update time
        st.write('Next update at: ', next_update)
        
        # Generate table
        df = generateTable(data=data)
    
        with st.container():
            st.write('Upcoming games:')
            # st.write(df)
            st.table(df)

        # time.sleep(delay_in_seconds)

if __name__ == "__main__":
    main()