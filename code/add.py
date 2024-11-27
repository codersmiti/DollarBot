import helper
import logging
from telebot import types
from datetime import datetime
import cv2

import re

# pytesseract.pytesseract.tesseract_cmd = r' c:\\users\\vedan\\appdata\\roamin\\python\\python312\site-packages'

import requests
import copy

from typing import Dict
from google.cloud import vision

# import random
import numpy as np

import os
import io


credentials_content = """
{
  "type": "service_account",
  "project_id": "mythical-sky-442720-c9",
  "private_key_id": "9edd34c633db5acac3331b3e620f45c9de76eca4",
  "private_key": "-----BEGIN PRIVATE KEY-----/nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwVMWaZ7wd+T8V/n8vPmVNxnOIa/NrQAOUhmvwOQFLJY6fuYEuWVed/5qVtMOuPt+0NU73t4wFqtCKPe/n7OTl1pW8sRytV42l6duw5/DEOsxRNKXtEHEQhiRzFmnWiUWNKCJcwca9Zi38QiAK/nc6o/Qtj/5SIxlfFfwJGloepFkBf0XyStFqGeA9QIncRWt/vvMKaaMTsWIfrhMOaZ/nKY/Ygz5Qg/PQy6VG81p+9+zqnyPxJIPOQSiEOdl3LZqyme+yUAE30cOtkTasDjNL/nFGUMHzpjz8gDgtyrJaaIymK0UTA9ircsinJKivouoMopyupqlhjRG9QYDFbBKzGz/ncpWkWEHJAgMBAAECggEAAfAA1E5jubxvV+ghAd8//c9wxb/yyAAn5wFs2HtBHzJz/nSuzUYnCpRcsNLPT8i3nY0IP9Skq5QKai/9y7gmBmH/U7olGpKA6+Cwufi636LZpn/nOWpbQdelpbrbgqECDEpdfV8L3aciqHMzjosTDCsiN4GadVAGH4a5H0hLNx/E705W/nNtNfu5dYxSqSLtqabhcm+pG+G5BSmrg/0tecX22LWdBj1Scf6phBZh1qihkprtWr/nOTPpNiz+sOveJtsTvDAAW55OlhH6CZ3fXmoTakj8d9r67h0fJsbQqNAmE1KhMqs//nopk6YmKM40R3FPddo2IvsOmxCO1kHbxPRJ3W6PXrFwKBgQD5Kh2s7O1PaRddDxNP/nXTeSqIL9Tmw8XhVypWso6jorYw/rvZEvrsURbdJkFYWupaklRvVXfhguMRCGwSqx/nf6/V1Pu9VCcXM7a+oXNYNSvBRMoQYWODmk09qu+avYOFl35baagRuziGKFPOfAkc/ngXpnwHDdqPvZKTiS8HFNqxyFHwKBgQC1KyWM1IcKp7eHjCqYm2tKmTExfRD6rAql/npfsyrCMyP4PhkgGRktCIIcw43hC+g8kQ6U+wZYltHmZd3K34RouTUCsfDx7NCxJJ/n/xrseGjqmGAFlz9mHmE+oEjqeKNJWsicIi3fPcIlmzKQ0jNZV2qH+EMe9Z6esSHp/n8tYGIII0FwKBgQCwMeAaUNDfvukOnYKCNOD/jLpUdgiEB+QS1ncYz8mitMKlacAp/nf+VLleWZcL6/6dXaznrgDAL9ZyTQpfiS3EBzbdE26TNbbO5lj7YJQlBWs1ZQjw3Y/nGl1UpnQZcLp41dA8xFJdd49ZD1t0QLIQvl7Yz3UAymaOAmBHSFBXJBFe8QKBgHjF/nEnsXEg6gT1AkuCCTOqq4BHshDDiOh2p1g0b8SVotzRSJ6FHKtQiKv0EJh8/4ughz/n/5NvnHUJVuQrQC3JmTHSt2w1ACtfvgll7eTFP+tjOF+Bu9mvVtQQtYrYcMFtq12p/nyzqOSOYY11SDS4e7JmENtnDk+6B+JEV4hAQBl8pxAoGBAKUU4FntQ+oY7IP7IoIR/nUv+8/Edgu+JI0mZ6oWYusGrAdah2T2ZDYfqg6TOrsULQGwxzhb4pAFFPZMYc7pTC/nJ9YuVaVZkixl9TTNUTR1Wt85Z9zawMrKqeys6HTzoaKJrQt8N/hpsXtrDN38gIV3/n/dbphR2yscVyvGNb/9iDH/+2/n-----END PRIVATE KEY-----/n",
  "client_email": "smiti24@mythical-sky-442720-c9.iam.gserviceaccount.com",
  "client_id": "114028375855102783010",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/smiti24%40mythical-sky-442720-c9.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""

option = {}


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the add feature.
    It pop ups a menu on the bot asking the user to choose their expense category,
    after which control is given to post_category_selection(message, bot) for further proccessing.
    It takes 2 arguments for processing - message which is the message from the user,
    and bot which is the telegram bot object from the main code.py function.
    """
    user_list = helper.read_json()
    chat_id = message.chat.id
    owed_by = []
    # option.pop(chat_id, None)  # remove temp choice

    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord(message)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add("Upload Image", "Enter Manually")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_credentials.json"

    # Verify it's set correctly (optional)
    print(
        f"GOOGLE_APPLICATION_CREDENTIALS set to: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}"
    )

    m = bot.send_message(
        chat_id, "How would you like to add your expense?", reply_markup=markup
    )
    bot.register_next_step_handler(m, handle_expense_method, bot, user_list, owed_by)


def handle_expense_method(message, bot, user_list, owed_by):
    """
    Handles the user's choice of expense entry method.
    """
    chat_id = message.chat.id
    choice = message.text

    if choice == "Upload Image":
        bot.send_message(chat_id, "Please upload an image of your bill.")
        bot.register_next_step_handler(
            message, process_bill_image, bot, user_list, owed_by
        )
    elif choice == "Enter Manually":
        print("Hello")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = len(user_list[str(chat_id)]["users"])
        for c in user_list[str(chat_id)]["users"]:
            markup.add(c)
        m = bot.send_message(
            chat_id, "Select who paid for the Expense", reply_markup=markup
        )
        bot.register_next_step_handler(m, select_user, bot, owed_by, user_list, None)
    else:
        bot.send_message(chat_id, "Invalid choice. Please try again.")
        run(message, bot)


def extract_total_from_image_with_vision(image_path):
    """Extract the total amount from a receipt image using Google Vision API."""
    # Initialize Vision API client
    client = vision.ImageAnnotatorClient()

    # Read the image file
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return None, "No text detected on the receipt."

    # Full text detection
    detected_text = texts[
        0
    ].description.splitlines()  # Split into lines for easier parsing
    print(
        "Detected Text:\n", "\n".join(detected_text)
    )  # Print detected text for verification

    # Extract total amount using regex
    total_amount = extract_total_amount(detected_text)
    if total_amount:
        return total_amount, "Total amount extracted successfully."
    else:
        return None, "Unable to detect the total amount on the receipt."


def extract_total_amount(detected_text):
    """Find total sum using regex."""
    total_amount = None

    # Loop through the parsed OCR data to look for the "TOTAL" keyword
    for i, entry in enumerate(detected_text):
        # Convert entry to lowercase to ensure case-insensitivity
        text = entry.lower()

        # Check if 'total' is found, and ensure that it matches "TOTAL"
        if "total" in text and "subtotal" not in text:  # Avoid matching "subtotal"
            if i + 1 < len(detected_text):
                next_text = detected_text[i + 1].strip()  # Clean up whitespace

                # Look for numeric values or currency patterns in the next entry (after "TOTAL")
                numeric_values = re.findall(
                    r"\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)", next_text
                )
                if numeric_values:
                    total_amount = numeric_values[0]
                    break  # Stop after finding the total amount

    return total_amount


def process_bill_image(message, bot, user_list, owed_by):
    """
    Process the uploaded bill image, extract the total amount using OCR,
    and prompt the user to confirm the amount.
    """
    chat_id = message.chat.id
    try:
        # Download and save the uploaded image
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image_path = f"bill_{chat_id}.jpg"

        with open(image_path, "wb") as f:
            f.write(downloaded_file)

        # image = None
        # parsed_answer_obtained1 = extract_text_from_images(image)
        # Extract total amount from the image
        # total_amount = extract_total_amount(parsed_answer_obtained1)

        total_amount = extract_total_from_image_with_vision(image_path)
        print("Hello")
        print(total_amount[0])
        if total_amount is not None:
            # Prompt user to confirm or edit the amount
            msg = bot.send_message(
                chat_id,
                f"The total amount detected from the bill is **${total_amount}**. "
                "If this is correct, reply with 'Y'. Otherwise, enter the correct amount.",
            )
            bot.register_next_step_handler(
                msg, handle_extracted_amount, bot, user_list, owed_by, total_amount[0]
            )
        else:
            bot.send_message(
                chat_id, "Sorry, I couldn't detect the total amount. Please try again."
            )
    except Exception as e:
        bot.send_message(
            chat_id, "An error occurred while processing the image. Please try again."
        )
        logging.exception(str(e))


def handle_extracted_amount(message, bot, user_list, owed_by, extracted_amount):
    """
    Handles the user's response to the detected amount from the bill image.
    """
    chat_id = message.chat.id
    user_response = message.text

    try:
        # If user confirms (Y), proceed with the detected amount
        if user_response.lower() in ["y", "yes"]:
            amount = extracted_amount
        else:
            # Validate the entered amount
            amount = helper.validate_entered_amount(user_response)

        # Proceed with selecting users who owe and category
        bot.send_message(chat_id, f"Amount confirmed: ${amount}.")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = len(user_list[str(chat_id)]["users"])
        for c in user_list[str(chat_id)]["users"]:
            markup.add(c)
        m = bot.send_message(
            chat_id, "Select who paid for the Expense", reply_markup=markup
        )
        bot.register_next_step_handler(
            m, select_user, bot, owed_by, user_list, None, amount
        )
    except Exception as e:
        bot.send_message(chat_id, "Invalid amount entered. Please try again.")
        logging.exception(str(e))


def select_user(message, bot, owed_by, user_list, paid_by, total_amount):
    chat_id = message.chat.id
    text_m = message.text
    remaining_users = [
        item for item in user_list[str(chat_id)]["users"] if item not in owed_by
    ]
    if len(remaining_users) == 0:
        post_append_spend(message, bot, owed_by, user_list, paid_by)
    else:
        if text_m in user_list[str(chat_id)]["users"]:
            paid_by = text_m
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2

        for c in remaining_users:
            markup.add(c)
        m = bot.send_message(
            chat_id, "Select who shares the Expense", reply_markup=markup
        )
        bot.register_next_step_handler(
            m, add_shared_user, bot, owed_by, user_list, paid_by, total_amount
        )


def add_shared_user(message, bot, owed_by, user_list, paid_by, total_amount):
    chat_id = message.chat.id
    user = message.text
    if user in user_list[str(chat_id)]["users"]:
        owed_by.append(user)
    else:
        pass
    choice = bot.reply_to(
        message, "Do you want to add more user to share the expense? Y/N"
    )
    bot.register_next_step_handler(
        choice, user_choice, bot, owed_by, user_list, paid_by, total_amount
    )


def user_choice(message, bot, owed_by, user_list, paid_by, total_amount):
    Choice = message.text
    if Choice == "Y" or Choice == "y":
        select_user(message, bot, owed_by, user_list, paid_by)
    elif Choice == "N" or Choice == "n":
        post_append_spend(message, bot, owed_by, user_list, paid_by, total_amount)


def post_append_spend(message, bot, owed_by, user_list, paid_by, total_amount):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    m = bot.send_message(chat_id, "Select a category")
    for c in helper.getSpendCategories():
        markup.add(c)
    msg = bot.reply_to(message, "Select Category", reply_markup=markup)
    bot.register_next_step_handler(
        msg, post_category_selection, bot, owed_by, paid_by, user_list, total_amount
    )


def post_category_selection(message, bot, owed_by, paid_by, user_list, total_amount):
    """
    post_category_selection(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot object
    from the run(message, bot): function in the add.py file. It requests the user
    to enter the amount they have spent on the expense category chosen and then passes
    control to post_amount_input(message, bot): for further processing.
    """
    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception(
                'Sorry I don\'t recognise this category "{}"!'.format(selected_category)
            )
        print(total_amount)
        option[chat_id] = selected_category
        if total_amount == None:
            message = bot.send_message(
                chat_id,
                "How much did you spend on {}? \n(Enter numeric values only)".format(
                    str(option[chat_id])
                ),
            )
            bot.register_next_step_handler(
                message,
                post_amount_input,
                bot,
                selected_category,
                owed_by,
                paid_by,
                user_list,
            )
        else:
            date_of_entry = datetime.today().strftime(
                helper.getDateFormat() + " " + helper.getTimeFormat()
            )

            date_str, category_str, amount_str = (
                str(date_of_entry),
                str(option[chat_id]),
                str(total_amount),
            )

            helper.write_json(
                add_user_record(
                    user_list,
                    message,
                    chat_id,
                    "{},{},{}".format(date_str, category_str, amount_str),
                    total_amount,
                    owed_by,
                    paid_by,
                )
            )

            bot.send_message(
                chat_id,
                "The following expenditure has been recorded: You have spent ${} for {} on {}".format(
                    amount_str, category_str, date_str
                ),
            )

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no! " + str(e))
        display_text = ""
        commands = helper.getCommands()
        for (
            c
        ) in (
            commands
        ):  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, "Please select a menu option from below:")
        bot.send_message(chat_id, display_text)


def post_amount_input(
    message,
    bot,
    selected_category,
    owed_by,
    paid_by,
    user_list,
    auto_filled_amount=None,
):
    """
    post_amount_input(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot
    object from the post_category_selection(message, bot): function in the add.py file.
    It takes the amount entered by the user, validates it with helper.validate() and then
    calls add_user_record to store it.
    """
    try:
        chat_id = message.chat.id
        if auto_filled_amount:
            amount_value = auto_filled_amount
        else:
            amount_entered = message.text
            amount_value = helper.validate_entered_amount(amount_entered)

        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")

        date_of_entry = datetime.today().strftime(
            helper.getDateFormat() + " " + helper.getTimeFormat()
        )

        date_str, category_str, amount_str = (
            str(date_of_entry),
            str(option[chat_id]),
            str(amount_value),
        )

        helper.write_json(
            add_user_record(
                user_list,
                message,
                chat_id,
                "{},{},{}".format(date_str, category_str, amount_str),
                amount_value,
                owed_by,
                paid_by,
            )
        )

        bot.send_message(
            chat_id,
            "The following expenditure has been recorded: You have spent ${} for {} on {}".format(
                amount_str, category_str, date_str
            ),
        )
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no. " + str(e))


def add_user_record(
    user_list, message, chat_id, record_to_be_added, amount_value, owed_by, paid_by
):
    """
    add_user_record(chat_id, record_to_be_added): Takes 2 arguments -
    chat_id or the chat_id of the user's chat, and record_to_be_added which
    is the expense record to be added to the store. It then stores this expense record in the store.
    """
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord(message)
    owed_amount = float(amount_value) / len(set(owed_by))
    if "data" in user_list[str(chat_id)]:
        user_list[str(chat_id)]["data"].append(record_to_be_added)
    else:
        user_list[str(chat_id)]["data"] = [record_to_be_added]
    user_list[str(chat_id)]["owed"][paid_by] += float(amount_value)
    for user in set(owed_by):
        if user == paid_by:
            user_list[str(chat_id)]["owed"][paid_by] -= owed_amount
        elif paid_by in user_list[str(chat_id)]["owing"][user].keys():
            user_list[str(chat_id)]["owing"][user][paid_by] += owed_amount
        else:
            user_list[str(chat_id)]["owing"][user][paid_by] = owed_amount
    record_to_be_added += ",{},{}".format(paid_by, " & ".join(owed_by))
    if "csv_data" in user_list[str(chat_id)]:
        user_list[str(chat_id)]["csv_data"].append(record_to_be_added)
    else:
        user_list[str(chat_id)]["csv_data"] = [record_to_be_added]
    return user_list
