<p align="center">
<img src="static/img/smokey_bot.jpg" height="150px">
  </p>

<h2 align="center"> Smokey Bot <img src="https://img.shields.io/website/https/evening-coast-69979.herokuapp.com?down_color=lightgrey&down_message=offline&label=bot&style=flat-square&up_color=blue&up_message=online">
<a href="https://www.buymeacoffee.com/idiomprog"><img src="https://img.shields.io/badge/Donate-Buy%20Me%20a%20Coffee-orange?style=flat-square&logo=buy+me+a+coffee" alt="Donate"></a>
</h2>

<p align="center">
  A telegram bot that provides real-time worldwide air pollution data at your fingertips, made using <a href="https://python-telegram-bot.org/" rel="noopener noreferrer">python-telegram-bot</a> library.
</p>

## Description
This bot allows you to get real-time air quality data based on your geolocation and even lets you search for AQI data by providing city name and more. It provides AQI data for any place over world. It uses the data available from [World Air Qualitiy Index](https://waqi.info/).

## Features
- Check air quality for any location worldwide
- Get detailed pollutant information (PM2.5, PM10, CO, NO2, SO2, O3)
- Learn about air pollution and protection measures
- Find recommended anti-pollution masks
- Use inline mode in any chat for quick checks

## Commands
- `/start` - Start the bot and get welcome message
- `/quality` - Check Air Quality Index of your current location
- `/search <city>` - Check Air Quality Index of any city
- `/guide` - Get detailed information about smog and how to tackle it
- `/masks` - View information about anti-pollution masks and buying guide
- `/help` - Display list of available commands
- `/feedback` - Send feedback to the bot creator
- `/rate` - Rate the bot on Bot Store

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
