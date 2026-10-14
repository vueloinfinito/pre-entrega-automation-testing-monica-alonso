# Pre-entrega de Automatización QA — SauceDemo

Proyecto de automatización de pruebas web para [SauceDemo](https://www.saucedemo.com/), realizado con Python, Pytest y Selenium WebDriver.

## Objetivo

Automatizar y validar tres flujos básicos:
1. Inicio de sesión exitoso con `standard_user`.
2. Navegación y verificación del catálogo de productos.
3. Agregado del primer producto al carrito y verificación del ítem.

Cada prueba inicia su propia sesión y realiza el login de forma independiente para reducir dependencias entre tests.

## Tecnologías

- Python 3.10 o superior
- Pytest
- Selenium WebDriver
- pytest-html para generar el reporte HTML
- Git y GitHub

## Estructura

```text
pre-entrega-automation-testing/
├── tests/
│   └── test_saucedemo.py
├── utils/
│   └── saucedemo_helpers.py
├── reports/
│   └── .gitkeep
├── screenshots/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
├── conftest.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requisitos previos

- Tener Python instalado.
- Tener Google Chrome instalado.
- Tener Git instalado para publicar el proyecto.
- Contar con conexión a Internet para acceder a SauceDemo e instalar las dependencias.


## Instalación

Desde la carpeta raíz del proyecto:

### Windows (PowerShell o CMD)

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecutar las pruebas

Desde la raíz del repositorio:

```bash
pytest tests/test_saucedemo.py -v
```

Generar el reporte HTML solicitado:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

El reporte se genera luego de ejecutar el comando. 

Para ejecutar todas las pruebas:

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

## Casos de prueba

### 1. Login exitoso
- Abre SauceDemo.
- Ingresa las credenciales válidas de práctica.
- Espera explícitamente la navegación a `/inventory.html`.
- Verifica el encabezado `Products` y el título de la pestaña `Swag Labs`.

### 2. Catálogo
- Verifica la URL de inventario y el encabezado.
- Comprueba que haya productos visibles.
- Valida la presencia del menú, el selector de ordenamiento y el primer producto.
- Registra y valida el nombre y el precio del primer producto.

### 3. Carrito
- Agrega el primer producto.
- Verifica que el contador del carrito indique `1`.
- Abre el carrito y comprueba que el producto agregado esté presente.

## Evidencias y logs

- Si un test falla, `conftest.py` intenta guardar una captura en `screenshots/`.
- Los mensajes de ejecución se registran en `logs/pytest.log`.
- Las carpetas se conservan en Git mediante archivos `.gitkeep`; los reportes, logs y capturas generados no se versionan por defecto.

## Publicar en GitHub

1. Creo un repositorio **público** llamado `pre-entrega-automation-testing-monica-alonso` .
2. En una terminal, dentro de la carpeta del proyecto, ejecuto:

```bash
git init
git add .
git commit -m "chore: estructura inicial del proyecto"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/pre-entrega-automation-testing-nombre-apellido.git
git push -u origin main
```

3. Para reflejar el progreso con commits descriptivos, uso mensajes como:

```bash
git add README.md requirements.txt .gitignore
git commit -m "docs: agregar instrucciones y dependencias"

git add tests/test_saucedemo.py utils/saucedemo_helpers.py conftest.py
git commit -m "test: automatizar login, catálogo y carrito"

git push
```


## Credenciales de prueba

- Usuario: `standard_user`
- Contraseña: `secret_sauce`


