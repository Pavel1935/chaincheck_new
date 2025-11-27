from telethon import TelegramClient
from Constants import Constants  # если так называется твой файл
from pathlib import Path

SESSION_PATH = str(Path(__file__).parent / "chainscheck_qa_bot.session")

client = TelegramClient(
    SESSION_PATH,
    Constants.API_ID,
    Constants.API_HASH
)

client.start(phone=Constants.PHONE_NUMBER)

print("SESSION CREATED:", SESSION_PATH)
client.disconnect()
