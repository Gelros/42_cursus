# Developer documentation

## Prerequisites

A Debian virtual machine with Docker Engine, the Docker Compose plugin, `make` and `git`. Check with `docker compose version`. The VM clock must be synchronised (`timedatectl`), otherwise `apt` refuses the Debian repositories during the builds.

## Set up the environment from scratch

1. Domain name: add `127.0.0.1 guilacol.42.fr` to `/etc/hosts`.
2. Configuration: copy `srcs/.env.example` to `srcs/.env` and adapt it. Keys: `DOMAIN_NAME`, `DATA_PATH`, `MYSQL_DATABASE`, `MYSQL_USER`, `WP_VERSION`, `WP_TITLE`, `WP_ADMIN_USER` (must not contain "admin"), `WP_ADMIN_EMAIL`, `WP_USER`, `WP_USER_EMAIL`.
3. Secrets: create four single-line files in `secrets/`, without trailing newline, letters and digits only (the passwords are inserted in SQL):

```bash
mkdir -p secrets
for name in db_root_password db_password wp_admin_password wp_user_password; do
    read -rsp "Value for $name: " v; echo
    printf '%s' "$v" > "secrets/$name.txt"
done
chmod 600 secrets/*.txt
```

`secrets/` and `srcs/.env` are listed in `.gitignore` and must never be committed.

## Build and launch

`make` creates `$DATA_PATH/mariadb` and `$DATA_PATH/wordpress`, then runs `docker compose -f srcs/docker-compose.yml up -d --build`. Other targets: `stop`, `start`, `down`, `logs`, `clean`, `fclean`, `re`.

## Manage containers and volumes

```bash
docker compose -f srcs/docker-compose.yml ps
docker compose -f srcs/docker-compose.yml logs <service>
docker exec -it mariadb mariadb -uroot -p
docker exec wordpress wp user list --path=/var/www/wordpress --allow-root
docker network inspect inception_inception
docker volume ls
docker volume inspect inception_mariadb_data inception_wordpress_data
```

## Where the data is stored and how it persists

| Data | Named volume | Host folder |
|---|---|---|
| MariaDB databases | `inception_mariadb_data` | `/home/guilacol/data/mariadb` |
| WordPress files | `inception_wordpress_data` | `/home/guilacol/data/wordpress` |

The volumes are Docker named volumes (local driver, `type: none`, `o: bind`, `device:` set to the host folder), so the data survives container removal and reboots. The init scripts are idempotent: MariaDB initialises only if its data directory is empty, and WordPress copies its files, creates `wp-config.php`, installs the site and creates the users only if they do not already exist. To reset the project completely, run `make fclean`.

## Sources layout

- `srcs/requirements/mariadb`: Dockerfile, `conf/99-inception.cnf` (listen on all interfaces), `tools/init.sh` (bootstrap, then `exec mariadbd`).
- `srcs/requirements/wordpress`: Dockerfile (php-fpm, WP-CLI, pinned WordPress), `conf/www.conf` (pool listening on port 9000), `tools/init.sh`.
- `srcs/requirements/nginx`: Dockerfile, `conf/nginx.conf` (template with the domain placeholder), `tools/init.sh` (certificate, then `exec nginx`).
