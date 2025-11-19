/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 15:41:40 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/14 09:48:25 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "printf.h"
#include <stdio.h>

static int	ft_format(va_list ap, char c)
{
	int	count;

	count = 0;
	if (c == '%')
		return (count += ft_putchar('%'));
	else if (c == 'd' || c == 'i')
		return (count += ft_putnbr((int)va_arg(ap, int)));
	else if (c == 's')
		return (count += ft_putstr((char *)va_arg(ap, char *)));
	else if (c == 'c')
		return (count += ft_putchar((int)va_arg(ap, int)));
	else if (c == 'x' || c == 'X')
		return (count += ft_puthex(c, (unsigned int)va_arg(ap, unsigned int)));
	else if (c == 'p')
		return (count += ft_putptr((void *)va_arg(ap, void *)));
	else if (c == 'u')
		return (count += ft_putnbr((unsigned int)va_arg(ap, unsigned int)));
	else
	{
		ft_putchar('%');
		ft_putchar(c);
		return (2);
	}
}

int	ft_printf(const char *str, ...)
{
	va_list	ap;
	int		i;
	int		count;

	va_start(ap, str);
	i = 0;
	count = 0;
	while (str[i])
	{
		if (str[i] == '%' && str[i + 1])
		{
			count += ft_format(ap, str[i + 1]);
			i++;
		}
		else
			count += ft_putchar(str[i]);
		i++;
	}
	va_end(ap);
	return (count);
}
/* #include <stdio.h>

int	main(void)
{
	char *str;
	str = "hello";
	printf("******TEST FT_PRINTF******\n");

	int size_ft;
	printf("\n");

	size_ft = ft_printf("Test avec un 'a' = %c\n", 'a');
	printf("Taille = %d\n", size_ft);

	size_ft = ft_printf("Test avec un 2 pourcent = %%\n");
	printf("Taille = %d\n", size_ft);

	size_ft = ft_printf("Test avec un INT = %u\n", 25);
	printf("Taille = %d\n", size_ft);

	size_ft = ft_printf("Test avec un INT negatif = %d\n", -25);
	printf("Taille = %d\n", size_ft);

	size_ft = ft_printf("Test avec un CHAR * = %s\n", "hello");
	printf("Taille = %d\n", size_ft);

	size_ft = ft_printf("Test HEXA = %x\n", 100000);
	printf("Taille = %d\n", size_ft);

	size_ft = ft_printf("Test avec aucun arg valable '%llll'\n");
	printf("Taille = %d\n", size_ft);

	size_ft = ft_printf("Test avec un pointeur = %p\n", str);
	printf("Taille = %d\n", size_ft);

	size_ft = ft_printf("Test avec un char * NULL = %s\n", NULL);
	printf("Taille = %d\n", size_ft);

	size_ft = ft_printf("Test avec un pointeur NULL = %p\n", NULL);
	printf("Taille = %d\n", size_ft);

	printf("\n");
	printf("\n");

	printf("******TEST PRINTF******\n");

	int size;
	printf("\n");

	size = printf("Test avec un 'a' = %c\n", 'a');
	printf("Taille = %d\n", size);

	size = printf("Test avec un 2 pourcent = %%\n");
	printf("Taille = %d\n", size);

	size = printf("Test avec un INT = %u\n", 25);
	printf("Taille = %d\n", size);

	size = printf("Test avec un INT negatif = %d\n", -25);
	printf("Taille = %d\n", size);

	size = printf("Test avec un CHAR * = %s\n", "hello");
	printf("Taille = %d\n", size);

	size = printf("Test HEXA = %x\n", 100000);
	printf("Taille = %d\n", size);

	size = printf("Test avec aucun arg valable '%llll'\n");
	printf("Taille = %d\n", size);

	size = printf("Test avec un pointeur = %p\n", str);
	printf("Taille = %d\n", size);

	size = printf("Test avec un char * NULL = %s\n", NULL);
	printf("Taille = %d\n", size);

	size = printf("Test avec un pointeur NULL = %p\n", NULL);
	printf("Taille = %d\n", size);
} */