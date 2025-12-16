
NAME        = push_swap

CC          = cc
CFLAGS      = -Wall -Wextra -Werror

INC_DIR     = includes
LIBFT_DIR   = libft
LIBFT       = $(LIBFT_DIR)/libft.a

SRCS        = \
	src/main.c \
	src/parse/parsing.c \
	src/parse/check_errors.c \
	src/parse/fill_stack.c \
	src/stack/stack_utils.c \
	src/stack/stack_utils2.c \
	src/operations/push.c \
	src/operations/swap.c \
	src/operations/rotate.c \
	src/operations/reverse_rotate.c \
	src/algo/sort_small.c \
	src/algo/sort_big.c \
	src/algo/utils_algo.c \
	src/utils/errors.c \
	src/utils/free.c \
	src/utils/utils.c

OBJS        = $(SRCS:.c=.o)

# =========================
# Rules
# =========================

all: $(NAME)

$(NAME): $(OBJS) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJS) $(LIBFT) -o $(NAME)

%.o: %.c
	$(CC) $(CFLAGS) -I$(INC_DIR) -I$(LIBFT_DIR) -c $< -o $@

$(LIBFT):
	$(MAKE) -C $(LIBFT_DIR) bonus

clean:
	rm -f $(OBJS)
	$(MAKE) -C $(LIBFT_DIR) clean

fclean: clean
	rm -f $(NAME)
	$(MAKE) -C $(LIBFT_DIR) fclean

re: fclean all

.PHONY: all clean fclean re
