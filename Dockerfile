# build api
FROM --platform=arm64 python:3.8.10-alpine AS python
WORKDIR /usr/src/app

COPY api .

RUN pip install --upgrade pip 
RUN pip install pipenv

COPY Pipfile* /app/
RUN pipenv install --system --dev

# build app
FROM --platform=arm64 node:18.9.0-alpine AS node
WORKDIR /usr/src/app

COPY --from=python /usr/src/app /usr/src/app
COPY frontend .
RUN npm install

# build
FROM alpine
WORKDIR /app
COPY --from=node /usr/src/app /usr/src/app
EXPOSE 3000 7001