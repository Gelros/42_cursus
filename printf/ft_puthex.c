/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 14:31:43 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/14 16:57:32 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static char	*ft_base(char c)
{
	char	*base;
	char	*base2;

	base = "0123456789abcdef";
	base2 = "0123456789ABCDEF";
	if (c == 'x')
		return (base);
	else
		return (base2);
}

int	ft_puthex(char c, unsigned long n)
{
	int		count;
	char	*base;

	count = 0;
	base = ft_base(c);
	if (n > 15)
		count += ft_puthex(c, n / 16);
	count += ft_putchar(base[n % 16]);
	return (count);
}
