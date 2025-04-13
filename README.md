# Mail API

Mail API es una aplicación basada en FastAPI diseñada para gestionar listas negras de correos electrónicos y proporcionar una API robusta para manejar solicitudes relacionadas con la validación y creación de entradas en listas negras.

**POSTMAN COLLECTION**: https://www.postman.com/cloudy-rocket-562143/putt-party/collection/kxuedaz/devops-mail-api

**POSTMAN DOC**: https://documenter.getpostman.com/view/10868035/2sB2cYeM7u

## Tabla de Contenidos

- [Mail API](#mail-api)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Características](#características)
  - [Requisitos Previos](#requisitos-previos)
  - [Instalación](#instalación)
  - [Ejecución](#ejecución)
  - [Comandos Disponibles](#comandos-disponibles)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Endpoints Principales](#endpoints-principales)
    - [\[POST\] /blacklists](#post-blacklists)
    - [\[GET\] /blacklists/{email}](#get-blacklistsemail)
    - [\[GET\] /health](#get-health)
    - [\[GET\] /](#get-)

## Características

- API RESTful construida con FastAPI.
- Middleware para autenticación JWT y detección de IP del cliente.
- Gestión de listas negras de correos electrónicos.
- Integración con SQLAlchemy para manejo de bases de datos.
- Migraciones de base de datos con Alembic.
- Configuración basada en variables de entorno.
- Soporte para pruebas con Pytest y generación de reportes de cobertura.

## Requisitos Previos

- Python 3.12 o superior.
- PostgreSQL como base de datos.
- [UV](https://astral.sh/blog/uv) o `pip` para manejar dependencias.

## Instalación

1. Clona este repositorio:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd mail-api
    ```

2. Crea un entorno virtual e instala las dependencias:
    ```bash
    # usando uv
    uv sync

    # usando pip
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. Configura las variables de entorno en el archivo .env:
    ```bash
    APP_TITLE="Mail API"
    APP_VERSION="0.1.0"
    DEBUG=False
    LOG_LEVEL=INFO
    DB_HOST="localhost"
    DB_PORT=5432
    DB_USER="postgres"
    DB_PASSWORD="postgres"
    DB_NAME="mail_db"
    DB_DRIVER="postgresql+psycopg"
    ```

4. Realiza las migraciones de la base de datos:
    ```bash
    # usando uv
    uv run python manage.py migrate

    # usando pip
    python manage.py migrate
    ```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
# usando uv
uv run python manage.py runserver --host 0.0.0.0 --port 8000 --reload

# usando pip
python manage.py runserver --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en http://localhost:8000.

## Comandos Disponibles
El archivo manage.py incluye varios comandos útiles:

* Ejecutar el servidor:
    ```bash
    python manage.py runserver
    ```

* Crear migraciones:
    ```bash
    python manage.py makemigrations
    ```

* Aplicar migraciones:
    ```bash
    python manage.py migrate
    ```

* Formatear código:
    ```bash
    python manage.py format <ruta>
    ```

* Ejecutar pruebas:
    ```bash
    python manage.py tests
    ```

* Generar cobertura de pruebas:
    ```bash
    python manage.py coverage
    ```

* Generar un token JWT:
    ```bash
    python manage.py get_jwt
    ```

## Estructura del Proyecto

```bash
.
├── .env                        # Variables de entorno
├── manage.py                   # Comandos de gestión
├── src/
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── routes.py               # Definición de rutas principales
│   ├── application/            # Lógica de negocio
│   │   ├── services/           # Capa de servicios
│   ├── domain/                 # Entidades y repositorios
│   │   ├── entities/           # Entidades del sistema
│   │   ├── exceptions/         # Excepciones del sistema
│   │   ├── repositories/       # Interfaces de repositorio
│   ├── infrastructure/         # Adaptadores y configuración
│   │   ├── adapters/
│   │   │   ├── input/          # Controladores de API
│   │   │   ├── output/         # Repositorios y modelos de base de datos
│   │   ├── commons/            # Middlewares, configuración y utilidades
│   │   ├── dependencies/       # Inyección de dependencias
│   ├── tests/                  # Pruebas unitarias
```

## Endpoints Principales

### [POST] /blacklists
Crea una nueva entrada en la lista negra.

### [GET] /blacklists/{email}
Valida si un correo electrónico está en la lista negra.

### [GET] /health
Verifica el estado de la API.

### [GET] /
Endpoint raíz.