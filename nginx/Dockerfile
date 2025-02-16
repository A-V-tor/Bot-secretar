FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

COPY localhost.crt /etc/ssl/certs/localhost.crt

COPY localhost.key /etc/ssl/private/localhost.key
