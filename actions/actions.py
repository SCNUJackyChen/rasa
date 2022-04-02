# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import pandas as pd
import sys
sys.path.append(".")

from spell_checker.spellcheck import SpellCheck

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.types import DomainDict

import time

from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
model = AutoModelForSequenceClassification.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
LABELS = ["neg", "neu", "pos"]

path_to_db = "actions/kopi_list.xlsx"
db = pd.read_excel(path_to_db)
db["Name"] = db["Name"].str.lower()
spell_check = SpellCheck(db["Name"])

import mysql.connector
cnx = mysql.connector.connect(user='root',
                             password='123456',
                             host='localhost', # db for docker
                             database='rasa',
                             auth_plugin='mysql_native_password')
cursor = cnx.cursor(buffered=True)

class ValidateCoffeePreferenceForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_coffee_preference_form"

    def validate_Sweetness(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        
        if slot_value == "sugar":
            slot_value = "sweet"
        if slot_value == "more sugar":
            slot_value = "sweeter"

        if slot_value.lower().strip() in ['half', 'no sugar', 'less sweet', 'sweeter']:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"Sweetness": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"Sweetness": None}

    def validate_State(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value.lower().strip() in ['iced', 'warm', 'lukewarm']:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"State": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"State": None}

    def validate_Milkness(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value.lower().strip() in ['condensed milk', 'no milk', 'evaporated milk']:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"Milkness": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"Milkness": None}
    
    def validate_Strength(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value.lower().strip() in ['normal', 'weak', 'strong', 'stronger']:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"Strength": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"Strength": None}

    def validate_Size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value.lower().strip() in ['large', 'medium', 'small']:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"Size": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"Size": None}


class ValidateCoffeeNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_coffee_name_form"

    def validate_coffee_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        coffee_list = list(db["Name"].values)
        
        if slot_value.lower().strip() in coffee_list:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"coffee_name": slot_value.lower().strip()}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text=f"I cannot find this coffee. I'm assuming you mis-spelled.")
            spell_check.check(slot_value.lower().strip())
            hint = spell_check.correct()
            dispatcher.utter_message(text=f"Do you mean " + hint + "? Please input again.")
            return {"coffee_name": None}

class ActionConfirmCoffeeName(Action):

    def name(self) -> Text:
        return "action_confirm_coffee_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        coffee_name = tracker.get_slot('coffee_name')

        res = ""
        ret = []
        target = db.loc[db['Name'] == coffee_name]
        if not target.empty:  # target must not be empty
            sweetness = target["Sweetness"].values[0]
            milkness = target["Milkness"].values[0]
            strength = target["Strength"].values[0]
            state = target["State"].values[0]
            ret = [SlotSet("Sweetness", sweetness), \
                SlotSet("State", state), \
                SlotSet("Milkness", milkness), \
                SlotSet("Strength", strength)]   
        else:
            ret = [SlotSet("coffee_name", None)]
        
        return ret

class ActionResetCoffeePreferenceForm(Action):

    def name(self):
        return "action_reset_coffee_preference_form"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("Sweetness", None), \
                SlotSet("Size", None), \
                SlotSet("State", None), \
                SlotSet("Milkness", None), \
                SlotSet("Strength", None), \
                SlotSet("coffee_name", None) ]   

                
class ActionResetCustomerInfoForm(Action):

    def name(self):
        return "action_reset_customer_info_form"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("email", None), \
                SlotSet("address", None), \
                SlotSet("customer_name", None)]  

# class ActionSetCoffeeNameByPreference(Action):

#     def name(self):
#         return "action_set_coffee_name_by_preference"

#     def run(self, dispatcher, tracker, domain):
#         sweetness = tracker.get_slot('Sweetness')
#         milkness = tracker.get_slot('Milkness')
#         strength = tracker.get_slot('Strength')
#         state = tracker.get_slot('State')

#         coffee_name = db.loc[(db['Sweetness'] == sweetness) & \
#                      (db['Milkness'] == milkness) & \
#                      (db['Strength'] == strength) & \
#                      (db['State'] == state) ]
#         ret = []
#         if (coffee_name.empty):
#             res = "Sorry, no kopi match.."
#             dispatcher.utter_message(text = res)
#         else:
#             ret = [SlotSet("coffee_name", str(coffee_name['Name'].values[0]))]
        
#         return ret

class ActionSelectCoffeeNameByPreference(Action):

    def name(self):
        return "action_select_coffee_name_by_preference"

    def run(self, dispatcher, tracker, domain):
        sweetness = tracker.get_slot('Sweetness')
        milkness = tracker.get_slot('Milkness')
        strength = tracker.get_slot('Strength')
        state = tracker.get_slot('State')

        cursor.execute('select Name from rasa.kopi_list where sweetness = %s and milkness = %s and strength = %s and state = %s limit 1;',[sweetness,milkness,strength,state])
        record = cursor.fetchone()

        res = ""
        ret = []
        if record[0] is None:
            res = "Sorry, there is no coffee to suit your taste" 
        else:           
            res = "According to your preference, we recommend you to order " + record[0]
            ret = [SlotSet("coffee_name", record[0])]
        
        dispatcher.utter_message(text = res)
        return ret

class ActionSubmitOrder(Action):

    def name(self):
        return "action_submit_order"

    def run(self, dispatcher, tracker, domain):
        kopiname = tracker.get_slot('coffee_name')
        size = tracker.get_slot('Size')
        customername = tracker.get_slot('customer_name')
        email = tracker.get_slot('email')
        address = tracker.get_slot('address')
        m = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        #m = str(random.randint(1,1000))

        cursor.execute('insert into rasa.order(order_id,kopi_name,size,customer_name,email,address) values (%s,%s,%s,%s,%s,%s);',[m,kopiname,size,customername,email,address])
        cnx.commit() 

        return []

class ActionGetSentimentsScore(Action):

    def name(self):
        return "action_get_sentiments_score"
    
    def run(self, dispatcher, tracker, domain):
        text = tracker.current_state()["latest_message"]["text"]
        aspects = tracker.current_state()["latest_message"]["entities"]
        res = []
        for aspect in aspects:
            value = aspect["value"]
            query = tokenizer("[CLS] " + text + " [SEP] " + value + " [SEP]", return_tensors="pt")
            outputs = model(**query)
            outputs_list = outputs.get("logits").detach().numpy().tolist()[0]
            prediction = LABELS[outputs_list.index(max(outputs_list))]
            res.append([value, prediction])
        
        ret = [SlotSet("ABSA_result", res)]
        return ret


class ActionSubmitUserFeedback(Action):

    def name(self):
        return "action_submit_user_feedback"
    
    def run(self, dispatcher, tracker, domain):
        res = tracker.get_slot('ABSA_result')

        m = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))

        for i, p in enumerate(res):
            aspect, review = p
            cursor.execute('insert into rasa.feedback(idfeedback,aspect,review) values (%s,%s,%s);',[m + str(i), aspect, review])
            cnx.commit() 

        return []




if __name__ == "__main__" :
    
    # path_to_db = "actions/kopi_list.xlsx"
    # db = pd.read_excel(path_to_db)
    # sweetness = "sweeter"
    # milkness = "no milk"
    # strength = "stronger"
    # state = "warm"
    # coffee_name = db.loc[(db['Sweetness'] == sweetness) & \
    #                  (db['Milkness'] == milkness) & \
    #                  (db['Strength'] == strength) & \
    #                  (db['State'] == state) ]
    # print(coffee_name["Name"].values[0])

    # coffee = "kopi O"
    # db["Name"] = db["Name"].str.lower()
    # coffee_list = list(db["Name"].values)
    # print(coffee_list[0:5])
    # print(coffee.lower().strip() in coffee_list)

    # with open("temp.txt", 'w') as f:
    #     for name in db["Name"]:
    #         print('- [' + name + '](coffee_name)', file=f)
    



    # set the string
    string_to_be_checked = "kopi o pang"
    spell_check.check(string_to_be_checked.lower().strip())

    # print suggestions and correction
    print (spell_check.suggestions())
    print (spell_check.correct())