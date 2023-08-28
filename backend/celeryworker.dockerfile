FROM python:3.9

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.5.1
ENV PATH /root/.local/bin:$PATH
RUN cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock ./

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"
RUN poetry install --no-interaction --no-ansi


# /start Project-specific dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*	

# install node for tool testing
ENV NODE_VERSION=19.6.0
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

COPY ./app ./

# TOOLS DEPENDENCIES

# install pa-website-validator and its dependencies
ARG DEBIAN_FRONTEND=noninteractive
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
# Install Google Chrome Stable and fonts
# Note: this installs the necessary libs to make the browser work with Puppeteer.
RUN apt-get update && apt-get install gnupg wget -y && \
  wget --quiet --output-document=- https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-archive.gpg && \
  sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
  apt-get update && \
  apt-get install google-chrome-stable jq -y --no-install-recommends && \
  rm -rf /var/lib/apt/lists/*
# Download master or tag from github
WORKDIR /app/app/tools/validation/
RUN git clone --branch v2.6.0 https://github.com/italia/pa-website-validator temp_clone && \
    mv temp_clone/* temp_clone/.git* pawebsitevalidator && \
    rm -rf temp_clone && \
    cd pawebsitevalidator && \
    npm ci && \
    npm -g i .

# install mauve dependencies
WORKDIR /app/app/tools/accessibility/mauve/
RUN npm ci && npm -g i .


# /end Project-specific dependencies	

ENV C_FORCE_ROOT=1
# COPY ./app /app
WORKDIR /app
ENV PYTHONPATH=/app
COPY ./app/worker-start.sh /worker-start.sh
RUN chmod +x /worker-start.sh
CMD ["bash", "/worker-start.sh"]
