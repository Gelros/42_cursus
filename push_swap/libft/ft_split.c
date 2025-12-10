/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 14:23:22 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/08 14:50:03 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	is_charset(char s, char c)
{
	if (s == c)
		return (1);
	return (0);
}

static size_t	count_words(char const *s, char c)
{
	size_t	i;
	size_t	count_word;

	i = 0;
	count_word = 0;
	while (s[i])
	{
		if (s[i] != c)
		{
			count_word++;
			while (s[i] && s[i] != c)
				i++;
		}
		else
			i++;
	}
	return (count_word);
}

char	*ft_strndup(const char *s, int len)
{
	char	*n_str;
	size_t	i;

	n_str = malloc(sizeof(char) * len + 1);
	if (!n_str)
		return (NULL);
	i = 0;
	while (i < (size_t)len)
	{
		n_str[i] = s[i];
		i++;
	}
	n_str[i] = '\0';
	return (n_str);
}

static char	**ft_free(char **str, int len)
{
	int	i;

	i = 0;
	while (i < len)
	{
		free(str[i]);
		i++;
	}
	free(str);
	return (NULL);
}

char	**ft_split(char const *s, char c)
{
	int		i;
	int		len;
	char	**n_str;

	n_str = malloc(sizeof(char *) * (count_words(s, c) + 1));
	if (!n_str)
		return (NULL);
	i = 0;
	while (*s)
	{
		if (!is_charset(*s, c))
		{
			len = 0;
			while (s[len] && !is_charset(s[len], c))
				len++;
			n_str[i] = ft_strndup(s, len);
			if (!n_str[i++])
				return (ft_free(n_str, i));
			s += len;
		}
		else
			s++;
	}
	n_str[i] = NULL;
	return (n_str);
}

/* int    main(int arc, char **arv)
{
	(void)arc;
	(void)arv;

	char **tab;
	int    i;

	tab = ft_split(arv[1], arv[2][0]);
	for(i = 0; i <= (int)count_words(arv[1], arv[2][0]); i++)
	{
		printf("tab[%d] : %s\n", i, tab[i]);
		free(tab[i]);
	}

	free(tab);
	return (0);
} */