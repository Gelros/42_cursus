#!/bin/sh
set -e

: "${DOMAIN_NAME:?DOMAIN_NAME is empty}"
: "${MYSQL_DATABASE:?MYSQL_DATABASE is empty}"
: "${MYSQL_USER:?MYSQL_USER is empty}"
: "${WP_TITLE:?WP_TITLE is empty}"
: "${WP_ADMIN_USER:?WP_ADMIN_USER is empty}"
: "${WP_ADMIN_EMAIL:?WP_ADMIN_EMAIL is empty}"
: "${WP_USER:?WP_USER is empty}"
: "${WP_USER_EMAIL:?WP_USER_EMAIL is empty}"

DB_PASSWORD=$(cat /run/secrets/db_password)
WP_ADMIN_PASSWORD=$(cat /run/secrets/wp_admin_password)
WP_USER_PASSWORD=$(cat /run/secrets/wp_user_password)

case "$(printf '%s' "$WP_ADMIN_USER" | tr '[:upper:]' '[:lower:]')" in
    *admin*)
        echo "Error: WP_ADMIN_USER must not contain 'admin'" >&2
        exit 1
        ;;
esac

WP="wp --path=/var/www/wordpress --allow-root"

mkdir -p /var/www/wordpress /run/php

if [ ! -f /var/www/wordpress/wp-settings.php ]; then
    cp -a /usr/src/wordpress/. /var/www/wordpress/
fi

if [ ! -f /var/www/wordpress/wp-config.php ]; then
    $WP config create \
        --dbname="$MYSQL_DATABASE" \
        --dbuser="$MYSQL_USER" \
        --dbpass="$DB_PASSWORD" \
        --dbhost=mariadb
fi

if ! $WP core is-installed; then
    $WP core install \
        --url="https://${DOMAIN_NAME}" \
        --title="$WP_TITLE" \
        --admin_user="$WP_ADMIN_USER" \
        --admin_password="$WP_ADMIN_PASSWORD" \
        --admin_email="$WP_ADMIN_EMAIL" \
        --skip-email
fi

if ! $WP user get "$WP_USER" > /dev/null 2>&1; then
    $WP user create "$WP_USER" "$WP_USER_EMAIL" \
        --user_pass="$WP_USER_PASSWORD" \
        --role=author
fi

chown -R www-data:www-data /var/www/wordpress

exec php-fpm8.2 -F
