FROM python:3.12.4-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR app/

FROM base AS builder

COPY ./src ./src
COPY ./pyproject.toml ./pyproject.toml

RUN pip install build && \
    python3 -m build --wheel

FROM base AS web-api

COPY --from=builder ./app/dist ./

RUN $(printf "pip install %s[web_api]" contribution*.whl)

ENTRYPOINT ["contribution", "run-web-api"]
CMD ["--workers", "1"]

FROM base AS event-consumer

COPY --from=builder ./app/dist ./

RUN $(printf "pip install %s[event_consumer]" contribution*.whl)

ENTRYPOINT ["contribution", "run-event-consumer"]
CMD ["--workers", "1"]
