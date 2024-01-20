from random import randrange
from player import Player
from card_helper import generateStartingHand

class NonPlayablePlayer(Player):
    def __init__(self, id):
        super().__init__()
        
        warfunds = randrange(1e6, 1e7+1)
        self.Name = f'NPC#{id}'
        self.Cards = generateStartingHand()
        self.WarFunds = warfunds
        self.Debt = warfunds
    
    def getRandomCard(self):
        return self.Cards[randrange(len(self.Cards))]