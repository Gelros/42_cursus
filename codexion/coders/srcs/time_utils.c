#include "../includes/codexion.h"

long	get_time_ms(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return (tv.tv_sec * 1000L + tv.tv_usec / 1000);
}

int	is_running(t_simu *simu)
{
	int	running;

	pthread_mutex_lock(&simu->mutex_run);
	running = simu->is_running;
	pthread_mutex_unlock(&simu->mutex_run);
	return (running);
}
