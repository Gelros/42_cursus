#include "../../includes/push_swap.h"

void	free_split(char **args)
{
	int i;

	if (!args)
		return ;

	i = 0;
	while (args[i])
	{
		free(args[i]);
		i++;
	}
	free(args);
}
