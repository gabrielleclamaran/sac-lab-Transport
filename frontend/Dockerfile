# build stage
FROM node:18-alpine as build
WORKDIR /app
COPY . .
RUN npm install && npm run build

# production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html