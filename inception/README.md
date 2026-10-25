*This project has been created as part of the 42 curriculum by guilacol.*

# Inception

## Description

Inception sets up a small web infrastructure with Docker Compose inside a Debian virtual machine. Three services run in dedicated containers, each built from its own Dockerfile on `debian:bookworm`:

- **NGINX**: the only entrypoint, reachable on port 443 with TLS 1.2 or 1.3 only.
- **WordPress + php-fpm**: the website, without any web server inside the container.
- **MariaDB**: the database, without any web server inside the container.

Two named volumes persist the database and the website files under `/home/guilacol/data`. A dedicated Docker network connects the containers, and passwords are provided as Docker secrets.

## Instructions

Prerequisites: a Debian virtual machine with Docker Engine, the Docker Compose plugin, `make` and `git`.

1. Clone the repository.
2. Create `srcs/.env` and the files of `secrets/` (see `DEV_DOC.md`).
3. Add `127.0.0.1 guilacol.42.fr` to `/etc/hosts`.
4. Run `make`, then open `https://guilacol.42.fr` (accept the self-signed certificate warning).

| Command | Effect |
|---|---|
| `make` | Create data folders, build the images and start everything |
| `make stop` / `make start` | Stop / restart the containers |
| `make down` | Remove the containers and the network (data is kept) |
| `make fclean` | Remove containers, images, volumes **and the data** |
| `make re` | `fclean` followed by `make` |

More details: `USER_DOC.md` (usage) and `DEV_DOC.md` (development).

## Project description

### Docker and the sources included

Docker runs each service as an isolated process (a container) started from an image built by our own Dockerfile. No ready-made image is pulled: only the base `debian:bookworm` is used.

### Main design choices

- **Base image**: `debian:bookworm` (Debian 12), the penultimate stable release since Debian 13 is the current one. A precise tag is used, never `latest`.
- **PID 1**: every init script ends with `exec`, so the real service receives the stop signals. NGINX runs with `daemon off;` and php-fpm with `-F`. No `tail -f`, `sleep infinity` or infinite loop is used.
- **Startup order**: a MariaDB `healthcheck` and `depends_on: condition: service_healthy` start WordPress only when the database answers.
- **MariaDB initialisation**: done in `--bootstrap` mode (SQL read from standard input, no background process). The script is idempotent: it initialises only if the data directory is empty.
- **Least privilege**: WordPress connects with a dedicated user limited to its own database, never with `root`.
- **TLS certificate**: self-signed, generated when the NGINX container starts, so the private key is not stored in an image layer.

### Comparisons

**Virtual machines vs Docker.** A VM embeds a full operating system with its own kernel on top of a hypervisor: strong isolation, but heavy and slow to start. A container shares the host kernel and isolates only a process: it starts in seconds and uses few resources, with weaker isolation. This project runs containers inside a VM.

**Secrets vs environment variables.** Environment variables are visible through `docker inspect`, `env`, and are inherited by child processes. Docker secrets are mounted as read-only files in `/run/secrets/` and do not appear in the environment. Therefore `.env` only holds non-sensitive values (domain name, user names) and passwords live in `secrets/`.

**Docker network vs host network.** A user-defined bridge network isolates the containers and lets them reach each other by service name through Docker's internal DNS. With the host network, a container uses the host's network stack directly: no isolation and port conflicts. It is forbidden here, as are `links`.

**Docker volumes vs bind mounts.** A named volume is managed by Docker, while a bind mount maps a host path directly into the container. The subject requires named volumes whose data lives in `/home/guilacol/data`: they are declared as named volumes using the `local` driver with the `device` option pointing to that folder.

## Resources

- Docker documentation: https://docs.docker.com/
- Docker Compose file reference: https://docs.docker.com/compose/
- NGINX documentation: https://nginx.org/en/docs/
- PHP-FPM manual: https://www.php.net/manual/en/install.fpm.php
- MariaDB Knowledge Base: https://mariadb.com/kb/en/
- WP-CLI handbook: https://wp-cli.org/
- OpenSSL documentation: https://www.openssl.org/docs/

### Use of AI

An AI assistant (Claude) was used as a tutor and pair-programming aid, for:

- explaining concepts (containers, Compose, PID 1, TLS, secrets, volumes);
- drafting first versions of the Dockerfiles, the init scripts, the Compose file and the Makefile;
- diagnosing errors from logs (for example a virtual machine clock drift that broke `apt`, and the MariaDB initialisation being skipped because the Debian package pre-initialises its data directory);
- drafting this documentation.

Every file was built and tested on the virtual machine by the author, who reviewed each line in order to be able to explain it. No secret value was shared with the AI.
