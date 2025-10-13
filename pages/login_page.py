import logging
from Constants import Constants
from pages.base_page import BasePage
from playwright.sync_api import expect
from locators.login_locators import LoginLocators

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    def enter_wallet_address(self, address: str):
        self.page.locator(LoginLocators.WALLET_ADDRESS_INPUT).fill(address)
        self.page.locator(LoginLocators.CHECK_FORM_BUTTON).click()

    def enter_email(self, email: str):
        # self.page.on("response", self._log_auth_response)
        self.page.locator(LoginLocators.ENTER_EMAIL_INPUT).fill(email)
        self.page.locator(LoginLocators.LOG_IN_BUTTON).click()

    def enter_code(self, code: str):
        self.fill_code_by_indexed_inputs(LoginLocators.CODE_INPUTS, code)

    def check_final_result(self):
        self.page.locator(LoginLocators.CHECK_FORM_BUTTON).click()
        self.page.locator(LoginLocators.MAIN_BUTTON).wait_for()
        expect(self.page.locator(LoginLocators.MAIN_BUTTON)).to_be_enabled()

    def click_new_check_button(self):
        self.wait_and_click(LoginLocators.CHECK_FORM_BUTTON)

    def wait_for_invalid_address_text(self, timeout=10000):
        locator = self.page.get_by_text("INVALID_ADDRESS")
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_be_visible()

    def select_network(self, network_name: str = "BSC"):
        # Кликаем по кнопке выбора сети
        self.wait_and_click('button[role="button"]:has-text("button")')
        # Кликаем по нужной сети (по умолчанию — "BSC")
        self.wait_and_click(f'button[role="button"]:has-text("{network_name}")')

    def wait_for_invalid_email_text(self, timeout=10000):
        locator = self.page.get_by_text("wrong or not valid email")
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_be_visible()

    def enter_invalid_email(self, email: str):
        self.page.locator(LoginLocators.ENTER_EMAIL_INPUT).fill(email)
        self.wait_and_click(LoginLocators.LOG_IN_BUTTON)

    def enter_wallet_address_with_chainge_network(self, address: str, network_name: str = "BSC"):
        self.page.locator(LoginLocators.WALLET_ADDRESS_INPUT).fill(address)
        self.select_network(network_name)
        self.wait_and_click(LoginLocators.CHECK_FORM_BUTTON)

    def click_back_button_and_check_result(self):
        self.wait_and_click(LoginLocators.BACK_BUTTON)
        self.page.locator(LoginLocators.LOG_IN_BUTTON).click()

        locator = self.page.get_by_text("Error: unknown auth error")
        expect(locator).to_be_visible(timeout=5000)

    def check_120sec_pause(self):
        locator = self.page.get_by_text("Error: unknown auth error")
        expect(locator).to_be_visible(timeout=5000)

    def enter_incorrect_address(self):
        locator = self.page.get_by_text("Error: please enter a valid address")
        expect(locator).to_be_visible(timeout=6000)








