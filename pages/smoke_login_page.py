from Constants import Constants
from pages.base_page import BasePage
from playwright.sync_api import expect
from locators.smoke_login_locators import LoginLocators


class LoginPage(BasePage):
    def enter_wallet_address(self, address: str):
        self.page.locator(LoginLocators.WALLET_ADDRESS_INPUT).fill(address)
        self.page.locator(LoginLocators.CHECK_FOR_FREE_BUTTON).click()

    def enter_email(self, email: str):
        self.page.locator(LoginLocators.ENTER_EMAIL_INPUT).fill(email)
        self.page.locator(LoginLocators.LOG_IN_BUTTON).click()

    def enter_code(self, code: str):
        self.fill_code_by_indexed_inputs(LoginLocators.CODE_INPUTS, code)
        # expect(self.page.locator(LoginLocators.NEW_CHECK_BUTTON)).to_be_enabled()

    def check_final_result(self):
        self.page.locator(LoginLocators.CHECK_FOR_FREE_BUTTON).click()
        self.page.locator(LoginLocators.MAIN_BUTTON).wait_for()
        expect(self.page.locator(LoginLocators.MAIN_BUTTON)).to_be_enabled()

    def click_check_for_free_button(self,timeout=10000):
        self.page.locator(LoginLocators.CHECK_FOR_FREE_BUTTON).click()

    def wait_for_invalid_address_text(self,timeout=10000):
        locator = self.page.get_by_text("INVALID_ADDRESS")
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_be_visible()

    def select_network(self, network_name: str):
        self.page.get_by_role("button", name="button").click()
        self.page.get_by_role("button", name="BSC").click()

    def wait_for_invalid_email_text(self, timeout=10000):
        locator = self.page.get_by_text("wrong or not valid email")
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_be_visible()

    def enter_invalid_email(self, email: str):
        self.page.locator(LoginLocators.ENTER_EMAIL_INPUT).fill(email)
        self.page.locator(LoginLocators.LOG_IN_BUTTON).click()

    def enter_wallet_address_with_chainge_network(self, address: str):
        self.page.locator(LoginLocators.WALLET_ADDRESS_INPUT).fill(address)
        self.page.get_by_role("button", name="button").click()
        self.page.get_by_role("button", name="BSC").click()
        self.page.locator(LoginLocators.CHECK_FOR_FREE_BUTTON).click()



з