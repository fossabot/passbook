FROM docker.beryju.org/passbook/dev:latest as static-build

COPY ./passbook/ /app/passbook
COPY ./manage.py /app/
COPY ./requirements.txt /app/

WORKDIR /app/

RUN ./manage.py collectstatic --no-input

FROM nginx:latest

COPY --from=static-build /app/static /static/static/
COPY ./passbook/core/nginx.conf /etc/nginx/nginx.conf