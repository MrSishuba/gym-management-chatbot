from datetime import datetime, timedelta
import pytz
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

# Set timezone to Central Africa Time (CAT)
CAT = pytz.timezone("Africa/Johannesburg")

class ActionGetTime(Action):
    def name(self):
        return "action_get_time"

    def run(self, dispatcher, tracker, domain):
        current_time = datetime.now(CAT).strftime("%H:%M %p")
        dispatcher.utter_message(text=f"The current time is {current_time}.")
        return [SlotSet("time", current_time)]

class ActionGetDate(Action):
    def name(self):
        return "action_get_date"

    def run(self, dispatcher, tracker, domain):
        current_date = datetime.now(CAT).strftime("%A, %d %B %Y")
        dispatcher.utter_message(text=f"Today's date is {current_date}.")
        return [SlotSet("date", current_date)]

class ActionGetPastDate(Action):
    def name(self):
        return "action_get_past_date"

    def run(self, dispatcher, tracker, domain):
        time_interval = tracker.get_slot("time_interval")
        if not time_interval:
            dispatcher.utter_message(text="Sorry, I didn't understand the time interval.")
            return []

        try:
            if "day" in time_interval:
                days_ago = int(time_interval.split()[0])
                past_date = datetime.now(CAT) - timedelta(days=days_ago)
            elif "hour" in time_interval:
                hours_ago = int(time_interval.split()[0])
                past_date = datetime.now(CAT) - timedelta(hours=hours_ago)
            elif "month" in time_interval:
                months_ago = int(time_interval.split()[0])
                past_date = datetime.now(CAT) - timedelta(days=30 * months_ago)  # Approximation
            elif "year" in time_interval:
                years_ago = int(time_interval.split()[0])
                past_date = datetime.now(CAT) - timedelta(days=365 * years_ago)  # Approximation
            else:
                dispatcher.utter_message(text="Sorry, I didn't understand the time interval.")
                return []

            past_date_str = past_date.strftime("%A, %d %B %Y")
            dispatcher.utter_message(text=f"The date {time_interval} ago was {past_date_str}.")
            return [SlotSet("past_date", past_date_str)]
        except ValueError:
            dispatcher.utter_message(text="Sorry, there was an error processing the time interval.")
            return []

class ActionGetFutureDate(Action):
    def name(self):
        return "action_get_future_date"

    def run(self, dispatcher, tracker, domain):
        time_interval = tracker.get_slot("time_interval")
        if not time_interval:
            dispatcher.utter_message(text="Sorry, I didn't understand the time interval.")
            return []

        try:
            if "day" in time_interval:
                days_from_now = int(time_interval.split()[0])
                future_date = datetime.now(CAT) + timedelta(days=days_from_now)
            elif "hour" in time_interval:
                hours_from_now = int(time_interval.split()[0])
                future_date = datetime.now(CAT) + timedelta(hours=hours_from_now)
            elif "month" in time_interval:
                months_from_now = int(time_interval.split()[0])
                future_date = datetime.now(CAT) + timedelta(days=30 * months_from_now)  # Approximation
            elif "year" in time_interval:
                years_from_now = int(time_interval.split()[0])
                future_date = datetime.now(CAT) + timedelta(days=365 * years_from_now)  # Approximation
            else:
                dispatcher.utter_message(text="Sorry, I didn't understand the time interval.")
                return []

            future_date_str = future_date.strftime("%A, %d %B %Y")
            dispatcher.utter_message(text=f"The date {time_interval} from now will be {future_date_str}.")
            return [SlotSet("future_date", future_date_str)]
        except ValueError:
            dispatcher.utter_message(text="Sorry, there was an error processing the time interval.")
            return []
