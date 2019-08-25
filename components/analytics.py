import json
import os

import requests

import config

TRACK_TOKEN = os.environ.get("track_token", config.track_token)


def track_message_inc(update):
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey={0}'.format(
        TRACK_TOKEN)

    data = {
        'text': update.message.text,
        'userId': str(update.message.from_user.id),
        'conversationId': str(update.message.chat.id)
    }

    requests.post(url, data=json.dumps(data), headers={
                      'Content-type': 'application/json'})


def track_message_out(update, text):
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=outgoing&apiKey={0}'.format(
        TRACK_TOKEN)

    data = {
        'text': text,
        'userId': str(update.message.from_user.id),
        'conversationId': str(update.message.chat.id)
    }

    requests.post(url, data=json.dumps(data), headers={
                      'Content-type': 'application/json'})


def track_button_out(update, text, buttons):
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=outgoing&apiKey={0}'.format(
        TRACK_TOKEN)

    data = {
        'text': text,
        'userId': str(update.message.from_user.id),
        'conversationId': str(update.message.chat.id),
        'buttons': buttons
    }

    requests.post(url, data=json.dumps(data), headers={
                      'Content-type': 'application/json'})


def track_button_in(update, text, button):
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey={0}'.format(
        TRACK_TOKEN)

    data = {
        'text': text,
        'userId': str(update.message.from_user.id),
        'conversationId': str(update.message.chat.id),
        'buttonClick': button
    }

    requests.post(url, data=json.dumps(data), headers={
                      'Content-type': 'application/json'})


def inline_button_in(query, text, button):
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey={0}'.format(
        TRACK_TOKEN)

    data = {
        'text': text,
        'userId': str(query.from_user.id),
        'conversationId': str(query.message.chat.id),
        'buttonClick': button
    }

    requests.post(url, data=json.dumps(data), headers={
                      'Content-type': 'application/json'})
