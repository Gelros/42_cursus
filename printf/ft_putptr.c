/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putptr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 15:54:32 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/14 16:57:45 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_base(unsigned long nb)
{
	char	*base;
	int		count;

	count = 0;
	base = "0123456789abcdef";
	if (nb > 15)
		count += ft_base(nb / 16);
	count += ft_putchar(base[nb % 16]);
	return (count);
}

int	ft_putptr(void *ptr)
{
	unsigned long	n;
	int				count;

	if (!ptr)
		return (write(1, "(nil)", 5));
	n = (unsigned long)ptr;
	count = 0;
	count += write(1, "0x", 2);
	count += ft_base(n);
	return (count);
}
