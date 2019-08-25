from telegram import (InlineQueryResultArticle, InlineQueryResultLocation,
                      InputTextMessageContent)
from telegram.ext import InlineQueryHandler

from utils.aqi import get_details, search_place

from .strings import messages


def send_inline(bot, update):
    if update.inline_query is not None and update.inline_query.query == '':

        loc = update.inline_query.location
        lat = loc['latitude']
        long = loc['longitude']
        details = get_details(lat, long)

        msg = InputTextMessageContent(
            message_text=details[0], parse_mode="Markdown", disable_web_page_preview=True)

        guide = InputTextMessageContent(
            message_text=messages['masksAvailableMsg'], parse_mode="Markdown", disable_web_page_preview=True)

        results = [
            InlineQueryResultLocation(type='location', id=34, latitude=lat, longitude=long, title="Your Location's AQI : "+str(
                details[1]), input_message_content=msg, thumb_url="https://i.imgur.com/ZtiI8iQ.png"),

            InlineQueryResultArticle(
                type='article', id=254, title="Various masks you can consider...", input_message_content=guide, description="Gives you the list of masks you can buy.", thumb_url="https://i.imgur.com/ZeVCqXD.png")
        ]
        bot.answerInlineQuery(update.inline_query.id, results=results,
                              switch_pm_text="Pm me for guides and other info...", switch_pm_parameter="test")

    if update.inline_query is not None and update.inline_query.query:
        query = update.inline_query.query
        output = search_place(query)

        if output:
            lat = output[0]['lat']
            long = output[0]['long']
            name = output[0]['name']

            details = get_details(lat, long)

            msg = InputTextMessageContent(
                message_text=details[0], parse_mode="Markdown", disable_web_page_preview=True)

            response_list = [InlineQueryResultLocation(
                type='location', id=0, latitude=lat, longitude=long, title=name, input_message_content=msg)]

            bot.answerInlineQuery(update.inline_query.id, results=response_list,
                                  switch_pm_text="Pm me for guides and other info...", switch_pm_parameter="test")


def register(dp):
    dp.add_handler(InlineQueryHandler(send_inline))
