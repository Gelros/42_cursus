*This project has been created as part of the 42 curriculum by guilacol.*

# Codexion

## Description

Codexion is a concurrent programming simulation inspired by the classic Dining Philosophers problem. A group of coders sit in a circular co-working hub, each needing two USB dongles simultaneously to compile their quantum code. The simulation models real-world resource contention: coders must compete for shared dongles, avoid deadlocks, prevent burnout, and respect cooldown periods — all while running in parallel threads.

The program implements POSIX threads with mutex and condition variable synchronization, a priority queue (min-heap) for fair arbitration, and two scheduling policies: FIFO (First In, First Out) and EDF (Earliest Deadline First).

The simulation stops either when a coder burns out (fails to compile within `time_to_burnout` milliseconds) or when all coders have compiled at least `number_of_compiles_required` times.

## Instructions

### Compilation

```bash
make
```

### Usage

```bash
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

### Arguments

| Argument | Description |
|---|---|
| `number_of_coders` | Number of coders and dongles (>= 1) |
| `time_to_burnout` | Milliseconds before a coder burns out without compiling (>= 1) |
| `time_to_compile` | Milliseconds to compile (requires 2 dongles) (>= 0) |
| `time_to_debug` | Milliseconds to debug (>= 0) |
| `time_to_refactor` | Milliseconds to refactor (>= 0) |
| `number_of_compiles_required` | Compiles needed per coder to stop the simulation (>= 1) |
| `dongle_cooldown` | Milliseconds a dongle is unavailable after release (>= 0) |
| `scheduler` | Arbitration policy: `fifo` or `edf` |

### Examples

```bash
# Normal simulation
./codexion 4 800 200 200 200 5 100 fifo

# EDF scheduler
./codexion 4 800 200 200 200 5 100 edf

# Single coder (burns out immediately — cannot hold 2 dongles)
./codexion 1 800 200 200 200 5 100 fifo
```

### Cleanup

```bash
make clean    # Remove object files
make fclean   # Remove object files and binary
make re       # Recompile from scratch
```

## Resources

### Documentation and References

- [POSIX Threads Programming — Blaise Barney, LLNL](https://hpc-tutorials.llnl.gov/posix/)
- [The Little Book of Semaphores — Allen B. Downey](https://greenteapress.com/wp/semaphores/)
- [pthread_cond_timedwait — Linux man page](https://man7.org/linux/man-pages/man3/pthread_cond_timedwait.3p.html)
- [Coffman Conditions for Deadlock — Wikipedia](https://www.codequoi.com/threads-mutex-et-programmation-concurrente-en-c/)
- [Earliest Deadline First Scheduling — Wikipedia](https://en.wikipedia.org/wiki/Earliest_deadline_first_scheduling)
- [Priority Queue / Binary Heap — Wikipedia](https://en.wikipedia.org/wiki/Binary_heap)

### AI Usage

Claude (claude.ai) was used throughout this project for the following purposes:

- **Understanding the subject**: Breaking down the problem statement, clarifying the rules around burnout detection, cooldown handling, and scheduler behavior.
- **Learning new concepts**: Step-by-step explanation and hands-on exercises for POSIX threads, mutexes, condition variables, `gettimeofday`, and min-heap implementation before writing any project code.
- **Debugging**: Identifying race conditions, deadlocks, incorrect mutex usage, and timing issues through iterative analysis of program output and code review.

All generated or suggested code was reviewed, understood, and validated before integration.

## Blocking Cases Handled

### Deadlock Prevention

Deadlock was prevented using the **asymmetric locking strategy**: odd-numbered coders acquire their left dongle first, then their right; even-numbered coders acquire their right first, then their left. This breaks the circular wait condition (one of Coffman's four necessary conditions for deadlock), ensuring that two neighboring coders can never simultaneously hold the dongle the other needs.

The four Coffman conditions are: mutual exclusion (a dongle can only be held by one coder at a time), hold and wait (a coder holds one dongle while waiting for the other), no preemption (a dongle cannot be forcibly taken), and circular wait (which is broken by the asymmetric acquisition order).

### Starvation Prevention

Starvation is prevented through the scheduler enforced by the priority queue. Under FIFO, requests are served in arrival order, guaranteeing that every waiting coder will eventually be served. Under EDF, the coder closest to burnout is prioritized, preventing any coder from dying while others with more time compile ahead of them. The min-heap ensures O(log n) insertion and O(1) access to the most urgent request.

### Cooldown Handling

After a dongle is released, it is unavailable for `dongle_cooldown` milliseconds. This is enforced inside `take_dongle` using `pthread_cond_timedwait`, which automatically wakes the waiting thread when the cooldown expires — avoiding both busy-waiting and the risk of a thread sleeping forever after a missed broadcast.

### Precise Burnout Detection

A dedicated monitor thread checks every millisecond whether any coder has exceeded `time_to_burnout` milliseconds since their last compile start. This guarantees that the burnout log is printed within 10ms of the actual deadline as required by the subject. Upon detecting a burnout, the monitor sets `is_running = 0` and broadcasts on all dongle condition variables to unblock any waiting coders.

### Log Serialization

All output is protected by a dedicated `mutex_logs` mutex. Every call to `log_action` locks this mutex before calling `printf` and unlocks after, ensuring that no two log messages ever interleave on the same line.

## Thread Synchronization Mechanisms

### `pthread_mutex_t`

Two global mutexes are used at the simulation level: `mutex_logs` serializes all output, and `mutex_run` protects read/write access to `is_running`. Each dongle also has its own `mutex` to protect its state (`in_use`, `released_at`, `queue`) from concurrent access by neighboring coders. This per-resource granularity allows two coders on opposite sides of the hub to acquire different dongles in parallel without contention.

Race conditions are prevented by always locking the relevant mutex before reading or modifying any shared field, and unlocking immediately after the critical section. For example, `is_running` is never read directly — all access goes through the `is_running()` helper which locks and unlocks `mutex_run`.

### `pthread_cond_t`

Each dongle has a condition variable used to block coders that cannot yet acquire it (because it is in use, in cooldown, or not their turn according to the scheduler). When a dongle is released, `pthread_cond_broadcast` wakes all waiting coders; each one re-evaluates the wait condition and either proceeds or goes back to sleep. `while` loops (not `if`) guard all `cond_wait` calls to handle spurious wakeups correctly.

`pthread_cond_timedwait` is used instead of `pthread_cond_wait` so that a coder waiting for a cooldown to expire will wake up automatically at the right moment, without relying on an external broadcast.

### Priority Queue (Min-Heap)

Each dongle maintains a min-heap of waiting coders. Under FIFO, the priority is the timestamp of the request (earlier = higher priority). Under EDF, the priority is `last_compile_start + time_to_burnout` (sooner deadline = higher priority). In both cases, `extract()` always returns the most urgent coder in O(log n), and the `while` loop in `take_dongle` ensures a coder only proceeds when it is at the head of the heap.

### Thread-Safe Communication Between Coders and Monitor

The monitor thread communicates with coder threads exclusively through `is_running` (protected by `mutex_run`) and `pthread_cond_broadcast` on dongle condition variables. Coders check `is_running` at each phase transition. When the monitor sets `is_running = 0`, it immediately broadcasts on all dongle conditions so that any coder blocked in `cond_wait` wakes up, checks the flag, and exits cleanly.
