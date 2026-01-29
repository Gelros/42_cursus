/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 13:43:31 by guilacol          #+#    #+#             */
/*   Updated: 2026/01/29 13:56:42 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/push_swap.h"

void	ra(t_list **a, int print)
{
	t_list	*tmp;
	t_list	*last;

	if (!*a || !(*a)->next)
		return ;
	tmp = *a;
	*a = (*a)->next;
	tmp->next = NULL;
	last = *a;
	while (last->next)
		last = last->next;
	last->next = tmp;
	if (print)
		write(1, "ra\n", 3);
}

void	rb(t_list **b, int print)
{
	t_list	*tmp;
	t_list	*last;

	if (!*b || !(*b)->next)
		return ;
	tmp = *b;
	*b = (*b)->next;
	tmp->next = NULL;
	last = *b;
	while (last->next)
		last = last->next;
	last->next = tmp;
	if (print)
		write(1, "rb\n", 3);
}

void	rr(t_list **a, t_list **b, int print)
{
	ra(a, 0);
	rb(b, 0);
	if (print)
		write(1, "rr\n", 3);
}
