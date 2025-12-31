#include "../../includes/push_swap.h"

static int	min_pos(t_list *a)
{
	int	min_val;

	min_val = stack_min(a);
	return (stack_pos(a, min_val));
}

void	sort_3(t_list **a)
{
	int	first;
	int	sec;
	int	third;

	first = *(int *)(*a)->content;
	sec = *(int *)(*a)->next->content;
	third = *(int *)(*a)->next->next->content;
	if (first > sec && sec < third && third > first) /* Cas avec 2 1 3 */
		sa(a, 1);
	else if (first > sec && sec > third) /* Cas avec 3 2 1 */
	{
		ra(a, 1);
		sa(a, 1);
	}
	else if (first > sec && sec < third && third < first) /* Cas avec 3 1 2 */
		ra(a, 1);
	else if (first < sec && sec > third && third > first) /* Cas avec 1 3 2 */
	{
		sa(a, 1);
		ra(a, 1);
	}
	else if (first < sec && sec > third && third < first) /* Cas avec 2 3 1 */
		rra(a, 1);
}
void	sort_5(t_list **a, t_list **b)
{
	int	min_val_pos;

	while (ft_lstsize(*a) > 3)
	{
		min_val_pos = min_pos(*a);
		if (min_val_pos < ft_lstsize(*a) / 2)
			while (min_val_pos-- > 0)
				ra(a, 1);
		else
			while (min_val_pos++ < ft_lstsize(*a))
				rra(a, 1);
		pb(a, b, 1);
	}
	sort_3(a);
	while (*b)
		pa(a, b, 1);
}

void	sort_small(t_list **a, t_list **b)
{
	int	size;

	*b = NULL;
	size = ft_lstsize(*a);
	if (size == 2 && *(int *)(*a)->content > *(int *)(*a)->next->content)
		sa(a, 1);
	if (size == 3)
		sort_3(a);
	if (size == 4 || size ==  5)
		sort_5(a, b);
}
