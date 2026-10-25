FROM debian:bookworm

ARG WP_VERSION
ARG WPCLI_VERSION=2.12.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        php8.2-fpm php8.2-cli php8.2-mysql php8.2-curl php8.2-gd \
        php8.2-xml php8.2-mbstring php8.2-zip curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /usr/local/bin/wp \
        "https://github.com/wp-cli/wp-cli/releases/download/v${WPCLI_VERSION}/wp-cli-${WPCLI_VERSION}.phar" \
    && chmod +x /usr/local/bin/wp

RUN test -n "${WP_VERSION}" \
    && wp core download --version="${WP_VERSION}" --path=/usr/src/wordpress --allow-root

COPY conf/www.conf /etc/php/8.2/fpm/pool.d/www.conf
COPY tools/init.sh /usr/local/bin/init.sh
RUN chmod +x /usr/local/bin/init.sh

EXPOSE 9000

ENTRYPOINT ["/usr/local/bin/init.sh"]
