/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 16:46:00 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/14 16:47:58 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <stdlib.h>
# include <unistd.h>

int	ft_putchar(char c);
int	ft_putnbr(long nb);
int	ft_putstr(char *s);
int	ft_puthex(char c, unsigned long n);
int	ft_putptr(void *ptr);
int	ft_printf(const char *str, ...);

#endif