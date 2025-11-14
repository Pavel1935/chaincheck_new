from pages.bot_base_page import BotBasePage
import time
import re
from Constants import Constants


class AMLBotPage(BotBasePage):

    def click_language(self, langauge_button):
        msg = self.get_last_message()
        self.click(msg, langauge_button)

    def check_balance_value(self, balance_button):
        msg = self.get_last_message(limit=5)
        for btn in ["Balance", "Баланс"]:
            try:
                self.click(msg, btn)
                break
            except Exception:
                continue

        time.sleep(5)
        reply = self.get_last_message(limit=5)

        nums = re.findall(r"\d+", reply.text)
        return int(nums[0]) if nums else 0

    def check_wallet(self, address, network=""):
        self.send(address)
        time.sleep(1)

        msg = self.get_last_message(limit=5)
        self.click(msg, network)

        time.sleep(3)
        return self.get_last_message().text





