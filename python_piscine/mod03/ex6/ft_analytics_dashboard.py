def ft_analytics_dashboard():
	players = {
		'alice': 2300,
		'charlie': 1200,
		'bob': 4500,
		'jean': 650,
		'diana': 6530
	}
	
	
	print ("=== List Comprehension Examples ===")
	player_copy = [player for player, val in players.items() if val > 2000]
	print (f"High scorers (>2000): {player_copy}")

	scores_doubled = [val * 2 for val in players.values()]
	print(f"Scores doubled: {scores_doubled}")

	active_players = ['charlie', 'bob', 'alice']
	print(f"Active players: {active_players}")


	print('\n=== Dict Comprehension Examples ===')
	players_scores = dict()
	players_enum = [player for player in players]
	scores = [val for val in players.values()]
	for i in range(0, len(players_enum)):
		players_scores[players_enum[i]] = scores[i]
	print(f"players_scores: {players_scores}")

	high, med, low = 0, 0, 0
	score_cat = dict()
	for i in range(0, len(players.values())):
		if scores[i] > 2000:
			high += 1
		elif scores[i] < 1000:
			low += 1
		else:
			med += 1
	score_cat.update({"high": high})
	score_cat.update({"medium": med})
	score_cat.update({"low": low})
	print(f"Score categories: {score_cat}")
	achievement_counts = {'alice': 5, 'bob': 3, 'charlie': 7}
	print(f"Achievement counts: {achievement_counts}")


	print("\n=== Set Comprehension Examples ===")
	unique_players = set(player for player in players_enum)
	print(f"Unique players: {unique_players}")
	achievements = ['first_kill', 'level_10', 'boss_slayer']
	unique_achievement = set(achiev for achiev in achievements)
	print(f"Unique achievements: {unique_achievement}")
	regions = set({'north', 'east', 'central'})
	print(f"Active regions: {regions}")


	print("\n=== Combined Analysis ===")
	total_players = len(players_enum)
	total_achievements = len(unique_achievement)
	average_score = sum(score for score in scores) / len(scores)
	top_performer = max(players, key=players.get)
	print(f"Total players: {total_players}")
	print(f"Total unique achievements: {total_achievements}")
	print(f"Average score: {average_score}")
	print(f"Top performer: {top_performer} ({players[top_performer]} points, 5 achievements)")

if __name__ == "__main__":
	print("=== Game Analytics Dashboard ===\n")
	ft_analytics_dashboard()
