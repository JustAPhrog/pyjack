from array import array
import sys
import random

# Initial random generator with sys time-date
random.seed()

cards = (
    ('One', 1),
    ('Two', 2),
    ('Three', 3),
    ('Four', 4),
    ('Five', 5),
    ('Six', 6),
    ('Seven', 7),
    ('Eight', 8),
    ('Nine', 9),
    ('Ten', 10),
    ('Jack', 10),
    ('Queen', 10),
    ('King', 10),
    ('Ace', [1, 10]),
)

class Player:
    def __init__(self, name:str, wins=0, loses=0, cards:list=[]) -> None:
        self.name = name
        self.wins = wins
        self.loses = loses
        self.cards = cards
    
    def cards_value(self):
        cards_value = 0
        for card in self.cards:
            cards_value += card[1]
        return cards_value
    


class Game:
    """Main class which hold deck and players"""
    def __init__(self, host_name='Croupier', players=[], deck=[]):
        self.host = Player(host_name)
        self.players = players
        self.deck = deck
        self.current_game = 0

    def create_deck(self) -> None:
        for i in range(56):
            self.deck.append(cards[i % 14]) 
        random.shuffle(self.deck)