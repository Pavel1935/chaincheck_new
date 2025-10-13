class LoginLocators:
    # Кнопка "New check" внизу формы (рядом с инпутом)
    CHECK_FORM_BUTTON = '[data-testid="form-check-submit-btn"]'
    # Кнопка "New check" в хэдере (верхняя)
    CHECK_HEADER_BUTTON = '[data-testid="header-check-btn"]'
    # Инпут для ввода адреса кошелька
    WALLET_ADDRESS_INPUT = "input[placeholder='Wallet address']"
    # Инпут для ввода адреса почты
    ENTER_EMAIL_INPUT = "input[placeholder='Enter email']"
    # Кнопка "Log In"
    LOG_IN_BUTTON = "button:has-text('Log In')"
    # Кнопка "Main"
    MAIN_BUTTON = "button:has-text('Main')"
    # Инпут для ввода проверочного кода из письма
    CODE_INPUTS = "[data-melt-pin-input-input]"
    # Текст невалидный адрес
    TEXT = "INVALID_ADDRESS"
    # Кнопка "Назад"
    BACK_BUTTON = "[data-test-id='auth-code-back']"
