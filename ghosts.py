import pygame
from globalVariables import *
from main import *
vec = pygame.math.Vector2
from environment import *
import collections
import random

class Ghost:

    def __init__(self, game, pos, ghost):
        self.game = game
        self.gridPos = pos
        self.pixPos = vec((pos.x*20)+35,(pos.y*20)+35)
        self.startPos = (pos.x,pos.y)
        self.ghost = ghost
        self.colour = self.game.env.setGhosts(ghost)
        self.dir = vec(0,0)
        self.speed = self.setSpeed()
        self.adj = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.horizontal,self.vertical = 28,30
        self.ydirs = [vec(0,0),vec(0,1),vec(0,-1)]
        self.xdirs = [vec(0,0),vec(1,0),vec(-1,0)]

    def moveGhosts(self):
        self.target = self.setTarget()
        if self.target != self.gridPos:
            self.pixPos += self.dir * self.speed
            if self.inCentreOfGrid(): self.dir = self.newPath(self.target)
        self.gridPos = self.updateGridPosition()

    def setSpeed(self):
        if self.game.level == 3:
            if self.ghost == 0 or self.ghost == 3: return 4
            if self.ghost == 2: return 2
            if self.ghost == 1: return 1
        elif self.game.level == 2:
            if self.ghost == 0: return 4
            if self.ghost == 2: return 2
            if self.ghost == 1: return 1
            if self.ghost == 3: return 0.5
        elif self.game.level == 1: return 1

    def setTarget(self):
        if self.game.eyeUsed[self.ghost]: return vec(self.startPos)
        if self.insideGhostArea(self.gridPos) and not self.insideGhostArea(self.game.pac.gridPos): return vec(13,11)
        if self.game.level == 2 or self.game.level == 3: self.game.allTargetPacman = True

        if self.game.leavePacmanAlone: return self.randomTarget()
        if self.game.allTargetPacman: return self.game.pac.gridPos

        if self.ghost == 0 or self.ghost == 2: return self.game.pac.gridPos
        return self.randomTarget()

    def randomTarget(self): return vec(self.game.env.freeSpaces[random.randint(0,len(self.game.env.freeSpaces)-1)])

    def insideGhostArea(self,gridPos): return gridPos in self.game.env.gArea

    def updateGridPosition(self):
        return vec((self.pixPos[0]-margin + self.game.width//2)//self.game.width + 1,
        (self.pixPos[1]-margin + self.game.height//2)//self.game.height + 1)

    def inCentreOfGrid(self):
        return (self.pixPos.x+25) % 20 == 0 and self.dir in self.xdirs or (self.pixPos.y+25) % 20 == 0 and self.dir in self.ydirs

    def newPath(self, target):
        self.newGridPos = (self.calculateShortestPath([int(self.gridPos.x), int(self.gridPos.y)], [int(target[0]), int(target[1])]))
        return vec(self.newGridPos[0] - self.gridPos[0], self.newGridPos[1]- self.gridPos[1])

    def withinBounds(self,dir,pos):
        return ([dir[0]+pos[0], dir[1]+pos[1]]) if ((dir[0]+pos[0] >= 0) and
        (dir[0] + pos[0] < self.horizontal)) and ((dir[1]+pos[1] >= 0) and (dir[1] + pos[1] < self.vertical)) else None

    def calculateShortestPath(self, currentPos, targetGridPos):
        self.grid = [[False for _ in range(self.horizontal)] for _ in range(self.vertical)]
        for wall in self.game.env.walls:
            if wall[0] < self.horizontal and wall[1] < self.vertical: self.grid[int(wall[1])][int(wall[0])] = True
        q,self.ghostostToPlayerPath,visited = collections.deque(),[],[]
        q.append(currentPos)
        while q:
            self.currentGridPos = q.popleft()
            visited.append(self.currentGridPos)
            if self.currentGridPos == targetGridPos: break
            else:
                for currDir in self.adj:
                    self.newPos = self.withinBounds(currDir,self.currentGridPos)
                    if self.newPos and (self.newPos not in visited) and (not self.grid[self.newPos[1]][self.newPos[0]]):
                        q.append(self.newPos)
                        self.ghostostToPlayerPath.append((self.currentGridPos,self.newPos))
        self.shortestPath = [targetGridPos]
        while True:
            for dir in self.ghostostToPlayerPath:
                if dir[1] == targetGridPos:
                    targetGridPos = dir[0]
                    self.shortestPath.insert(0, dir[0])
            if targetGridPos == currentPos: break

        return self.shortestPath[1]
