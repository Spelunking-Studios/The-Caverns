import os, json
from map import Map

class Level:
    """Represents a single number"""
    def __init__(self, game, number = 1):
        """Initializes the level
        
        Arguments:
        -----
        game: Game
        number: int
        """
        self.game = game
        self.map = Map(self)
        self.number = number
        self.loaded = False
    def load(self):
        """Loads the level"""
        if self.loaded:
            return
        levelFile = open(self.game.asset(
            os.path.join("levels", "level1.json")
        ), "r")
        levelData = json.load(levelFile)
        self.map.loadFromJSON(levelData)
        self.loaded = True
    def update(self):
        """Updates the level"""
        pass
    def draw(self):
        """Draws the level"""
        self.map.draw()