#pylint: disable = C0103, C0116, W0312, C0115

"""
generates appropriate action for all valid cheats
"""

class Cheats:

    def __init__(self, game):
        self.game = game
        self.tooEasyUsed = False
        self.cheatDictionary = {'hesoyam':self.increaseLife,
                                'pauseghosts':self.pauseTheGhosts,
                                'resumeghosts':self.moveGhosts,
                                'changebg':self.changeBackGround,
                                'leavemealone':self.changeTargetToRandom,
                                'followme':self.everyoneTargetsPacman,
                                'makeghostsnormal':self.normalGhostMovement,
                                'makemeimmortal':self.makePacmanimmortal,
                                'makememortal':self.makePacmanMortal,
                                'toohard':self.makeGameEasy,
                                'resumeplayer':self.resumePacman,
                                'pauseplayer':self.pausePacman,
                                'tooeasy': self.makeItHard,
                                'fastgameplay':self.makeGameFast,
                                'slowgameplay': self.makeGameSlow
                                }

    def checkForCheats(self, text):
        for i in self.cheatDictionary:
            if i in text.lower():
                self.cheatDictionary.get(i)()
                self.activateCheat()
                break

    def activateCheat(self):
        self.game.cheatActivated = True
        self.game.text = ''

    def pauseTheGhosts(self):
        self.game.pauseGhosts = True

    def moveGhosts(self):
        self.game.pauseGhosts = False

    def increaseLife(self):
        self.game.pac.lives = 3

    def pausePacman(self):
        self.game.pausePlayer = True

    def resumePacman(self):
        self.game.pausePlayer = False

    def makePacmanimmortal(self):
        self.game.immortal = True

    def makeGameSlow(self):
        self.game.fastMode = False

    def makePacmanMortal(self):
        self.game.immortal = False

    def makeGameFast(self):
        self.game.fastMode = True

    def makeGameEasy(self):
        self.game.level = 2
        self.tooEasyUsed = False
        for ghost in self.game.ghosts:
            ghost.speed = ghost.setSpeed()

    def changeTargetToRandom(self):
        self.game.leavePacmanAlone = True
        self.game.allTargetPacman = False

    def normalGhostMovement(self):
        self.game.allTargetPacman = self.game.leavePacmanAlone = False

    def makeItHard(self):
        self.tooEasyUsed = self.game.allTargetPacman = True
        self.game.leavePacmanAlone = False

    def everyoneTargetsPacman(self):
        self.game.leavePacmanAlone = False
        self.game.allTargetPacman = True

    def changeBackGround(self):
        if self.game.env.currentBg == self.game.env.background:
            self.game.env.currentBg = self.game.env.background2
        else:
            self.game.env.currentBg = self.game.env.background
