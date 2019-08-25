import logging

from telegram.ext import Updater

import config
from components import register

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=config.bot_token)

register(updater.dispatcher)

updater.start_polling(config.polling_interval)

updater.idle()
