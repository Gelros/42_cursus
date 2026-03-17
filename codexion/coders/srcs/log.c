#include "../includes/codexion.h"

void	log_action(t_coder *coder, char *str)
{
	pthread_mutex_lock(&coder->simu->mutex_logs);
	printf("%ld %d %s\n", get_time_ms() - coder->simu->start_time, coder->id,
		str);
	pthread_mutex_unlock(&coder->simu->mutex_logs);
}
