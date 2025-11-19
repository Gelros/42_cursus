/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 10:35:30 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/19 17:40:04 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*ft_is_empty(char *tmp, char *buf, ssize_t size)
{
	ssize_t	len;
	char	*tmp2;

	if (!tmp)
		tmp = ft_strdup(buf);
	else
	{
		tmp2 = ft_strdup(tmp);
		free(tmp);
		len = ft_strlen(buf) + ft_strlen(tmp2);
		tmp = malloc(sizeof(char) * len + 1);
		if (!tmp)
			return (NULL);
		tmp = ft_strjoin(tmp2, buf);
		free(tmp2);
	}
	return (tmp);
}

char	*ft_end(char **buffer, char **tmp, ssize_t n_bytes)
{
	char	*line;
	char	*tmp2;

	if (**tmp && *tmp && n_bytes == 0)
	{
		line = ft_strdup(*tmp);
		free(*tmp);
		free(*buffer);
		*buffer = NULL;
		*tmp = NULL;
	}
	else
	{
		line = ft_substr(*tmp, 0, (ft_strlen(*tmp) - ft_strlen(ft_strchr(*tmp,
							'\n') + 1)));
		tmp2 = ft_strdup(ft_strchr(*tmp, '\n') + 1);
		free(*tmp);
		*tmp = ft_strdup(tmp2);
		free(tmp2);
	}
	return (line);
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
		buffer = malloc(sizeof(char) * (BUFFER_SIZE));
		if (!buffer)
			return (NULL);
		n_bytes = read(fd, buffer, BUFFER_SIZE);
		tmp = ft_is_empty(tmp, buffer, n_bytes);
		free(buffer);
		buffer = NULL;
	}
	return (ft_end(&buffer, &tmp, n_bytes));
}

int	main(void)
{
	char *str = NULL;
	char *buffer = NULL;

	int fd = open("./file.txt", O_RDONLY);
	str = get_next_line(fd);
	printf("%s", str);
	str = get_next_line(fd);
	printf("%s", str);

	/* while (str)
	{
		printf("%s", str);
		str = get_next_line(fd);
	} */
	free(str);
	return (0);
}