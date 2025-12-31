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
	if (!check_errors(args) && argc > 2)
		return (free_stack(a), 0);
	fill_stack(a, args);
	if (!has_duplicates(*a))
		return (0);
	if (need_free)
		free_split(args);
	return (1);
}
