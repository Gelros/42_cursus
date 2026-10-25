#!/bin/sh
set -e

: "${DOMAIN_NAME:?DOMAIN_NAME is empty}"

SSL_DIR=/etc/nginx/ssl
mkdir -p "$SSL_DIR"

if [ ! -f "$SSL_DIR/inception.crt" ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$SSL_DIR/inception.key" \
        -out "$SSL_DIR/inception.crt" \
        -subj "/CN=${DOMAIN_NAME}" \
        -addext "subjectAltName=DNS:${DOMAIN_NAME}"
    chmod 600 "$SSL_DIR/inception.key"
fi

sed "s/__DOMAIN_NAME__/${DOMAIN_NAME}/g" \
    /etc/nginx/templates/inception.conf.template \
    > /etc/nginx/conf.d/inception.conf

exec nginx -g "daemon off;"
