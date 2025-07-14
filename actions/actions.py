# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

# class ActionGetProjectPrice(Action):
#     def name(self) -> Text:
#         return "action_get_project_price"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         project = next(tracker.get_latest_entity_values("project_name"), None)
#         location = next(tracker.get_latest_entity_values("location"), None)
        
#         if project and location:
#             # Replace with real DB/API lookup
#             response = f"The starting price for {project} in {location} is around ₹2.5 Cr."
#         else:
#             response = "Please specify both the project name and the location."

#         dispatcher.utter_message(text=response)
#         return []

# class ActionGetProjectOverview(Action):
#     def name(self) -> Text:
#         return "action_get_project_overview"

#     def run(self, dispatcher, tracker, domain):
#         project = next(tracker.get_latest_entity_values("project_name"), None)
#         response = f"{project} is a premium residential project with 2 & 3 BHK options." if project else "Please specify the project name."
#         dispatcher.utter_message(text=response)
#         return []

# class ActionListProjectsByLocation(Action):
#     def name(self) -> Text:
#         return "action_list_projects_by_location"

#     def run(self, dispatcher, tracker, domain):
#         location = next(tracker.get_latest_entity_values("location"), None)
#         response = f"Here are some projects available in {location}: Purva Clermont, Purva Silversands." if location else "Please specify the location."
#         dispatcher.utter_message(text=response)
#         return []


# actions/actions.py

import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Load your Excel data
DATA_PATH = "actions/ProjectPageContent.xlsx"
df = pd.read_excel(DATA_PATH)


class ActionGetProjectPrice(Action):
    def name(self) -> Text:
        return "action_get_project_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text", "").lower()

        for _, row in df.iterrows():
            project_name = str(row.get("Project Name", "")).lower()
            location = str(row.get("Location", "")).lower()

            if project_name in user_message and location in user_message:
                price = row.get("Price", "Price not available")
                dispatcher.utter_message(text=f"The starting price for {row['Project Name']} in {row['Location']} is around {price}.")
                return []

        dispatcher.utter_message(text="Sorry, I couldn't find the price for that project in the given location.")
        return []
    class ActionListProjectsByLocation(Action):
        def name(self) -> Text:
            return "action_list_projects_by_location"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # Properly extract the location entity
            location = next(tracker.get_latest_entity_values("location"), None)

            if not location:
                dispatcher.utter_message(text="Could you please specify a location?")
                return []

            # Normalize case for comparison
            location = location.lower()
            filtered = df[df['Location'].str.lower() == location]

            if not filtered.empty:
                project_names = filtered['Project Name'].tolist()
                projects = ", ".join(project_names)
                dispatcher.utter_message(
                    text=f"Here are some projects available in {location.title()}: {projects}"
                )
            else:
                dispatcher.utter_message(
                    text=f"Sorry, I couldn't find any projects in {location.title()}."
                )

            return []