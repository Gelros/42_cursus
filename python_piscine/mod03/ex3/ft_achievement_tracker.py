def achievement_tracker() -> None:
    print("=== Achievement Tracker System ===\n")
    players = {
        "alice": {'first_kill', 'level_10', 'treasure_hunter', 'speed_demon', 'speed_demon'},
        "bob": {'first_kill', 'level_10', 'boss_slayer', 'collector'},
        "charlie": {'level_10', 'treasure_hunter', 'boss_slayer', 'speed_demon', 'perfectionist'}
    }
    for p in players:
        print(f"Player {p} achievement: {players[p]}")
    
    print("\n=== Achievement Analytics ===")
    unique = set()
    for p in players:
        unique = unique.union(players[p])
    print(f"All unique achievements: {unique}")
    print(f"Total unique achievements:", len(unique))
    
    common = set.intersection(*players.values())
    print(f"\nCommon to all players: {common}")
    
    unique_alice = players['alice'].difference(players['bob'].union(players['charlie']))
    unique_bob = players['bob'].difference(players['alice'].union(players['charlie']))
    unique_charlie = players['charlie'].difference(players['alice'].union(players['bob']))
    rare_achievement = unique_alice.union(unique_bob, unique_charlie)
    print(f"Rare achievements (1 player): {rare_achievement}\n")
    
    print(f"Alice vs Bob common: {players["alice"].intersection(players["bob"])}")
    print(f"Alice unique: {players["alice"].difference(players["bob"])}")
    print(f"bob unique: {players["bob"].difference(players["alice"])}")
    
if __name__ == "__main__":
    achievement_tracker()