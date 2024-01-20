from random import randrange

from card_type import CardType

def generateRandomCard():
    return CardType(randrange(1, 4))

def generateStartingHand():
    return [generateRandomCard() for i in range(3)]

def parse_card_name(card):
    card_lower = card.lower()
    if card_lower == "rock": return CardType.Rock
    if card_lower == "paper": return CardType.Paper
    if card_lower == "scissors": return CardType.Scissors
    return CardType.Unknown,

def parse_card_code(card):
    if card == CardType.Rock: return "Rock"
    if card == CardType.Paper: return "Paper"
    if card == CardType.Scissors: return "Scissors"
    raise Exception("Unknown card type")