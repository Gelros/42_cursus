/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 10:35:30 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/20 15:26:26 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	char	*res;
	size_t	i;

	res = malloc(nmemb * size);
	if (!res)
		return (NULL);
	i = 0;
	while (i < nmemb * size)
	{
		res[i] = 0;
		i++;
	}
	return ((void *)res);
}

char	*ft_is_empty(char *tmp, char *buf)
{
	size_t	len_tmp;
	size_t	len_buf;
	char	*str;

	len_tmp = 0;
	len_buf = 0;
	if (tmp)
		len_tmp = ft_strlen(tmp);
	len_buf = ft_strlen(buf);
	str = ft_calloc(sizeof(char), (len_tmp + len_buf) + 1);
	if (tmp)
		ft_memcpy(str, tmp, len_tmp);
	ft_memcpy(str + len_tmp, buf, len_buf);
	str[len_buf + len_tmp] = '\0';
	free(tmp);
	tmp = NULL;
	return (str);
}

char	*ft_is_nothing(char **buffer, char **tmp)
{
	free(*buffer);
	*buffer = NULL;
	free(*tmp);
	*tmp = NULL;
	return (NULL);
}

char	*ft_end(char **buffer, char **tmp, ssize_t n_bytes)
{
	char	*line;
	char	*tmp2;

	if (ft_strchr(*tmp, '\n') == NULL && *tmp && **tmp && n_bytes == 0)
	{
		line = ft_strdup(*tmp);
		free(*buffer);
		*buffer = NULL;
		free(*tmp);
		*tmp = NULL;
		return (line);
	}
	if (ft_strchr(*tmp, '\n') != NULL)
	{
		line = ft_substr(*tmp, 0, (ft_strlen(*tmp) - ft_strlen(ft_strchr(*tmp,
							'\n') + 1)));
		tmp2 = ft_strdup(ft_strchr(*tmp, '\n') + 1);
		free(*tmp);
		*tmp = ft_strdup(tmp2);
		free(tmp2);
		return (line);
	}
	return (ft_is_nothing(buffer, tmp));
}

char	*get_next_line(int fd)
{
	static char	*tmp;
	char		*buffer;
	ssize_t		n_bytes;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	buffer = NULL;
	n_bytes = 1;
	while (n_bytes != 0)
	{
		if (ft_strchr(tmp, '\n') != NULL)
			return (ft_end(&buffer, &tmp, n_bytes));
		buffer = ft_calloc(sizeof(char), (BUFFER_SIZE) + 1);
		if (!buffer)
			return (NULL);
		n_bytes = read(fd, buffer, BUFFER_SIZE);
		if (n_bytes <= 0)
			break ;
		buffer[n_bytes] = '\0';
		tmp = ft_is_empty(tmp, buffer);
		free(buffer);
		buffer = NULL;
	}
	return (ft_end(&buffer, &tmp, n_bytes));
}

#include <stdio.h>
int	main(void)
{
	char *str = NULL;
	char *buf;

	int fd = open("./file.txt", O_RDONLY);

	str = get_next_line(fd);
	while (str)
	{
		printf("%s",str);
		free(str);
		str = get_next_line(fd);
	}
	return (0);
}