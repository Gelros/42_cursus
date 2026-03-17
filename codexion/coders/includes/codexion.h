#include "../heap/heap.h"
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <unistd.h>

typedef struct s_simu	t_simu;

typedef struct s_params
{
	int					n_coders;
	int					t_burnout;
	int					t_compile;
	int					t_debug;
	int					t_refactor;
	int					n_compiles_required;
	int					dongle_cooldown;
	char				*scheduler;
}						t_params;

typedef struct s_dongle
{
	int					id;
	int					in_use;
	long				released_at;
	t_heap				queue;
	pthread_mutex_t		mutex;
	pthread_cond_t		cond;
}						t_dongle;

typedef struct s_coder
{
	int					id;
	int					n_compiles;
	long				last_compile;
	t_dongle			*left;
	t_dongle			*right;
	pthread_t			thread;
	t_simu				*simu;
}						t_coder;

typedef struct s_simu
{
	t_dongle			*dongles;
	t_coder				*coders;
	t_params			*params;
	int					is_running;
	pthread_mutex_t		mutex_logs;
	pthread_mutex_t		mutex_run;
	pthread_t			thread;
}						t_simu;

long					get_time_ms(void);
void					push(t_heap *heap, int id, long priority);
t_entry					extract(t_heap *heap);
void					take_dongle(t_coder *coder, t_dongle *dongle);
void					take_dongles(t_coder *coder);
int						init(t_simu *simu, t_params *params);
void					log_action(t_coder *coder, char *str);
void					release_dongle(t_dongle *dongle);
void					release_dongles(t_coder *coder);
void					free_all(t_simu *simu);
void					*monitor_routine(void *arg);
void					*coder_routine(void *arg);
int						is_running(t_simu *simu);