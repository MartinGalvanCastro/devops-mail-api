import os
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
def runserver_aws(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    migrate()
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


@app.command()
def push_docker_image():
    account_id = os.getenv("AWS_ACCOUNT_ID")
    if account_id is None:
        raise Exception("AWS_ACCOUNT_ID environment variable is not set")

    # Step 1: Build the main build image
    run(
        [
            "docker",
            "build",
            "--platform",
            "linux/amd64",
            "--target",
            "build",
            "-t",
            "devops/blacklist-api-python:build",
            ".",
        ],
        check=True,
    )

    # Step 2: Build the aws_server image using the main build stage as cache
    run(
        [
            "docker",
            "build",
            "--platform",
            "linux/amd64",
            "--target",
            "aws_server",
            "-t",
            "devops/blacklist-api-python:latest",
            ".",
        ],
        check=True,
    )

    # Step 3: Tag the aws_server image for AWS ECR
    ecr_tag = f"{account_id}.dkr.ecr.us-east-1.amazonaws.com/devops/blacklist-api-python:latest"
    run(["docker", "tag", "devops/blacklist-api-python:latest", ecr_tag], check=True)

    # Step 4: Push the image to AWS ECR
    run(["docker", "push", ecr_tag], check=True)

    typer.echo("Docker image built, tagged, and pushed successfully.")


if __name__ == "__main__":
    app()
