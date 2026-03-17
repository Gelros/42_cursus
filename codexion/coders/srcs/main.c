#include "../includes/codexion.h"

static int	parsing(int ac, char **av)
{
	int	i;

	i = 0;
	while (++i < ac)
	{
		if (i == 1 || i == 6)
		{
			if (atoi(av[i]) < 1)
				return (1);
		}
		else if ((i >= 2 && i <= 5) || i == 7)
		{
			if (atoi(av[i]) < 0)
				return (1);
		}
		else
		{
			if (strcmp(av[i], "fifo") != 0 && strcmp(av[i], "edf") != 0)
				return (1);
		}
	}
	return (0);
}

static int	launch(char **av)
{
	t_params	param;
	t_simu		simu;
	int			i;

	param.n_coders = atoi(av[1]);
	param.t_burnout = atoi(av[2]);
	param.t_compile = atoi(av[3]);
	param.t_debug = atoi(av[4]);
	param.t_refactor = atoi(av[5]);
	param.n_compiles_required = atoi(av[6]);
	param.dongle_cooldown = atoi(av[7]);
	param.scheduler = av[8];
	init(&simu, &param);
	pthread_create(&simu.thread, NULL, monitor_routine, &simu);
	i = -1;
	while (++i < param.n_coders)
		pthread_create(&simu.coders[i].thread, NULL, coder_routine, &simu.coders[i]);
	pthread_join(simu.thread, NULL);
	i = -1;
	while (++i < param.n_coders)
		pthread_join(simu.coders[i].thread, NULL);
	free_all(&simu);
	return (0);
}

int	main(int ac, char **av)
{
	if (ac != 9)
	{
		printf("Veuillez entrer le bon nombre d'arguments...\n");
		printf("Nombre attendu: 8\n");
		return (1);
	}
	if (parsing(ac, av))
	{
		printf("Arguments invalides\n");
		return (1);
	}
	launch(av);
	return (0);
}
