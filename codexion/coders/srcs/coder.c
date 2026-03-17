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

void	*coder_routine(void *arg)
{
	t_coder *coder = (t_coder *)arg;
	while (coder->simu->is_running)
	{
		take_dongles(coder);
		coder->last_compile = get_time_ms();
		compile(coder);
		coder->n_compiles++;
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
