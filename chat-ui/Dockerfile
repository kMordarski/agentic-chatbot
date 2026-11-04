FROM node:22 AS build
WORKDIR /usr/local/app

COPY package*.json ./

RUN npm ci

COPY . .

ARG VITE_API_URL 
ARG VITE_API_KEY 

RUN npm run build

FROM nginx:alpine

COPY --from=build /usr/local/app/dist /usr/share/nginx/html
