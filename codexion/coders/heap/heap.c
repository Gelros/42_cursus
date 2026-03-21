/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 11:01:13 by guilacol          #+#    #+#             */
/*   Updated: 2026/03/21 11:28:53 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/codexion.h"

void	push(t_heap *heap, int id, long priority)
{
	int		i;
	int		parent;
	t_entry	tmp;

	if (heap->size >= 64)
		return ;
	i = heap->size;
	heap->entries[i].id = id;
	heap->entries[i].priority = priority;
	heap->size++;
	while (i > 0)
	{
		parent = (i - 1) / 2;
		if (heap->entries[i].priority < heap->entries[parent].priority)
		{
			tmp = heap->entries[i];
			heap->entries[i] = heap->entries[parent];
			heap->entries[parent] = tmp;
			i = parent;
		}
		else
			break ;
	}
}

static void	swap_down(t_heap *heap, int i)
{
	t_entry	tmp;
	int		s;

	while (1)
	{
		s = i;
		if (i * 2 + 1 < heap->size && heap->entries[i * 2 + 1].priority
			< heap->entries[s].priority)
			s = i * 2 + 1;
		if (i * 2 + 2 < heap->size && heap->entries[i * 2 + 2].priority
			< heap->entries[s].priority)
			s = i * 2 + 2;
		if (s == i)
			break ;
		tmp = heap->entries[i];
		heap->entries[i] = heap->entries[s];
		heap->entries[s] = tmp;
		i = s;
	}
}

t_entry	extract(t_heap *heap)
{
	t_entry	root;

	if (heap->size <= 0)
		return ((t_entry){-1, -1});
	root = heap->entries[0];
	heap->entries[0] = heap->entries[--heap->size];
	if (heap->size > 0)
		swap_down(heap, 0);
	return (root);
}
