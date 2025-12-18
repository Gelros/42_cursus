#include "../../includes/push_swap.h"

int	get_value(t_list *node)
{
	if (!node || !node->content)
		return (0);
	return (*(int *)node->content);
}

int	stack_min(t_list *a)
{
	int		min;
	t_list	*tmp;

	if (!a || !a->content)
		return (0);
	min = *(int *)a->content;
	tmp = a->next;
	while (tmp)
	{
		if (*(int *)tmp->content < min)
			min = *(int *)tmp->content;
		tmp = tmp->next;
	}
	return (min);
}

int	stack_max(t_list *a)
{
	int		max;
	t_list	*tmp;

	if (!a || !a->content)
		return (0);
	max = *(int *)a->content;
	tmp = a->next;
	while (tmp)
	{
		if (*(int *)tmp->content > max)
			max = *(int *)tmp->content;
		tmp = tmp->next;
	}
	return (max);
}

int	stack_pos(t_list *a, int value)
{
	t_list	*tmp;
	int		pos;

	tmp = a;
	pos = 0;
	while (tmp)
	{
		if (*(int *)tmp->content == value)
			return (pos);
		pos++;
		tmp = tmp->next;
	}
	return (-1);
}

int	is_sorted(t_list *a)
{
	t_list	*tmp;

	if (!a)
		return (1);
	tmp = a;
	while (tmp && tmp->next)
	{
		if (*(int *)tmp->content > *(int *)tmp->next->content)
			return (0);
		tmp = tmp->next;
	}
	return (1);
}
