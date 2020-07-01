#pylint: disable = C0103, C0116, W0312, C0115, C0411

"""
model class (player)
"""
import sys
import pygame
vec = pygame.math.Vector2
from globalVariables import margin

class Player:

    def __init__(self, game, initialPos):
        self.game = game
        self.gridPos = initialPos
        self.startPos = initialPos
        self.pixPos = vec((initialPos[0] * 20) + 35, (initialPos[1] * 20) + 35)
        self.wantDir = None
        self.dir = vec(1, 0)
        self.speed = 4
        self.lives = 3
        self.xdir = [(1, 0), (-1, 0)]
        self.ydir = [(0, 1), (0, -1)]

    def update(self, currChoice):
        if not self.game.pausePlayer:
            self.updateDir()
            self.updateGridPos()
            self.updateImage(currChoice)

    def updateDir(self):
        if self.wantDir and self.newMoveIsPossible():
            self.dir, self.wantDir = self.wantDir, None
        if self.thereIsNoWall(self.dir):
            self.pixPos += self.dir * self.speed

    def updateImage(self, currChoice):
        if not self.game.energizerUsed:
            if currChoice == 2:
                self.game.env.currImage = self.game.env.mouthClosed
            else:
                self.game.env.currImage = self.game.env.images.get((self.dir[0], self.dir[1]))
        else:
            if self.game.energizerTickCount < 200:
                if currChoice == 2:
                    self.game.env.currImage = self.game.env.pinkMouthClosed
                else:
                    self.game.env.currImage = self.game.env.energizerImages.get((self.dir[0],
                                                                                 self.dir[1]))
                self.game.energizerTickCount += 1
            else:
                self.game.energizerTickCount = 0
                self.game.energizerUsed = self.game.leavePacmanAlone = False

    def updateGridPos(self):
        if self.inCentreOfGrid():
            self.gridPos = ((self.pixPos.x - margin + self.game.width // 2) // 20 + 1,
                            (self.pixPos.y - margin + self.game.height // 2) // 20 + 1)

    def playerMovements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                try:
                    self.wantDir = vec(self.game.env.dirs.get(event.key))
                except ValueError:
                    self.game.text += event.unicode

    def inCentreOfGrid(self):
        return (self.pixPos.x + margin // 2) % self.game.height == 0 and \
                (self.pixPos.y + margin // 2) % self.game.width == 0

    def newMoveIsPossible(self):
        if self.wantDir in self.xdir and self.dir in self.ydir or \
           self.wantDir in self.ydir and self.dir in self.xdir:
            return self.inCentreOfGrid() and self.thereIsNoWall(self.wantDir)
        return self.thereIsNoWall(self.wantDir)

    def thereIsNoWall(self, vel):
        return vec(self.gridPos+vel) not in self.game.env.walls
