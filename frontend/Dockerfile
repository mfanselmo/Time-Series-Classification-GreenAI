FROM node:16.10.0

ENV HOST=0.0.0.0
WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

RUN npm install -g npm@8.15.0
RUN npm install @vue/cli@4.5.13 -g

COPY package.json .
COPY package-lock.json .
RUN npm install

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
COPY ./ ./
RUN npm run build
EXPOSE 8080

