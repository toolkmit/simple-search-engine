# base image
FROM python:3.7.1-alpine

# Create and set work directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app

# run server
CMD flask run --host=0.0.0.0