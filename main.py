import pygame
from game import constant
import asyncio

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(48000, -16, 3, 1024)
        self.screen = pygame.display.set_mode(constant.SCREEN_SIZE)
        pygame.display.set_caption(constant.TITLE)
        self.clock = pygame.time.Clock()
        constant.init()
        from game import menu, music_select, instructions, board, highscore, credits
        self.states = {
            "leaderboard" : highscore.Leaderboard,
            "credits" : credits.Credits,
            "menu" : menu.Menu,
            "music select" : music_select.Music_Select,
            "instructions" : instructions.Instructions,
            "game" : board.Board,
            "score" : highscore.Score
        }
        self.current = None
        self.state = None
        self.scores = {"min" : 0, "sec" : 0, "bees" : 0, "combos" : []}
        self.running = True
    def set_state(self, state):
        if self.current != None:
            self.current.kill()
        self.state = state
        self.current = self.states[self.state](self)

async def main():
    game = Game()
    game.set_state("menu")
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if game.state == "leaderboard":
                    if event.key == pygame.K_RETURN:
                        game.set_state("menu")
                elif game.state == "credits":
                    if event.key == pygame.K_RETURN:
                        game.set_state("menu")
                elif game.state == "menu":
                    if event.key == pygame.K_RETURN:
                        game.set_state("music select")
                    elif event.key == pygame.K_l:
                        game.set_state("leaderboard")
                    elif event.key == pygame.K_c:
                        game.set_state("credits")
                elif game.state == "music select":
                    if event.key == pygame.K_RETURN:
                        game.set_state("instructions")
                elif game.state == "instructions":
                    if event.key == pygame.K_RETURN:
                        constant.SFX_CHANNEL.play(constant.SELECT_SOUND)
                        game.set_state("game")
                elif game.state == "game":
                    if event.key == pygame.K_r and game.current.paused == True:
                        game.set_state("game")
                    elif event.key == pygame.K_m and game.current.paused == True:
                        game.set_state("menu")
                elif game.state == "score":
                    if event.key == pygame.K_RETURN and game.current.leaderboard.current_slot == None:
                        game.set_state("menu")
        game.screen.fill(constant.BG)
        game.current.update()
        pygame.display.update()
        await asyncio.sleep(0)
        game.clock.tick(constant.FPS)
    pygame.quit()

asyncio.run(main())