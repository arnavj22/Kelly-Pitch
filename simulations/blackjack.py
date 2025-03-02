import random

# Deck Generated from ChatGPT

# Define the Card class
class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_card_value()
    
    def get_card_value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11  # Can be changed later based on game logic
        else:
            return int(self.rank)
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Define the Deck class (4 decks)
class Deck:
    discard = []
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks for _ in range(4)]
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck using random.shuffle"""
        random.shuffle(self.cards)

    def draw_card(self):
        """Draw a card from the top of the deck"""
        self.discard.append(self.cards.pop())
        return self.discard[-1]

    def reset(self):
        """Reset the deck to 52 cards and shuffle it"""
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
        self.shuffle()

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"

# ----------------------------------------------

def runBlackjack(turns):
    deck = Deck()

    for _ in range(turns):
        dealer1 = deck.draw_card()
        dealer2 = deck.draw_card()

        mine1 = deck.draw_card()
        mine2 = deck.draw_card()

        # do own policy
        mine = mine1.get_card_value() + mine2.get_card_value()

        # do dealer acitions
        dealer = dealer1.get_card_value() + dealer2.get_card_value()
        while dealer <= 16:
            dealer += deck.draw_card().get_card_value()

        
        if mine > 21:
            pass # you lose

        if dealer > 21:
            pass # you win

        if mine > dealer:
            pass
            # you win. deal with special bj case
        elif mine < dealer:
            pass
            # you lose
        else:
            pass
            # tie, you get back money

        if (len(deck.cards) / 208 < 0.75): # reshuffle into the shoe when this happens
            deck.cards += deck.discard
            deck.shuffle()
            print("shuffling")

runBlackjack(1000)


    


