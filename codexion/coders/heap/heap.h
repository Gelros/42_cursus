typedef struct s_entry // Structre de donnée pour Thread
{
    int     id;       // ID du thread
    long    priority; // Timestamp/Deadline : définit l'ordre de passage dans le Heap
} t_entry;

typedef struct s_heap // Structure qui sert de dicionnaire pour les Threads
{
    t_entry entries[64]; // Tableau représentant l'arbre binaire (max 64 éléments)
    int     size;       // Nombre actuel d'éléments stockés dans le tas
} t_heap;
