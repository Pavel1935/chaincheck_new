import asyncio
from telethon import TelegramClient

from Constants import Constants  # или твой правильный путь

async def main():
    client = TelegramClient("chainscheck_qa_bot", Constants.API_ID, Constants.API_HASH)
    await client.connect()
    authorized = await client.is_user_authorized()
    print("AUTHORIZED:", authorized)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
