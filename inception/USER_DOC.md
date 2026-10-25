# User documentation

## Services provided

| Service | Role | Reachable from outside |
|---|---|---|
| NGINX | Web entrypoint, HTTPS (TLS 1.2/1.3) | Yes, port 443 only |
| WordPress + php-fpm | The website and its administration panel | No (through NGINX) |
| MariaDB | The website database | No (internal network only) |

## Start and stop

From the project root:

- `make`: build and start everything (first start takes about a minute).
- `make stop`: stop the containers, keeping everything.
- `make start`: start them again.
- `make down`: remove the containers and the network. The data is kept.
- `make fclean`: remove everything, **including the website and the database**.

## Access the website and the administration panel

The domain must resolve to the machine: `/etc/hosts` must contain `127.0.0.1 guilacol.42.fr`.

- Website: https://guilacol.42.fr
- Administration panel: https://guilacol.42.fr/wp-admin

The certificate is self-signed, so the browser shows a warning. Accept it to continue. Plain `http://` does not work: only port 443 is open.

## Locate and manage credentials

- User names and non-sensitive settings: `srcs/.env` (`WP_ADMIN_USER`, `WP_USER`, `MYSQL_USER`...).
- Passwords: one file each in `secrets/` (`wp_admin_password.txt`, `wp_user_password.txt`, `db_password.txt`, `db_root_password.txt`).

Neither `secrets/` nor `srcs/.env` is stored in git. Passwords are only read when the database and the site are first created: after editing a password file, run `make fclean` then `make` (this erases the site content). A WordPress account password can also be changed from the administration panel.

## Check that the services are running

```bash
docker compose -f srcs/docker-compose.yml ps
curl -k -I https://guilacol.42.fr
```

- The three containers must be `Up`, and `mariadb` must be `healthy`.
- `curl` must answer `HTTP/1.1 200 OK`.
- If a service misbehaves: `docker compose -f srcs/docker-compose.yml logs <service>`.
