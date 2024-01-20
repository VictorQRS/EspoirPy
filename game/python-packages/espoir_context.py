from collections import Counter

from card_helper import parse_card_code
from non_playable_player import NonPlayablePlayer
from player import Player

MAX_PLAYERS = 100

class EspoirContext:
    def __init__(self):
        self.MainCharacter = Player()
        self.Players = [self.MainCharacter]
        for i in range(1, MAX_PLAYERS):
            self.Players.append(NonPlayablePlayer(i))
        
        # TODO: 10-min task

    def startGame():
        pass

    def finishGame():
        pass

    def getCardFrequency(self):
        cards = []
        for player in self.Players:
            cards.extend(player.Cards)
        return Counter(cards)

    def showCardfrequency(self):
        groupedCards = self.getCardFrequency()

        groupedCardsStrArr = []
        for group in groupedCards:
            groupedCardsStrArr.append(f"{groupedCards[group]}x{parse_card_code(group)}")

        groupedCardsStr = ",".join(groupedCardsStrArr)
        return f'Only {groupedCardsStr} remaining.'