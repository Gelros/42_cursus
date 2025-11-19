/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_striteri.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/07 12:29:08 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/08 15:40:45 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_striteri(char *s, void (*f)(unsigned int, char *))
{
	int	i;

	i = 0;
	while (s[i])
	{
		f((unsigned int)i, &s[i]);
		i++;
	}
}

/* void	uppercase(unsigned int i, char *c)
{
	(void)i;
	*c = (char)ft_toupper(*c);
}

int	main(int ac, char **av)
{
	if (ac != 2)
	{
		fprintf(stderr, "Usage: %s <string>\n", av[0]);
		return (1);
	}
	char *str;
	str = av[1];
	printf("Original:\t`%s`\t[%p]\n", str, str);
	ft_striteri(str, uppercase);
	printf("Result:\t\t`%s`\t[%p]\n", str, str);
	return (0);
} */