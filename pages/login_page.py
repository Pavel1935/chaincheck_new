from pages.base_page import BasePage
from playwright.sync_api import expect
from locators.login_locators import LoginLocators


class LoginPage(BasePage):
    def enter_wallet_address(self, address: str):
        self.page.locator(LoginLocators.WALLET_ADDRESS_INPUT).fill(address)
        self.page.locator(LoginLocators.CHECK_FOR_FREE_BUTTON).click()

    def enter_email(self, email: str):
        self.page.locator(LoginLocators.ENTER_EMAIL_INPUT).fill(email)
        self.page.locator(LoginLocators.LOG_IN_BUTTON).click()

    def enter_code(self, code: str):
        self.fill_code_by_indexed_inputs(LoginLocators.CODE_INPUTS, code)
        expect(self.page.locator(LoginLocators.NEW_CHECK_BUTTON)).to_be_enabled()

    def check_final_result(self):
        self.page.locator(LoginLocators.CHECK_FOR_FREE_BUTTON).click()
        self.page.locator(LoginLocators.MAIN_BUTTON).wait_for()
        expect(self.page.locator(LoginLocators.MAIN_BUTTON)).to_be_enabled()
