/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/07 12:11:27 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/07 12:28:25 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
	char	*n_str;
	int		i;
	int		size;

	i = 0;
	size = ft_strlen(s);
	n_str = malloc(sizeof(char) * size + 1);
	if (!n_str)
		return (NULL);
	while (s[i])
	{
		n_str[i] = f((unsigned int)i, s[i]);
		i++;
	}
	n_str[i] = '\0';
	return (n_str);
}
