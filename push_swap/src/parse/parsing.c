#include "../../includes/push_swap.h"

char	**split_arguments(int argc, char **argv)
{
	if (argc == 2)
		return (ft_split(argv[1], ' '));
	else
		return (argv + 1);
}

int	parse_args(int argc, char **argv, t_list **a)
{
	char	**args;
	int		need_free;

	need_free = 0;
	args = split_arguments(argc, argv);
	if (argc == 2)
		need_free = 1;
	if (!args)
		return (0);
	if (!check_errors(args) && argc == 2)
		return (free_split(args), 0);
	fill_stack(a, args);
	if (!has_duplicates(*a))
		return (0);
	if (need_free)
		free_split(args);
	return (1);
}

int	main(int argc, char **argv)
{
	t_list	*a;
	t_list	*tmp;
	int		i;

	a = NULL;
	if (argc < 2)
	{
		print_error();
		return (1);
	}
	if (!parse_args(argc, argv, &a))
	{
		print_error();
		return (1);
	}
	/* Affichage temporaire pour vérifier le contenu de la stack */
	tmp = a;
	i = 0;
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
