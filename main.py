#pylint: disable=C0116, C0103, W0312, E1101, C0115

"""
game class
"""

import sys
import pygame
from pygame.math import Vector2 as vec
import pacman
import cheats
import ghosts
import environment

class Game:

    def __init__(self):
        self.env = environment.Environment(self)
        self.env.renderEnvironment()
        self.width = self.height = 20
        self.pac = pacman.Player(self, vec(self.env.pPos))
        self.level = 3 #levels 1 to 3
        self.ghosts = [(ghosts.Ghost(self, vec(self.env.gPos[i]), i)) for i in range(4)]
        self.text = ''
        self.cheat = cheats.Cheats(self)
        self.beginScreen = True
        self.play = self.won = self.over = self.immortal = False
        self.cheatActivated = self.energizerUsed = self.pauseGhosts = self.pausePlayer = False
        self.currentScore = 0
        self.cheatDisplayTime = self.energizerTickCount = 0
        self.currChoice = self.winTickCount = self.gameTick = 0
        self.leavePacmanAlone = self.allTargetPacman = self.readyDisplayed = self.fastMode = False
        self.collisionTick = 15
        self.coins, self.energizers = [], []
        self.eyeUsed = [False] * 4

    def mainGameLoop(self):
        while True:
            if self.beginScreen:
                self.env.displayStartScreen()
                self.waitForInput()
            elif self.play:
                self.update()
                self.pac.playerMovements(self.currChoice)
                self.checkCheat()
                self.checkWin()
                self.currChoice = (self.currChoice + 1) % 3
            elif self.over:
                self.env.gameOverScreen()
                self.waitForInput()
            elif self.won:
                if self.winTickCount < 100:
                    self.update()
                    self.pausePlayer = self.pauseGhosts = True
                    self.winTickCount += 1
                else:
                    self.winTickCount = 0
                    self.pausePlayer = self.pauseGhosts = self.play = False
                    self.reset()
            else:
                break
        pygame.quit()
        sys.exit()

    def update(self):
        if self.gameTick < 50:
            self.pauseGhosts = self.pausePlayer = True
        elif self.gameTick >= 50 and not self.readyDisplayed:
            self.readyDisplayed = True
            self.pauseGhosts = self.pausePlayer = False
        self.pac.update(self.currChoice)
        self.updateCoins()
        if self.won:
            self.env.displayTwoMazes(self.winTickCount%20)
        else:
            self.env.displayLayout()
        self.env.displayCoins()
        self.env.displayScoreAndLives()
        self.env.drawSprite(self.env.currImage, self.pac.pixPos)
        self.drawGhostIfEnergizerUsed()
        self.checkCollision()
        self.gameTick += 1
        pygame.display.update()

    def displayGhost(self, image):
        for i in range(4):
            if self.eyeUsed[i]:
                self.env.drawSprite(self.env.eye, self.ghosts[i].pixPos)
            else: self.env.drawSprite(image, self.ghosts[i].pixPos)

    def displayTwoGhostImages(self):
        a = self.energizerTickCount % 10
        if a < 5:
            self.displayGhost(self.env.scared)
        else:
            self.displayGhost(self.env.scaredLight)

    def drawGhostIfEnergizerUsed(self):
        if not self.energizerUsed:
            for i in range(4):
                self.env.drawSprite(self.ghosts[i].colour, self.ghosts[i].pixPos)
        else:
            if self.energizerTickCount < 150:
                self.displayGhost(self.env.scared)
            else:
                self.displayTwoGhostImages()

    def checkCollision(self):
        if not self.pauseGhosts:
            for ghost in self.ghosts:
                ghost.moveGhosts()
        for i in range(4):
            if self.ghosts[i].gridPos == self.pac.gridPos and not self.eyeUsed[i]:
                if not self.immortal and not self.energizerUsed:
                    self.removeLife()
                elif self.energizerUsed:
                    pygame.time.delay(200)
                    self.collisionTick = 0
                    self.currentScore += 50
                    self.goToStartPosition(self.ghosts[i], i)
            if self.ghosts[i].inCentreOfGrid():
                if self.cheat.tooEasyUsed or self.eyeUsed[i]:
                    self.ghosts[i].speed = 4
            if self.eyeUsed[i] and self.ghosts[i].gridPos == vec(self.ghosts[i].startPos):
                self.resetGhost(self.ghosts[i], i)
                self.eyeUsed[i] = False
            if self.pauseGhosts and self.eyeUsed[i]:
                self.ghosts[i].moveGhosts()
        if self.collisionTick <= 15:
            self.collisionTick += 1

    def goToStartPosition(self, ghost, i):
        ghost.colour = self.env.eye
        self.eyeUsed[i] = True
        ghost.target = vec(ghost.startPos)

    def waitForInput(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.over:
                    self.reset()
                self.play = True
                self.beginScreen = False
                break

    def checkCheat(self):
        self.cheat.checkForCheats(self.text)

    def updateCoins(self):
        if self.pac.gridPos in self.env.coins:
            self.env.coins.remove(self.pac.gridPos)
            self.currentScore += 1

        elif self.pac.gridPos in self.env.energizers:
            self.energizerUsed = self.leavePacmanAlone = True
            self.energizerTickCount = 0
            self.env.energizers.remove(self.pac.gridPos)
            self.currentScore += 1

    def checkWin(self):
        if self.env.coins == [] and self.env.energizers == []:
            self.won = True
            self.play = False

    def resetPacmanAndGhosts(self):
        self.pauseGhosts = self.pausePlayer = False
        self.pac.gridPos = vec(self.pac.startPos)
        self.pac.pixPos = vec((self.pac.startPos[0]*20) + 35, (self.pac.startPos[1]*20) + 35)
        self.pac.dir = vec(1, 0)
        self.eyeUsed = [False] * 4
        self.immortal = self.energizerUsed = False
        self.energizerTickCount = self.gameTick = 0
        self.readyDisplayed = self.cheat.tooEasyUsed = self.fastMode = False
        self.cheat.moveGhosts()
        self.cheat.resumePacman()
        self.cheat.normalGhostMovement()
        self.cheat.makePacmanMortal()
        self.env.currImage = self.env.right
        self.pac.wantDir = None
        for i in range(4):
            self.resetGhost(self.ghosts[i], i)

    def removeLife(self):
        pygame.time.wait(1000)
        self.pac.lives -= 1
        if self.pac.lives == 0:
            self.play = False
            self.over = True
            pygame.time.wait(1500)
        else:
            self.resetPacmanAndGhosts()

    def reset(self):
        self.pac.lives = 3
        if self.env.coins == [] and self.env.energizers == [] and self.level < 3:
            self.level += 1
            self.allTargetPacman = True
        else:
            self.level = 1
            self.allTargetPacman = False
        self.currentScore = 0
        self.resetPacmanAndGhosts()
        self.env.switchBackground()
        self.coins, self.energizers = [], []
        self.env.updateCoinsAndEnergizers()
        self.won = self.over = False
        self.play = True

    def resetGhost(self, ghost, i):
        if self.level == 3:
            ghost.speed = ghost.setSpeed()
        ghost.gridPos = vec(ghost.startPos)
        ghost.pixPos = vec((ghost.gridPos.x * 20) + 35, (ghost.gridPos.y * 20) + 35)
        ghost.dir = vec(0, 0)
        ghost.colour = self.env.setGhosts(i)

pygame.init()
pygame.display.set_caption('Pac-man')
pygame.font.init()
if __name__ == '__main__':
    g = Game()
    g.mainGameLoop()
