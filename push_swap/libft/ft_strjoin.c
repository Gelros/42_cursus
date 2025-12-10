/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 09:50:44 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/08 13:14:56 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	len_join(char const *s1, char const *s2)
{
	size_t	len_s1;
	size_t	len_s2;
	size_t	len_max;

	len_s1 = ft_strlen(s1);
	len_s2 = ft_strlen(s2);
	len_max = len_s1 + len_s2;
	return (len_max);
}

char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*n_str;
	size_t	len_max;
	int		i;
	int		j;

	if (!s1 || !s2)
		return (NULL);
	len_max = len_join(s1, s2);
	n_str = malloc(sizeof(char) * len_max + 1);
	if (!n_str)
		return (NULL);
	i = -1;
	while (++i < (int)ft_strlen(s1))
		n_str[i] = s1[i];
	j = 0;
	while (i < (int)len_max)
	{
		n_str[i] = s2[j];
		i++;
		j++;
	}
	n_str[i] = '\0';
	return (n_str);
}

/* int	main(int arc, char **arv)
{
	if (arc < 2)
	{
		printf("please take tow arguments\n");
		return (0);
	}

	char *test2 = ft_strjoin(arv[1], arv[2]);

	printf("result me : %s\n", test2);

	free(test2);

	return (0);
} */