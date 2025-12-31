#include "../../includes/push_swap.h"

int	has_duplicates(t_list *a)
{
	t_list	*tmp1;
	t_list	*tmp2;

	tmp1 = a;
	while (tmp1)
	{
		tmp2 = tmp1->next;
		while (tmp2)
		{
			if (*(int *)tmp1->content == *(int *)tmp2->content)
			{
				ft_lstclear(&a, free);
				printf("Doublon detecté");
				return (0);
			}
			tmp2 = tmp2->next;
		}
		tmp1 = tmp1->next;
	}
	return (1);
}

void	fill_stack(t_list **a, char **args)
{
	t_list	*lst;
	int		*value;
	int		i;

	i = 0;
	while (args[i])
	{
		value = malloc(sizeof(int));
		if (!value)
			return ;
		*value = ft_atoi(args[i]);
		lst = ft_lstnew(value);
		if (!lst)
			return ;
		ft_lstadd_back(a, lst);
		i++;
	}
}
