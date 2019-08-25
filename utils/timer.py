import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def feedback_msg(bot, job):
    buttons = [[
        InlineKeyboardButton('Try inline search!',
                             switch_inline_query_current_chat=''), ],
               ]
    reply_markup = InlineKeyboardMarkup(buttons)

    bot.send_message(chat_id=job.context.effective_user.id,
                     text="Thanks for availing the services that I provide! 😃 Did you know you can also use this bot inline? \n\nShare how you feel about my services with my creator by using /feedback and rate me using /rate.", reply_markup=reply_markup)
    # TODO: Remove this print statement when you're done testing things out!
    print("Job executed at {0}".format(time.time()))
