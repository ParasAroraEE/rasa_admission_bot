# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


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
from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests


class ActionAdmissionForm(FormAction):

    def name(self) -> Text:
        return "admission_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        print("required_slots(tracker:Tracker)")
        return["name", "ssn", "subject_code"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "subject_code": [
                self.from_entity(entity="subject", intent="subject_entry"),
            ],
        }

    @staticmethod
    def subject_db() -> List[Text]:
        """Database of supported cuisines"""

        return [
            "physics",
            "computer",
            "biology",
            "chemistry",
            "maths",
            "science",

        ]

    def validate_subject_code(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if value.lower() in self.subject_db():

            return {"subject_code": value}
        else:
            dispatcher.utter_message(template="utter_wrong_subject")

            return {"subject_code": None}

    def validate_ssn(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if len(value) == 6:

            return {"ssn": value}
        else:
            dispatcher.utter_message(template="utter_wrong_ssn")

            return {"ssn": None}

    def submit(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:

        dispatcher.utter_message(template="utter_submit")

        return []
