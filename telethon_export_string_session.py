from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from Constants import Constants

with TelegramClient(StringSession(), Constants.API_ID, Constants.API_HASH) as client:
    print("TG_STRING_SESSION=" + client.session.save())

