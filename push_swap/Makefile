# =========================
# Variables
# =========================
NAME = push_swap

CC = cc
CFLAGS = -Wall -Wextra -Werror
INCLUDE_DIR = includes
SRC_DIR = src
LIBFT_DIR = libft

# Récupération de tous les fichiers .c du dossier src et ses sous-dossiers
SRC = $(shell find $(SRC_DIR) -name "*.c")
OBJ = $(SRC:.c=.o)

# Libft
LIBFT = $(LIBFT_DIR)/libft.a

# =========================
# Règle par défaut
# =========================
all: $(NAME)

# =========================
# Compilation de libft si nécessaire
# =========================
$(LIBFT):
	@make -C $(LIBFT_DIR)

# =========================
# Compilation de push_swap
# =========================
$(NAME): $(OBJ) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJ) $(LIBFT) -I$(INCLUDE_DIR) -o $(NAME)

# =========================
# Nettoyage
# =========================
clean:
	@rm -f $(OBJ)
	@make clean -C $(LIBFT_DIR)

fclean: clean
	@rm -f $(NAME)
	@make fclean -C $(LIBFT_DIR)

re: fclean all
