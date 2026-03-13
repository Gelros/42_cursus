#include "../includes/codexion.h"

void    take_dongle(t_coder *coder, t_dongle *dongle)
{
    long    priority;

    pthread_mutex_lock(&dongle->mutex);
    if (strcmp(coder->simu->params->scheduler, "fifo") == 0)
        priority = get_time_ms();
    else
        priority = coder->last_compile + coder->simu->params->t_burnout;
    push(&dongle->queue, coder->id, priority);
    while (dongle->in_use || dongle->queue.entries[0].id != coder->id
        || get_time_ms() < dongle->released_at + coder->simu->params->dongle_cooldown)
        pthread_cond_wait(&dongle->cond, &dongle->mutex);
    extract(&dongle->queue);
    dongle->in_use = 1;
    log_action(coder, "has taken a dongle");
    pthread_mutex_unlock(&dongle->mutex);
}

void	take_dongles(t_coder *coder)
{
	take_dongle(coder, coder->left);
	take_dongle(coder, coder->right);
}

void    release_dongle(t_dongle *dongle)
{
    pthread_mutex_lock(&dongle->mutex);
    dongle->in_use = 0;
    dongle->released_at = get_time_ms();
    pthread_cond_broadcast(&dongle->cond);
    pthread_mutex_unlock(&dongle->mutex);
}
