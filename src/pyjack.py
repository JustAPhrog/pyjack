from array import array
import sys
import random
import logging

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
    ('Ace', [1, 11]),
)

def is_ace(card):
    return card == cards[-1]

def is_not_ace(card):
    return card != cards[-1]

class Player:
    """Player"""
    def __init__(self, name:str, wins=0, loses=0, deck_cards:list[tuple]=None) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.wins = wins
        self.loses = loses
        self.cards = deck_cards if deck_cards is not None else []
    
    def __str__(self):
        return "%s with %s" % (self.name, self.cards)

    def score(self) -> int:
        cards_value = 0
        for card in filter(is_not_ace, self.cards):
            cards_value += card[1] 
        for _ in filter(is_ace, self.cards):
            if cards_value + cards[-1][1][1] <= 21:
                cards_value += cards[-1][1][1]
            else:
                cards_value += cards[-1][1][0]
        self.log.debug('%s %s', self.name, cards_value)
        return cards_value

    def add_card(self, card:tuple) -> None:
        self.log.debug('To %s add %s', self.name, card)
        self.cards.append(card)


class Game:
    """Main class which hold deck and players"""
    def __init__(self, host_name:str, players:list[Player], deck:list):
        self.log = logging.getLogger(self.__class__.__name__)
        self.host = Player(host_name)
        self.players = players
        self.deck = deck
        self.current_game = 0

    def _create_deck(self, nr_decks:int) -> None:
        for i in range(56 * nr_decks):
            self.deck.append(cards[i % 14]) 
        random.shuffle(self.deck)
        self.log.debug('Deck created')

    def _take_card(self) -> tuple:
        card = self.deck.pop()
        self.log.debug('Card taken %s', card)
        return card

    def _round(self, player:Player) -> None:
        self.log.debug('%s turn', player.name)
        self.log.debug('staring cards %s', player.cards)
        while True:
            decision = input('Next card or pass? c or p')
            while decision not in ['c', 'p']:
                self.log.debug('Wrong input %s', decision)
                decision = input('Wrong input. Only \'c\' or \'p\'')
            if decision == 'c':
                player.add_card(self._take_card())
            else:
                break
        self.log.debug('Cards %s', player.cards)
        # self.log.debug('Final score %s', player.score())

    def _host_round(self) -> None:
        self.log.debug('Host %s round', self.host.name)
        while True:
            # self.log.debug('host score %s', self.host.score())
            if self.host.score() < 21:
                self.host.add_card(self._take_card())
            else:
                break
        self.log.debug('Cards %s', self.host.cards)
        # self.log.debug('Final score %s', self.host.score())

    def _check_scores(self) -> None:
        self.log.debug('check scores')
        results = [(player.score(), player.name) for player in self.players]
        results.append((self.host.score(), self.host.name))

        results = sorted(results, key=lambda k: k[0])
        self.log.debug('Results %s', results)

    def _make_game(self) -> None:
        self.current_game += 1
        self.log.debug('New game %s', self.current_game)
        self.log.debug('%s taking 2 cards', self.host.name)
        for _ in range(2):
            self.host.add_card(self._take_card())
        for player in self.players:
            self._round(player)
        self._host_round()
        self._check_scores()


    def main_loop(self, decks:int) -> None:
        try:
            if len(self.deck) == 0:
                self._create_deck(decks)
            self.log.debug('Deck last cards %s', self.deck[-3:])
            self._make_game()
            self.log.debug('End of game')
        except KeyboardInterrupt:
            self.log.debug('User ends loop')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(lineno)d:%(funcName)s - %(message)s")
    g = Game(host_name='Croupier', players=[Player('p1')], deck=[])
    g.main_loop(1)
