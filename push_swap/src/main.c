/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 13:44:33 by guilacol          #+#    #+#             */
/*   Updated: 2026/01/29 17:16:45 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/push_swap.h"

int	main(int argc, char **argv)
{
	t_list	*a;
	t_list	*b;

	a = NULL;
	b = NULL;
	if (argc <= 2 && !is_split(argv))
		return (0);
	if (!parse_args(argc, argv, &a))
	{
		print_error();
		return (1);
	}
	assign_index(a);
	if (is_sorted(a))
		return (free_stack(&a), 0);
	if (ft_lstsize(a) > 5)
		sort_big(&a, &b);
	else
		sort_small(&a, &b);
	return (free_all(&a, &b), 0);
}
