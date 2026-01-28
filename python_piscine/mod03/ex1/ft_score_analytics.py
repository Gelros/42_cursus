import sys

def player_analytics() -> None:
    n_player = len(sys.argv) - 1
    arg = sys.argv[1:]
    scores = []

    print("=== Player Score Analytics ===")
    if n_player == 0:
        print(f"No scores provided. Usage: python3 {sys.argv[0]} <score1> <score2> ...")

    if n_player > 0:
        for p in arg:
            scores.append(int(p))
        total = sum(p for p in scores)
        average = total / n_player
        print("Scores processed:", scores)
        print("Total player:", n_player)
        print("Total score:", total)
        print("Average score:", average)
        print("High score:", max(scores))
        print("Low score:", min(scores))
        print("Score range:", max(scores) - min(scores))
    
if __name__ == "__main__":
    player_analytics()