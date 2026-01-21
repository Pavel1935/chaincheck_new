from telethon.sync import TelegramClient
from pathlib import Path
from Constants import Constants  # поправь путь, если нужно

SESSION_PATH = str(Path(__file__).parent / "chainscheck_qa_bot")

client = TelegramClient(
    SESSION_PATH,
    Constants.API_ID,
    Constants.API_HASH
)

client.start(phone=Constants.PHONE_NUMBER)

print("SESSION CREATED AND AUTHORIZED:", SESSION_PATH)
client.disconnect()

