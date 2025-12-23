#include "../includes/push_swap.h"

int	main(int argc, char **argv)
{
	t_list	*a;
	t_list	*b;
	t_list	*tmp;
	t_list	*tmp2;
	int		i;

	a = NULL;
	b = NULL;
	if (argc < 2 || !parse_args(argc, argv, &a))
	{
		print_error();
		return (1);
	}
	/* Affichage temporaire pour vérifier le contenu de la stack */
	tmp = a;
	tmp2 = b;
	i = 0;
	if (is_sorted(tmp))
		return (free_stack(&a), 0);
	while (tmp)
	{
		printf("Avant a[%d] = %d\n", i, *(int *)tmp->content);
		tmp = tmp->next;
		i++;
	}
	i = 0;
	while (tmp2)
	{
		printf("Avant b[%d] = %d\n", i, *(int *)tmp2->content);
		tmp2 = tmp2->next;
		i++;
	}
	printf("\n");
    printf("\n");
    printf("\n");
	printf("\n");
	ra(&a,1);
	tmp2 = b;
	tmp = a;
	i = 0;
	while (tmp)
	{
		printf("apres a[%d] = %d\n", i, *(int *)tmp->content);
		tmp = tmp->next;
		i++;
	}
	i = 0;
    printf("\n");
    printf("\n");
	while (tmp2)
	{
		printf("Apres b[%d] = %d\n", i, *(int *)tmp2->content);
		tmp2 = tmp2->next;
		i++;
	}
	/* Nettoyage */
	free_all(&a, &b);
	return (0);
}
