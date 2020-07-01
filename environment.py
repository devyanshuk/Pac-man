#pylint: disable=W0312, C0103, C0116, C0115

"""
View class
"""

import pygame
from pygame.math import Vector2 as vec
from globalVariables import *
clock = pygame.time.Clock()

class Environment:

    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((width, height))
        self.initializeSprites()
        self.currentBg = self.background
        self.initializeFontsAndRender()
        self.walls, self.coins, self.gPos = [], [], []
        self.freeSpaces, self.energizers, self.gArea = [], [], []
        self.pPos = None
        self.totalPoints = 0
        self.width = self.height = 20
        self.clock = clock

        self.dirs = {pygame.K_LEFT: (-1, 0),
                     pygame.K_RIGHT:(1, 0),
                     pygame.K_UP: (0, -1),
                     pygame.K_DOWN: (0, 1)}

        self.images = {(-1, 0):self.left,
                       (1, 0):self.right,
                       (0, -1):self.up,
                       (0, 1):self.down}

        self.energizerImages = {(-1, 0):self.pinkLeft,
                                (1, 0):self.pinkRight,
                                (0, -1):self.pinkUp,
                                (0, 1):self.pinkDown}

    def initializeSprites(self):
        self.right = pygame.image.load("sprites/right.png")
        self.up = pygame.image.load("sprites/up.png")
        self.mouthClosed = pygame.image.load('sprites/closed.png')
        self.down = pygame.transform.flip(self.up, False, True)
        self.left = pygame.transform.flip(self.right, True, False)

        self.pinkRight = pygame.image.load("sprites/pinkRight.png")
        self.pinkUp = pygame.image.load("sprites/pinkUp.png")
        self.pinkMouthClosed = pygame.image.load("sprites/pinkClosed.png")
        self.pinkDown = pygame.transform.flip(self.pinkUp, False, True)
        self.pinkLeft = pygame.transform.flip(self.pinkRight, True, False)

        self.background2 = pygame.transform.scale(pygame.image.load("background/mazeRed.png"),
                                                  (mazeWidth, mazeHeight))
        self.background = pygame.transform.scale(pygame.image.load("background/mazeBlack.png"),
                                                 (mazeWidth, mazeHeight))


    def initializeFontsAndRender(self):
        self.asset_url = "fonts/pacFont.ttf"
        self.introTextFont = pygame.font.Font(self.asset_url, 27)
        self.endTextFont = pygame.font.Font(self.asset_url, 22)
        self.scoreFont = pygame.font.Font(None, 37)
        self.readyFont = pygame.font.Font(None, 30)
        self.livesFont = pygame.font.Font(None, 35)
        self.endScoreFont = pygame.font.Font(None, 46)
        self.scared = pygame.transform.scale(pygame.image.load("sprites/scared.png"),
                                             (20, 20))
        self.scaredLight = pygame.transform.scale(pygame.image.load("sprites/scaredLight.png"),
                                                  (20, 20))
        self.eye = pygame.transform.scale(pygame.image.load("sprites/eye.png"), (20, 20))
        self.fifty = self.scoreFont.render('+50', False, (255, 255, 255))
        self.currImage = self.lives_img = self.right

    def renderEnvironment(self):
        with open('layout.txt') as i:
            for y, line in enumerate(i):
                for x, char in enumerate(line):
                    if char == '#':
                        self.walls.append(vec(x, y))
                    elif char == '1':
                        self.coins.append(vec(x, y))
                        self.freeSpaces.append((x, y))
                        self.totalPoints += 1
                    elif char == 'P':
                        self.pPos = (x, y)
                    elif char == 'G':
                        self.gPos.append((x, y))
                        self.gArea.append((x, y))
                    elif char == 'E':
                        self.freeSpaces.append((vec(x, y)))
                        self.energizers.append((x, y))
                        self.totalPoints += 1
                    elif char == '0':
                        self.gArea.append((x, y))

    def setGhosts(self, ghost):
        return {0 : pygame.transform.scale(pygame.image.load('sprites/Red.png'),
                                           (20, 20)),
                1 : pygame.transform.scale(pygame.image.load('sprites/Pink.png'),
                                           (20, 20)),
                2 : pygame.transform.scale(pygame.image.load('sprites/Yellow.png'),
                                           (20, 20)),
                3 : pygame.transform.scale(pygame.image.load('sprites/Blue.png'),
                                           (20, 20))}.get(ghost)

    def displayStartScreen(self):
        self.screen.fill(black)
        self.screen.blit(self.introTextFont.render('1   2    3    4     5    6    7    8    9',
                                                   True, ((255, 255, 102))),
                         (width // 17, height//3))
        self.screen.blit(self.introTextFont.render('PRESS THE SPACEBAR TO BEGIN',
                                                   True, (170, 132, 58)),
                         (6, height//2-50))
        self.screen.blit(self.introTextFont.render('1 ONE player ONLY 9',
                                                   False, (44, 167, 198)),
                         (width // 8, height//2+50))
        pygame.display.update()

    def displayLayout(self, colour=black):
        self.screen.fill(colour)
        self.screen.blit(self.currentBg, (margin // 2, margin // 2))

    def displayScoreAndLives(self):
        self.screen.blit(self.scoreFont.render(f'Score: {self.game.currentScore}',
                                               False, (255, 255, 255)), (90, 5))
        if not self.game.readyDisplayed:
            self.screen.blit(self.readyFont.render('READY!', False, (250, 243, 127)), (270, 390))
        self.screen.blit(self.livesFont.render('Lives:', True, white), (350, 2))
        for x in range(self.game.pac.lives):
            self.screen.blit(self.lives_img, (430 + 25 * x, 5))
        if self.game.collisionTick < 15:
            self.screen.blit(self.fifty, (280, 300))

    def drawSprite(self, obj, pixelPos):
        self.screen.blit(obj, ((pixelPos.x - self.width // 2), (pixelPos.y - self.height // 2)))
        self.displayCheatActivated()
        if not self.game.fastMode:
            self.clock.tick(150)

    def displayCoins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (33, 175, 75),
                               (int(coin[0] * self.width) + self.width // 2 + margin // 2,
                                int(coin[1] * self.height)+self.height // 2 + margin // 2), 4)

        for energizer in self.energizers:
            pygame.draw.circle(self.screen, (151, 194, 231),
                               (int(energizer[0] * self.width) +
                                self.width // 2 + margin // 2,
                                int(energizer[1] * self.height) +
                                self.height // 2 + margin // 2), 6)

    def switchBackground(self):
        if self.currentBg == self.background:
            self.currentBg = self.background2
        else:
            self.currentBg = self.background

    def displayCheatActivated(self):
        if self.game.cheatActivated:
            if self.game.cheatDisplayTime < 80:
                self.screen.blit(self.livesFont.render('Cheat Activated',
                                                       True, white), (205, mazeHeight + 30))
                self.game.cheatDisplayTime += 1
            else:
                self.game.cheatDisplayTime = 0
                self.game.cheatActivated = False

    def updateCoinsAndEnergizers(self):
        with open('layout.txt') as i:
            for y, line in enumerate(i):
                for x, c in enumerate(line):
                    if c == '1':
                        self.coins.append(vec(x, y))
                    elif c == 'E':
                        self.energizers.append(vec(x, y))

    def displayTwoMazes(self, count):
        if count <= 10:
            self.currentBg = self.background
        else:
            self.currentBg = self.background2
        self.displayLayout()

    def gameOverScreen(self):
        self.screen.fill(black)
        self.screen.blit(self.introTextFont.render('1 Game Over 1',
                                                   True, (170, 132, 58)), (160, 140))
        self.screen.blit(self.introTextFont.render('Score:', True,
                                                   (170, 132, 58)), (215, 180))
        self.screen.blit(self.endScoreFont.render(f'{self.game.currentScore}',
                                                  True, (170, 132, 58)), (350, 180))
        self.screen.blit(self.endTextFont.render('Press SPACE bar to PLAY AGAIN', True,
                                                 (190, 190, 190)), (40, height//3+50))
        self.screen.blit(self.endTextFont.render('Press the escape button to QUIT',
                                                 True, (114, 141, 202)), (40, height//3 + 100))
        pygame.display.update()
