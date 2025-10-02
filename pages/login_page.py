import logging
from Constants import Constants
from pages.base_page import BasePage
from playwright.sync_api import expect
from locators.login_locators import LoginLocators

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    def enter_wallet_address(self, address: str):
        self.page.locator(LoginLocators.WALLET_ADDRESS_INPUT).fill(address)
        self.page.locator(LoginLocators.CHECK_FOR_FREE_BUTTON).click()

    def enter_email(self, email: str):
        # self.page.on("response", self._log_auth_response)
        self.page.locator(LoginLocators.ENTER_EMAIL_INPUT).fill(email)
        self.page.locator(LoginLocators.LOG_IN_BUTTON).click()

    def enter_code(self, code: str):
        self.fill_code_by_indexed_inputs(LoginLocators.CODE_INPUTS, code)

    from playwright.sync_api import expect

    def click_check_for_free_button(self):
        button_check_for_free = self.page.locator("#secCheck").get_by_role("button", name="Check for Free")
        expect(button_check_for_free).to_be_visible(timeout=10000)
        expect(button_check_for_free).to_be_enabled(timeout=10000)
        button_check_for_free.click()

    def check_final_result(self):
        # ищем кнопку "Check for Free"
        button_check = self.page.locator("#secCheck").get_by_role("button", name="Check for Free")
        # ищем кнопку "New check"
        button_new = self.page.locator("#secCheck").get_by_role("button", name="New check")

        # если видна кнопка "Check for Free"
        if button_check.count() > 0 and button_check.is_visible():
            expect(button_check).to_be_enabled(timeout=10000)
            button_check.click()
        # иначе жмём "New check"
        elif button_new.count() > 0 and button_new.is_visible():
            expect(button_new).to_be_enabled(timeout=10000)
            button_new.click()
        else:
            raise Exception("Кнопка для проверки не найдена")

        # ждём основной элемент
        self.page.locator(LoginLocators.MAIN_BUTTON).wait_for()
        expect(self.page.locator(LoginLocators.MAIN_BUTTON)).to_be_enabled()

    def click_new_check_button(self):
        button = self.page.locator("#secCheck").get_by_role("button", name="New check")
        expect(button).to_be_visible(tomeout=10000)
        expect(button).to_be_enabled(timeout=10000)
        button.click()

    def wait_for_invalid_address_text(self,timeout=10000):
        locator = self.page.get_by_text("INVALID_ADDRESS")
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_be_visible()

    def select_network(self, network_name: str):
        self.page.get_by_role("button", name="button").click()
        button = self.page.get_by_role("button", name="BSC")
        expect(button).to_be_visible(timeout=10000)
        expect(button).to_be_enabled(timeout=10000)
        button.click()

    def wait_for_invalid_email_text(self, timeout=10000):
        locator = self.page.get_by_text("wrong or not valid email")
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_be_visible()

    def enter_invalid_email(self, email: str):
        self.page.locator(LoginLocators.ENTER_EMAIL_INPUT).fill(email)
        button = self.page.locator(LoginLocators.LOG_IN_BUTTON)
        expect(button).to_be_visible(timeout=10000)
        expect(button).to_be_enabled(timeout=10000)
        button.click()

    def enter_wallet_address_with_chainge_network(self, address: str):
        self.page.locator(LoginLocators.WALLET_ADDRESS_INPUT).fill(address)
        network_button = self.page.get_by_role("button", name="button")

        expect(network_button).to_be_visible(timeout=10000)
        expect(network_button).to_be_enabled(timeout=10000)
        network_button.click()

        button_bcs = self.page.get_by_role("button", name="BSC")
        expect(button_bcs).to_be_visible(timeout=10000)
        expect(button_bcs).to_be_enabled(timeouy=10000)
        button_bcs.click()

        button_check = self.page.locator(LoginLocators.CHECK_FOR_FREE_BUTTON)
        expect(button_check).to_be_visible(timeout=10000)
        expect(button_check).to_be_enabled(timeout=10000)
        button_check.click()

    def click_back_button_and_check_result(self):
        button_back = self.page.locator(LoginLocators.BACK_BUTTON)
        expect(button_back).to_be_visible(timeout=10000)
        expect(button_back).to_be_enabled(timeout=10000)
        button_back.click()
        self.page.locator(LoginLocators.LOG_IN_BUTTON).click()

        locator = self.page.get_by_text("Error: unknown auth error")
        expect(locator).to_be_visible(timeout=5000)

    def check_120sec_pause(self):
        locator = self.page.get_by_text("Error: unknown auth error")
        expect(locator).to_be_visible(timeout=5000)

    def enter_incorrect_address(self):
        locator = self.page.get_by_text("Error: please enter a valid address")
        expect(locator).to_be_visible(timeout=6000)








