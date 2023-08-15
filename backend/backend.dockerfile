FROM ghcr.io/br3ndonland/inboard:fastapi-0.37.0-python3.9

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

WORKDIR /app/

# Update poetry to 1.5.1 (uninstall and re-install)
RUN rm -rf "${POETRY_HOME:-~/.poetry}"
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.5.1
ENV PATH /root/.local/bin:$PATH
RUN cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-interaction --no-root ; else poetry install --no-interaction --no-root --no-dev ; fi"
RUN pip install --upgrade setuptools

COPY ./app/alembic/versions/* ./app/alembic/versions/

ARG BACKEND_APP_MODULE=app.main:app
ARG BACKEND_PRE_START_PATH=/app/prestart.sh
ARG BACKEND_PROCESS_MANAGER=gunicorn
ARG BACKEND_WITH_RELOAD=false
ENV APP_MODULE=${BACKEND_APP_MODULE} PRE_START_PATH=${BACKEND_PRE_START_PATH} PROCESS_MANAGER=${BACKEND_PROCESS_MANAGER} WITH_RELOAD=${BACKEND_WITH_RELOAD}
COPY ./app/ /app/
