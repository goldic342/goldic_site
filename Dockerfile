FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt --no-cache-dir --upgrade

COPY . /app

RUN staticjinja build --outpath /app/build 

FROM caddy:2.10.2-alpine

COPY --from=builder /app/build /usr/share/caddy
COPY --from=builder /app/static /usr/share/caddy/static

# Move index related files to root
RUN mv /usr/share/caddy/static/images/favicon.ico /usr/share/caddy
RUN mv /usr/share/caddy/static/data/robots.txt /usr/share/caddy

COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE 3001
