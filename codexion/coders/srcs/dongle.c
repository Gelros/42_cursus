/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 10:47:56 by guilacol          #+#    #+#             */
/*   Updated: 2026/03/21 11:35:06 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/codexion.h"

static void	wait_dongle(t_coder *coder, t_dongle *dongle)
{
	struct timespec	ts;
	long			wakeup;

	wakeup = dongle->released_at + coder->simu->params->dongle_cooldown;
	ts.tv_sec = wakeup / 1000;
	ts.tv_nsec = (wakeup % 1000) * 1000000;
	pthread_cond_timedwait(&dongle->cond, &dongle->mutex, &ts);
}

int	take_dongle(t_coder *coder, t_dongle *dongle)
{
	long			priority;

	pthread_mutex_lock(&dongle->mutex);
	if (strcmp(coder->simu->params->scheduler, "fifo") == 0)
		priority = get_time_ms();
	else
		priority = coder->last_compile + coder->simu->params->t_burnout;
	push(&dongle->queue, coder->id, priority);
	while ((dongle->in_use || dongle->queue.entries[0].id != coder->id
			|| get_time_ms() < dongle->released_at
			+ coder->simu->params->dongle_cooldown) && is_running(coder->simu))
		wait_dongle(coder, dongle);
	if (!is_running(coder->simu))
	{
		extract(&dongle->queue);
		pthread_mutex_unlock(&dongle->mutex);
		return (0);
	}
	extract(&dongle->queue);
	dongle->in_use = 1;
	log_action(coder, "has taken a dongle");
	pthread_mutex_unlock(&dongle->mutex);
	return (1);
}

int	take_dongles(t_coder *coder)
{
	if (coder->id % 2 == 0)
	{
		if (!take_dongle(coder, coder->right))
			return (0);
		if (!take_dongle(coder, coder->left))
		{
			release_dongle(coder->right);
			return (0);
		}
	}
	else
	{
		if (!take_dongle(coder, coder->left))
			return (0);
		if (!take_dongle(coder, coder->right))
		{
			release_dongle(coder->left);
			return (0);
		}
	}
	return (1);
}

void	release_dongle(t_dongle *dongle)
{
	pthread_mutex_lock(&dongle->mutex);
	dongle->in_use = 0;
	dongle->released_at = get_time_ms();
	pthread_cond_broadcast(&dongle->cond);
	pthread_mutex_unlock(&dongle->mutex);
}

void	release_dongles(t_coder *coder)
{
	release_dongle(coder->right);
	release_dongle(coder->left);
}
