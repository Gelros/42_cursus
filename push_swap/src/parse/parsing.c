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
	char **args;

	args = split_arguments(argc, argv);
	if (!args)
		return (0);
	if (!check_errors(args))
		return (free_split(args), 0);
	fill_stack(a, args);
	free_split(args);
    return (1);
}