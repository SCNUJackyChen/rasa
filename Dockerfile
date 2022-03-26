FROM python:3.7-slim

RUN python -m pip install rasa

WORKDIR /app
COPY . .

RUN rasa train nlu

USER 1001

ENTRYPOINT ["rasa"]

CMD ["run", "actions"]

CMD ["run", "--enable-api", "--cors", "\"*\""]