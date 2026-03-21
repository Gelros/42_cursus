/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.h                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 11:23:10 by guilacol          #+#    #+#             */
/*   Updated: 2026/03/21 11:23:12 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

typedef struct s_entry
{
	int		id;
	long	priority;
}			t_entry;

typedef struct s_heap
{
	t_entry	entries[64];
	int		size;
}			t_heap;
