from random import randrange
from battle_denial_reason import BattleDenialReason
from battle_result import BattleResult
from card_type import CardType
from leave_denial_reason import LeaveDenialReason
from non_playable_player import NonPlayablePlayer

def canBattleOccur(player1, player2, stars):
    if player1.Name == player2.Name:
        return (False, BattleDenialReason.PlayersCanNotFightThemselves)
    if player1.Stars < stars:
        return (False, BattleDenialReason.Player1LackStars)
    if player2.Stars < stars:
        return (False, BattleDenialReason.Player2LackStars)
    if stars == 0:
        return (False, BattleDenialReason.ZeroStars)
    return (True, None)

def fight_p(player1, card1, player2, card2, stars):
    player1.removeCard(card1)
    player2.removeCard(card2)

    result = fight_c(card1, card2)
    if result == BattleResult.Victory:
        player1.Stars += stars
        player2.Stars -= stars
    elif result == BattleResult.Loss:
        player1.Stars -= stars
        player2.Stars += stars
    return result

def fight_c(card1, card2):
    if card1 == card2: return BattleResult.Draw
    if card1 == CardType.Rock:
        if card2 == CardType.Paper: return BattleResult.Loss
        if card2 == CardType.Scissors: return BattleResult.Victory
    if card1 == CardType.Paper:
        if card2 == CardType.Rock: return BattleResult.Victory
        if card2 == CardType.Scissors: return BattleResult.Loss
    if card1 == CardType.Scissors:
        if card2 == CardType.Paper: return BattleResult.Victory
        if card2 == CardType.Rock: return BattleResult.Loss
    raise Exception("CardType not allowed.")

def getRandomPlayer(context):
    index = randrange(1, len(context.Players))
    return context.Players[index]

def simulateBattles(context):
    maxSimultaneousBattles = min(20, len(context.Players))
    numSimultaneousBattles = randrange(maxSimultaneousBattles)

    for i in range(0, numSimultaneousBattles):
        player1 = NonPlayablePlayer(0)
        player2 = NonPlayablePlayer(0)
        while player1.Name == player2.Name:
            player1 = getRandomPlayer(context)
            player2 = getRandomPlayer(context)
        
        card1 = player1.getRandomCard()
        card2 = player2.getRandomCard()
        stars = randrange(1, min(player1.Stars, player2.Stars) + 1)
        fight_p(player1, card1, player2, card2, stars)

        # kick players that has 0 stars or 0 cards
        # TODO: this logic needs to change as people can buy stuff
        context.Players = [player for player in context.Players if player.Stars > 0 and len(player.Cards) > 0]
                
def canLeave(player):
    if player.Cards.Any():
        return (False, LeaveDenialReason.PlayerHasCards)
    if player.Stars < 3:
        return (False, LeaveDenialReason.NotEnoughStars)
    return (True, None)

def rewardCerimony(player):
    player.Stars -= 3
    reward = player.Stars * 1e6
    player.WarFunds += reward
    return reward

def debtCerimony(player):
    return (player.Debt, player.Debt - player.WarFunds)