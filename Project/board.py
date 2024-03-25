import numpy as np
from bitarray import bitarray
from enum import Enum
import random
import copy
import time

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
        
class Piece(Enum):
    PAWN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class TTEntry():
    def __init__(self, depth, value, type, age):
        self.depth = depth
        self.value = value
        self.type = type
        self.age = age


class Board:
    PAWN_POS_TABLE = [0,   0,   0,   0,   0,   0,  0,   0,
                      -35,  -1, -20, -23, -15,  24, 38, -22,
                      -26,  -4,  -4, -10,   3,   3, 33, -12,
                      -27,  -2,  -5,  12,  17,   6, 10, -25,
                      -14,  13,   6,  21,  23,  12, 17, -23,
                      -6,   7,  26,  31,  65,  56, 25, -20,
                      98, 134,  61,  95,  68, 126, 34, -11,
                      0,   0,   0,   0,   0,   0,  0,   0
                      ]

    KNIGHT_POS_TABLE = [-105, -21, -58, -33, -17, -28, -19,  -23,
                        -29, -53, -12,  -3,  -1,  18, -14,  -19,
                        -23,  -9,  12,  10,  19,  17,  25,  -16,
                        -13,   4,  16,  13,  28,  19,  21,   -8,
                        -9,  17,  19,  53,  37,  69,  18,   22,
                        -47,  60,  37,  65,  84, 129,  73,   44,
                        -73, -41,  72,  36,  23,  62,   7,  -17,
                        -167, -89, -34, -49,  61, -97, -15, -107
                        ]

    BISHOP_POS_TABLE = [-33,  -3, -14, -21, -13, -12, -39, -21,
                        4,  15,  16,   0,   7,  21,  33,   1,
                        0,  15,  15,  15,  14,  27,  18,  10,
                        -6,  13,  13,  26,  34,  12,  10,   4,
                        -4,   5,  19,  50,  37,  37,   7,  -2,
                        -16,  37,  43,  40,  35,  50,  37,  -2,
                        -26,  16, -18, -13,  30,  59,  18, -47,
                        -29,   4, -82, -37, -25, -42,   7,  -8,
                        ]

    ROOK_POS_TABLE = [-19, -13,   1,  17, 16,  7, -37, -26,
                      -44, -16, -20,  -9, -1, 11,  -6, -71,
                      -45, -25, -16, -17,  3,  0,  -5, -33,
                      -36, -26, -12,  -1,  9, -7,   6, -23,
                      -24, -11,   7,  26, 24, 35,  -8, -20,
                      -5,  19,  26,  36, 17, 45,  61,  16,
                      27,  32,  58,  62, 80, 67,  26,  44,
                      32,  42,  32,  51, 63,  9,  31,  43,
                      ]

    QUEEN_POS_TABLE = [-1, -18,  -9,  10, -15, -25, -31, -50,
                       -35,  -8,  11,   2,   8,  15,  -3,   1,
                       -14,   2, -11,  -2,  -5,   2,  14,   5,
                       -9, -26,  -9, -10,  -2,  -4,   3,  -3,
                       -27, -27, -16, -16,  -1,  17,  -2,   1,
                       -13, -17,   7,   8,  29,  56,  47,  57,
                       -24, -39,  -5,   1, -16,  57,  28,  54,
                       -28,   0,  29,  12,  59,  44,  43,  45,
                       ]

    KING_POS_TABLE = [-15,  36,  12, -54,   8, -28,  24,  14,
                      1,   7,  -8, -64, -43, -16,   9,   8,
                      -14, -14, -22, -46, -44, -30, -15, -27,
                      -49,  -1, -27, -39, -46, -44, -33, -51,
                      -17, -20, -12, -27, -30, -25, -14, -36,
                      -9,  24,   2, -16, -20,   6,  22, -22,
                      29,  -1, -20,  -7,  -8,  -4, -38, -29,
                      -65,  23,  16, -15, -56, -34,   2,  13,
                      ]

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

            # Previous states for unmake move
            self.prevHalfMoveClock = []
            self.prevCapture = []
            self.prevCastlingRights = []
            self.prevEPs = []

            # Number of full moves (starts at 1 and increments after blacks move)
            self.fullMoves = int(fields[5])

            # Transposition table with positions and their evaluations
            self.transpositionTable = {}

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
            self.castlingRights = copy.copy(orig.castlingRights)
            self.enPassant = orig.enPassant
            self.halfMoveClock = orig.halfMoveClock
            self.prevHalfMoveClock = orig.prevHalfMoveClock
            self.prevCapture = orig.prevCapture
            self.prevCastlingRights = copy.copy(orig.prevCastlingRights)
            self.prevEPs = orig.prevEPs
            self.fullMoves = orig.fullMoves
            self.transpositionTable = copy.copy(orig.transpositionTable)

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
        moves.extend(self.generatePseudoLegalPawnMoves())
        moves.extend(self.generatePseudoLegalKnightMoves())
        moves.extend(self.generatePseudoLegalKingMoves())
        moves.extend(self.generatePseudoLegalRookMoves())
        moves.extend(self.generatePseudoLegalBishopMoves())
        moves.extend(self.generatePseudoLegalQueenMoves())
        moves.sort(key=lambda move: move[2], reverse=True)
        return moves
    
    def generatePseudoLegalRookMoves(self) -> list[tuple[int,int,int]]:
        moves = []
        for position in range(64):
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
    
    def generatePseudoLegalBishopMoves(self) -> list[tuple[int,int,int]]:
        moves = []
        for position in range(64):
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
    
    def generatePseudoLegalQueenMoves(self) -> list[tuple[int,int,int]]:
        moves = []
        for position in range(64):
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

    def generatePseudoLegalKingMoves(self) -> list[tuple[int, int, int]]:
        moves = []
        if self.toPlay == Colour.WHITE:
            position = self.whiteKing.index(1)
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
        elif self.toPlay == Colour.BLACK:
            position = self.blackKing.index(1)
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

    def generatePseudoLegalKnightMoves(self) -> list[tuple[int, int, int]]:
        moves = []
        for position in range(64):
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

    def generatePseudoLegalPawnMoves(self) -> list[tuple[int, int, int]]:
        moves = []
        for position in range(64):
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
                self.prevHalfMoveClock.append(self.halfMoveClock-1)
                self.halfMoveClock = 0
                self.whitePawns[startPos] = False
                
                if code == 5:
                    self.blackPawns[endPos-8] = False
                    self.prevCapture.append(Piece.PAWN)

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
                    self.prevCastlingRights.append(copy.copy(self.castlingRights))
                    self.castlingRights.discard('Q')
                if startPos == 7:
                    self.prevCastlingRights.append(copy.copy(self.castlingRights))
                    self.castlingRights.discard('K')

            elif self.whiteQueens[startPos]:
                self.whiteQueens[startPos] = False
                self.whiteQueens[endPos] = True

            elif self.whiteKing[startPos]:
                self.prevCastlingRights.append(copy.copy(self.castlingRights))
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
            
            self.prevEPs.append(self.enPassant)
            if code == 1:
                self.enPassant = indexToPos(startPos+8)
            else:
                self.enPassant = ''

            if code in [4, 12, 13, 14, 15]:
                self.prevHalfMoveClock.append(self.halfMoveClock-1)
                self.halfMoveClock = 0
                if self.blackBishops[endPos]:
                    self.blackBishops[endPos] = False
                    self.prevCapture.append(Piece.BISHOP)
                elif self.blackKing[endPos]:
                    self.blackKing[endPos] = False
                    self.prevCapture.append(Piece.KING)
                elif self.blackKnights[endPos]:
                    self.blackKnights[endPos] = False
                    self.prevCapture.append(Piece.KNIGHT)
                elif self.blackPawns[endPos]:
                    self.blackPawns[endPos] = False
                    self.prevCapture.append(Piece.PAWN)
                elif self.blackRooks[endPos]:
                    self.blackRooks[endPos] = False
                    self.prevCapture.append(Piece.ROOK)
                    if endPos == 56:
                        self.prevCastlingRights.append(copy.copy(self.castlingRights))
                        self.castlingRights.discard('q')
                    elif endPos == 63:
                        self.prevCastlingRights.append(copy.copy(self.castlingRights))
                        self.castlingRights.discard('k')
                elif self.blackQueens[endPos]:
                    self.blackQueens[endPos] = False
                    self.prevCapture.append(Piece.QUEEN)

        elif self.toPlay == Colour.BLACK:
            self.toPlay = Colour.WHITE
            self.fullMoves += 1
            if self.blackPawns[startPos]:
                self.prevHalfMoveClock.append(self.halfMoveClock-1)
                self.halfMoveClock = 0
                self.blackPawns[startPos] = False
                
                if code == 5:
                    self.whitePawns[endPos+8] = False
                    self.prevCapture.append(Piece.PAWN)

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
                    self.prevCastlingRights.append(copy.copy(self.castlingRights))
                    self.castlingRights.discard('q')
                if startPos == 63:
                    self.prevCastlingRights.append(copy.copy(self.castlingRights))
                    self.castlingRights.discard('k')

            elif self.blackQueens[startPos]:
                self.blackQueens[startPos] = False
                self.blackQueens[endPos] = True

            elif self.blackKing[startPos]:
                self.prevCastlingRights.append(copy.copy(self.castlingRights))
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
            
            self.prevEPs.append(self.enPassant)
            if code == 1:
                self.enPassant = indexToPos(startPos-8)
            else:
                self.enPassant = ''

            if code in [4, 12, 13, 14, 15]:
                self.prevHalfMoveClock.append(self.halfMoveClock-1)
                self.halfMoveClock = 0
                if self.whiteBishops[endPos]:
                    self.whiteBishops[endPos] = False
                    self.prevCapture.append(Piece.BISHOP)
                elif self.whiteKing[endPos]:
                    self.whiteKing[endPos] = False
                    self.prevCapture.append(Piece.KING)
                elif self.whiteKnights[endPos]:
                    self.whiteKnights[endPos] = False
                    self.prevCapture.append(Piece.KNIGHT)
                elif self.whitePawns[endPos]:
                    self.whitePawns[endPos] = False
                    self.prevCapture.append(Piece.PAWN)
                elif self.whiteRooks[endPos]:
                    self.whiteRooks[endPos] = False
                    self.prevCapture.append(Piece.ROOK)
                    if endPos == 0:
                        self.prevCastlingRights.append(copy.copy(self.castlingRights))
                        self.castlingRights.discard('Q')
                    elif endPos == 7:
                        self.prevCastlingRights.append(copy.copy(self.castlingRights))
                        self.castlingRights.discard('K')
                elif self.whiteQueens[endPos]:
                    self.whiteQueens[endPos] = False
                    self.prevCapture.append(Piece.QUEEN)       

        self.whitePieces = self.whitePawns | self.whiteKnights | self.whiteBishops | self.whiteRooks | self.whiteQueens | self.whiteKing
        self.blackPieces = self.blackPawns | self.blackKnights | self.blackBishops | self.blackRooks | self.blackQueens | self.blackKing
        self.pieces = self.blackPieces | self.whitePieces

    def unmake(self, move):
        (startPos, endPos, code) = move
        self.halfMoveClock -= 1
        if self.toPlay == Colour.BLACK:
            self.toPlay = Colour.WHITE
            if self.whitePawns[endPos] or code in range(8,16):
                self.halfMoveClock = self.prevHalfMoveClock.pop()
                self.whitePawns[startPos] = True
                
                if code == 5:
                    self.blackPawns[endPos-8] = True
                    self.prevCapture.pop()

                if code == 8 or code == 12:
                    self.whiteKnights[endPos] = False
                elif code == 9 or code == 13:
                    self.whiteBishops[endPos] = False
                elif code == 10 or code == 14:
                    self.whiteRooks[endPos] = False
                elif code == 11 or code == 15:
                    self.whiteQueens[endPos] = False
                else:
                    self.whitePawns[endPos] = False

            elif self.whiteKnights[endPos]:
                self.whiteKnights[startPos] = True
                self.whiteKnights[endPos] = False

            elif self.whiteBishops[endPos]:
                self.whiteBishops[startPos] = True
                self.whiteBishops[endPos] = False

            elif self.whiteRooks[endPos]:
                self.whiteRooks[startPos] = True
                self.whiteRooks[endPos] = False
                if startPos == 0 or startPos == 7:
                    self.castlingRights = self.prevCastlingRights.pop()

            elif self.whiteQueens[endPos]:
                self.whiteQueens[startPos] = True
                self.whiteQueens[endPos] = False

            elif self.whiteKing[endPos]:
                self.castlingRights = self.prevCastlingRights.pop()
                self.whiteKing[startPos] = True
                self.whiteKing[endPos] = False
                if code == 2:
                    self.whiteRooks[7] = True
                    self.whiteRooks[5] = False
                elif code == 3:
                    self.whiteRooks[0] = True
                    self.whiteRooks[3] = False
            
            self.enPassant = self.prevEPs.pop()

            if code in [4, 12, 13, 14, 15]:
                self.halfMoveClock = self.prevHalfMoveClock.pop()
                prevCapture = self.prevCapture.pop()
                if prevCapture == Piece.BISHOP:
                    self.blackBishops[endPos] = True
                elif prevCapture == Piece.KING:
                    self.blackKing[endPos] = True
                elif prevCapture == Piece.KNIGHT:
                    self.blackKnights[endPos] = True
                elif prevCapture == Piece.PAWN:
                    self.blackPawns[endPos] = True
                elif prevCapture == Piece.ROOK:
                    self.blackRooks[endPos] = True
                    if endPos == 56 or endPos == 63:
                        self.castlingRights = self.prevCastlingRights.pop()
                elif prevCapture == Piece.QUEEN:
                    self.blackQueens[endPos] = True

        elif self.toPlay == Colour.WHITE:
            self.toPlay = Colour.BLACK
            self.fullMoves -= 1
            if self.blackPawns[endPos] or code in range(8,16):
                self.halfMoveClock = self.prevHalfMoveClock.pop()
                self.blackPawns[startPos] = True
                
                if code == 5:
                    self.whitePawns[endPos+8] = True
                    self.prevCapture.pop()

                if code == 8 or code == 12:
                    self.blackKnights[endPos] = False
                elif code == 9 or code == 13:
                    self.blackBishops[endPos] = False
                elif code == 10 or code == 14:
                    self.blackRooks[endPos] = False
                elif code == 11 or code == 15:
                    self.blackQueens[endPos] = False
                else:
                    self.blackPawns[endPos] = False

            elif self.blackKnights[endPos]:
                self.blackKnights[startPos] = True
                self.blackKnights[endPos] = False

            elif self.blackBishops[endPos]:
                self.blackBishops[startPos] = True
                self.blackBishops[endPos] = False

            elif self.blackRooks[endPos]:
                self.blackRooks[startPos] = True
                self.blackRooks[endPos] = False
                if startPos == 56 or startPos == 63:
                    self.castlingRights = self.prevCastlingRights.pop()

            elif self.blackQueens[endPos]:
                self.blackQueens[startPos] = True
                self.blackQueens[endPos] = False

            elif self.blackKing[endPos]:
                self.castlingRights = self.prevCastlingRights.pop()
                self.blackKing[startPos] = True
                self.blackKing[endPos] = False
                if code == 2:
                    self.blackRooks[63] = True
                    self.blackRooks[61] = False
                elif code == 3:
                    self.blackRooks[56] = True
                    self.blackRooks[59] = False
            
            self.enPassant = self.prevEPs.pop()

            if code in [4, 12, 13, 14, 15]:
                self.halfMoveClock = self.prevHalfMoveClock.pop()
                prevCapture = self.prevCapture.pop()
                if prevCapture == Piece.BISHOP:
                    self.whiteBishops[endPos] = True
                elif prevCapture == Piece.KING:
                    self.whiteKing[endPos] = True
                elif prevCapture == Piece.KNIGHT:
                    self.whiteKnights[endPos] = True
                elif prevCapture == Piece.PAWN:
                    self.whitePawns[endPos] = True
                elif prevCapture == Piece.ROOK:
                    self.whiteRooks[endPos] = True
                    if endPos == 0 or endPos == 7:
                        self.castlingRights = self.prevCastlingRights.pop()
                elif prevCapture == Piece.QUEEN:
                    self.whiteQueens[endPos] = True    

        self.whitePieces = self.whitePawns | self.whiteKnights | self.whiteBishops | self.whiteRooks | self.whiteQueens | self.whiteKing
        self.blackPieces = self.blackPawns | self.blackKnights | self.blackBishops | self.blackRooks | self.blackQueens | self.blackKing
        self.pieces = self.blackPieces | self.whitePieces

    def evalMaterial(self) -> int:
        whiteMaterial = self.whitePawns.count()*100 + self.whiteBishops.count()*300 + self.whiteKnights.count()*300 + self.whiteRooks.count()*500 + self.whiteQueens.count()*900
        blackMaterial = self.blackPawns.count()*100 + self.blackBishops.count()*300 + self.blackKnights.count()*300 + self.blackRooks.count()*500 + self.blackQueens.count()*900
        return whiteMaterial - blackMaterial
    
    def evalPositioning(self):
        value = 0
        for i in range(64):
            if self.whitePawns[i]:
                value += self.PAWN_POS_TABLE[i]
            elif self.blackPawns[i]:
                value -= self.PAWN_POS_TABLE[i^56]
            elif self.whiteKnights[i]:
                value += self.KNIGHT_POS_TABLE[i]
            elif self.blackKnights[i]:
                value -= self.KNIGHT_POS_TABLE[i^56]
            elif self.whiteBishops[i]:
                value += self.BISHOP_POS_TABLE[i]
            elif self.blackBishops[i]:
                value -= self.BISHOP_POS_TABLE[i^56]
            elif self.whiteRooks[i]:
                value += self.ROOK_POS_TABLE[i]
            elif self.blackRooks[i]:
                value -= self.ROOK_POS_TABLE[i^56]
            elif self.whiteQueens[i]:
                value += self.QUEEN_POS_TABLE[i]
            elif self.blackQueens[i]:
                value -= self.QUEEN_POS_TABLE[i^56]
            elif self.whiteKing[i]:
                value += self.KING_POS_TABLE[i]
            elif self.blackKing[i]:
                value -= self.KING_POS_TABLE[i^56]
        return value
            
    def evalDoubledPawns(self, penalty=30):
        value = 0
        for i in range(8):
            file = bitarray('1000000010000000100000001000000010000000100000001000000010000000') >> i
            value -= penalty * ((file & self.whitePawns).count()- 1)
            value += penalty * ((file & self.blackPawns).count()- 1)
        return value

    def heuristicEval(self, moves=None):
        if self.gameOver(moves):
            return self.getResult(moves)*10000
        mat_eval = self.evalMaterial()
        pos_eval = self.evalPositioning()
        pawn_eval = self.evalDoubledPawns()
        return mat_eval+pos_eval+pawn_eval
    
    def generateTTKey(self):
        result = self.whitePawns.to01()+self.whiteKnights.to01()+self.whiteBishops.to01()+self.whiteRooks.to01()+self.whiteQueens.to01()+str(self.whiteKing.index(1))
        result += self.blackPawns.to01()+self.blackKnights.to01()+self.blackBishops.to01()+self.blackRooks.to01()+self.blackQueens.to01()+str(self.blackKing.index(1))
        
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

        return result
    
    def age(self):
        if self.toPlay == Colour.WHITE:
            return 2*self.fullMoves
        return 2*self.fullMoves+1

    def orderMoves(self, moves):
        reversed = False
        if self.toPlay == Colour.WHITE:
            reversed = True
        evaluatedPositions = []
        boundedPositions = []
        unknownPositions = []
        for move in moves:
            self.applyMove(move)
            key = self.generateTTKey()
            self.unmake(move)
            if key in self.transpositionTable:
                transpositionEntry = self.transpositionTable[key]
                if transpositionEntry.type == 1:
                    evaluatedPositions.append((move, transpositionEntry.value))
                else:
                    boundedPositions.append((move, transpositionEntry.value))
            else:
                unknownPositions.append(move)
        evaluatedPositions.sort(key=lambda move: move[1], reverse=reversed)
        boundedPositions.sort(key=lambda move: move[1], reverse=reversed)
        return [item[0] for item in evaluatedPositions]+[item[0] for item in boundedPositions]+unknownPositions

    def eval(self, depth, alpha=-float('inf'), beta=float('inf'), quiescenceDepth=10):
        key = self.generateTTKey()
        transpositionEntry = None
        if key in self.transpositionTable:
            transpositionEntry = self.transpositionTable[key]
            if transpositionEntry.type == 1 and transpositionEntry.depth >= depth:
                return transpositionEntry.value

        if depth == 0:
            value = self.quiescenceEval(quiescenceDepth, alpha, beta)
            newEntry = TTEntry(0, value, 1, self.age())
            self.transpositionTable[key] = newEntry
            return value
        
        moves = self.generateMoves()
        moves = self.orderMoves(moves)

        if len(moves) == 0:
            value = self.heuristicEval(moves)
            newEntry = TTEntry(0, value, 1, self.age())
            self.transpositionTable[key] = newEntry
            return value
        
        if self.toPlay == Colour.WHITE:
            value = -float('inf')
            beatAlpha = False
            for move in moves:
                self.applyMove(move)
                value = max(value, self.eval(depth-1, alpha, beta, quiescenceDepth))
                self.unmake(move)
                if value > beta:
                    newEntry = TTEntry(depth, value, 2, self.age())
                    self.transpositionTable[key] = newEntry
                    return value
                if value > alpha:
                    alpha = value
                    beatAlpha = True
            if beatAlpha:
                newEntry = TTEntry(depth, value, 1, self.age())
            else:
                newEntry = TTEntry(depth, value, 3, self.age())
            self.transpositionTable[key] = newEntry
            return value
        else:
            value = float('inf')
            beatBeta = False
            for move in moves:
                self.applyMove(move)
                value = min(value, self.eval(depth-1, alpha, beta, quiescenceDepth))
                self.unmake(move)
                if value < alpha:
                    newEntry = TTEntry(depth, value, 3, self.age())
                    self.transpositionTable[key] = newEntry
                    return value
                if value < beta:
                    beta = value
                    beatBeta = True
            if beatBeta:
                newEntry = TTEntry(depth, value, 1, self.age())
            else:
                newEntry = TTEntry(depth, value, 2, self.age())
            self.transpositionTable[key] = newEntry
            return value
        
    def quiescenceEval(self, depth, alpha=-float('inf'), beta=float('inf')):
        allMoves = self.generateMoves()
        moves = self.generateQuiescenceMoves(allMoves)
        moves = self.orderMoves(moves)

        key = self.generateTTKey()
        transpositionEntry = None
        if key in self.transpositionTable:
            transpositionEntry = self.transpositionTable[key]
            if transpositionEntry.type == 1:
                return transpositionEntry.value

        if depth == 0 or len(moves) == 0:
            value = self.heuristicEval(allMoves)
            newEntry = TTEntry(0, value, 1, self.age())
            self.transpositionTable[key] = newEntry
            return value
        
        if self.toPlay == Colour.WHITE:
            value = self.heuristicEval(allMoves)
            beatAlpha = False
            for move in moves:
                self.applyMove(move)
                value = max(value, self.quiescenceEval(depth-1, alpha, beta))
                self.unmake(move)
                if value >= beta:
                    newEntry = TTEntry(0, value, 2, self.age())
                    self.transpositionTable[key] = newEntry
                    return value
                if value > alpha:
                    alpha = value
                    beatAlpha = True
            if beatAlpha:
                newEntry = TTEntry(0, value, 1, self.age())
            else:
                newEntry = TTEntry(0, value, 3, self.age())
            self.transpositionTable[key] = newEntry
            return value
        else:
            value = self.heuristicEval(allMoves)
            beatBeta = False
            for move in moves:
                self.applyMove(move)
                value = min(value, self.quiescenceEval(depth-1, alpha, beta))
                self.unmake(move)
                if value <= alpha:
                    newEntry = TTEntry(0, value, 3, self.age())
                    self.transpositionTable[key] = newEntry
                    return value
                if value < beta:
                    beta = value
                    beatBeta = True
            if beatBeta:
                newEntry = TTEntry(0, value, 1, self.age())
            else:
                newEntry = TTEntry(0, value, 2, self.age())
            self.transpositionTable[key] = newEntry
            return value
    
    def gameOver(self, moves=None):
        if moves == None:
            moves = self.generateMoves()
        if self.halfMoveClock >= 100:
            return True
        if len(moves) == 0:
            return True
        if self.whitePawns.any() or self.whiteRooks.any() or self.whiteQueens.any() or self.blackPawns.any() or self.blackRooks.any() or self.blackQueens.any():
            return False
        if self.whiteBishops.count() >= 2 or (self.whiteBishops.count() == 1 and self.whiteKnights.count() == 1):
            return False
        if self.blackBishops.count() >= 2 or (self.blackBishops.count() == 1 and self.blackKnights.count() == 1):
            return False
        return True

    def getResult(self, moves=None):
        if moves == None:
            moves = self.generateMoves()
        if len(moves) == 0 and self.inCheck()[0]:
            if self.toPlay == Colour.WHITE:
                return -1
            else:
                return 1
        elif self.gameOver(moves):
            return 0
        else:
            return None
        
    def inCheck(self):
        flag = False
        checkingPiecePositions = []
        self.toPlay = Colour.opposite(self.toPlay)
        moves = self.generatePseudoLegalMoves()
        for move in moves: 
            self.applyMove(move)
            if not self.blackKing.any() or not self.whiteKing.any():
                flag = True
                checkingPiecePositions.append(move[0])
            self.unmake(move)
        self.toPlay = Colour.opposite(self.toPlay)
        return flag, checkingPiecePositions

    def copy(self):
        return Board(orig=self)
    
    def generateMoves(self) -> list[tuple[int, int, int]]:
        moves = self.generatePseudoLegalMoves()
        legalMoves = []
        inCheck, positions = self.inCheck()
        if inCheck:
            if self.toPlay == Colour.WHITE:
                kingPos = self.whiteKing.index(1)
            else:
                kingPos = self.blackKing.index(1)
            if len(positions) > 1:
                for move in moves:
                    if move[0] == kingPos and self.validMove(move):
                        legalMoves.append(move)
            else:
                checkingPiecePosition = positions[0]
                kingDiagonal = diagonalMask(kingPos)
                kingAntiDiagonal = antiDiagonalMask(kingPos)
                kingRank = rankMask(kingPos)
                kingFile = fileMask(kingPos)
                checkLine = None
                if kingDiagonal[checkingPiecePosition]:
                    checkLine = kingDiagonal
                elif kingAntiDiagonal[checkingPiecePosition]:
                    checkLine = kingAntiDiagonal
                elif kingRank[checkingPiecePosition]:
                    checkLine = kingRank
                elif kingFile[checkingPiecePosition]:
                    checkLine = kingFile
                if checkLine != None:
                    for move in moves:
                        if move[2] not in [2,3] and ((move[0] == kingPos and not checkLine[move[1]]) or checkLine[move[1]]) and self.validMove(move):
                            legalMoves.append(move)
                else:
                    for move in moves:
                        if ((move[0] == kingPos and move[2] not in [2,3]) or move[1] == checkingPiecePosition) and self.validMove(move):
                            legalMoves.append(move)
        else:
            if self.toPlay == Colour.WHITE:
                kingPos = self.whiteKing.index(1)
                kingDiagonal = diagonalMask(kingPos)
                kingAntiDiagonal = antiDiagonalMask(kingPos)
                kingRank = rankMask(kingPos)
                kingFile = fileMask(kingPos)
                for move in moves:
                    if move[2] == 5 or move[0] == kingPos:
                        if self.validMove(move):
                            if move[2] == 2:
                                if self.validMove((4, 5, 0)):
                                    legalMoves.append(move)
                            elif move[2] == 3:
                                if self.validMove((4, 3, 0)):
                                    legalMoves.append(move)
                            else:
                                legalMoves.append(move)
                    elif not ((kingDiagonal[move[0]] and (kingDiagonal & (self.blackBishops | self.blackQueens)).any() and not kingDiagonal[move[1]]) 
                              or (kingAntiDiagonal[move[0]] and (kingAntiDiagonal & (self.blackBishops | self.blackQueens)).any() and not kingAntiDiagonal[move[1]]) 
                              or (kingRank[move[0]] and (kingRank & (self.blackRooks | self.blackQueens)).any() and not kingRank[move[1]])
                              or (kingFile[move[0]] and (kingFile & (self.blackRooks | self.blackQueens)).any() and not kingFile[move[1]])):
                        legalMoves.append(move)
                    elif self.validMove(move):
                        legalMoves.append(move)
            else:
                kingPos = self.blackKing.index(1)
                kingDiagonal = diagonalMask(kingPos) | self.blackKing
                kingAntiDiagonal = antiDiagonalMask(kingPos) | self.blackKing
                kingRank = rankMask(kingPos) | self.blackKing
                kingFile = fileMask(kingPos) | self.blackKing
                for move in moves:
                    if move[2] == 5 or move[0] == kingPos:
                        if self.validMove(move):
                            if move[2] == 2:
                                if self.validMove((60, 61, 0)):
                                    legalMoves.append(move)
                            elif move[2] == 3:
                                if self.validMove((60, 59, 0)):
                                    legalMoves.append(move)
                            else:
                                legalMoves.append(move)
                    elif not ((kingDiagonal[move[0]] and (kingDiagonal & (self.whiteBishops | self.whiteQueens)).any() and not kingDiagonal[move[1]]) 
                              or (kingAntiDiagonal[move[0]] and (kingAntiDiagonal & (self.whiteBishops | self.whiteQueens)).any() and not kingAntiDiagonal[move[1]]) 
                              or (kingRank[move[0]] and (kingRank & (self.whiteRooks | self.whiteQueens)).any() and not kingRank[move[1]])
                              or (kingFile[move[0]] and (kingFile & (self.whiteRooks | self.whiteQueens)).any() and not kingFile[move[1]])):
                        legalMoves.append(move)
                    elif self.validMove(move):
                        legalMoves.append(move)
        return legalMoves
    
    def generateQuiescenceMoves(self, moves=None) -> list[tuple[int, int, int]]:
        if moves == None:
            moves = self.generateMoves()
        loudMoves = []
        for move in moves:
            if move[2] >= 8 or move[2] == 4 and not (self.whitePawns[move[1]] or self.blackPawns[move[1]]):
                loudMoves.append(move)
        return loudMoves
    
    def validMove(self, move):
        flag = True
        self.applyMove(move)
        nextMoves = self.generatePseudoLegalMoves()
        if self.toPlay == Colour.WHITE:
            kingPos = self.blackKing.index(1)
        else:
            kingPos = self.whiteKing.index(1)
        for nextMove in nextMoves:
            if (nextMove[1] == kingPos):
                flag = False
        self.unmake(move)
        return flag
            
    def perft(self, depth):
        moves = self.generateMoves()
        if len(moves) == 0 or depth == 0:
            return 1
        
        if depth == 1:
            return len(moves)
        
        nodes = 0
        
        for move in moves:
            self.applyMove(move)
            nodes += self.perft(depth-1)
            self.unmake(move)
        
        return nodes

    def gcTranspositionTable(self):
        age = self.age()
        keys = list(self.transpositionTable.keys())
        for key in keys:
            if self.transpositionTable[key].age <= age:
                self.transpositionTable.pop(key)

    def bestMove(self, eval_depth=3, quiescenceDepth=10, perMove=10):
        start = time.time()
        moves = self.generateMoves()
        for depth in range(eval_depth+1):
            moves = self.orderMoves(moves)
            bestMove = moves[0]
            self.applyMove(bestMove)
            bestEval = self.eval(depth, quiescenceDepth=quiescenceDepth)
            self.unmake(bestMove)
            for move in moves[1:]:
                self.applyMove(move)
                if self.toPlay == Colour.BLACK:
                    eval = self.eval(depth, alpha=bestEval, quiescenceDepth=quiescenceDepth)
                    if eval > bestEval:
                        bestEval = eval
                        bestMove = move
                else:
                    eval = self.eval(depth, beta=bestEval, quiescenceDepth=quiescenceDepth)
                    if eval < bestEval:
                        bestEval = eval
                        bestMove = move
                self.unmake(move)
                if time.time() - start > perMove:
                    return bestMove, bestEval
        return bestMove, bestEval

    def playGame(self, eval_depth=3, moves=-1, quiescenceDepth=10, perMove=10):
        while not self.gameOver() and moves != 0:
            moves -= 1
            self.gcTranspositionTable()
            bestMove, bestEval = self.bestMove(eval_depth, quiescenceDepth=quiescenceDepth, perMove=perMove)
            self.applyMove(bestMove)
            print(self.getString())
            print(bestEval)
        print(self.getResult())

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

def playAgainstEngine(FEN=None):
    board = Board(FEN)
    print(board.getString())
    chosen = Colour.fromString(input("play as white(w) or black(b)?"))
    if  board.toPlay == chosen:
        response_0 = posToIndex(input("start position: "))
        response_1 = posToIndex(input("end position: "))
        response_2 = int(input("move code: "))
        board.applyMove((response_0, response_1, response_2))
        print(board.getString())
    while not board.gameOver():
        bestMove, bestEval = board.bestMove(4, 4, 15)
        board.applyMove(bestMove)
        print(board.getString())
        print(bestMove, bestEval)
        if board.gameOver():
            break
        response_0 = posToIndex(input("start position: "))
        response_1 = posToIndex(input("end position: "))
        response_2 = int(input("move code: "))
        board.applyMove((response_0, response_1, response_2))
        print(board.getString())
    print(board.getResult())

def main():
    # '3r1rk1/pp1n2b1/1qp3p1/4p1Np/4Q1n1/3P2P1/PPP3BP/R1B2R1K b - - 0 17'
    playAgainstEngine()

    while True:
        command = input().strip()

        if command == "xboard":
            # Respond to xboard command
            print("feature done=0")
            print("feature myname=\"ExplainableEngine\"")
            print("feature ping=1")
            print("feature setboard=1")

        elif command == "new":
            # Respond to new game command
            board = Board()

        elif command.startswith("force"):
            # Respond to force mode command
            pass

        elif command.startswith("protover"):
            # Respond to protocol version command
            print("feature done=1")

        elif command.startswith("quit"):
            # Respond to quit command
            break

        elif command.startswith("go"):
            # Respond to go command
            move = board.bestMove(4, 10, 10)
            board.applyMove(move)
            algebraic_move = indexToPos(move[0])+indexToPos(move[1])
            print("move", algebraic_move)

        elif command.startswith("usermove"):
            # Handle user move
            algebraic_move = command.split()[1]
            move = board.findMove(algebraic_move)
            board.applyMove(move)

        elif command.startswith("ping"):
            # Respond to ping command
            print("pong", command.split()[1])

        elif command.startswith("setboard"):
            # Set the board to the given position
            fen = " ".join(command.split()[1:])
            board = Board(fen)

        else:
            # Unknown command, send "Error" response
            print("Error")
    

if __name__ == "__main__":
    main()
