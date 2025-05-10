FROM python:3.13-slim AS build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY ./pyproject.toml ./uv.lock*  /app/

RUN uv pip compile pyproject.toml --quiet --output-file requirements.txt \
    && pip install -r requirements.txt

COPY  . .

# Stage for Fastapi server
FROM build AS server
CMD ["python", "manage.py", "runserver", "--port", "8000", "--host", "0.0.0.0", "--reload"]

FROM build AS aws_server
EXPOSE 8000
CMD ["python", "manage.py", "runserver-aws", "--port", "8000", "--host", "0.0.0.0", "--reload"]

# Stage for migrations
FROM build AS migrate
CMD ["python", "manage.py", "migrate"]