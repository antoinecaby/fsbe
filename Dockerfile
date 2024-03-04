FROM mwalbeck/python-poetry:1.7-3.12 as requirements-stage
WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM ghcr.io/multi-py/python-uvicorn:py3.11-0.27.0 as develop-stage
# Mac M1: ghcr.io/multi-py/python-uvicorn:py3.11-0.25.0
# The official image is tiangolo/uvicorn-gunicorn-fastapi:python3.11 but currently does not support ARM images
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt