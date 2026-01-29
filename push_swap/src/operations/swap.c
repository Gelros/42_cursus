/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 13:43:37 by guilacol          #+#    #+#             */
/*   Updated: 2026/01/29 13:56:50 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/push_swap.h"

void	sa(t_list **a, int print)
{
	int	tmp;

	tmp = *(int *)(*a)->content;
	*(int *)(*a)->content = *(int *)(*a)->next->content;
	*(int *)(*a)->next->content = tmp;
	if (print)
		write(1, "sa\n", 3);
}

void	sb(t_list **b, int print)
{
	int	tmp;

	tmp = *(int *)(*b)->content;
	*(int *)(*b)->content = *(int *)(*b)->next->content;
	*(int *)(*b)->next->content = tmp;
	if (print)
		write(1, "sb\n", 3);
}

void	ss(t_list **a, t_list **b, int print)
{
	sa(a, 0);
	sb(b, 0);
	if (print)
		write(1, "ss\n", 3);
}
