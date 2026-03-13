#include "../includes/codexion.h"

void	push(t_heap *heap, int id, long priority)
{
	int		i;
	int		parent;
	t_entry	tmp;

	if (heap->size >= 64)
		return ;
	// Place l'element a la fin
	i = heap->size;
	heap->entries[i].id = id;
	heap->entries[i].priority = priority;
	heap->size++;
	// Sift-Up : Faire remonter l'élément
	while (i > 0)
	{
		parent = (i - 1) / 2;
		if (heap->entries[i].priority < heap->entries[parent].priority)
		{
			tmp = heap->entries[i];
			heap->entries[i] = heap->entries[parent];
			heap->entries[parent] = tmp;
			i = parent;
		}
		else
			break ;
	}
}

t_entry extract(t_heap *heap)
{
    if (heap->size == 0)  // Cas ou la heap est vide on renvoie -1 -1 pour le signaler id/priority
    {
        t_entry empty = {-1, -1};
        return (empty);
    }

    t_entry root = heap->entries[0];

    heap->size--;
    if (heap->size > 0)
        heap->entries[0] = heap->entries[heap->size]; // 2. Le dernier prend la place
    
    int i = 0;
    while (1)
    {
        int left = (i * 2) + 1;
        int right = (i * 2) + 2;
        int smallest = i;
        
        // On regarde si l'un des enfant est plus important
        if (left < heap->size && heap->entries[left].priority < heap->entries[smallest].priority)
            smallest = left;
        if (right < heap->size && heap->entries[right].priority < heap->entries[smallest].priority)
            smallest = right;

        // Si jamais l'un des enfant est plus important que le parent on swap
        if (smallest != i)
        {
            t_entry tmp = heap->entries[i];
            heap->entries[i] = heap->entries[smallest];
            heap->entries[smallest] = tmp;
            i = smallest;
        }
        else
            break;
    }
    return root;
}
