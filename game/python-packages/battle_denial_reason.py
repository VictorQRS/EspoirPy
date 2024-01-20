from enum import IntEnum

class BattleDenialReason(IntEnum):
    Player1LackStars = 0,
    Player2LackStars = 1,
    PlayersCanNotFightThemselves = 2,
    ZeroStars = 3,