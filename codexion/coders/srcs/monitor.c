/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 10:48:26 by guilacol          #+#    #+#             */
/*   Updated: 2026/03/21 11:34:26 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/codexion.h"

int	is_burnout(t_coder *coder, t_simu *simu)
{
	long	time_coder;
	int		i;

	pthread_mutex_lock(&coder->mutex);
	time_coder = get_time_ms() - coder->last_compile;
	pthread_mutex_unlock(&coder->mutex);
	if (time_coder >= simu->params->t_burnout)
	{
		log_action(coder, "burned out");
		pthread_mutex_lock(&simu->mutex_run);
		simu->is_running = 0;
		i = -1;
		while (++i < simu->params->n_coders)
		{
			pthread_mutex_lock(&simu->dongles[i].mutex);
			pthread_cond_broadcast(&simu->dongles[i].cond);
			pthread_mutex_unlock(&simu->dongles[i].mutex);
		}
		pthread_mutex_unlock(&simu->mutex_run);
		return (1);
	}
	return (0);
}

int	all_done(t_simu *simu)
{
	int	i;
	int	n;

	i = 0;
	pthread_mutex_lock(&simu->coders[i].mutex);
	n = simu->coders[i].n_compiles;
	pthread_mutex_unlock(&simu->coders[i].mutex);
	while (i < simu->params->n_coders)
	{
		if (n < simu->params->n_compiles_required)
			return (0);
		i++;
	}
	return (1);
}

static void	stop_simulation(t_simu *simu)
{
	int	i;

	pthread_mutex_lock(&simu->mutex_run);
	simu->is_running = 0;
	pthread_mutex_unlock(&simu->mutex_run);
	i = -1;
	while (++i < simu->params->n_coders)
	{
		pthread_mutex_lock(&simu->dongles[i].mutex);
		pthread_cond_broadcast(&simu->dongles[i].cond);
		pthread_mutex_unlock(&simu->dongles[i].mutex);
	}
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
			if (is_burnout(&simu->coders[i], simu))
				break ;
		if (!is_running(simu))
			break ;
		if (all_done(simu))
		{
			stop_simulation(simu);
			break ;
		}
		usleep(1000);
	}
	return (NULL);
}
