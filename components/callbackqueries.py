import json

from telegram import (ChatAction, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardRemove)
from telegram.ext import CallbackQueryHandler

from utils.aqi import get_details, search_place
from utils.decorators import feedback_timer

from .analytics import track_button_out
from .strings import guide, messages, pollutants


@feedback_timer
def guide_buttons(bot, update, user_data, job_queue):
    query = update.callback_query

    if query.data not in ['definition', 'effects', 'sources',
                          'high_risk', 'measures', 'dos', 'donts', 'send_guide_msg']:
        return

    buttons = {
        "definition": "What is Smog?",
        "effects": "How does it affect our body?",
        "sources": "What are its sources?",
        "high_risk": "Who are at a higher risk?",
        "measures": "Some precautionary measures?",
        "dos": "Do's ☑️",
        "donts": "Don'ts ❎",
        "back": "Back ⬅️",
    }

    guide_keyboard = [
        [InlineKeyboardButton(buttons['definition'],
                              callback_data='definition')],
        [InlineKeyboardButton(
            buttons['effects'], callback_data='effects')],
        [InlineKeyboardButton(buttons['sources'],
                              callback_data='sources')],
        [InlineKeyboardButton(buttons['high_risk'],
                              callback_data='high_risk')],
        [InlineKeyboardButton(
            buttons['measures'], callback_data='measures')]
    ]

    measures_keyboard = [
        [
            InlineKeyboardButton(buttons['dos'], callback_data='dos'),
            InlineKeyboardButton(buttons['donts'], callback_data="donts")
        ],
        [
            InlineKeyboardButton(
                buttons['back'], callback_data='send_guide_msg')
        ]
    ]

    main_page = InlineKeyboardMarkup(guide_keyboard)
    second_page = InlineKeyboardMarkup(measures_keyboard)

    if query.data in ['effects', 'sources', 'high_risk', 'definition']:
        bot.edit_message_text(text=guide[query.data], chat_id=query.message.chat_id,
                              message_id=query.message.message_id, parse_mode="Markdown", reply_markup=main_page)

    elif query.data == 'measures':
        bot.edit_message_text(text='There are certain dos and don\'ts that will help in reducing the ill effects of smog, click the buttons below!',
                              chat_id=query.message.chat_id, message_id=query.message.message_id,
                              parse_mode="Markdown", reply_markup=second_page)

    elif query.data in ['dos', 'donts', 'send_guide_msg']:

        if query.data == 'send_guide_msg':
            text = messages['send_guide_msg']
            reply_markup = main_page

        else:
            text = guide[query.data]
            reply_markup = second_page

        bot.edit_message_text(text=text, chat_id=query.message.chat_id, message_id=query.message.message_id,
                              parse_mode="Markdown", reply_markup=reply_markup, disable_web_page_preview=True)

    bot.answer_callback_query(callback_query_id=query.id)


@feedback_timer
def search_buttons(bot, update, user_data, job_queue):
    query = update.callback_query

    if query.data in ['definition', 'effects', 'sources', 'high_risk',
                      'measures', 'dos', 'donts', 'send_guide_msg', 'masks_guide_msg', 'masks_available_msg']:
        return

    callback_data = json.loads(query.data)
    if callback_data['correct_location']:
        long = query.message.venue.location.longitude
        lat = query.message.venue.location.latitude
        result = get_details(lat, long)
        message = result[0]
        aqi = result[1]
        pol = result[2]
        bot.edit_message_reply_markup(
            chat_id=query.message.chat_id, message_id=query.message.message_id)
        bot.send_chat_action(chat_id=query.message.chat_id,
                             action=ChatAction.TYPING)
        bot.send_message(
            text=message, chat_id=query.message.chat_id, parse_mode="Markdown",
            disable_web_page_preview=True)
        if aqi > 101:
            bot.send_chat_action(chat_id=query.message.chat_id,
                                 action=ChatAction.TYPING)
            bot.send_message(chat_id=query.message.chat_id,
                             text=messages['high_pollution_msg'], reply_markup=ReplyKeyboardRemove())
            if pol in ['pm25', 'pm10']:
                bot.send_message(chat_id=query.message.chat_id,
                                 text=messages[f"{pol}_mask"])
    else:
        venue_title = query.message.venue.title

        bot.delete_message(chat_id=query.message.chat_id,
                           message_id=query.message.message_id)

        output = search_place(venue_title)

        result_id = callback_data['result']
        if output:
            if result_id < len(output) - 1:
                result_id += 1

                place = output[result_id]

                lat = place['lat']
                long = place['long']

                keyboard = [
                    [
                        InlineKeyboardButton(
                            "Is this the correct location?", callback_data='Isthis?')
                    ],
                    [
                        InlineKeyboardButton("Yes",
                                             callback_data=json.dumps({'correct_location': True})),
                        InlineKeyboardButton(
                            "No", callback_data=json.dumps({'correct_location': False, 'result': result_id}))
                    ]
                ]

                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_chat_action(chat_id=query.message.chat_id,
                                     action=ChatAction.FIND_LOCATION)
                bot.sendVenue(chat_id=query.message.chat_id, latitude=lat, longitude=long, title=venue_title,
                              address=place['name'], reply_markup=reply_markup)

            else:
                bot.send_message(
                    text='Sorry, no more results found.', chat_id=query.message.chat_id)


@feedback_timer
def masks_buttons(bot, update, user_data, job_queue):
    query = update.callback_query

    if query.data not in ['masks_guide_msg', 'masks_available_msg']:
        return

    custom_keyboard = [
        [
            InlineKeyboardButton(
                'Buying Guide', callback_data='masks_guide_msg')
        ],
        [
            InlineKeyboardButton(
                'Different Masks Availalble', callback_data='masks_available_msg')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(custom_keyboard)

    bot.edit_message_text(text=messages[query.data], chat_id=query.message.chat_id,
                          message_id=query.message.message_id, reply_markup=reply_markup,
                          parse_mode="Markdown", disable_web_page_preview=True)
    bot.answer_callback_query(callback_query_id=query.id)


@feedback_timer
def pollutants_buttons(bot, update, user_data, job_queue):
    query = update.callback_query
    if query.data not in ['pm10', 'pm25', 'o3', 'no2', 'so2', 'co']:
        return
    bot.edit_message_text(
        text=query.message.text, chat_id=query.message.chat_id, message_id=query.message.message_id)
    bot.send_message(
        text=pollutants[query.data], chat_id=query.message.chat_id, reply_markup=ReplyKeyboardRemove())


def register(dp):
    dp.add_handler(CallbackQueryHandler(
        guide_buttons, pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CallbackQueryHandler(
        masks_buttons, pass_user_data=True, pass_job_queue=True), group=1)
    dp.add_handler(CallbackQueryHandler(
        pollutants_buttons, pass_user_data=True, pass_job_queue=True), group=2)
    dp.add_handler(CallbackQueryHandler(
        search_buttons, pass_user_data=True, pass_job_queue=True), group=3)
