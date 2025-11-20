/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 11:35:12 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/20 14:52:04 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

size_t	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

char	*ft_strdup(const char *s)
{
	char	*n_str;
	size_t	i;

	n_str = ft_calloc(sizeof(char), (ft_strlen((char *)s) + 1));
	if (!n_str)
		return (NULL);
	i = 0;
	while (s[i])
	{
		n_str[i] = s[i];
		i++;
	}
	n_str[i] = '\0';
	return (n_str);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*string;
	size_t	i;

	if (start >= (unsigned int)ft_strlen((char *)s) || len == 0)
		return (ft_strdup(""));
	string = ft_calloc(sizeof(char), (len + 1));
	if (!string)
		return (NULL);
	i = 0;
	while (s[start] && i < len)
	{
		string[i] = s[start];
		i++;
		start++;
	}
	string[i] = '\0';
	return (string);
}

char	*ft_strchr(const char *s, int c)
{
	size_t	i;

	i = 0;
	if (!s)
		return (NULL);
	while (s[i])
	{
		if (s[i] == (char)c)
			return ((char *)&s[i]);
		i++;
	}
	if (s[i] == '\0' && (char)c == '\0')
		return ((char *)&s[i]);
	return (NULL);
}

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	unsigned char	*temp_dest;
	const char		*temp_src;
	size_t			i;

	if (dest == NULL && src == NULL)
		return (dest);
	temp_dest = dest;
	temp_src = src;
	i = 0;
	while (i < n)
	{
		temp_dest[i] = temp_src[i];
		i++;
	}
	return (dest);
}
