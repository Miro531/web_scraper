import requests
import json
from datetime import datetime
import pandas as pd

url = "https://www.sofascore.com/api/v1/sport/tennis/scheduled-events/2024-11-07"

response = requests.request("GET", url)

jsondata = json.loads(response.text)


# Check if 'events' key exists and is a list
if 'events' in jsondata and isinstance(jsondata['events'], list):
    events_data = []

    # Loop through each event
    for event in jsondata["events"]:
        try:
            # Tournament and match information
            tournament_name = event["season"]["name"]
            round_name = event["roundInfo"]["name"]
            match_status = event["status"]["description"]
            start_time = datetime.fromtimestamp(
                event["startTimestamp"]).strftime('%Y-%m-%d %H:%M:%S')

            # Player information
            home_player_name = event["homeTeam"]["name"]
            away_player_name = event["awayTeam"]["name"]

            # Check the winner based on winnerCode
            winner = home_player_name if event["winnerCode"] == 1 else away_player_name

            # Extract data into a dictionary
            events_data.append({
                "Tournament": tournament_name,
                "Start Time": start_time,
                "Home Player": home_player_name,
                "Away Player": away_player_name,
                "Round": round_name,
                "Status": match_status,
                "Winner": winner
            })
        except KeyError as err:
            print("Missing key in event data: {err}")

    # Transform the list of dictionaries into a pandas DataFrame.
    df = pd.DataFrame(events_data)

    # Print the DataFrame on terminal.
    print(df.head())

    # Save the DataFrame to CSV or Excel.
    df.to_csv("tennis_events.csv", index=False)
    # df.to_excel("tennis_events.xlsx", index=False)

else:
    print("No data was found.")
