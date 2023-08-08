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

RUN poetry install --no-interaction --no-ansi

COPY ./app /app

WORKDIR /app/app/scheduler/

CMD ["python3", "-u", "scheduler.py"]