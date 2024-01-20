from collections import Counter

from card_helper import parse_card_code

class Player:
    def __init__(self):
        self.Name = ""
        self.WarFunds = 0
        self.Debt = 0
        self. Stars = 3
        self.Cards = []
    
    def lookAtCards(self):
        groupedCards = Counter(self.Cards)

        groupedCardsStrArr = []
        for group in groupedCards:
            groupedCardsStrArr.append(f"{groupedCards[group]}x{parse_card_code(group)}")

        groupedCardsStr = ",".join(groupedCardsStrArr)
        return f'You have {groupedCardsStr}'
    
    def removeCard(self, card):
        self.Cards.remove(card)