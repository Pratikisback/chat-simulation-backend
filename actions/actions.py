import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Load the data at the module level
df = pd.read_csv("actions/final.csv")

# Clean column names just in case
df.columns = df.columns.str.strip()

class ActionListProjectsByLocation(Action):
    def name(self) -> Text:
        return "action_list_projects_by_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract the location from user message
        user_message = tracker.latest_message.get('text', '')
        location = None
        for city in df['Location'].unique():
            if city.lower() in user_message.lower():
                location = city
                break

        if not location:
            dispatcher.utter_message(text="Please specify a valid location.")
            return []

        filtered = df[df['Location'].str.lower() == location.lower()]

        if not filtered.empty:
            projects = ", ".join(filtered['Project Name'].tolist())
            dispatcher.utter_message(
                text=f"Here are some projects available in {location.title()}: {projects}"
            )
        else:
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find any projects in {location.title()}."
            )

        return []


class ActionGetProjectPrice(Action):
    def name(self) -> Text:
        return "action_get_project_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message.get("text", "").lower()
        matched = df[df["Project Name"].str.lower().apply(lambda x: x in text)]

        if not matched.empty:
            row = matched.iloc[0]
            price = row["Starting Price"]
            project = row["Project Name"]
            city = row["Location"]
            dispatcher.utter_message(text=f"The starting price for {project} in {city} is {price}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the price for that project.")

        return []


class ActionGetProjectOverview(Action):
    def name(self) -> Text:
        return "action_get_project_overview"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message.get("text", "").lower()
        matched = df[df["Project Name"].str.lower().apply(lambda x: x in text)]

        if not matched.empty:
            row = matched.iloc[0]
            project = row["Project Name"]
            overview = row["Overview"]
            dispatcher.utter_message(text=f"Here’s a quick overview of {project}: {overview}")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find an overview for that project.")

        return []


class ActionGetLargerProject(Action):
    def name(self) -> Text:
        return "action_get_larger_project"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.latest_message.get("text", "").lower()
        filtered = df[df["Location"].str.lower() == location]

        if not filtered.empty and "Total Land Area" in df.columns:
            filtered["Area"] = pd.to_numeric(filtered["Total Land Area"], errors="coerce")
            largest = filtered.sort_values(by="Area", ascending=False).iloc[0]
            dispatcher.utter_message(
                text=f"The largest project in {location.title()} is {largest['Project Name']} with {largest['Total Land Area']} of land."
            )
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't determine the largest project in {location.title()}.")

        return []
