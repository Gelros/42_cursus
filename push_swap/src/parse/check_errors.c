#include "../../includes/push_swap.h"

int	is_valid_number(const char *str)
{
	long	res;
	int		i;
	int		sign;

	res = 0;
	i = 0;
	sign = 1;
	if (str[i] == '+' || str[i] == '-')
	{
		if (str[i++] == '-')
			sign = -1;
	}
	if (!str[i])
		return (0);
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		res = res * 10 + (str[i++] - '0');
		if ((sign == 1 && res > INT_MAX) || (sign == -1 && -res < INT_MIN))
			return (0);
	}
	return (1);
}

int	check_errors(char **args)
{
	int	j;

	j = 0;
	while (args[j])
	{
		if (!is_valid_number(args[j]))
			return (0);
		j++;
	}
	return (1);
}
