import helper
import logging
import csv
from io import StringIO

# === Documentation of history.py ===


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot which
    is the telegram bot object from the main code.py function. It calls helper.py to get the user's
    historical data and based on whether there is data available, it either prints an error message or
    displays the user's historical data.
    """

    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)

        if user_history is None:
            raise Exception("Sorry! No spending records found!")

        if len(user_history) == 0:
            bot.send_message(chat_id, "Sorry! No spending records found!")
        else:
            # Create a tabular representation of the data
            tabular_data = ""
            tabular_data += "+-------------------+-------------------+-------------+\n"
            tabular_data += "|     DATE          |    CATEGORY       |   AMOUNT    |\n"
            tabular_data += "+-------------------+-------------------+-------------+\n"

            for line in user_history:
                rec = line.split(",")  # Assuming data is comma-separated
                if len(rec) == 3:
                    tabular_data += "| {:<15} | {:<17} | {:<11} |\n".format(
                        rec[0], rec[1], rec[2]
                    )

            tabular_data += "+-------------------+-------------------+-------------+"
            tabular_data += ""

            # Send the tabular data as a Markdown-formatted message
            bot.send_message(chat_id, tabular_data, parse_mode="Markdown")

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops! " + str(e))
