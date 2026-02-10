from abc import ABC, abstractmethod


class Card(ABC):

	card = []

	def __init__(self, name: str, cost: int, rarity: str):
		self.name = name
		self.cost = cost
		self.rarity = rarity
		self.card.append(self)

	@abstractmethod
	def play(self, game_state: dict) -> dict:
		...

	def get_card_info(self) -> dict:
		return self.card

	def is_playable(self, available_mana: int) -> bool:
		is_available = False
		if available_mana <= 3:
			is_available = True
		return is_available
