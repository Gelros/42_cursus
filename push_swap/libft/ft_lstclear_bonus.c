/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstclear.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/09 15:07:02 by guilacol          #+#    #+#             */
/*   Updated: 2025/11/10 09:13:11 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstclear(t_list **lst, void (*del)(void*))
{
	t_list	*i;
	t_list	*tmp;

	i = *lst;
	while (i)
	{
		tmp = i->next;
		ft_lstdelone(i, del);
		i = tmp;
	}
	*lst = NULL;
}
