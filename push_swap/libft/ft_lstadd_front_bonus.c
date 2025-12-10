/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_front.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/08 16:27:12 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/09 11:15:36 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstadd_front(t_list **lst, t_list *new)
{
	if (*lst)
		new->next = *lst;
	*lst = new;
}
/* int	main(void)
{
	t_list *start;
	t_list *new;
	char *content1 = NULL;
	char *content2 = "Hello";

	start = ft_lstnew(content1);
	new = ft_lstnew(content2);
	ft_lstadd_front(&start, new);
	printf("%s\n%s\n", (char *)start->content, (char *)start->next->content);
	free(start->next);
	free(start);
} */