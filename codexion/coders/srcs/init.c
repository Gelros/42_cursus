/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 10:48:06 by guilacol          #+#    #+#             */
/*   Updated: 2026/03/21 11:03:18 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/codexion.h"

void	struct_init(t_simu *simu, t_params *params)
{
	int	i;

	i = -1;
	while (++i < params->n_coders)
	{
		pthread_mutex_init(&simu->dongles[i].mutex, NULL);
		pthread_cond_init(&simu->dongles[i].cond, NULL);
		pthread_mutex_init(&simu->coders[i].mutex, NULL);
		simu->dongles[i].in_use = 0;
		simu->dongles[i].released_at = get_time_ms() - params->dongle_cooldown;
		simu->dongles[i].queue.size = 0;
		simu->dongles[i].id = i;
		simu->coders[i].id = i + 1;
		simu->coders[i].n_compiles = 0;
		simu->coders[i].last_compile = get_time_ms();
		simu->coders[i].left = &simu->dongles[i];
		simu->coders[i].right = &simu->dongles[(i + 1) % params->n_coders];
		simu->coders[i].simu = simu;
	}
}

int	init(t_simu *simu, t_params *params)
{
	pthread_mutex_init(&simu->mutex_logs, NULL);
	pthread_mutex_init(&simu->mutex_run, NULL);
	simu->coders = malloc(sizeof(t_coder) * params->n_coders);
	simu->dongles = malloc(sizeof(t_dongle) * params->n_coders);
	if (!simu->coders || !simu->dongles)
		return (free(simu->coders), 1);
	simu->is_running = 1;
	simu->params = params;
	simu->start_time = get_time_ms();
	struct_init(simu, params);
	return (0);
}
