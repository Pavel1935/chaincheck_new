import time
BOT_USERNAME = "chainscheck_bot"


class TestChainsCheckBotSync:
    """"Проверяет, что кнопка 'Баланс' работает и бот отвечает"""
    def test_balance_button(self, telegram_client):
        msg = telegram_client.get_messages(BOT_USERNAME, limit=1)[0]
        msg.click(text="Баланс")  # Пробуем нажать “Баланс”

        time.sleep(3)
        reply = telegram_client.get_messages(BOT_USERNAME, limit=1)[0]
        text = reply.text.strip()

        print(f"\nОтвет бота:\n{text}")  #Делаем assert по тексту из ответа
        assert "провер" in text.lower() or "остал" in text.lower(), "Ответ не похож на баланс"

    def test_language_button(self, telegram_client):
        msg = telegram_client.get_messages(BOT_USERNAME, limit=3)[0]
        try:  #Пробуем нажать “Язык” или “Language”
            msg.click(text="Язык")
            print("✅ Нажата кнопка: Язык")
        except Exception:
            msg.click(text="Language")
            print("✅ Нажата кнопка: Language")

        msg = telegram_client.get_messages(BOT_USERNAME, limit=3)[0]
        msg.click(text="RU (русский)") #Выбрать в меню "русский"

        time.sleep(3)
        reply = telegram_client.get_messages(BOT_USERNAME, limit=3)[0]
        text = reply.text.strip()

        print(f"\nОтвет бота:\n{text}")  #Делаем assert по тексту из ответа
        assert "Готов" in text.lower() or "кошелек" in text.lower()

    def test_get_score(self, telegram_client):
        # telegram_client.get_messages(BOT_USERNAME, limit=3)[0]
        telegram_client.send_message(BOT_USERNAME, "0x36b12020B741A722Ca21a0ef2B9E8977f8715b4f")

        msg = telegram_client.get_messages(BOT_USERNAME, limit=5)[0]
        msg.click(text="BSC")

        time.sleep(3)
        reply = telegram_client.get_messages(BOT_USERNAME, limit=3)[0]

        text = reply.text.strip()

        print(f"\nОтвет бота:\n{text}")
        assert "Report" in text.lower() or "risk" in text.lower()

    def test_error_invalid_address(self, telegram_client):
        telegram_client.send_message(BOT_USERNAME, "0SpartskMoscowx36b12020B741A722Ca21a0ef2B9E8977f8715b4f")
        time.sleep(3)

        reply = telegram_client.get_messages(BOT_USERNAME, limit=3)[0]
        text = reply.text.strip()
        print(f"\nОтвет бота:\n{text}")

        assert "omething" in text.lower() or "то-то" in text.lower()

