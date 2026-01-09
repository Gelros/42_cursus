#include "../../includes/push_swap.h"

static int	n_bit(t_list *a)
{
	t_list	*tmp;
	int		val_max;
	int		index_max;
	int		bit;

	val_max = stack_max(a);
	tmp = a;
	bit = 0;
	while (*(int *)tmp->content != val_max)
		tmp = tmp->next;
	index_max = tmp->index;
	while (index_max != 0)
	{
		index_max /= 2;
		bit++;
	}
	return (bit);
}

void	sort_big(t_list **a, t_list **b)
{
	int	bit;
	int	passes;
	int	i;
	int	n_el;

	passes = n_bit(*a);
	bit = 0;
	n_el = ft_lstsize(*a);
	while (passes != 0)
	{
		i = 0;
		while (i != n_el)
		{
			if ((((*a)->index >> bit) & 1) == 0)
				pb(a, b, 1);
			else
				ra(a, 1);
			i++;
		}
		while (*b)
			pa(a, b, 1);
		bit++;
		passes--;
	}
}

void	assign_index(t_list *a)
{
	t_list	*tmp;
	t_list	*first_node;
	int		value;

	first_node = a;
	while (a)
	{
		tmp = first_node;
		value = 0;
		while (tmp)
		{
			if (*(int *)a->content > *(int *)tmp->content)
				value++;
			tmp = tmp->next;
		}
		a->index = value;
		a = a->next;
	}
}
