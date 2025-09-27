# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
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
class ActionSayShirtSize(Action):

    def name(self) -> Text:
        return "action_say_shirt_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shirt_size = tracker.get_slot("shirt_size")
        if not shirt_size:
            dispatcher.utter_message(text="I don't know your shirt size.")
        else:
            dispatcher.utter_message(text=f"Your shirt size is {shirt_size}!")
        return []

class CreateTrainingPlan(Action):
    def name(self) -> Text:
        return "action_training_plan"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        training_plan = tracker.get_slot("training_plan")
        if not training_plan:
            dispatcher.utter_message(text="Please specify a training plan.")
        else:
            if training_plan == "weight":
                dispatcher.utter_message(text="What is your weight? (Kg)")
                last_user_message = tracker.latest_message['text']
                SlotSet("weight", last_user_message)
                slot_value = tracker.get_slot("weight")
                dispatcher.utter_message(slot_value)
            elif training_plan == "fitness":
                dispatcher.utter_message(text="What is your fgoal?")
            elif training_plan == "cardio":
                dispatcher.utter_message(text="What is your cgoal?")
        return[]