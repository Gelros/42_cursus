/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putptr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 15:54:32 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/14 09:43:57 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "printf.h"
#include <stdio.h>

static int	ft_base(unsigned long nb)
{
	char	*base;
	int		i;
	char	ca;
	char	n;
	int		count;

	i = -1;
	n = '0';
	ca = 'a';
	count = 0;
	base = malloc(sizeof(char) * 16);
	if (!base)
		return (0);
	while (++i < 10)
		base[i] = n++;
	while (i < 16)
		base[i++] = ca++;
	if (nb > 16)
		count += ft_base(nb / 16);
	count += ft_putchar(base[nb % 16]);
	return (count);
}

int	ft_putptr(void *ptr)
{
	long	n;
	int		count;

	if (!ptr)
		return (write(1, "(nil)", 5));
	n = (unsigned long)ptr;
	count = 0;
	count += write(1, "0x", 2);
	count += ft_base(n);
	return (count);
}
