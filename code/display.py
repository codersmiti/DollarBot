import time
import helper
import graphing
import logging
from telebot import types

from datetime import datetime
from collections import defaultdict

# === Documentation of display.py ===


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot
    which is the telegram bot object from the main code.py function.
    """
    user_list=helper.read_json()
    print('###',user_list)
    chat_id = message.chat.id
    print(chat_id)
    history = helper.getUserHistory(chat_id)
    if history is None:
        bot.send_message(
            chat_id, "Oops! Looks like you do not have any spending records!"
        )
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Display all expenses")
        markup.add("Display owings")
        m = bot.send_message(chat_id, "Select what to display",reply_markup=markup)
        bot.register_next_step_handler(m, display_choice, bot,user_list,chat_id)


def display_choice(message,bot,user_list,chat_id):
    chat_id = message.chat.id
    choice = message.text
    if choice == 'Display all expenses':
        display_expenses(message,bot)
    elif choice =='Display owings':
         display_owings(message,bot,user_list,chat_id)
    else:
        m = bot.send_message(chat_id, "Select correct choice")
        bot.register_next_step_handler(m, run, bot)

def display_owings(message,bot,user_list,chat_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = len(user_list[str(chat_id)]["users"])
        for c in user_list[str(chat_id)]["users"]:
                markup.add(c)
        m = bot.send_message(chat_id, "Select user who's owings you want to display",reply_markup=markup)
        bot.register_next_step_handler(m, select_user, bot,user_list,chat_id)

def select_user(message,bot,user_list,chat_id):
    chat_id = message.chat.id
    user = message.text
    owing_dictionary = helper.calculate_owing(user_list,chat_id)
    final_string = ''
    for owed in owing_dictionary[user]["owes"]:
            final_string+=str("\n "+owed)
    for owing in owing_dictionary[user]["owing"]:
            final_string+=str("\n "+owing)
    if final_string == '':
        final_string = str(user)+' owes or is owed nothing'
    m = bot.send_message(chat_id, final_string)

def display_expenses(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for mode in helper.getSpendDisplayOptions():
        markup.add(mode)
    # markup.add('Day', 'Month')
    msg = bot.reply_to(
        message,
        "Please select a category to see the total expense",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, display_total, bot)

def display_total(message, bot):
    """
    display_total(message, bot): It takes 2 arguments for processing - message which is
    the message from the user, and bot which is the telegram bot object from the
    run(message, bot): function in the same file. This function loads the user's data using
    the helper file's getUserHistory(chat_id) method. After this, depending on the option user
    has chosen on the UI, it calls the calculate_spendings(queryResult): to process the queried
    data to return to the user after which it finally passes the data to the UI for the user to view.
    """
    try:
        chat_id = message.chat.id
        DayWeekMonth = message.text

        if DayWeekMonth not in helper.getSpendDisplayOptions():
            raise Exception(
                'Sorry I can\'t show spendings for "{}"!'.format(DayWeekMonth)
            )

        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")

        bot.send_message(chat_id, "Hold on! Calculating...")
        # show the bot "typing" (max. 5 secs)
        bot.send_chat_action(chat_id, "typing")
        time.sleep(0.5)

        total_text = ""

        if DayWeekMonth == "Day":
            query = datetime.now().today().strftime(helper.getDateFormat())
            # query all that contains today's date
            queryResult = [
                value for index, value in enumerate(history) if str(query) in value
            ]
        elif DayWeekMonth == "Month":
            query = datetime.now().today().strftime(helper.getMonthFormat())
            # query all that contains today's date
            queryResult = [
                value for index, value in enumerate(history) if str(query) in value
            ]
        total_text = calculate_spendings(queryResult)
        print("###########",total_text)
        monthly_budget = helper.getCategoryBudget(chat_id)
        if monthly_budget == None:
            message = "Looks like you have not entered any category-wise budget yet. Please enter your budget and then try to display the expenses."
            bot.send_message(chat_id, message)

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
        else:
            print("Print Total Spending", total_text)
            print("Print monthly budget", monthly_budget)

            spending_text = ""
            if len(total_text) == 0:
                spending_text = "You have no spendings for {}!".format(DayWeekMonth)
                bot.send_message(chat_id, spending_text)
            else:
                spending_text = "Here are your total spendings {}:\nCATEGORIES,AMOUNT \n----------------------\n{}".format(
                    DayWeekMonth.lower(), total_text
                )
                print("hello")
                bot.send_message(chat_id, "Please select a visualization option:")
                display_visualization_options(message, bot, queryResult, DayWeekMonth)
                # os.remove('expenditure.png')
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))

def display_visualization_options(message, bot, queryResult, DayWeekMonth):
    """
    Display visualization options for the user.
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = ["Pie Chart", "Bar Graph with Budget", "Bar Graph without Budget","Monthly Comparisions(Bar Graph)","Monthly Comparisions(Line Chart)"]
    for option in options:
        markup.add(option)

    msg = bot.reply_to(
        message,
        "Choose how you want to visualize your spending:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(
        msg, generate_visualization, bot, queryResult, DayWeekMonth
    )

def generate_visualization(message, bot, queryResult, DayWeekMonth):
    """
    Generate the requested visualization and send it to the user.
    """
    chat_id = message.chat.id
    visualization_type = message.text
    
    
    history = helper.getUserHistory(chat_id)
    if history is None:
        raise Exception("Oops! Looks like you do not have any spending records!")

    try:
        if visualization_type not in [
            "Pie Chart",
            "Bar Graph with Budget",
            "Bar Graph without Budget",
            "Monthly Comparisions(Bar Graph)",
            "Monthly Comparisions(Line Chart)",
        ]:
            bot.send_message(
                chat_id, "Invalid option selected. Please try again."
            )
            return

        total_text = calculate_spendings(queryResult)
        spending_dict = {
            cat.split(" $")[0]: float(cat.split(" $")[1])
            for cat in total_text.strip().split("\n")
        }

        monthly_spendings = calculate_monthly_spendings(history)
        months, spending_values = prepare_monthly_data(monthly_spendings)
        
        # Handle visualization types
        if visualization_type == "Pie Chart":
            graphing.visualize_pie_chart(spending_dict)
        elif visualization_type == "Bar Graph with Budget":
            monthly_budget = helper.getCategoryBudget(chat_id)
            if monthly_budget is None:
                bot.send_message(
                    chat_id,
                    "You haven't entered a category-wise budget. Please update your budget and try again.",
                )
                return
            graphing.visualize_bar_with_budget(spending_dict, monthly_budget)
        elif visualization_type == "Bar Graph without Budget":
            graphing.visualize_bar_without_budget(spending_dict)

        elif visualization_type == "Monthly Comparisions(Bar Graph)":
            graphing.visualize_bar_graph(months, spending_values)
            
        elif visualization_type == "Monthly Comparisions(Line Chart)":
            graphing.visualize_line_chart(months, spending_values) 
        # Send the generated visualization
        bot.send_photo(chat_id, photo=open("expenditure.png", "rb"))
        #os.remove("expenditure.png")

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))
from datetime import datetime
from collections import defaultdict

def calculate_monthly_spendings(queryResult):
    """
    Groups expenses by month (and year) and calculates total spendings per month.
    queryResult: List of expense records (e.g., ['21-Nov-2024,Food,100.0', ...])
    """
    monthly_spendings = defaultdict(float)  # Default dictionary to accumulate totals by month

    for row in queryResult:
        # Example row format: '21-Nov-2024,Food,100.0'
        date_str, category, amount = row.split(",")
        date = datetime.strptime(date_str, "%d-%b-%Y %H:%M")  # Parse date and time
  
        month_year = date.strftime("%b-%Y")  # Format as 'Nov-2024'
        
        # Accumulate total spending for each month
        monthly_spendings[month_year] += float(amount)

    return monthly_spendings

def prepare_monthly_data(monthly_spendings):
    """
    Prepare the data for plotting by extracting months and total spending amounts.
    """
    months = list(monthly_spendings.keys())  # List of months (e.g., 'Nov-2024', 'Dec-2024')
    spending_values = list(monthly_spendings.values())  # Corresponding spending values
    
    return months, spending_values


def calculate_spendings(queryResult):
    """
    calculate_spendings(queryResult): Takes 1 argument for processing - queryResult
    which is the query result from the display total function in the same file.
    It parses the query result and turns it into a form suitable for display on the UI by the user.
    """
    
    total_dict = {}
    print("!!!!!!",queryResult)
    for row in queryResult:
        # date,cat,money
        s = row.split(",")
        # cat
        cat = s[1]
        if cat in total_dict:
            # round up to 2 decimal
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])
    total_text = ""
    for key, value in total_dict.items():
        total_text += str(key) + " $" + str(value) + "\n"
    return total_text
