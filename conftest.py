"""Fixtures compartidos y evidencias automáticas de Pytest."""

import logging
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
LOGS_DIR = ROOT_DIR / "logs"

SCREENSHOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOGS_DIR / "pytest.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    force=True,
)
logger = logging.getLogger(__name__)


@pytest.fixture
def driver():
    """Crea un navegador Chrome para cada test y lo cierra al finalizar."""
    options = Options()
    # Para ejecutar sin ventana, descomentá la siguiente línea:
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-notifications")

    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(30)
    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda una captura de pantalla cuando falla una prueba."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        if browser is not None:
            safe_test_name = "".join(
                character if character.isalnum() or character in "-_" else "_"
                for character in item.name
            )
            screenshot_path = SCREENSHOTS_DIR / f"{safe_test_name}.png"
            try:
                browser.save_screenshot(str(screenshot_path))
                logger.error("Test fallido: %s. Captura: %s", item.name, screenshot_path)
                print(f"\nCaptura de pantalla guardada en: {screenshot_path}")
            except Exception:
                logger.exception("No se pudo guardar la captura para %s", item.name)
