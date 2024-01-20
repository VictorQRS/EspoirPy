define me = Character("Me")
define president = Character("President")
define employee = Character("Employee")

init python:
    import espoir_context
    import card_helper
    import game_logic
    from battle_result import BattleResult
    from battle_denial_reason import BattleDenialReason
    from leave_denial_reason import LeaveDenialReason
    
    context = espoir_context.EspoirContext()
    n = 0

label start:
    scene bg room
    
    "This is a game of wits, pay attention to it."

# label welcome:
#     scene espoir
#     show president
    
#     president "Welcome do Espoir, the best and most expensive cruiser in the world."
#     president "You are more than welcome to enjoy its luxury for free."
#     president "Well, free as long you can buy yourselves a ticket."
#     president "For you to afford it, you'll need to play a game."

# label warfund:
#     scene money mountain
#     show president
    
#     president "In this game, you may need money. We're going to lend you some, but there are two rules."
#     president "First, the minimum amount is $1 Million and the maximum amount is $10 Million. Of course, the unit is in millions, so I won't allow you to choose pocket change such as $500000"
#     president "Secondly, as this is a loan, we require you to return it to us with interest of 1.5\% every ten minutes."

#     python:
#         context.MainCharacter.WarFunds = renpy.input(
#             "How many millions do you want?",
#             "1",
#             "1234567890",
#             length=2)
    
#     "You have chosen $[context.MainCharacter.WarFunds] Million."

# label game_explanation:
#     scene game explanation 1
#     show president

#     president "The game is pretty simple: Restricted Rock-Paper-Scissors. Each player shall receive three cards in the beginning, those of which can be of any type Rock, Paper or Scissor."
#     president "Then, 2 players will decide to play against each other, bet at least one star, and if both parties agree, they will play a card."
#     president "And just like Rock-Paper-Scissor, rock beats scissor, which beats paper, which beats rock."
#     president "The winner wins the bet and it's their possession by right."
#     president "The cards used for this bet are then thrown away."
#     president "But remember, you are not allowed to throw away your cards. And you'll be heavily penalized for that!"

#     scene game explanation 2
#     show president
#     president "To leave this room, one needs to pay 3 stars and have NO cards left."
#     president "Remember that you still need to pay your debt, and if you don't have the amount with you, you'll need to pay that even after the Espoir returns to land."
#     president "Ah! About those who could not leave this room by the end of this 1 hour journey, well... let's just say it will not be pretty."

label card_distribution:
    scene wall
    show employee

    employee "Now, let's start card distribution..."

    scene introspect
    show me

    $ context.MainCharacter.Cards = card_helper.generateStartingHand()
    $ mc_hand = context.MainCharacter.lookAtCards()

    "[mc_hand]"

    scene wall
    show president

    president "Now that everyone received their cards, let the game begin!"

label hall:
    scene hall

    $ card_frequency = context.showCardfrequency()
    "[card_frequency]"

label menu_hall:
    $ chosen = context.Players[1:][n:n+5]
    
    menu hall_choices:
        "Choose an option:"

        "Battle [chosen[0].Name]":
            $ opponent = chosen[0]
            $ n = 0
            jump battle_negotiation
        "Battle [chosen[1].Name]":
            $ opponent = chosen[1]
            $ n = 0
            jump battle_negotiation
        "Battle [chosen[2].Name]":
            $ opponent = chosen[2]
            $ n = 0
            jump battle_negotiation
        "Battle [chosen[3].Name]":
            $ opponent = chosen[3]
            $ n = 0
            jump battle_negotiation
        "Battle [chosen[4].Name]":
            $ opponent = chosen[4]
            $ n = 0
            jump battle_negotiation
        "prev" if n != 0:
            $ n -= 5
            jump menu_hall
        "next" if len(chosen) == 5:
            $ n += 5
            jump menu_hall
        "leave":
            jump leave

label battle_negotiation:
    scene battle
    show me at right
    show opponent at left
    
    "[opponent.Name]" "Wanna fight me? Fine."

    python:
        stars = int(renpy.input(
            "How many stars you want to bet on?",
            "1",
            "1234567890",
            length=1))
        battleAllowedInfo = game_logic.canBattleOccur(context.MainCharacter, opponent, stars)
        battleAllowed = battleAllowedInfo[0]
        battleNotAllowedReason = battleAllowedInfo[1]
    
    if battleAllowed:
        "[opponent.Name]" "You're on!"
        jump battle

    if battleNotAllowedReason == BattleDenialReason.Player2LackStars:
        "[opponent.Name]" "I don't have that much, search someone else"
    if battleNotAllowedReason == BattleDenialReason.Player1LackStars:
        "[opponent.Name]" "You must be on drugs, you don't have that much! Search someone else"
    if battleNotAllowedReason == BattleDenialReason.ZeroStars:
        "[opponent.Name]" "Zero? Are you crazy? Search someone else to annoy."
    jump hall

label battle:
    scene battle
    show me at right
    show opponent at left
    
    $ mc_hand = context.MainCharacter.lookAtCards()
    "[mc_hand]"

    python:
        card = card_helper.parse_card_name(renpy.input("What card are you going to play?"))
        parsedCard = card_helper.parse_card_code(card)
        opponentCard = opponent.getRandomCard()
        parsedOpponentCard = card_helper.parse_card_code(opponentCard)
        fight_result = game_logic.fight_p(context.MainCharacter, card, opponent, opponentCard, stars)
    
    "You played [parsedCard]"
    "[opponent.Name] played [parsedOpponentCard]"
    
    if fight_result == BattleResult.Victory:
        "Congratulations! You won [stars] stars."
    if fight_result == BattleResult.Loss:
        "Too bad! You lost [stars] stars."
    if fight_result == BattleResult.Draw:
        "It's a draw! No stars changed hands."
    
    "You now have [context.MainCharacter.Stars] stars in total."

    # They should never be smaller than 0, but just in case.
    $ canNoLogerPlay = context.MainCharacter.Stars <= 0 or (context.MainCharacter.Stars < 3 and len(context.MainCharacter.Cards) <= 0)
    if canNoLogerPlay:
        jump game_over_failure
    
    $ game_logic.simulateBattles(context)

    jump hall

label leave:
    python:
        isLeavedAllowedInfo = game_logic.canLeave(context.MainCharacter)
        isLeaveAllowed = isLeavedAllowedInfo[0]
        isLeaveNorAllowedReason = isLeavedAllowedInfo[1]
    
    if isLeaveAllowed:
        jump reward_cerimony
        
    if isLeaveNorAllowedReason == LeaveDenialReason.PlayerHasCards:
        employee "You still have cards in your possession, you must use them up before leaving."
    if isLeaveNorAllowedReason == LeaveDenialReason.NotEnoughStars:
        employee "You need at least 3 stars to leave this room. Go get some more before leaving."
    jump hall

label reward_cerimony:
    scene wall
    show employee

    employee "Congratulations for clearing out the Restricted Rock-Paper-Scissors game!"
    employee "You have [context.MainCharacter.Stars] stars and we'll collect three for your ticket."

    $ context.MainCharacter.Stars -= 3

    employee "Additionally, we'd like to tell that you can sell the excess of stars, each costing $1 million."

    $ reward = game_logic.rewardCerimony(context.MainCharacter)
    $ remainingStars = context.MainCharacter.Stars
    if remainingStars > 0:
        employee "It seems you have an additional of [remainingStars] stars."
        employee "So here's your $[reward]."
    else:
        employee "It's unfortunate that you don't have any remaining stars."

label debt_cerimony:
    scene wall
    show employee

    $ debtInfo = game_logic.debtCerimony(context.MainCharacter)
    $ baseDebt = debtInfo[0]
    $ actualDebt = debtInfo[1]

    employee "Now, for the debt collection, according to our calculations you owe us $[baseDebt]."
    employee "We will now collect that from your war funds."

    if actualDebt > 0:
        employee "It seems you now owe us $[actualDebt]. Don't worry, you can enjoy the cruise, but we will be seeing each other soon..."
    else:
        $ actualReward = -1 * actualDebt;
        employee "Congratulations, you survived the game and is now leaving with $[actualReward] in your account. That was truly a great night, wasn't it?"
    return

label game_over_failure:
    employee "Game is over! It's time for you to pay..."
    employee "Say good bye to your life. Die? Oh no, far worse..."
    return