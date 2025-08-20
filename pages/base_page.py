from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def fill_input(self, locator, value):
        self.page.locator(locator).fill(value)

    def click_text(self, text: str):
        self.page.get_by_text(text).click()

    def wait_for_text(self, text: str, timeout=10000):
        self.page.get_by_text(text).wait_for(state="visible", timeout=timeout)

    def fill_code_by_indexed_inputs(self, selector, code: str):
        self.page.locator(selector).first.wait_for()
        inputs = self.page.locator(selector)
        for i, digit in enumerate(code):
            inputs.nth(i).fill(digit)
