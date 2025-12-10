/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/05 09:46:09 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/08 12:23:31 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_strncmp(const char *s1, const char *s2, size_t n)
{
	unsigned int	i;
	unsigned char	*str;
	unsigned char	*str2;

	str = (unsigned char *)s1;
	str2 = (unsigned char *)s2;
	i = 0;
	while (i < n)
	{
		if (str[i] != str2[i])
			return (str[i] - str2[i]);
		if (!str[i])
			break ;
		i++;
	}
	return (0);
}

/* int main(int ac, char **av)
{
	char *str1;
	char *str2;
	int n;

	str1 = av[1]; 
	str2 = av[2];
	n = atoi(av[3]); 
	if (ac != 4)
		return (0);
	else
	{
		printf("True function = %d\n", strncmp(str1, str2, n));
		printf("ft function = %d\n", ft_strncmp(str1, str2, n));
	}
	return (0);
} */