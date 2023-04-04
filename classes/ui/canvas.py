from classes.ui.bar import Bar
from classes.maths.vector2 import Vector2
from classes.entities.player import player

slots = []
playerHealthBar = Bar(Vector2(20,20),Vector2(450,20),(255, 66, 103),(136,33,53),player.stat_healthMax)
playerManaBar = Bar(Vector2(20,60),Vector2(225,20),(25, 159, 255),(0,67,120),player.stat_manaMax)
def draw_gameCanvas(screen):
    playerHealthBar.set_value(player.stat_health)
    playerManaBar.set_value(player.stat_mana)
    # ----- #
    playerHealthBar.draw(screen)
    playerManaBar.draw(screen)
