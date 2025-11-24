import time
import pytest
import allure

BOT_USERNAME = "chainscheck_bot"


class TestChainsCheckBotSync:
    @pytest.mark.smoke
    @pytest.mark.bot
    @allure.step('Проверка получения баланса')
    def test_balance_button(self, telegram_client):
        msgs = telegram_client.get_messages(BOT_USERNAME, limit=5)
        telegram_client.send_message(BOT_USERNAME, "🔙 Назад")

        keyboard_buttons = []
        for msg in msgs:
            if msg.reply_markup and hasattr(msg.reply_markup, "rows"):
                for row in msg.reply_markup.rows:
                    for btn in row.buttons:
                        keyboard_buttons.append(btn.text)

        balance_btn = next(
            (b for b in keyboard_buttons if "balance" in b.lower() or "баланс" in b.lower()),
            None
        )

        assert balance_btn, "Кнопка Баланс не найдена!"

        telegram_client.send_message(BOT_USERNAME, balance_btn)

        time.sleep(3)
        reply = telegram_client.get_messages(BOT_USERNAME, limit=1)[0]
        text = reply.text.strip()
        print(text)

        assert "проверк" in text.lower() or "have" in text.lower(), "Ответ не похож на баланс"

    def test_language_button(self, telegram_client):
        msgs = telegram_client.get_messages(BOT_USERNAME, limit=5)

        # keyboard_buttons = []
        # for msg in msgs:
        #     if msg.reply_markup and hasattr(msg.reply_markup, "rows"):
        #         for row in msg.reply_markup.rows:
        #             for btn in row.buttons:
        #                 keyboard_buttons.append(btn.text)
        #
        # language_btn = next(
        #     (b for b in keyboard_buttons if "language" in b.lower() or "язык" in b.lower()),
        #     None
        # )
        telegram_client.send_message(BOT_USERNAME, "🌐 Язык")
        telegram_client.send_message(BOT_USERNAME, "🌐 Language")
        telegram_client.send_message(BOT_USERNAME, "RU (русский)")

        time.sleep(3)
        reply = telegram_client.get_messages(BOT_USERNAME, limit=3)[0]
        text = reply.text.strip()

        print(f"\nОтвет бота:\n{text}")
        assert "wallet" in text.lower() or "кошелек" in text.lower() #Делаем assert по тексту из ответа

    @pytest.mark.smoke
    @pytest.mark.bot
    @allure.step('Позитивная проверка получения оценик риска')
    def test_get_score(self, telegram_client):
        telegram_client.send_message(BOT_USERNAME, "0x36b12020B741A722Ca21a0ef2B9E8977f8715b4f") #Вводим адрес валидный

        telegram_client.get_messages(BOT_USERNAME, limit=5)
        telegram_client.send_message(BOT_USERNAME, "BSC")

        time.sleep(3)
        reply = telegram_client.get_messages(BOT_USERNAME, limit=3)[0]
        text = reply.text.strip()

        print(f"\nОтвет бота:\n{text}")
        assert "Report" in text.lower() or "отчет" in text.lower() #Делаем assert по тексту из ответа

    def test_error_invalid_address(self, telegram_client):
        telegram_client.send_message(BOT_USERNAME, "0SpartskMoscowx36b12020B741A722Ca21a0ef2B9E8977f8715b4f")
        time.sleep(3) #Вводим адрес невалидный

        reply = telegram_client.get_messages(BOT_USERNAME, limit=3)[0]
        text = reply.text.strip()
        print(f"\nОтвет бота:\n{text}")

        assert "omething" in text.lower() or "то-то" in text.lower()  #Делаем assert по тексту из ответа
