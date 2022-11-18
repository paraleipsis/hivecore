FROM nikolaik/python-nodejs:python3.10-nodejs18-alpine
WORKDIR /usr/src
EXPOSE 3000 7001

RUN pip3 install --upgrade pip 
COPY api api
COPY api/requirements.txt ./api
RUN cd api && pip3 install -r requirements.txt

COPY frontend frontend
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install --force --verbose
RUN cd frontend && npm run build


COPY docker-entrypoint.sh .
RUN ["chmod", "+x", "docker-entrypoint.sh"]
ENTRYPOINT ["./docker-entrypoint.sh"]
