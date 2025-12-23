#include "../../includes/push_swap.h"

void	sa(t_list **a, int print)
{
	t_list	*tmp;

	tmp = (*a)->next->content;
	if (!tmp || tmp->next == NULL)
		return ;
	(*a)->next->content = (*a)->content;
	(*a)->content = tmp;
	if (print)
		write(1, "sa\n", 3);
}
void	sb(t_list **b, int print)
{
	t_list	*tmp;

	tmp = (*b)->next->content;
	if (!tmp || tmp->next == NULL)
		return ;
	(*b)->next->content = (*b)->content;
	(*b)->content = tmp;
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
