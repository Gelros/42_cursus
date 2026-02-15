from ex4.TournamentCard import TournamentCard


class TournamentPlatform:
    def __init__(self):
        self.cards = {}
        self.matchs = []
        self.status = "active"

    def register_card(self, card: TournamentCard) -> str:
        card_id = f"{card.name.lower().replace(' ', '_')}001"
        self.cards[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        card1 = self.cards.get(card1_id, None)
        card2 = self.cards.get(card2_id, None)
        card1_stat = card1.get_combat_stats()
        card2_stat = card2.get_combat_stats()
        if card1_stat["attack"] >= card2_stat["defense"]:
            winner = card1
            winner_id = card1_id
            loser = card2
            loser_id = card2_id
        else:
            winner = card2
            winner_id = card2_id
            loser = card1
            loser_id = card1_id
        winner.update_wins(1)
        winner.calculate_rating()
        loser.update_losses(1)
        loser.calculate_rating()

        result = {
            "winner": winner_id,
            "loser": loser_id,
            "winner_rating": winner.rating,
            "loser_rating": loser.rating
        }
        self.matchs.append(result)
        return result

    def get_leaderboard(self):
        res = sorted(
            self.cards.values(),
            key=lambda card: card.rating,
            reverse=True
        )
        return [card.get_rank_info() for card in res]

    def generate_tournament_report(self):
        avg = sum(
            card.rating for card in self.cards.values()) / len(self.cards)
        return {
            "total_cards": len(self.cards),
            "matches_played": len(self.matchs),
            "avg_rating": avg,
            "platform_status": self.status
        }
