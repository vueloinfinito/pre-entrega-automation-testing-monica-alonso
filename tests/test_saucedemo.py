"""Pruebas de login, catálogo y carrito de SauceDemo."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.saucedemo_helpers import (
    DEFAULT_TIMEOUT,
    login_as_standard_user,
)


def test_login_exitoso_redirige_al_inventario(driver):
    """Valida que el usuario pueda iniciar sesión y vea el inventario."""
    login_as_standard_user(driver)

    assert "/inventory.html" in driver.current_url, (
        f"Se esperaba /inventory.html, pero la URL fue: {driver.current_url}"
    )
    assert driver.title == "Swag Labs", (
        f"Se esperaba el título 'Swag Labs', pero fue: {driver.title}"
    )

    page_heading = driver.find_element(By.CLASS_NAME, "title")
    assert page_heading.text == "Products", (
        f"Se esperaba el encabezado 'Products', pero fue: {page_heading.text}"
    )


def test_catalogo_muestra_productos_y_datos_del_primero(driver):
    """Verifica encabezado, controles de interfaz y datos del primer producto."""
    login_as_standard_user(driver)
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    assert "/inventory.html" in driver.current_url
    assert driver.title == "Swag Labs"

    heading = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )
    assert heading.text == "Products"

    menu_button = wait.until(
        EC.visibility_of_element_located((By.ID, "react-burger-menu-btn"))
    )
    assert menu_button.is_displayed(), "El botón del menú no está visible."

    sort_dropdown = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "product_sort_container")
        )
    )
    assert sort_dropdown.is_displayed(), "El filtro de ordenamiento no está visible."

    products = wait.until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )
    assert len(products) >= 1, "No se encontraron productos visibles."

    first_product = products[0]
    product_name = first_product.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text
    product_price = first_product.find_element(
        By.CLASS_NAME, "inventory_item_price"
    ).text

    assert product_name, "El primer producto no tiene nombre."
    assert product_price.startswith("$"), (
        f"El precio del primer producto no tiene el formato esperado: {product_price}"
    )

    # Se imprimen los datos para que queden visibles en la consola de Pytest.
    print(f"Primer producto: {product_name} | Precio: {product_price}")


def test_agregar_primer_producto_y_verificar_carrito(driver):
    """Agrega el primer producto y verifica que aparezca en el carrito."""
    login_as_standard_user(driver)
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    first_product = wait.until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )[0]

    product_name = first_product.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text

    add_button = first_product.find_element(
        By.CSS_SELECTOR, "button.btn_inventory"
    )
    wait.until(lambda _driver: add_button.is_enabled())
    add_button.click()

    cart_badge = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert cart_badge.text == "1", (
        f"Se esperaba un contador de carrito igual a 1, pero fue {cart_badge.text}"
    )

    cart_link = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
    )
    cart_link.click()

    wait.until(EC.url_contains("/cart.html"))
    cart_items = wait.until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "cart_item")
        )
    )
    assert len(cart_items) == 1, (
        f"Se esperaba un producto en el carrito, pero se encontraron {len(cart_items)}"
    )

    cart_product_name = cart_items[0].find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text
    assert cart_product_name == product_name, (
        f"El producto del carrito ('{cart_product_name}') no coincide "
        f"con el producto agregado ('{product_name}')."
    )
