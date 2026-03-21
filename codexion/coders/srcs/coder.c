/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 10:47:49 by guilacol          #+#    #+#             */
/*   Updated: 2026/03/21 11:29:45 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/codexion.h"

void	compile(t_coder *coder)
{
	log_action(coder, "is compiling");
	usleep(coder->simu->params->t_compile * 1000);
}

void	debug(t_coder *coder)
{
	log_action(coder, "is debugging");
	usleep(coder->simu->params->t_debug * 1000);
}

void	refactor(t_coder *coder)
{
	log_action(coder, "is refactoring");
	usleep(coder->simu->params->t_refactor * 1000);
}

static void	do_compile(t_coder *coder)
{
	pthread_mutex_lock(&coder->mutex);
	coder->last_compile = get_time_ms();
	pthread_mutex_unlock(&coder->mutex);
	compile(coder);
	pthread_mutex_lock(&coder->mutex);
	coder->n_compiles++;
	pthread_mutex_unlock(&coder->mutex);
}

void	*coder_routine(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	while (is_running(coder->simu))
	{
		if (!take_dongles(coder))
			break ;
		if (!is_running(coder->simu))
		{
			release_dongles(coder);
			break ;
		}
		do_compile(coder);
		release_dongles(coder);
		if (!is_running(coder->simu))
			break ;
		debug(coder);
		if (!is_running(coder->simu))
			break ;
		refactor(coder);
	}
	return (NULL);
}
