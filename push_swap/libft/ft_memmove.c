/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/04 13:52:55 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/11 10:26:02 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t size)
{
	const char	*temp_src;
	char		*temp_dest;
	size_t		i;

	if (!dest && !src)
		return (NULL);
	temp_src = src;
	temp_dest = dest;
	i = -1;
	if (temp_dest == temp_src)
		return (dest);
	else if (temp_dest > temp_src)
	{
		while (size > 0)
		{
			size--;
			temp_dest[size] = temp_src[size];
		}
	}
	else
	{
		while (++i < size)
			temp_dest[i] = temp_src[i];
	}
	return (dest);
}
