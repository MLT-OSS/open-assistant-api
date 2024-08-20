FROM node:16.14.2 as ui-build

WORKDIR /app

COPY ./ /app

RUN yarn install && yarn run build:dev


FROM nginx:alpine

COPY ./deploy/nginx/default_dev.conf /etc/nginx/conf.d/default.conf
COPY --from=ui-build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
