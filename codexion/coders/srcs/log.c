/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: guilacol <guilacol@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 10:48:10 by guilacol          #+#    #+#             */
/*   Updated: 2026/03/21 11:03:18 by guilacol         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/codexion.h"

void	log_action(t_coder *coder, char *str)
{
	pthread_mutex_lock(&coder->simu->mutex_logs);
	printf("%ld %d %s\n", get_time_ms() - coder->simu->start_time, coder->id,
		str);
	pthread_mutex_unlock(&coder->simu->mutex_logs);
}
