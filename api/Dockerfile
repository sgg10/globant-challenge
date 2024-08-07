FROM python:3.11 AS python

# Python runtime stage
FROM python AS python-runtime-stage

ARG BUILD_ENVIRONMENT="#!{ENVIRONMENT}!#"
ARG APP_HOME=/code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN addgroup --system fastapi \
    && adduser --system --ingroup fastapi fastapi

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    # psycopg2 dependencies
    libpq-dev \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=fastapi:fastapi ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY --chown=fastapi:fastapi . ${APP_HOME}

RUN pip install --upgrade pip \
    && pip install -r requirements/${BUILD_ENVIRONMENT}.txt

# make fastapi owner of the WORKDIR directory as well.
RUN chown fastapi:fastapi ${APP_HOME}

USER fastapi

CMD [ "/start" ]
