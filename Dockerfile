FROM python:3.9 AS prod

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./htmlpdf.py" ]


FROM prod AS dev

RUN pip install --no-cache-dir -r requirements-test.txt -r requirements-lint.txt

CMD ["sh", "-c", "pylint --version && pylint -v . && mypy --version && mypy . && pytest --cov=htmlpdf"]
