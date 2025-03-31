from datetime import datetime, timedelta, timezone
from subprocess import run

import typer
import uvicorn
from jose import jwt

from src.infrastructure.commons.settings.base import settings

app = typer.Typer()


@app.command()
def runserver(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    uvicorn.run("src.main:app", host=host, port=port, reload=reload)


@app.command()
def makemigrations():
    run(
        [
            "alembic",
            "revision",
            "--autogenerate",
            "-m",
            f"""Migration {datetime.now().strftime("%d_%m_%Y")}""",
        ],
        check=True,
    )


@app.command()
def migrate():
    run(["alembic", "upgrade", "head"], check=True)


@app.command()
def format(path: str):
    run(
        ["ruff", "check", "--select", "I", "--fix", path],
        check=True,
    )
    run(
        ["ruff", "format", path],
        check=True,
    )


@app.command()
def test():
    run(["python", "-m", "pytest", "-vv"], check=True)


@app.command()
def coverage():
    run(["python", "-m", "pytest", "--cov", "--cov-report=html"], check=True)


@app.command()
def get_jwt():
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    print(token)


if __name__ == "__main__":
    app()
