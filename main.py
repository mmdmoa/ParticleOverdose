import pygame as pg
from pygame.locals import *

from core.event_holder import EventHolder
import core.common_resources as cr
from core.game import Game
from core.constants import *
from core.common_functions import *
import core.constants as const
import asyncio

pic = "./pic.png"
res = "./pic_res.png"

pg.init()

cr.font = pg.font.SysFont('monospace', 20)
cr.little_font = pg.font.SysFont('Arial', 15)
cr.smallest_font = pg.font.SysFont('monospace', 10)

font = cr.font
last_time = 0


def game_over_text() :
    diamonds = cr.game.player.acquired_diamonds

    return cr.little_font.render(
        f"You found {diamonds} Diamonds in {last_time} seconds! Good Job! press X to replay", True,
        "red", "gray")


def win_text() :
    return cr.little_font.render(
        f"You all Diamonds in {last_time} seconds! Very nice! press X to replay", True, "red",
        "gray")


pg.mouse.set_visible(False)

just_lost = False
just_won = False


async def main() :
    global last_time, just_lost, just_won

    # cr.screen = pg.display.set_mode([900, 640], SCALED | FULLSCREEN)
    if IS_WEB :  # web only, scales automatically
        cr.screen = pg.display.set_mode([900 * 0.6, 640 * 0.6])
    else :
        cr.screen = pg.display.set_mode([900 * 0.6, 640 * 0.6], SCALED | FULLSCREEN)

    start_playing = False

    cr.event_holder = EventHolder()
    cr.event_holder.should_render_debug = False
    cr.event_holder.determined_fps = 1000

    start_playing_text = font.render("press P to start Playing!", True, "red")


    def reset_game() :
        cr.world = json.loads(open(levels_root + "test.json").read())
        cr.game = Game()
        cr.game.init()


    reset_game()

    fps_text = lambda : cr.smallest_font.render(f"FPS :{int(cr.event_holder.final_fps)}"
                                              f" PARTICLES: {cr.game.player.particles.__len__()}",
        True, "white")

    # I F**king love OOP :heart:
    while not cr.event_holder.should_quit :
        if cr.game.player.lives == 0 and not just_lost :
            just_lost = True
            last_time = round(now() - cr.game.timer, 2)

        if cr.game.player.acquired_diamonds == cr.game.level.total_diamonds and not just_won :
            print("Won!")
            just_won = True
            last_time = round(now() - cr.game.timer, 2)

        if K_F3 in cr.event_holder.pressed_keys :
            cr.event_holder.should_render_debug = not cr.event_holder.should_render_debug

        if K_x in cr.event_holder.released_keys :
            if just_won or just_lost :
                reset_game()
                just_lost = False
                just_won = False

        cr.event_holder.get_events()
        if start_playing and not (just_lost or just_won) :
            cr.game.check_events()

        cr.game.render()
        if not start_playing :
            text_rect = start_playing_text.get_rect()
            text_rect.center = cr.screen.get_rect().center
            cr.screen.blit(start_playing_text, text_rect)
            if K_p in cr.event_holder.released_keys or K_LCTRL in cr.event_holder.released_keys :
                start_playing = True
                just_lost = False
                cr.game.timer = now()

        text = fps_text()
        cr.screen.blit(fps_text(),
            (cr.screen.get_width() - text.get_width(), cr.screen.get_height() - text.get_height()))

        if just_lost :
            surface = game_over_text()
            rect = surface.get_rect()
            rect.center = cr.screen.get_rect().center
            cr.screen.blit(surface, rect)

        if just_won :
            surface = game_over_text()
            rect = surface.get_rect()
            rect.center = cr.screen.get_rect().center
            cr.screen.blit(surface, rect)

        pg.display.update()

        # pg.image.save(cr.screen, "./dump.jpg")

        await asyncio.sleep(0)


if __name__ == '__main__' :
    asyncio.run(main())
