from enum import Enum

class Colour(Enum):
    WHITE = 1
    BLACK = 2
    
    def opposite(col):
        if col == Colour.BLACK:
            return Colour.WHITE
        else:
            return Colour.BLACK
        
    def fromString(string: str):
        if string.lower() in ["w", "white"]:
            return Colour.WHITE
        if string.lower() in ["b", "black"]:
            return Colour.BLACK