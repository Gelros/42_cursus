#include "../includes/codexion.h"

int	init(t_simu *simu, t_params *params)
{
	int	i;

	pthread_mutex_init(&simu->mutex_logs, NULL);
	pthread_mutex_init(&simu->mutex_run, NULL);
	simu->coders = malloc(sizeof(t_coder) * params->n_coders);
	simu->dongles = malloc(sizeof(t_dongle) * params->n_coders);
	if (!simu->coders || !simu->dongles)
		return (free(simu->coders), 1);
	simu->is_running = 1;
	i = -1;
	while (++i < params->n_coders)
	{
		pthread_mutex_init(&simu->dongles[i].mutex, NULL);
		pthread_cond_init(&simu->dongles[i].cond, NULL);
		simu->dongles[i].in_use = 0;
		simu->dongles[i].released_at = 0;
		simu->dongles[i].queue.size = 0;
		simu->dongles[i].id = i;
		simu->coders[i].id = i + 1;
		simu->coders[i].n_compiles = 0;
		simu->coders[i].last_compile = get_time_ms();
		simu->coders[i].left = &simu->dongles[i];
		simu->coders[i].right = &simu->dongles[(i + 1) % params->n_coders];
		simu->coders[i].simu = simu;
	}
    return (0);
}
