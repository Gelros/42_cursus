/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_utils2.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 13:44:07 by guilacol          #+#    #+#             */
/*   Updated: 2026/01/29 13:44:09 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/push_swap.h"

void	free_stack(t_list **stack)
{
	t_list	*tmp;

	if (!stack || !*stack)
        return ;
	while (*stack)
	{
		tmp = (*stack)->next;
		if ((*stack)->content)
            free((*stack)->content);
		free(*stack);
		*stack = tmp;
	}
	*stack = NULL;
}
