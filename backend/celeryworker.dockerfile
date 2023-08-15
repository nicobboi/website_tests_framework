FROM python:3.9

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.5.1
ENV PATH /root/.local/bin:$PATH
RUN cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"
RUN poetry install --no-interaction --no-ansi


# /start Project-specific dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*	

# install node for tool testing
# ENV NODE_VERSION=19.6.0
# RUN apt install -y curl
# RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
# ENV NVM_DIR=/root/.nvm
# RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
# RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
# RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
# ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"


# DA SISTEMARE
COPY ./app /app

# # install mauve dependencies
# WORKDIR /app/app/tools/accessibility/mauve/
# # COPY ./app/app/tools/accessibility/mauve/package.json ./app/app/tools/accessibility/mauve/package-lock.json ./
# RUN npm install

# # install pa-website-validator and its dependencies
# WORKDIR /app/app/tools/validation/pa-website-validator/
# RUN curl -sSL https://github.com/italia/pa-website-validator/archive/refs/tags/v2.5.1.tar.gz -o project.tar.gz \
#     && tar -xzvf project.tar.gz --strip-components 1 \
#     && rm project.tar.gz
# RUN npm install


WORKDIR /app/
# /end Project-specific dependencies	

ENV C_FORCE_ROOT=1
# COPY ./app /app
WORKDIR /app
ENV PYTHONPATH=/app
COPY ./app/worker-start.sh /worker-start.sh
RUN chmod +x /worker-start.sh
CMD ["bash", "/worker-start.sh"]
