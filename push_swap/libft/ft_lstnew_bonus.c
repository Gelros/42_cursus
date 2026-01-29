/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstnew_bonus.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/08 11:56:33 by guilacol          #+#    #+#             */
/*   Updated: 2026/01/29 17:28:43 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstnew(void *content)
{
	t_list	*list;

	list = malloc(sizeof(t_list));
	if (!list)
		return (NULL);
	list->content = content;
	list->next = NULL;
	return (list);
}
/* int    main(void)
{
    char    *str = "Hello World";
    t_list    *elem;

    elem = ft_lstnew(str);
    printf("Content: %s\n", (char *)elem->content);
    free(elem);
} */