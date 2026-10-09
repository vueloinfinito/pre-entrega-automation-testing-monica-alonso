"""Funciones auxiliares reutilizables para SauceDemo."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
DEFAULT_TIMEOUT = 10


def wait_for_element(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Espera hasta que un elemento esté visible y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def login_as_standard_user(driver):
    """Realiza el login con el usuario estándar de SauceDemo."""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    username_input = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    password_input = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    username_input.clear()
    username_input.send_keys(USERNAME)
    password_input.clear()
    password_input.send_keys(PASSWORD)

    wait.until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    ).click()

    # La espera explícita confirma que la navegación terminó.
    wait.until(EC.url_contains("/inventory.html"))
    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )
