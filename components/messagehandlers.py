from telegram import (ChatAction, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardRemove)
from telegram.ext import BaseFilter, Filters, MessageHandler

import config
from utils.aqi import get_details
from utils.decorators import feedback_timer

from .analytics import track_button_in, track_button_out, track_message_out
from .strings import messages
from utils.classes import FeedbackData


class FilterFeedbackRec(BaseFilter):
    def filter(self, message):
        return 'Now send me your message so that I can forward it to my creator.' == message.reply_to_message.text


class FilterLocCancel(BaseFilter):
    def filter(self, message):
        return 'Cancel' == message.text


# Creating instances of filter classes
filter_feedbackRec = FilterFeedbackRec()
filter_locationcancel = FilterLocCancel()

feedbackDataOb = FeedbackData()

@feedback_timer
def send_masks_available(bot, update, user_data, job_queue):
    button = {
        'buttonID': 'sendMasksAvailable'
    }
    track_button_out(update, 'Different Masks Available', button)
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text=messages['masksAvailableMsg'],
                     disable_web_page_preview=True, parse_mode="Markdown", reply_to_message_id=update.message.message_id)
    track_message_out(update, messages['masksAvailableMsg'])


def feedback_received(bot, update):
    bot.forwardMessage(chat_id=config.dev_id, from_chat_id=update.message.chat_id,
                       message_id=update.message.message_id)
    feedbackDataOb.chatid = update.message.chat_id
    feedbackDataOb.messageid = update.message.message_id
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages['feedback_sent_msg'], reply_to_message_id=update.message.message_id)


@feedback_timer
def location_cancel(bot, update, user_data, job_queue):
    button = {
        'buttonId': 'noLocSend'
    }
    track_button_in(update, 'Cancel', button)
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages['privacy_msg'], parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
    track_message_out(update, messages['privacy_msg'])


@feedback_timer
def send_masks_guide(bot, update, user_data, job_queue):
    button = {
        'buttonId': 'sendMasksGuide'
    }
    track_button_in(update, 'Buying Guide', button)
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages['masksGuideMsg'], parse_mode="Markdown", reply_to_message_id=update.message.message_id)
    track_message_out(update, messages['masksGuideMsg'])


@feedback_timer
def location_received(bot, update, user_data, job_queue):
    button = {
        'buttonId': 'locSend'
    }
    track_button_in(update, 'Send my location 🗺️', button)
    lat = update.message.location['latitude']
    longt = update.message.location['longitude']
    result = get_details(lat, longt)
    message = result[0]
    aqi = result[1]
    pol = result[2]
    keyboard = [[InlineKeyboardButton(
        f"What is {pol.upper()}?", callback_data=f"{pol}")], ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text=message, disable_web_page_preview=True,
                     parse_mode="Markdown", reply_to_message_id=update.message.message_id, reply_markup=reply_markup)
    track_message_out(update, message)
    if aqi > 101:
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id,
                         text=messages['high_pollution_msg'], reply_markup=ReplyKeyboardRemove())
        track_message_out(update, messages['high_pollution_msg'])
        if pol in ['pm25', 'pm10']:
            bot.send_message(chat_id=update.message.chat_id,
                             text=messages[f"{pol}_mask"])
            track_message_out(update, messages[f"{pol}_mask"])


def register(dp):
    dp.add_handler(MessageHandler(
        Filters.location, location_received, pass_user_data=True, pass_job_queue=True))
    dp.add_handler(MessageHandler(filter_locationcancel,
                                  location_cancel, pass_user_data=True, pass_job_queue=True))
    dp.add_handler(MessageHandler(filter_feedbackRec, feedback_received))
