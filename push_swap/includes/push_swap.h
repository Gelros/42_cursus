#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

/* ==== Includes ==== */

# include "../libft/libft.h"
# include <limits.h>
# include <stdio.h>
# include <stdlib.h>
# include <unistd.h>

/* ==== Parsing ==== */

int		parse_args(int argc, char **argv, t_list **a);
char	**split_arguments(int argc, char **argv);
int		check_errors(char **args);
int		is_valid_number(const char *str);
int		has_duplicates(t_list *a);
void	fill_stack(t_list **a, char **args);

/* ==== Stack utils ==== */

int		get_value(t_list *node);
int		stack_min(t_list *a);
int		stack_max(t_list *a);
int		stack_index_of(t_list *a, int value);
void	free_stack(t_list **stack);

/* ==== Operations ==== */

void	sa(t_list **a, int print);
void	sb(t_list **b, int print);
void	ss(t_list **a, t_list **b, int print);

void	pa(t_list **a, t_list **b, int print);
void	pb(t_list **a, t_list **b, int print);

void	ra(t_list **a, int print);
void	rb(t_list **b, int print);
void	rr(t_list **a, t_list **b, int print);

void	rra(t_list **a, int print);
void	rrb(t_list **b, int print);
void	rrr(t_list **a, t_list **b, int print);

/* ==== Algorithms ==== */

void	sort_small(t_list **a, t_list **b);
void	sort_big(t_list **a, t_list **b);
void	assign_index(t_list *a); // utile pour radix

/* ==== Utils ==== */

void	print_error(void);
void	free_all(t_list **a, t_list **b, char **args);
void	free_split(char **args);

#endif
