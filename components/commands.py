import json
import os

import requests
from telegram import (ChatAction, ForceReply, InlineKeyboardButton,
                      InlineKeyboardMarkup, KeyboardButton,
                      ReplyKeyboardMarkup)
from telegram.ext import CommandHandler

import config
from utils.decorators import feedback_timer, feedback_timer_search

from .analytics import track_button_out, track_message_inc, track_message_out
from .strings import messages
from utils.classes import FeedbackData

GEO_TOKEN = os.environ.get('geo_token', config.geo_token)
AQI_TOKEN = os.environ.get('aqi_token', config.aqi_token)


feedbackDataOb = FeedbackData()


@feedback_timer
def send_start(bot, update, user_data, job_queue):
    track_message_inc(update)
    username = update.message.from_user.first_name
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    track_message_out(update, 'Hi '+username+messages['welcome_msg'])
    bot.send_message(chat_id=update.message.chat_id, text='Hi '+username +
                     messages['welcome_msg'], reply_to_message_id=update.message.message_id)


@feedback_timer
def send_rate(bot, update, user_data, job_queue):
    track_message_inc(update)
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages['rate_msg'], reply_to_message_id=update.message.message_id,
                     disable_web_page_preview=True)
    track_message_out(update, messages['rate_msg'])


@feedback_timer
def send_help(bot, update, user_data, job_queue):
    track_message_inc(update)
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages['help_msg'], reply_to_message_id=update.message.message_id)
    track_message_out(update, messages['help_msg'])


@feedback_timer
def send_masks(bot, update, user_data, job_queue):
    track_message_inc(update)

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

    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text=messages['masks'], parse_mode="Markdown",
                     disable_web_page_preview=True, reply_to_message_id=update.message.message_id,
                     reply_markup=reply_markup)
    buttons = [
        {
            'id': 'button1',
            'label': 'Buying Guide',
            'value': 'send_masks_guide'
        },
        {
            'id': 'button2',
            'label': 'Different Masks Available',
            'value': 'send_masks_available'
        }
    ]
    track_button_out(update, messages['masks'], buttons)


@feedback_timer
def send_guide(bot, update, user_data, job_queue):
    track_message_inc(update)

    buttons = {
        'definition': "What is Smog?",
        'effects': "How does it affect our body?",
        'sources': "What are its sources?",
        'high_risk': "Who are at a higher risk?",
        "measures": "Some precautionary measures?"
    }

    keyboard = [
        [InlineKeyboardButton(buttons['definition'],
                              callback_data='definition')],
        [InlineKeyboardButton(buttons['effects'], callback_data='effects')],
        [InlineKeyboardButton(buttons['sources'], callback_data='sources')],
        [InlineKeyboardButton(buttons['high_risk'],
                              callback_data='high_risk')],
        [InlineKeyboardButton(buttons['measures'], callback_data='measures')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=update.message.chat_id, text="I have prepared a small guide 📖, to help you survive through the pollution. Take a look 👀 at it!",
                     reply_to_message_id=update.message.message_id, reply_markup=reply_markup)

    buttons = [
        {
            'id': 'button1',
            'label': 'What is smog?',
            'value': 'sendDefn'
        },
        {
            'id': 'button2',
            'label': 'How does it affect our body?',
            'value': 'sendEffects'
        },
        {
            'id': 'button3',
            'label': 'What are its sources?',
            'value': 'sendSources'
        },
        {
            'id': 'button4',
            'label': 'Who are at a higher risk?',
            'value': 'sendHighRisk'
        },
        {
            'id': 'button5',
            'label': 'Some precautionary measures?',
            'value': 'sendMeasures'
        }]
    track_button_out(update, messages['send_guide_msg'], buttons)


def feedback_reply_send(bot, update, args):
    if not args:
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.TYPING)
        bot.send_message(chat_id='378885344', text="You haven't sent me any message, try again!",
                         reply_to_message_id=update.message.message_id)
    else:
        msg = ' '.join(args)
        bot.send_message(chat_id='378885344', text="Reply Sent!",
                         reply_to_message_id=update.message.message_id)
        bot.send_message(chat_id=feedbackDataOb.chat_id,
                         reply_to_message_id=feedbackDataOb.message_id, text=msg)


@feedback_timer
def air_quality(bot, update, user_data, job_queue):
    track_message_inc(update)
    location_keyboard = KeyboardButton(
        text="Send my location 🗺️", request_location=True)
    cancel_button = KeyboardButton(text="Cancel")
    custom_keyboard = [[location_keyboard, cancel_button]]
    reply_markup = ReplyKeyboardMarkup(
        custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    buttons = [{
        'id': 'button1',
        'label': 'Send my location 🗺️',
        'value': 'locSend'
    },
        {
        'id': 'button2',
        'label': 'Cancel',
        'value': 'noLocSend'
    }]
    track_button_out(update, messages['location_request_msg'], buttons)

    bot.send_message(chat_id=update.message.chat_id,
                     text=messages['location_request_msg'], reply_markup=reply_markup,
                     reply_to_message_id=update.message.message_id)


@feedback_timer_search
def search_location(bot, update, args, user_data, job_queue):
    track_message_inc(update)

    if not args:
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id,
                         text=messages['search_fail'], parse_mode='Markdown', reply_to_message_id=update.message.message_id)
        track_message_out(update, messages['search_fail'])

    else:
        endpoint = f"https://api.waqi.info/search/?keyword={' '.join(args)}&token={AQI_TOKEN}"

        r = requests.get(endpoint)
        result = r.json()

        if result['status'] == 'ok' and len(result['data']) > 0:

            place = result['data'][0]

            lat = place["station"]["geo"][0]
            long = place["station"]["geo"][1]

            keyboard = [
                [InlineKeyboardButton(
                    "Is this the correct location?", callback_data='Isthis?')],
                [
                    InlineKeyboardButton("Yes",
                                         callback_data=json.dumps({'correct_location': True})),
                    InlineKeyboardButton(
                        "No", callback_data=json.dumps({'correct_location': False, 'result': 0}))
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_chat_action(chat_id=update.message.chat_id,
                                 action=ChatAction.FIND_LOCATION)
            bot.sendVenue(chat_id=update.message.chat_id, latitude=lat, longitude=long, title=' '.join(args).title(),
                          address=place['station']['name'], reply_markup=reply_markup, reply_to_message_id=update.message.message_id)


def send_feedback(bot, update):
    track_message_inc(update)
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages['accept_feedback_msg'], reply_to_message_id=update.message.message_id,
                     reply_markup=ForceReply())
    track_message_out(update, messages['accept_feedback_msg'])


def register(dp):
    dp.add_handler(CommandHandler('start', send_start,
                                  pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler('quality', air_quality,
                                  pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler('feedback', send_feedback))
    dp.add_handler(CommandHandler('guide', send_guide,
                                  pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler('masks', send_masks,
                                  pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler('search', search_location,
                                  pass_args=True, pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler('help', send_help,
                                  pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler(
        'reply', feedback_reply_send, pass_args=True))
    dp.add_handler(CommandHandler('rate', send_rate,
                                  pass_user_data=True, pass_job_queue=True))
