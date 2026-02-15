from ex3.GameStrategy import GameStrategy


class AgressiveStrategy(GameStrategy):
    def __init__(self, available_mana: int = 15):
        self.available_mana = available_mana
        self.total_damage = 0

    def execute_turn(self, hand: list, battlefield: list) -> dict:
        cards_played = []
        mana_used = 0
        damage_dealt = 0
        target = self.prioritize_targets(battlefield)
        sorted_hand = sorted(hand, key=lambda card: card.cost)
        for p in sorted_hand:
            if p.cost + mana_used <= self.available_mana:
                cards_played.append(p.name)
                mana_used += p.cost
                damage_dealt += getattr(p, "attack_power", p.cost)
        self.total_damage += damage_dealt
        return {
            "actions": {
                "cards_played": cards_played,
                "mana_used": mana_used,
                "targets_attacked": target,
                "damage_dealt": damage_dealt
                }
        }

    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list) -> list:
        prio = []
        for target in available_targets:
            if "Player" in target:
                prio.insert(0, target)
            else:
                prio.append(target)
        return prio
