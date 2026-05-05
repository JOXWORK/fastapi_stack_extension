FROM python:3.13.7-trixie

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /application

RUN pip install --upgrade pip wheel "poetry==2.1.4"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY application .

RUN chmod +x entrypoint.sh

RUN chmod +x run

ENTRYPOINT ["./entrypoint.sh"]

CMD ["./run"]