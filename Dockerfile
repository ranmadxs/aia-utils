FROM python:3.11.7
RUN echo "aia-utils image"
WORKDIR /aia-utils
COPY . .
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install
RUN rm -rf dist/
RUN poetry build

RUN ls -la dist/
RUN echo "aia-utils [end]"