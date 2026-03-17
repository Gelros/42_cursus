#include "../includes/codexion.h"

int	is_burnout(t_coder *coder, t_simu *simu)
{
	long	time_coder;

	time_coder = get_time_ms() - coder->last_compile;
	if (time_coder >= simu->params->t_burnout)
	{
		log_action(coder, "burned out");
		pthread_mutex_lock(&simu->mutex_run);
		simu->is_running = 0;
		pthread_mutex_unlock(&simu->mutex_run);
		return (1);
	}
	return (0);
}

int	all_done(t_simu *simu)
{
	int	i;

	i = -1;
	while (++i < simu->params->n_coders)
	{
		if (simu->coders[i].n_compiles < simu->params->n_compiles_required)
			return (0);
	}
	return (1);
}

void	*monitor_routine(void *arg)
{
	t_simu	*simu;
	int		i;

	simu = (t_simu *)arg;
	while (is_running(simu))
	{
		i = -1;
		while (++i < simu->params->n_coders)
		{
			if (is_burnout(&simu->coders[i], simu))
				break ;
		}
		if (all_done(simu))
		{
			pthread_mutex_lock(&simu->mutex_run);
			simu->is_running = 0;
			pthread_mutex_unlock(&simu->mutex_run);
			break ;
		}
		usleep(1000);
	}
	return (NULL);
}
