class BotBasePage:
    def __init__(self, client, bot_username):
        self.client = client
        self.bot = bot_username

    # def send_massage(self, telegram_client): telegram_client.send_message(Constants.BOT_USERNAME, "address")
    def send(self, text: str):
        """Отправить сообщение боту"""
        return self.client.send_message(self.bot, text)


    # def click_bot(self, telegram_client): msg = telegram_client.get_messages(Constants.BOT_USERNAME, limit=1)[0]
    #     msg.click(text="")
    def ckick(self, msg, text: str):
        """Кликнуть на кнопку в боте"""
        msg.click(text=text)

    def get_last_message(self, limit=3):
        """Получить последнее сообщение"""
        return self.client.get_messages(self.bot, limit=limit)[0]

    