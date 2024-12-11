FROM python:3.9 AS prod

WORKDIR /usr/src/app

COPY . .

RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

CMD [ "python", "./htmlpdf.py" ]


FROM prod AS dev

RUN --mount=type=cache,target=/root/.cache pip install -r requirements-test.txt -r requirements-lint.txt

CMD ["sh", "-c", "pylint --version && pylint -v . && mypy --version && mypy . && pytest --cov=htmlpdf"]
