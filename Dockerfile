FROM python:3.11.7
RUN echo "aia-utils image"
RUN apt-get update && apt-get -y install
RUN apt-get install iputils-ping -y
RUN apt-get install vim -y
RUN pip install --upgrade pip
RUN pip install poetry
RUN echo "aia-utils [end]"