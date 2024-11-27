import requests
import time
import helper
import graphing
from datetime import datetime
from collections import defaultdict


API_URL = "https://api.exchangerate-api.com/v4/latest/"


def run(message, bot):
    """
    Command: /convert <amount> <from_currency> <to_currency>
    Example: /convert 100 USD EUR
    """

    try:
        chat_id = message.chat.id
        text = message.text.split()

        if len(text) != 4:
            bot.send_message(
                chat_id, "Usage: /convert <amount> <from_currency> <to_currency>"
            )
            return

        _, amount, from_currency, to_currency = text
        from currency_converter import convert_currency

        result = convert_currency(amount, from_currency.upper(), to_currency.upper())
        bot.send_message(chat_id, result)
    except Exception as e:
        bot.send_message(message.chat.id, str(e))


def convert_currency(amount, from_currency, to_currency):
    try:
        response = requests.get(API_URL + from_currency)
        data = response.json()

        if "rates" not in data:
            return (
                "Unable to fetch exchange rates at the moment. Please try again later."
            )

        rates = data["rates"]
        if to_currency not in rates:
            return f"Currency '{to_currency}' is not supported."

        converted_amount = float(amount) * rates[to_currency]
        return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
    except Exception as e:
        return str(e)
