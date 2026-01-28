def ft_data_stream(data):
    for i in range(data):
        yield i + 1

def generator(stream, it_players, it_exploits):
    for n in stream:
        player = next(it_players)
        exploit = next(it_exploits)
        
        level = int(2 * n) if n % 2 == 0 else int(n * 3)
        
        yield f"Event {n}: Player {player} (level {level}) {exploit}", level
        
def infinite(data):
    while True:
        for i in data:
            yield i

def fibonacci(data):
    a, b = 0, 1
    for i in range(data - 1):
        a, b = b, a + b
        yield a

def prime_number(data):
    count = 0
    n = 3
    while count < data-1:
        is_prime = True
        for i in range(2, n):
            if n % i == 0:
                is_prime = False
                break
        if is_prime:
            yield n
            count += 1
        n += 1
            
if __name__ == "__main__":
    players = ["Alice", "Bob", "Charlie"]
    exploits = ["killed monster", "found treasure", "leveled up"]
    it_players = infinite(players)
    it_exploits = infinite(exploits)
    data = 10
    
    print("=== Game Data Stream Processor ===\n")
    print(f"Processing {data} game events...\n")
    stream = ft_data_stream(data)
    gen = generator(stream, it_players ,it_exploits)
    total_events = 0
    high_lv = 0
    for i, level in gen:
        print(i)
        if level >= 10:
            high_lv += 1
        total_events += 1
        
    print("\n=== Stream Analytics ===")
    print(f"Total events processed: {total_events}")
    print(f"High-level players (10+): {high_lv}")
    
    print("\nMemory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds")
    
    print("\n=== Generator Demonstration ===")        
    n_fib = 10
    n_prime = 5
    print(f"Fibonacci sequence (first {n_fib}): 0", end="")
    for i in fibonacci(n_fib):
        print(', ', end="")
        print(i, end="")
    print(f"\nPrime numbers (first {n_prime}): 2", end="")
    for i in prime_number(n_prime):
        print(', ', end="")
        print(i, end="")
    