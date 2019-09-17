<p align="center">
<img src="static/img/smokey_bot.jpg" height="150px">
  </p>

<h2 align="center"> Smokey Bot <img src="https://img.shields.io/website/https/evening-coast-69979.herokuapp.com?down_color=lightgrey&down_message=offline&label=bot&style=flat-square&up_color=blue&up_message=online">
<img src="http://hits.dwyl.io/udit-001/smokey-bot.svg" alt="Hit Count">
</h2>

<p align="center">
  A telegram bot that provides real-time worldwide air pollution data at your fingertips, made using <a href="https://python-telegram-bot.org/" rel="noopener noreferrer">python-telegram-bot</a> library.
</p>

## Description
This bot allows you to get real-time air quality data based on your geolocation and even lets you search for AQI data by providing city name and more. It provides AQI data for any place over world. It uses the data available from [World Air Qualitiy Index](https://waqi.info/).


## Installation
Install the required dependencies/libraries by running :

```bash
$ pip install -r requirements.txt
```

## Usage
To be able to run this bot, you will need to create a file named ``config.py`` in root directory and save a variable named `bot_token` and pass the token for your bot that you can obtain using [BotFather](https://t.me/BotFather).
Run using:

```bash
python bot.py
```
