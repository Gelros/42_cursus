/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/04 16:45:50 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/08 10:13:35 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	dst_len;
	size_t	src_len;
	size_t	i;

	dst_len = ft_strlen(dst);
	src_len = ft_strlen(src);
	i = 0;
	if (dst_len >= size)
		return (src_len + size);
	while (dst_len + i < size - 1 && src[i])
	{
		dst[dst_len + i] = src[i];
		i++;
	}
	dst[dst_len + i] = '\0';
	return (dst_len + src_len);
}
/* #include <bsd/string.h>
int	main(int ac, char **av)
{
	size_t	res;
	size_t	size;
	char	dst[100];

	if (ac != 4)
	{
		fprintf(stderr, "Usage: %s <dst> <src> <buffer>\n", av[0]);
		return (1);
	}
	snprintf(dst, sizeof(dst), "%s", av[1]);
	size = (size_t)ft_atoi(av[3]);
	res = ft_strlcat(dst, av[2], size);
	printf("String:\t`%s`\n", dst);
	printf("Length:\t%zu\n", res);
	return (0);
} */