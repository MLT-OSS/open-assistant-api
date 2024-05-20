FROM node:16.14.2 as ui-build
WORKDIR /playground-ui

COPY package.json yarn.lock ./
COPY . .

RUN yarn install
RUN yarn run build:dev


FROM nginx:alpine
COPY /deploy/nginx/default_dev.conf /etc/nginx/conf.d/default.conf
COPY --from=ui-build /playground-ui/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]