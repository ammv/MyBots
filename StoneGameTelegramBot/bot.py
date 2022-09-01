'''
Description: Hello! You can play in **Stone Game**
/start - [["Play with computer"]|["Play with user"]]

"Play with computer" -> "Input count of stones: "
'''
import asyncio
import configparser

from aiogram import Bot

def get_api_token():
    config = configparser.ConfigParser()
    config.read('bot.ini')
    return config['tg_bot']['token']

API_TOKEN = get_api_token()
    
BOT = Bot(token=API_TOKEN, parse_mode='MarkdownV2')