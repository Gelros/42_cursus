#include "../includes/push_swap.h"

int	main(int argc, char **argv)
{
	t_list *a;
	t_list *tmp;
	int i;

	a = NULL;
	if (argc < 2 || !parse_args(argc, argv, &a))
	{
		print_error();
		return (1);
	}
	/* Affichage temporaire pour vérifier le contenu de la stack */
	tmp = a;
	i = 0;
	if (is_sorted(tmp))
		return (0);
	while (tmp)
	{
		printf("a[%d] = %d\n", i, *(int *)tmp->content);
		tmp = tmp->next;
		i++;
	}
	/* Nettoyage */
	ft_lstclear(&a, free);
	return (0);
}
