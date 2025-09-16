class LoginLocators:
    WALLET_ADDRESS_INPUT = "input[placeholder='Wallet address']"
    CHECK_FOR_FREE_BUTTON = "button:has-text('Check for Free')"
    ENTER_EMAIL_INPUT = "input[placeholder='Enter email']"
    LOG_IN_BUTTON = "button:has-text('Log In')"
    NEW_CHECK_BUTTON = "button:has-text('New check')"
    NEW_CHECK_BUTTON = page.get_by_role("button", name="New check").click()
    MAIN_BUTTON = "button:has-text('Main')"
    CODE_INPUTS = "[data-melt-pin-input-input]"
    TEXT = "INVALID_ADDRESS"
    BACK_BUTTON = "[data-test-id='auth-code-back']"
