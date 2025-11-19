/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/05 16:17:59 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/10 18:31:13 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	malloc_size(char const *s, unsigned int start, size_t len)
{
	size_t	s_size;

	s_size = ft_strlen(s);
	if (start >= s_size)
		return (1);
	s_size = ft_strlen(&s[start]);
	if (s_size < len)
		return (s_size + 1);
	else
		return (len + 1);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*string;
	size_t	i;
	int		size;

	if (start >= (unsigned int)ft_strlen(s))
		return (ft_strdup(""));
	size = malloc_size(s, start, len);
	string = malloc(sizeof(char) * (size));
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

/* int    main(int arc, char **arv)
{
	if (arc < 2)
	{
		printf("please take tow arguments\n");
		return (0);
	}

	char *test2 = ft_substr(arv[1], atoi(arv[2]), atoi(arv[3]));

	printf("result me : %s\n", test2);

	free(test2);

	return (0);
} */