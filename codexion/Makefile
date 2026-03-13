# ── Output ────────────────────────────────────────────────────────────────── #

NAME		:= codexion

# ── Compiler & Flags ──────────────────────────────────────────────────────── #

CC			:= cc
CFLAGS		:= -Wall -Wextra -Werror -pthread
INCLUDES	:= -I coders/includes -I coders/heap

# ── Sources ───────────────────────────────────────────────────────────────── #

SRCS_DIR	:= coders/srcs
HEAP_DIR	:= coders/heap

SRCS		:= $(SRCS_DIR)/main.c		\
			   $(SRCS_DIR)/init.c		\
			   $(SRCS_DIR)/coder.c		\
			   $(SRCS_DIR)/dongle.c		\
			   $(SRCS_DIR)/scheduler.c	\
			   $(SRCS_DIR)/monitor.c	\
			   $(SRCS_DIR)/log.c		\
			   $(SRCS_DIR)/time_utils.c	\
			   $(SRCS_DIR)/free.c		\
			   $(HEAP_DIR)/heap.c

# ── Objects ───────────────────────────────────────────────────────────────── #

OBJS_DIR	:= objs
OBJS		:= $(patsubst $(SRCS_DIR)/%.c, $(OBJS_DIR)/%.o, \
			   $(filter $(SRCS_DIR)/%.c, $(SRCS))) \
			   $(patsubst $(HEAP_DIR)/%.c, $(OBJS_DIR)/%.o, \
			   $(filter $(HEAP_DIR)/%.c, $(SRCS)))

# ── Colors ────────────────────────────────────────────────────────────────── #

RESET		:= \033[0m
BOLD		:= \033[1m
GREEN		:= \033[32m
YELLOW		:= \033[33m
CYAN		:= \033[36m
RED			:= \033[31m

# ── Rules ─────────────────────────────────────────────────────────────────── #

all: $(NAME)

$(NAME): $(OBJS)
	@$(CC) $(CFLAGS) $(OBJS) -o $(NAME)
	@echo "$(BOLD)$(GREEN)✓ $(NAME) compiled successfully$(RESET)"

$(OBJS_DIR)/%.o: $(SRCS_DIR)/%.c
	@mkdir -p $(OBJS_DIR)
	@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@
	@echo "$(CYAN)  compiling $<...$(RESET)"

$(OBJS_DIR)/%.o: $(HEAP_DIR)/%.c
	@mkdir -p $(OBJS_DIR)
	@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@
	@echo "$(CYAN)  compiling $<...$(RESET)"

clean:
	@rm -rf $(OBJS_DIR)
	@echo "$(YELLOW)  object files removed$(RESET)"

fclean: clean
	@rm -f $(NAME)
	@echo "$(RED)  $(NAME) removed$(RESET)"

re: fclean all

# ── Phony ─────────────────────────────────────────────────────────────────── #

.PHONY: all clean fclean re