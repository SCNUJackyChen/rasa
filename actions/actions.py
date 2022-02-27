# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset

path_to_db = "actions/coffee_name.txt"
coffee_names = []
with open(path_to_db, 'r') as f:
    coffee_names = f.read().splitlines()

class ActionCoffeeList(Action):

    def name(self) -> Text:
        return "action_coffee_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        res = "Here are our coffee list: " + ', '.join(coffee_names)
        dispatcher.utter_message(text = res)

        return []


class ActionConfirmCoffeeName(Action):

    def name(self) -> Text:
        return "action_confirm_coffee_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        coffee_name = tracker.get_slot('coffee_name')

        res = ""
        ret = []
        if coffee_name in coffee_names:
            res = "Your choice: " + coffee_name
            ret = [SlotSet("coffee_name_is_collected", True)]
        else:
            res = "Sorry, we do not have this coffee: " + coffee_name
        
        dispatcher.utter_message(text = res)
        return ret

class ActionResetCoffeePreferenceForm(Action):

    def name(self):
        return "action_reset_coffee_preference_form"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("sweetness", None), \
                SlotSet("size", None), \
                SlotSet("ice_or_hot", None), \
                SlotSet("add_milk_or_not", None)]   

                
class ActionResetCustomerInfoForm(Action):

    def name(self):
        return "action_reset_customer_info_form"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("email", None), \
                SlotSet("address", None), \
                SlotSet("customer_name", None)]  
