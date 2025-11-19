# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/14 09:10:22 by guilacol          #+#    #+#              #
#    Updated: 2025/11/14 09:14:59 by guilacol         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

SRCS = ft_putstr.c ft_putptr.c ft_putnbr.c ft_puthex.c ft_putchar.c ft_printf.c

NAME = libftprintf.a

CFLAGS = -Wall -Wextra -Werror -c 

CC = cc

OBJ = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJ)
		ar rc $(NAME) $(OBJ)

%.o: %.c
		$(CC) $(CFLAGS) -c $< -o $@

clean:
		rm -f $(OBJ)

fclean: clean
		rm -f $(NAME)


re: fclean all

.PHONY: all clean fclean re