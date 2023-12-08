FROM python:3.11.0

RUN pip install poetry

ADD pyproject.toml ./
ADD poetry.lock ./

RUN poetry install

ADD ./ ./

ENV FILE "fallback"

CMD poetry run python src/run_pydicom_example.py $FILE
