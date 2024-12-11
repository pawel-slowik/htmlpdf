FROM python:3.9 AS prod

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./htmlpdf.py" ]


FROM prod AS dev

COPY requirements-test.txt requirements-lint.txt ./
RUN pip install --no-cache-dir -r requirements-test.txt -r requirements-lint.txt

CMD ["sh", "-c", "pylint --version && pylint -v . && mypy --version && mypy . && pytest --cov=htmlpdf"]
