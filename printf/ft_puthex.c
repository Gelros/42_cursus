/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 14:31:43 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/13 15:39:35 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "printf.h"

static char	*ft_base(char c)
{
	char	*base;
	int		i;
	char	ca;
	char	n;

	i = -1;
	n = '0';
	base = malloc(sizeof(char) * 16);
	if (!base)
		return (NULL);
	while (++i < 10)
		base[i] = n++;
	if (c == 'X')
	{
		ca = 'A';
		while (i < 16)
			base[i++] = ca++;
	}
	if (c == 'x')
	{
		ca = 'a';
		while (i < 16)
			base[i++] = ca++;
	}
	return (base);
}

int	ft_puthex(char c, unsigned long n)
{
	int		count;
	char	*base;

	count = 0;
	base = ft_base(c);
	if (n > 16)
		count += ft_puthex(c, n / 16);
	count += ft_putchar(base[n % 16]);
	return (count);
}
