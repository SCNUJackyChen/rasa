FROM python:3.7-slim

RUN python -m pip install rasa
RUN python -m pip install pandas
RUN python -m pip install mysql-connector
RUN python -m pip install openpyxl

WORKDIR /app
COPY . .

RUN rasa train

USER root

# ENTRYPOINT ["rasa"]

# CMD ["run", "--enable-api", "--cors", "*"]

CMD ["sh",  "run.sh"]