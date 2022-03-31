FROM python:3.7-slim

RUN python -m pip install rasa
RUN python -m pip install pandas
RUN python -m pip install mysql-connector
RUN python -m pip install openpyxl
RUN python -m pip install nltk
RUN python -m pip install spacy
RUN python -m spacy download en_core_web_md

WORKDIR /app
COPY . .

RUN rasa train

USER root

# ENTRYPOINT ["rasa"]

# CMD ["run", "--enable-api", "--cors", "*"]

CMD ["sh",  "run.sh"]