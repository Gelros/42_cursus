/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/05 15:12:48 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/10 18:34:47 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *s, int c)
{
	int	i;

	i = ft_strlen(s);
	if ((unsigned char)c == '\0')
		return ((char *)s + ft_strlen(s));
	while (--i >= 0)
		if ((unsigned char)s[i] == (unsigned char)c)
			return ((char *)&s[i]);
	return (NULL);
}
/* int    main(int arc, char **arv)
{
	char    *dest;
	char    *dest2;

	if (arc < 2)
	{
		printf("please take tow arguments\n");
		return (0);
	}

	dest = strrchr(arv[1], arv[2][0]);
	dest2 = ft_strrchr(arv[1], arv[2][0]);
	printf("result or : %s\nmy result : %s\n", dest, dest2);
	return (0);
} */