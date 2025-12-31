#include "../../includes/push_swap.h"

void	rra(t_list **a, int print)
{
	t_list	*last;
	t_list	*post_last;

	if (!*a || !(*a)->next)
		return ;
	last = *a;
	post_last = *a;
	while (last->next)
		last = last->next;
	while (post_last->next->next)
		post_last = post_last->next;
	post_last->next = NULL;
	last->next = *a;
	*a = last;
	if (print)
		write(1, "rra\n", 4);
}

void	rrb(t_list **b, int print)
{
    t_list	*last;
	t_list	*post_last;

	if (!*b || !(*b)->next)
		return ;
	last = *b;
	post_last = *b;
	while (last->next)
		last = last->next;
	while (post_last->next->next)
		post_last = post_last->next;
	post_last->next = NULL;
	last->next = *b;
	*b = last;
	if (print)
		write(1, "rrb\n", 4);
}

void	rrr(t_list **a, t_list **b, int print)
{
    rra(a, 0);
	rrb(b, 0);
	if (print)
		write(1, "rrr\n", 3);
}
