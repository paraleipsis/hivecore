FROM node:18-alpine
WORKDIR /usr/src/frontend

COPY package*.json ./
RUN npm install --force --verbose
RUN npm install --force -g sass
COPY . .

RUN ["chmod", "+x", "docker-entrypoint.sh"]
ENTRYPOINT ["./docker-entrypoint.sh"]