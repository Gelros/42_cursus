COMPOSE = docker compose -f srcs/docker-compose.yml

-include srcs/.env
DATA_PATH ?= /home/$(USER)/data

all: up

up:
	mkdir -p $(DATA_PATH)/mariadb $(DATA_PATH)/wordpress
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

start:
	$(COMPOSE) start

stop:
	$(COMPOSE) stop

logs:
	$(COMPOSE) logs -f

clean: down

fclean:
	$(COMPOSE) down -v --rmi all
	sudo rm -rf $(DATA_PATH)/mariadb/* $(DATA_PATH)/wordpress/*

re: fclean all

.PHONY: all up down start stop logs clean fclean re
