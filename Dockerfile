FROM python:3.7-slim

RUN python -m pip install rasa
RUN python -m pip install pandas
RUN python -m pip install mysql-connector
RUN python -m pip install openpyxl
RUN python -m pip install nltk
RUN python -m pip install fuzzywuzzy
RUN python -m pip install transformers
RUN python -m pip install sentencepiece
RUN python -m pip install farm-haystack
RUN python -m pip install torch --extra-index-url https://download.pytorch.org/whl/cpu

WORKDIR /app
COPY . .

RUN python download_model.py
RUN rasa train

USER root

# ENTRYPOINT ["rasa"]

# CMD ["run", "--enable-api", "--cors", "*"]

CMD ["sh",  "run.sh"]