import helper
from telebot import types
import logging
import budget_view
import budget_update
import budget_delete


def run(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getBudgetOptions()
    markup.row_width = 2
    for c in options.values():
        markup.add(c)
    msg = bot.reply_to(message, "Select Operation", reply_markup=markup)
    bot.register_next_step_handler(msg, post_operation_selection, bot)


def post_operation_selection(message, bot):
    try:
        chat_id = message.chat.id
        user_list = helper.read_json()
        op = message.text
        options = helper.getBudgetOptions()

        if op not in options.values():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception('Sorry I don\'t recognise this operation "{}"!'.format(op))
        if str(chat_id) not in user_list:
            user_list[str(chat_id)] = helper.createNewUserRecord(message)
        if op == options["add"]:
            budget_update.run(message, bot)
        if op == options["update"]:
            budget_update.run(message, bot)
        elif op == options["view"]:
            budget_view.run(message, bot)
        elif op == options["delete"]:
            budget_delete.run(message, bot)

        helper.write_json(user_list)

    except Exception as e:
        helper.throw_exception(e, message, bot, logging)
