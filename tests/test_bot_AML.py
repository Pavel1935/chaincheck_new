import time

BOT_USERNAME = "chainscheck_bot"


class TestChainsCheckBotSync:
    """"Проверяет, что кнопка 'Баланс' работает и бот отвечает"""
    def test_balance_button(self, telegram_client):
        msg = telegram_client.get_messages(BOT_USERNAME, limit=1)[0]
        msg.click(text="Баланс")

        time.sleep(3)
        reply = telegram_client.get_messages(BOT_USERNAME, limit=1)[0]
        text = reply.text.strip()

        print(f"\nОтвет бота:\n{text}")
        assert "провер" in text.lower() or "остал" in text.lower(), "Ответ не похож на баланс"

    def test_language_button(self, telegram_client):
        msg = telegram_client.get_messages(BOT_USERNAME, limit=1)[0]
        msg.click(text="Язык") #Выбрать в меню "Язык"
        msg.click(text="EN(английский)") #Выбрать в меню "английский"

        msg = telegram_client.send_message(BOT_USERNAME, "0x36b12020B741A722Ca21a0ef2B9E8977f8715b4f")

        msg = telegram_client.get_messages(BOT_USERNAME, limit=1)[0]
        msg.click(text="BSC")

        time.sleep(3)
        reply = telegram_client.get_messages(BOT_USERNAME, limit=1)[0]

        text = reply.text.strip()

        print(f"\nОтвет бота:\n{text}")
        assert "Report" in text.lower() or "risk" in text.lower()
