FROM ghcr.io/br3ndonland/inboard:fastapi-0.37.0-python3.9

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

WORKDIR /app/

# Neomodel has shapely and libgeos as dependencies
RUN apt-get update && apt-get install -y libgeos-dev

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

# /start Project-specific dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*	
# WORKDIR /app/
# /end Project-specific dependencies

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./app/alembic/versions/* ./app/alembic/versions/

ARG BACKEND_APP_MODULE=app.main:app
ARG BACKEND_PRE_START_PATH=/app/prestart.sh
ARG BACKEND_PROCESS_MANAGER=gunicorn
ARG BACKEND_WITH_RELOAD=false
ENV APP_MODULE=${BACKEND_APP_MODULE} PRE_START_PATH=${BACKEND_PRE_START_PATH} PROCESS_MANAGER=${BACKEND_PROCESS_MANAGER} WITH_RELOAD=${BACKEND_WITH_RELOAD}
COPY ./app/ /app/
