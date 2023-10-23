import numpy as np
from bitarray import bitarray
from enum import Enum

class Colour(Enum):
    WHITE = 1
    BLACK = 2

class Board:
    def __init__(self) -> None:
        self.whitePawns = bitarray('0000000011111111000000000000000000000000000000000000000000000000')
        self.whiteKnights = bitarray('0100001000000000000000000000000000000000000000000000000000000000')
        self.whiteBishops = bitarray('0010010000000000000000000000000000000000000000000000000000000000')
        self.whiteRooks = bitarray('1000000100000000000000000000000000000000000000000000000000000000')
        self.whiteQueens = bitarray('0001000000000000000000000000000000000000000000000000000000000000')
        self.whiteKing = bitarray('0000100000000000000000000000000000000000000000000000000000000000')

        self.whitePieces = self.whitePawns | self.whiteKnights | self.whiteBishops | self.whiteRooks | self.whiteQueens | self.whiteKing

        self.blackPawns = bitarray('0000000000000000000000000000000000000000000000001111111100000000')
        self.blackKnights = bitarray('0000000000000000000000000000000000000000000000000000000001000010')
        self.blackBishops = bitarray('0000000000000000000000000000000000000000000000000000000000100100')
        self.blackRooks = bitarray('0000000000000000000000000000000000000000000000000000000010000001')
        self.blackQueens = bitarray('0000000000000000000000000000000000000000000000000000000000010000')
        self.blackKing = bitarray('0000000000000000000000000000000000000000000000000000000000001000')

        self.blackPieces = self.blackPawns | self.blackKnights | self.blackBishops | self.blackRooks | self.blackQueens | self.blackKing

        self.toPlay = Colour.WHITE
        
        # KQkq (white can castle kingside, queenside, black can castle kingside queenside)
        self.castlingRights = bitarray('1111')

    def getString(self):
        result = ""
        for i in range(7,-1,-1):
            for j in range(8):
                if self.whitePawns[i*8+j]:
                    result += '♟︎'
                elif self.whiteKnights[i*8+j]:
                    result += '♞'
                elif self.whiteBishops[i*8+j]:
                    result += '♝'
                elif self.whiteRooks[i*8+j]:
                    result += '♜'
                elif self.whiteQueens[i*8+j]:
                    result += '♛'
                elif self.whiteKing[i*8+j]:
                    result += '♚'
                elif self.blackPawns[i*8+j]:
                    result += '♙'
                elif self.blackKnights[i*8+j]:
                    result += '♘'
                elif self.blackBishops[i*8+j]:
                    result += '♗'
                elif self.blackRooks[i*8+j]:
                    result += '♖'
                elif self.blackQueens[i*8+j]:
                    result += '♕'
                elif self.blackKing[i*8+j]:
                    result += '♔'
                else:
                    result += '.'
            result += '\n'
        return result

def main():
    board = Board()
    print(board.getString())

if __name__ == "__main__":
    main()