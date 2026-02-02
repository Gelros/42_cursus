/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   fill_stack.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 13:43:51 by guilacol          #+#    #+#             */
/*   Updated: 2026/01/29 17:28:52 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/push_swap.h"

int	has_duplicates(t_list *a)
{
	t_list	*tmp1;
	t_list	*tmp2;

	tmp1 = a;
	while (tmp1)
	{
		tmp2 = tmp1->next;
		while (tmp2)
		{
			if (*(int *)tmp1->content == *(int *)tmp2->content)
				return (0);
			tmp2 = tmp2->next;
		}
		tmp1 = tmp1->next;
	}
	return (1);
}

void	fill_stack(t_list **a, char **args)
{
	t_list	*lst;
	int		*value;
	int		i;

	i = 0;
	while (args[i])
	{
		value = malloc(sizeof(int));
		if (!value)
			return ;
		value[0] = ft_atoi(args[i]);
		lst = ft_lstnew(value);
		if (!lst)
		{
			free(value);
			return ;
		}
		ft_lstadd_back(a, lst);
		i++;
	}
	
}
