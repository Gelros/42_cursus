#include "../includes/push_swap.h"

int	main(int argc, char **argv)
{
	t_list	*a;
	t_list	*b;
	/* t_list	*tmp;
	t_list	*tmp2;
	int		i; */

	a = NULL;
	b = NULL;
	if (argc < 2 || !parse_args(argc, argv, &a))
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
	/* tmp2 = b;
	tmp = a;
	i = 0;
	while (tmp)
	{
		printf("a[%d] = %d\n", i, *(int *)tmp->content);
		tmp = tmp->next;
		i++;
	}
	i = 0;
	while (tmp2)
	{
		printf("b[%d] = %d\n", i, *(int *)tmp2->content);
		tmp2 = tmp2->next;
		i++;
	} */
	/* Nettoyage */
	free_all(&a, &b);
	return (0);
}
