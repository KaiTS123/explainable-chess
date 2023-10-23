import numpy as np
from bitarray import bitarray
from enum import Enum

class Colour(Enum):
    WHITE = 1
    BLACK = 2

class Board:
    def __init__(self, FEN:str) -> None:
        self.whitePawns = bitarray(64)
        self.whiteKnights = bitarray(64)
        self.whiteBishops = bitarray(64)
        self.whiteRooks = bitarray(64)
        self.whiteQueens = bitarray(64)
        self.whiteKing = bitarray(64)

        self.blackPawns = bitarray(64)
        self.blackKnights = bitarray(64)
        self.blackBishops = bitarray(64)
        self.blackRooks = bitarray(64)
        self.blackQueens = bitarray(64)
        self.blackKing = bitarray(64)

        self.whitePawns.setall(0)
        self.whiteKnights.setall(0)
        self.whiteBishops.setall(0)
        self.whiteRooks.setall(0)
        self.whiteQueens.setall(0)
        self.whiteKing.setall(0)

        self.blackPawns.setall(0)
        self.blackKnights.setall(0)
        self.blackBishops.setall(0)
        self.blackRooks.setall(0)
        self.blackQueens.setall(0)
        self.blackKing.setall(0)

        fields = FEN.split()

        ranks = fields[0].split('/')
        ranks.reverse()

        for i, rank in enumerate(ranks):
            file = 0
            for char in rank:
                if char == 'P':
                    self.whitePawns[i*8+file] = True
                elif char == 'N':
                    self.whiteKnights[i*8+file] = True
                elif char == 'B':
                    self.whiteBishops[i*8+file] = True
                elif char == 'R':
                    self.whiteRooks[i*8+file] = True
                elif char == 'Q':
                    self.whiteQueens[i*8+file] = True
                elif char == 'K':
                    self.whiteKing[i*8+file] = True
                elif char == 'p':
                    self.blackPawns[i*8+file] = True
                elif char == 'n':
                    self.blackKnights[i*8+file] = True
                elif char == 'b':
                    self.blackBishops[i*8+file] = True
                elif char == 'r':
                    self.blackRooks[i*8+file] = True
                elif char == 'q':
                    self.blackQueens[i*8+file] = True
                elif char == 'k':
                    self.blackKing[i*8+file] = True
                else:
                    file += int(char)-1
                file += 1



        self.whitePieces = self.whitePawns | self.whiteKnights | self.whiteBishops | self.whiteRooks | self.whiteQueens | self.whiteKing
        self.blackPieces = self.blackPawns | self.blackKnights | self.blackBishops | self.blackRooks | self.blackQueens | self.blackKing

        if fields[1] == 'w':
            self.toPlay = Colour.WHITE
        else:
            self.toPlay = Colour.BLACK
        
        # KQkq (white can castle kingside, queenside, black can castle kingside queenside)
        self.castlingRights = []
        for char in fields[2]:
            if char != '-':
                self.castlingRights.append(char)

        # Square over which a pawn has just passed while moving two squares
        self.enPassant = fields[3]

        # Number of halfmoves since last capture or pawn advance (for fifty-move rule)
        self.halfMoveClock = int(fields[4])

        # Number of full moves (starts at 1 and increments after blacks move)
        self.fullMoves = int(fields[5])

    @classmethod
    def getStartingBoard(cls) -> None:
        return cls('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def getString(self):
        result = ''
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

    def getFENString(self):
        result = ''
        for i in range(7,-1,-1):
            gaps = 0
            for j in range(8):
                if not(self.whitePieces[i*8+j] | self.blackPieces[i*8+j]):
                    gaps += 1
                elif self.whitePawns[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'P'
                elif self.whiteKnights[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'N'
                elif self.whiteBishops[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'B'
                elif self.whiteRooks[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'R'
                elif self.whiteQueens[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'Q'
                elif self.whiteKing[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'K'
                elif self.blackPawns[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'p'
                elif self.blackKnights[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'n'
                elif self.blackBishops[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'b'
                elif self.blackRooks[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'r'
                elif self.blackQueens[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'q'
                elif self.blackKing[i*8+j]:
                    if gaps != 0:
                        result += str(gaps)
                        gaps = 0
                    result += 'k'
            if gaps != 0:
                result += str(gaps)
            if i != 0:
                result += '/'
        
        result += ' '
        if self.toPlay == Colour.WHITE:
            result += 'w'
        else:
            result += 'b'
        
        result += ' '
        if len(self.castlingRights) == 0:
            result += '-'
        else:
            for item in self.castlingRights:
                result += item
        
        result += ' '
        result += self.enPassant

        result += ' '
        result += str(self.halfMoveClock)

        result += ' '
        result += str(self.fullMoves)

        return result

def main():
    FEN = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
    board = Board(FEN)
    print(board.getString())

if __name__ == "__main__":
    main()
