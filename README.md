# Coffee Fun! -- Intelligent Coffee Ordering Chatbot

An end-to-end conversational system configured on the Flask framework, with a backend chatbot configured on the RASA framework running on Docker. The chatbot supports 3 use cases: Chitchat, Coffee order and Feedback. See our demo by clicking the picture below.

[![Demo](https://github.com/SCNUJackyChen/rasa/blob/main/pics/overview.png)](https://drive.google.com/file/d/1d4lvbny-Xwi0GmAkEFfn_gQfmta_6WPI/view?usp=sharing)


# How to use

## Docker Images
### RASA backend
We deploy the RASA backend in Docker, you can either build from Dockerfile or pull from our released image.

Use `docker build -t <image_name> .` to build a docker image locally.

Use `docker pull scnujackychen/coffeefun` to pull image remotely.

### MySql
The MySql Docker can be pulled from our released image.

Use `docker pull scnujackychen/rasa_mysql`

Unzip the data volumn `mysql.zip` to `/rasa/`.

## Create container

### MySql
`docker run -it -v path_to_mysql_data_volumn --name database scnujackychen/rasa_mysql:latest`

### RASA backend
`docker run -it --name rasa -p 5005:5005 --link database:db scnujackychen/rasa_coffeefun:latest`

## Run Flask
`python UI\app.py`
