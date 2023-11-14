import numpy as np
from bitarray import bitarray
from enum import Enum
import random
import copy

class Colour(Enum):
    WHITE = 1
    BLACK = 2

class Board:
    def __init__(self, FEN=None, orig=None) -> None:
        if not orig and not FEN:
            FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

        if FEN:
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
            self.pieces = self.blackPieces | self.whitePieces

            if fields[1] == 'w':
                self.toPlay = Colour.WHITE
            else:
                self.toPlay = Colour.BLACK
            
            # KQkq (white can castle kingside, queenside, black can castle kingside queenside)
            self.castlingRights = set()
            for char in fields[2]:
                if char != '-':
                    self.castlingRights.add(char)

            # Square over which a pawn has just passed while moving two squares
            self.enPassant = fields[3]

            # Number of halfmoves since last capture or pawn advance (for fifty-move rule)
            self.halfMoveClock = int(fields[4])

            # Number of full moves (starts at 1 and increments after blacks move)
            self.fullMoves = int(fields[5])
        elif orig:
            self.whitePawns = copy.copy(orig.whitePawns)
            self.whiteKnights = copy.copy(orig.whiteKnights)
            self.whiteBishops = copy.copy(orig.whiteBishops)
            self.whiteRooks = copy.copy(orig.whiteRooks)
            self.whiteQueens = copy.copy(orig.whiteQueens)
            self.whiteKing = copy.copy(orig.whiteKing)

            self.blackPawns = copy.copy(orig.blackPawns)
            self.blackKnights = copy.copy(orig.blackKnights)
            self.blackBishops = copy.copy(orig.blackBishops)
            self.blackRooks = copy.copy(orig.blackRooks)
            self.blackQueens = copy.copy(orig.blackQueens)
            self.blackKing = copy.copy(orig.blackKing)

            self.whitePieces = self.whitePawns | self.whiteKnights | self.whiteBishops | self.whiteRooks | self.whiteQueens | self.whiteKing
            self.blackPieces = self.blackPawns | self.blackKnights | self.blackBishops | self.blackRooks | self.blackQueens | self.blackKing
            self.pieces = self.blackPieces | self.whitePieces

            self.toPlay = orig.toPlay
            self.castlingRights = orig.castlingRights
            self.enPassant = orig.enPassant
            self.halfMoveClock = orig.halfMoveClock
            self.fullMoves = orig.fullMoves

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
        if self.enPassant != '':
            result += self.enPassant
        else:
            result += '-'

        result += ' '
        result += str(self.halfMoveClock)

        result += ' '
        result += str(self.fullMoves)

        return result

    def generatePseudoLegalMoves(self) -> list[tuple[int, int, int]]:
        moves = []
        for i in range(64):
            moves.extend(self.generatePseudoLegalPawnMoves(i))
            moves.extend(self.generatePseudoLegalKnightMoves(i))
            moves.extend(self.generatePseudoLegalKingMoves(i))
            moves.extend(self.generatePseudoLegalRookMoves(i))
            moves.extend(self.generatePseudoLegalBishopMoves(i))
            moves.extend(self.generatePseudoLegalQueenMoves(i))
        return moves
    
    def generatePseudoLegalRookMoves(self, position) -> list[tuple[int,int,int]]:
        moves = []
        if self.toPlay == Colour.WHITE and self.whiteRooks[position]:
            endPos = position-1
            while endPos % 8 != 7 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 1
            if endPos % 8 != 7 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+1
            while endPos % 8 != 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 1
            if endPos % 8 != 0 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position-8
            while endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 8
            if endPos // 8 >= 0 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+8
            while endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 8
            if endPos // 8 != 8 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

        if self.toPlay == Colour.BLACK and self.blackRooks[position]:
            endPos = position-1
            while endPos % 8 != 7 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 1
            if endPos % 8 != 7 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+1
            while endPos % 8 != 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 1
            if endPos % 8 != 0 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position-8
            while endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 8
            if endPos // 8 >= 0 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+8
            while endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 8
            if endPos // 8 != 8 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))
        return moves
    
    def generatePseudoLegalBishopMoves(self, position) -> list[tuple[int,int,int]]:
        moves = []
        if self.toPlay == Colour.WHITE and self.whiteBishops[position]:
            endPos = position-9
            while endPos % 8 != 7 and endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 9
            if endPos % 8 != 7 and endPos // 8 >= 0 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position-7
            while endPos % 8 != 0 and endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 7
            if endPos % 8 != 0 and endPos // 8 >= 0 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+7
            while endPos % 8 != 7 and endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 7
            if endPos % 8 != 7 and endPos // 8 != 8 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+9
            while endPos % 8 != 0 and endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 9
            if endPos % 8 != 0 and endPos // 8 != 8 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))
            

        if self.toPlay == Colour.BLACK and self.blackBishops[position]:
            endPos = position-9
            while endPos % 8 != 7 and endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 9
            if endPos % 8 != 7 and endPos // 8 >= 0 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position-7
            while endPos % 8 != 0 and endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 7
            if endPos % 8 != 0 and endPos // 8 >= 0 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+7
            while endPos % 8 != 7 and endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 7
            if endPos % 8 != 7 and endPos // 8 != 8 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+9
            while endPos % 8 != 0 and endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 9
            if endPos % 8 != 0 and endPos // 8 != 8 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))
        return moves
    
    def generatePseudoLegalQueenMoves(self, position) -> list[tuple[int,int,int]]:
        moves = []
        if self.toPlay == Colour.WHITE and self.whiteQueens[position]:
            endPos = position-9
            while endPos % 8 != 7 and endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 9
            if endPos % 8 != 7 and endPos // 8 >= 0 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position-7
            while endPos % 8 != 0 and endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 7
            if endPos % 8 != 0 and endPos // 8 >= 0 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+7
            while endPos % 8 != 7 and endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 7
            if endPos % 8 != 7 and endPos // 8 != 8 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+9
            while endPos % 8 != 0 and endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 9
            if endPos % 8 != 0 and endPos // 8 != 8 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))
            
            endPos = position-1
            while endPos % 8 != 7 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 1
            if endPos % 8 != 7 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+1
            while endPos % 8 != 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 1
            if endPos % 8 != 0 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position-8
            while endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 8
            if endPos // 8 >= 0 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+8
            while endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 8
            if endPos // 8 != 8 and self.blackPieces[endPos]:
                moves.append((position, endPos, 4))

        if self.toPlay == Colour.BLACK and self.blackQueens[position]:
            endPos = position-9
            while endPos % 8 != 7 and endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 9
            if endPos % 8 != 7 and endPos // 8 >= 0 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position-7
            while endPos % 8 != 0 and endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 7
            if endPos % 8 != 0 and endPos // 8 >= 0 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+7
            while endPos % 8 != 7 and endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 7
            if endPos % 8 != 7 and endPos // 8 != 8 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+9
            while endPos % 8 != 0 and endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 9
            if endPos % 8 != 0 and endPos // 8 != 8 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))
            
            endPos = position-1
            while endPos % 8 != 7 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 1
            if endPos % 8 != 7 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+1
            while endPos % 8 != 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 1
            if endPos % 8 != 0 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position-8
            while endPos // 8 >= 0 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos -= 8
            if endPos // 8 >= 0 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))

            endPos = position+8
            while endPos // 8 != 8 and not self.pieces[endPos]:
                moves.append((position, endPos, 0))
                endPos += 8
            if endPos // 8 != 8 and self.whitePieces[endPos]:
                moves.append((position, endPos, 4))
        return moves

    def generatePseudoLegalKingMoves(self, position) -> list[tuple[int, int, int]]:
        moves = []
        if self.toPlay == Colour.WHITE and self.whiteKing[position]:
            if position // 8 < 7:
                if position % 8 > 0 and not self.whitePieces[position+7]:
                    moves.append((position, position+7, 4*self.blackPieces[position+7]))
                if position % 8 < 7 and not self.whitePieces[position+9]:
                    moves.append((position, position+9, 4*self.blackPieces[position+9]))
                if not self.whitePieces[position+8]:
                    moves.append((position, position+8, 4*self.blackPieces[position+8]))
            if position // 8 > 0:
                if position % 8 > 0 and not self.whitePieces[position-9]:
                    moves.append((position, position-9, 4*self.blackPieces[position-9]))
                if position % 8 < 7 and not self.whitePieces[position-7]:
                    moves.append((position, position-7, 4*self.blackPieces[position-7]))
                if not self.whitePieces[position-8]:
                    moves.append((position, position-8, 4*self.blackPieces[position-8]))
            if position % 8 > 0 and not self.whitePieces[position-1]:
                moves.append((position, position-1, 4*self.blackPieces[position-1]))
            if position % 8 < 7 and not self.whitePieces[position+1]:
                moves.append((position, position+1, 4*self.blackPieces[position+1]))
            if 'K' in self.castlingRights and not self.pieces[5:7].any():
                moves.append((4, 6, 2))
            if 'Q' in self.castlingRights and not self.pieces[1:4].any():
                moves.append((4, 2, 3))
        elif self.toPlay == Colour.BLACK and self.blackKing[position]:
            if position // 8 < 7:
                if position % 8 > 0 and not self.blackPieces[position+7]:
                    moves.append((position, position+7, 4*self.whitePieces[position+7]))
                if position % 8 < 7 and not self.blackPieces[position+9]:
                    moves.append((position, position+9, 4*self.whitePieces[position+9]))
                if not self.blackPieces[position+8]:
                    moves.append((position, position+8, 4*self.whitePieces[position+8]))
            if position // 8 > 0:
                if position % 8 > 0 and not self.blackPieces[position-9]:
                    moves.append((position, position-9, 4*self.whitePieces[position-9]))
                if position % 8 < 7 and not self.blackPieces[position-7]:
                    moves.append((position, position-7, 4*self.whitePieces[position-7]))
                if not self.blackPieces[position-8]:
                    moves.append((position, position-8, 4*self.whitePieces[position-8]))
            if position % 8 > 0 and not self.blackPieces[position-1]:
                moves.append((position, position-1, 4*self.whitePieces[position-1]))
            if position % 8 < 7 and not self.blackPieces[position+1]:
                moves.append((position, position+1, 4*self.whitePieces[position+1]))
            if 'k' in self.castlingRights and not self.pieces[61:63].any():
                moves.append((60, 62, 2))
            if 'q' in self.castlingRights and not self.pieces[57:60].any():
                moves.append((60, 58, 3))

        return moves

    def generatePseudoLegalKnightMoves(self, position) -> list[tuple[int, int, int]]:
        moves = []
        if self.toPlay == Colour.WHITE and self.whiteKnights[position]:
            if position // 8 < 6:
                if position % 8 > 0 and not self.whitePieces[position+15]:
                    moves.append((position, position+15, 4*self.blackPieces[position+15]))
                if position % 8 < 7 and not self.whitePieces[position+17]:
                    moves.append((position, position+17, 4*self.blackPieces[position+17]))
            if position // 8 < 7:
                if position % 8 > 1 and not self.whitePieces[position+6]:
                    moves.append((position, position+6, 4*self.blackPieces[position+6]))
                if position % 8 < 6 and not self.whitePieces[position+10]:
                    moves.append((position, position+10, 4*self.blackPieces[position+10]))
            if position // 8 > 1:
                if position % 8 < 7 and not self.whitePieces[position-15]:
                    moves.append((position, position-15, 4*self.blackPieces[position-15]))
                if position % 8 > 0 and not self.whitePieces[position-17]:
                    moves.append((position, position-17, 4*self.blackPieces[position-17]))
            if position // 8 > 0:
                if position % 8 < 6 and not self.whitePieces[position-6]:
                    moves.append((position, position-6, 4*self.blackPieces[position-6]))
                if position % 8 > 1 and not self.whitePieces[position-10]:
                    moves.append((position, position-10, 4*self.blackPieces[position-10]))

        elif self.toPlay == Colour.BLACK and self.blackKnights[position]:
            if position // 8 < 6:
                if position % 8 > 0 and not self.blackPieces[position+15]:
                    moves.append((position, position+15, 4*self.whitePieces[position+15]))
                if position % 8 < 7 and not self.blackPieces[position+17]:
                    moves.append((position, position+17, 4*self.whitePieces[position+17]))
            if position // 8 < 7 and not self.blackPieces[position+6]:
                if position % 8 > 1:
                    moves.append((position, position+6, 4*self.whitePieces[position+6]))
                if position % 8 < 6 and not self.blackPieces[position+10]:
                    moves.append((position, position+10, 4*self.whitePieces[position+10]))
            if position // 8 > 1:
                if position % 8 < 7 and not self.blackPieces[position-15]:
                    moves.append((position, position-15, 4*self.whitePieces[position-15]))
                if position % 8 > 0 and not self.blackPieces[position-17]:
                    moves.append((position, position-17, 4*self.whitePieces[position-17]))
            if position // 8 > 0 and not self.blackPieces[position-6]:
                if position % 8 < 6:
                    moves.append((position, position-6, 4*self.whitePieces[position-6]))
                if position % 8 > 1 and not self.blackPieces[position-10]:
                    moves.append((position, position-10, 4*self.whitePieces[position-10]))
        return moves

    def generatePseudoLegalPawnMoves(self, position) -> list[tuple[int, int, int]]:
        moves = []
        if self.toPlay == Colour.WHITE and self.whitePawns[position]:
            if position // 8 < 6 and not self.pieces[position+8]:
                moves.append((position, position+8, 0))
                if position // 8 == 1 and not self.pieces[position+16]:
                    moves.append((position, position+16, 1))
            if position // 8 < 6 and self.blackPieces[position+7] and position % 8 != 0:
                moves.append((position, position+7, 4))
            if position // 8 == 4 and posToIndex(self.enPassant) == position + 7 and position % 8 != 0:
                moves.append((position, position+7, 5))
            if position // 8 < 6 and position % 8 != 7 and self.blackPieces[position+9]:
                moves.append((position, position+9, 4))
            if position // 8 == 4 and posToIndex(self.enPassant) == position + 9 and position % 8 != 7:
                moves.append((position, position+9, 5))
            if position // 8 == 6 and not self.pieces[position+8]:
                moves.append((position, position+8, 8))
                moves.append((position, position+8, 9))
                moves.append((position, position+8, 10))
                moves.append((position, position+8, 11))
            if position // 8 == 6 and self.blackPieces[position+7] and position % 8 != 0:
                moves.append((position, position+7, 12))
                moves.append((position, position+7, 13))
                moves.append((position, position+7, 14))
                moves.append((position, position+7, 15))
            if position // 8 == 6 and position % 8 != 7 and self.blackPieces[position+9] :
                moves.append((position, position+9, 12))
                moves.append((position, position+9, 13))
                moves.append((position, position+9, 14))
                moves.append((position, position+9, 15))

        elif self.toPlay == Colour.BLACK and self.blackPawns[position]:
            if position // 8 > 1 and not self.pieces[position-8]:
                moves.append((position, position-8, 0))
                if position // 8 == 6 and not self.pieces[position-16]:
                    moves.append((position, position-16, 1))
            if position // 8 > 1 and self.whitePieces[position-7] and position % 8 != 7:
                moves.append((position, position-7, 4))
            if position // 8 == 3 and posToIndex(self.enPassant) == position - 7 and position % 8 != 7:
                moves.append((position, position-7, 5))
            if position // 8 > 1 and position % 8 != 0 and self.whitePieces[position-9]:
                moves.append((position, position-9, 4))
            if position // 8 == 3 and posToIndex(self.enPassant) == position - 9 and position % 8 != 0:
                moves.append((position, position-9, 5))
            if position // 8 == 1 and not self.pieces[position-8]:
                moves.append((position, position-8, 8))
                moves.append((position, position-8, 9))
                moves.append((position, position-8, 10))
                moves.append((position, position-8, 11))
            if position // 8 == 1 and self.whitePieces[position-7] and position % 8 != 7:
                moves.append((position, position-7, 12))
                moves.append((position, position-7, 13))
                moves.append((position, position-7, 14))
                moves.append((position, position-7, 15))
            if position // 8 == 1 and position % 8 != 0 and self.whitePieces[position-9]:
                moves.append((position, position-9, 12))
                moves.append((position, position-9, 13))
                moves.append((position, position-9, 14))
                moves.append((position, position-9, 15))
        return moves

    def applyMove(self, move):
        (startPos, endPos, code) = move
        self.halfMoveClock += 1
        if self.toPlay == Colour.WHITE:
            self.toPlay = Colour.BLACK
            if self.whitePawns[startPos]:
                self.halfMoveClock = 0
                self.whitePawns[startPos] = False
                
                if code == 5:
                    self.blackPawns[endPos-8] = False

                if code == 8 or code == 12:
                    self.whiteKnights[endPos] = True
                elif code == 9 or code == 13:
                    self.whiteBishops[endPos] = True
                elif code == 10 or code == 14:
                    self.whiteRooks[endPos] = True
                elif code == 11 or code == 15:
                    self.whiteQueens[endPos] = True
                else:
                    self.whitePawns[endPos] = True

            elif self.whiteKnights[startPos]:
                self.whiteKnights[startPos] = False
                self.whiteKnights[endPos] = True

            elif self.whiteBishops[startPos]:
                self.whiteBishops[startPos] = False
                self.whiteBishops[endPos] = True

            elif self.whiteRooks[startPos]:
                self.whiteRooks[startPos] = False
                self.whiteRooks[endPos] = True
                if startPos == 0:
                    self.castlingRights.discard('Q')
                if startPos == 7:
                    self.castlingRights.discard('K')

            elif self.whiteQueens[startPos]:
                self.whiteQueens[startPos] = False
                self.whiteQueens[endPos] = True

            elif self.whiteKing[startPos]:
                self.castlingRights.discard('K')
                self.castlingRights.discard('Q')
                self.whiteKing[startPos] = False
                self.whiteKing[endPos] = True
                if code == 2:
                    self.whiteRooks[7] = False
                    self.whiteRooks[5] = True
                elif code == 3:
                    self.whiteRooks[0] = False
                    self.whiteRooks[3] = True
            
            if code == 1:
                self.enPassant = indexToPos(startPos+8)
            else:
                self.enPassant = ''

            if code in [4, 12, 13, 14, 15]:
                self.halfMoveClock = 0
                if self.blackBishops[endPos]:
                    self.blackBishops[endPos] = False
                elif self.blackKing[endPos]:
                    self.blackKing[endPos] = False
                elif self.blackKnights[endPos]:
                    self.blackKnights[endPos] = False
                elif self.blackPawns[endPos]:
                    self.blackPawns[endPos] = False
                elif self.blackRooks[endPos]:
                    self.blackRooks[endPos] = False
                    if endPos == 56:
                        self.castlingRights.discard('q')
                    elif endPos == 63:
                        self.castlingRights.discard('k')
                elif self.blackQueens[endPos]:
                    self.blackQueens[endPos] = False

        elif self.toPlay == Colour.BLACK:
            self.toPlay = Colour.WHITE
            self.fullMoves += 1
            if self.blackPawns[startPos]:
                self.halfMoveClock = 0
                self.blackPawns[startPos] = False
                
                if code == 5:
                    self.whitePawns[endPos+8] = False

                if code == 8 or code == 12:
                    self.blackKnights[endPos] = True
                elif code == 9 or code == 13:
                    self.blackBishops[endPos] = True
                elif code == 10 or code == 14:
                    self.blackRooks[endPos] = True
                elif code == 11 or code == 15:
                    self.blackQueens[endPos] = True
                else:
                    self.blackPawns[endPos] = True

            elif self.blackKnights[startPos]:
                self.blackKnights[startPos] = False
                self.blackKnights[endPos] = True

            elif self.blackBishops[startPos]:
                self.blackBishops[startPos] = False
                self.blackBishops[endPos] = True

            elif self.blackRooks[startPos]:
                self.blackRooks[startPos] = False
                self.blackRooks[endPos] = True
                if startPos == 56:
                    self.castlingRights.discard('q')
                if startPos == 63:
                    self.castlingRights.discard('k')

            elif self.blackQueens[startPos]:
                self.blackQueens[startPos] = False
                self.blackQueens[endPos] = True

            elif self.blackKing[startPos]:
                self.castlingRights.discard('k')
                self.castlingRights.discard('q')
                self.blackKing[startPos] = False
                self.blackKing[endPos] = True
                if code == 2:
                    self.blackRooks[63] = False
                    self.blackRooks[61] = True
                elif code == 3:
                    self.blackRooks[56] = False
                    self.blackRooks[59] = True
            
            if code == 1:
                self.enPassant = indexToPos(startPos-8)
            else:
                self.enPassant = ''

            if code in [4, 12, 13, 14, 15]:
                self.halfMoveClock = 0
                if self.whiteBishops[endPos]:
                    self.whiteBishops[endPos] = False
                elif self.whiteKing[endPos]:
                    self.whiteKing[endPos] = False
                elif self.whiteKnights[endPos]:
                    self.whiteKnights[endPos] = False
                elif self.whitePawns[endPos]:
                    self.whitePawns[endPos] = False
                elif self.whiteRooks[endPos]:
                    self.whiteRooks[endPos] = False
                    if endPos == 0:
                        self.castlingRights.discard('Q')
                    elif endPos == 7:
                        self.castlingRights.discard('K')
                elif self.whiteQueens[endPos]:
                    self.whiteQueens[endPos] = False            

        self.whitePieces = self.whitePawns | self.whiteKnights | self.whiteBishops | self.whiteRooks | self.whiteQueens | self.whiteKing
        self.blackPieces = self.blackPawns | self.blackKnights | self.blackBishops | self.blackRooks | self.blackQueens | self.blackKing
        self.pieces = self.blackPieces | self.whitePieces

    def copy(self):
        return Board(orig=self)
    
    def generateMoves(self) -> list[tuple[int, int, int]]:
        moves = self.generatePseudoLegalMoves()
        legalMoves = []
        for move in moves:
            flag = False
            nextPos = self.copy()
            nextPos.applyMove(move)
            nextMoves = nextPos.generatePseudoLegalMoves()
            for nextMove in nextMoves: 
                nextNextPos = nextPos.copy()
                nextNextPos.applyMove(nextMove)
                if not nextNextPos.blackKing.any() or not nextNextPos.whiteKing.any():
                    flag = True
            if not flag:
                legalMoves.append(move)
        return legalMoves

def posToIndex(position: str) -> int:
    if len(position) != 2:
        return -1
    fileTranslation = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    return 8*(int(position[1])-1)+fileTranslation[position[0]]

def indexToPos(index: int) -> str:
    if index < 0 or index >= 64:
        return "-"
    fileTranslation = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    return fileTranslation[index % 8] + str(1 + index // 8 )

def northMask(position: int):
    result = bitarray('0000000010000000100000001000000010000000100000001000000010000000') >> position
    return result

def southMask(position: int):
    result = result = bitarray('0000000100000001000000010000000100000001000000010000000100000000') << (63-position)
    return result

def fileMask(position: int):
    result = bitarray('1000000010000000100000001000000010000000100000001000000010000000') >> (position&7)
    result[position] = 0
    return result

def rankMask(position: int):
    result = bitarray('1111111100000000000000000000000000000000000000000000000000000000') >> (position&56)
    result[position] = 0
    return result

def antiDiagonalMask(position: int):
    result = bitarray('0000000100000010000001000000100000010000001000000100000010000000')
    diag = 56-8*(position&7) - (position & 56)
    nort = -diag & ( diag >> 31)
    sout =  diag & (-diag >> 31)
    result = (result << sout) >> nort
    result[position] = 0
    return result

def diagonalMask(position: int):
    result = bitarray('1000000001000000001000000001000000001000000001000000001000000001')
    diag = 8*(position&7) - (position & 56)
    nort = -diag & ( diag >> 31)
    sout =  diag & (-diag >> 31)
    result = (result << sout) >> nort
    result[position] = 0
    return result

def rankMask(position: int):
    result = bitarray('1111111100000000000000000000000000000000000000000000000000000000') >> (position&56)
    result[position] = 0
    return result

def queenAttackMask(position: int):
    return rankMask(position) | fileMask(position) | diagonalMask(position) | antiDiagonalMask(position)

def rookAttackMask(position: int):
    return rankMask(position) | fileMask(position)

def bishopAttackMask(position: int):
    return diagonalMask(position) | antiDiagonalMask(position)

def bitMaskString(bits):
    result = ''
    for i in range(7,-1,-1):
        for j in range(8):
            if bits[i*8+j]:
                result += 'x'
            else:
                result += '.'
        result += '\n'
    return result

def main():
    board = Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    print(board.getString())
    moves = board.generateMoves()
    while len(moves) > 0:
        selected = random.choice(moves)
        # for move in moves:
        #     if move[2] in range(8,16):
        #         selected = move
        board.applyMove(selected)
        print(board.getString())
        moves = board.generateMoves()

if __name__ == "__main__":
    main()
