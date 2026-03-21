/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   free.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 10:48:01 by guilacol          #+#    #+#             */
/*   Updated: 2026/03/21 11:03:18 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/codexion.h"

void	free_all(t_simu *simu)
{
	int	i;

	i = -1;
	while (++i < simu->params->n_coders)
	{
		pthread_cond_destroy(&simu->dongles[i].cond);
		pthread_mutex_destroy(&simu->dongles[i].mutex);
	}
	free(simu->dongles);
	free(simu->coders);
	pthread_mutex_destroy(&simu->mutex_logs);
	pthread_mutex_destroy(&simu->mutex_run);
}
