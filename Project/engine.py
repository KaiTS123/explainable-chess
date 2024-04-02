import colour
import board
import ttentry
from bitarray import bitarray
import time
import sys
from bitarray_masks import *

class Engine:
    MG_PAWN_POS_TABLE = [0,   0,   0,   0,   0,   0,  0,   0,
                      -35,  -1, -20, -23, -15,  24, 38, -22,
                      -26,  -4,  -4, -10,   3,   3, 33, -12,
                      -27,  -2,  -5,  12,  17,   6, 10, -25,
                      -14,  13,   6,  21,  23,  12, 17, -23,
                      -6,   7,  26,  31,  65,  56, 25, -20,
                      98, 134,  61,  95,  68, 126, 34, -11,
                      0,   0,   0,   0,   0,   0,  0,   0
                      ]

    MG_KNIGHT_POS_TABLE = [-105, -21, -58, -33, -17, -28, -19,  -23,
                        -29, -53, -12,  -3,  -1,  18, -14,  -19,
                        -23,  -9,  12,  10,  19,  17,  25,  -16,
                        -13,   4,  16,  13,  28,  19,  21,   -8,
                        -9,  17,  19,  53,  37,  69,  18,   22,
                        -47,  60,  37,  65,  84, 129,  73,   44,
                        -73, -41,  72,  36,  23,  62,   7,  -17,
                        -167, -89, -34, -49,  61, -97, -15, -107
                        ]

    MG_BISHOP_POS_TABLE = [-33,  -3, -14, -21, -13, -12, -39, -21,
                        4,  15,  16,   0,   7,  21,  33,   1,
                        0,  15,  15,  15,  14,  27,  18,  10,
                        -6,  13,  13,  26,  34,  12,  10,   4,
                        -4,   5,  19,  50,  37,  37,   7,  -2,
                        -16,  37,  43,  40,  35,  50,  37,  -2,
                        -26,  16, -18, -13,  30,  59,  18, -47,
                        -29,   4, -82, -37, -25, -42,   7,  -8,
                        ]

    MG_ROOK_POS_TABLE = [-19, -13,   1,  17, 16,  7, -37, -26,
                      -44, -16, -20,  -9, -1, 11,  -6, -71,
                      -45, -25, -16, -17,  3,  0,  -5, -33,
                      -36, -26, -12,  -1,  9, -7,   6, -23,
                      -24, -11,   7,  26, 24, 35,  -8, -20,
                      -5,  19,  26,  36, 17, 45,  61,  16,
                      27,  32,  58,  62, 80, 67,  26,  44,
                      32,  42,  32,  51, 63,  9,  31,  43,
                      ]

    MG_QUEEN_POS_TABLE = [-1, -18,  -9,  10, -15, -25, -31, -50,
                       -35,  -8,  11,   2,   8,  15,  -3,   1,
                       -14,   2, -11,  -2,  -5,   2,  14,   5,
                       -9, -26,  -9, -10,  -2,  -4,   3,  -3,
                       -27, -27, -16, -16,  -1,  17,  -2,   1,
                       -13, -17,   7,   8,  29,  56,  47,  57,
                       -24, -39,  -5,   1, -16,  57,  28,  54,
                       -28,   0,  29,  12,  59,  44,  43,  45,
                       ]

    MG_KING_POS_TABLE = [-15,  36,  12, -54,   8, -28,  24,  14,
                      1,   7,  -8, -64, -43, -16,   9,   8,
                      -14, -14, -22, -46, -44, -30, -15, -27,
                      -49,  -1, -27, -39, -46, -44, -33, -51,
                      -17, -20, -12, -27, -30, -25, -14, -36,
                      -9,  24,   2, -16, -20,   6,  22, -22,
                      29,  -1, -20,  -7,  -8,  -4, -38, -29,
                      -65,  23,  16, -15, -56, -34,   2,  13,
                      ]
    
    EG_PAWN_POS_TABLE = [     0,   0,   0,   0,   0,   0,   0,   0,
                             13,   8,   8,  10,  13,   0,   2,  -7,
                              4,   7,  -6,   1,   0,  -5,  -1,  -8,
                             13,   9,  -3,  -7,  -7,  -8,   3,  -1,
                             32,  24,  13,   5,  -2,   4,  17,  17,
                             94, 100,  85,  67,  56,  53,  82,  84,
                            178, 173, 158, 134, 147, 132, 165, 187,
                              0,   0,   0,   0,   0,   0,   0,   0
                      ]

    EG_KNIGHT_POS_TABLE = [ -29, -51, -23, -15, -22, -18, -50, -64,
                            -42, -20, -10,  -5,  -2, -20, -23, -44,
                            -23,  -3,  -1,  15,  10,  -3, -20, -22,
                            -18,  -6,  16,  25,  16,  17,   4, -18,
                            -17,   3,  22,  22,  22,  11,   8, -18,
                            -24, -20,  10,   9,  -1,  -9, -19, -41,
                            -25,  -8, -25,  -2,  -9, -25, -24, -52,
                            -58, -38, -13, -28, -31, -27, -63, -99
                        ]

    EG_BISHOP_POS_TABLE = [ -23,  -9, -23,  -5, -9, -16,  -5, -17,
                            -14, -18,  -7,  -1,  4,  -9, -15, -27,
                            -12,  -3,   8,  10, 13,   3,  -7, -15,
                             -6,   3,  13,  19,  7,  10,  -3,  -9,
                             -3,   9,  12,   9, 14,  10,   3,   2,
                              2,  -8,   0,  -1, -2,   6,   0,   4,
                             -8,  -4,   7, -12, -3, -13,  -4, -14,
                            -14, -21, -11,  -8, -7,  -9, -17, -24
                        ]

    EG_ROOK_POS_TABLE = [   -9,  2,  3, -1, -5, -13,   4, -20,
                            -6, -6,  0,  2, -9,  -9, -11,  -3,
                            -4,  0, -5, -1, -7, -12,  -8, -16,
                            3,  5,  8,  4, -5,  -6,  -8, -11,
                            4,  3, 13,  1,  2,   1,  -1,   2,
                            7,  7,  7,  5,  4,  -3,  -5,  -3,
                            11, 13, 13, 11, -3,   3,   8,   3,
                            13, 10, 18, 15, 12,  12,   8,   5
                        ]

    EG_QUEEN_POS_TABLE = [  -33, -28, -22, -43,  -5, -32, -20, -41,
                            -22, -23, -30, -16, -16, -23, -36, -32,
                            -16, -27,  15,   6,   9,  17,  10,   5,
                            -18,  28,  19,  47,  31,  34,  39,  23,
                              3,  22,  24,  45,  57,  40,  57,  36,
                            -20,   6,   9,  49,  47,  35,  19,   9,
                            -17,  20,  32,  41,  58,  25,  30,   0,
                             -9,  22,  22,  27,  27,  19,  10,  20
                       ]

    EG_KING_POS_TABLE = [   -53, -34, -21, -11, -28, -14, -24, -43,
                            -27, -11,   4,  13,  14,   4,  -5, -17,
                            -19,  -3,  11,  21,  23,  16,   7,  -9,
                            -18,  -4,  21,  24,  27,  23,   9, -11,
                            -8,  22,  24,  27,  26,  33,  26,   3,
                            10,  17,  23,  15,  20,  45,  44,  13,
                            -12,  17,  14,  17,  17,  38,  23,  11,        
                            -74, -35, -18, -18, -11,  15,   4, -17
                      ]
    
    def __init__(self, FEN=None):
        self.board = board.Board(FEN)

        self.playing = colour.Colour.BLACK

        self.remaining_time = 30000
        self.opp_remaining_time = 30000

        # Transposition table with positions and their evaluations
        self.transpositionTable = {}

    def evalMaterial(self) -> int:
        whiteMaterial = self.board.whitePawns.count()*100 + self.board.whiteBishops.count()*300 + self.board.whiteKnights.count()*300 + self.board.whiteRooks.count()*500 + self.board.whiteQueens.count()*900
        blackMaterial = self.board.blackPawns.count()*100 + self.board.blackBishops.count()*300 + self.board.blackKnights.count()*300 + self.board.blackRooks.count()*500 + self.board.blackQueens.count()*900
        return whiteMaterial - blackMaterial
    
    def evalPositioning(self, phase):
        mg_value = 0
        for i in range(64):
            if self.board.whitePawns[i]:
                mg_value += self.MG_PAWN_POS_TABLE[i]
            elif self.board.blackPawns[i]:
                mg_value -= self.MG_PAWN_POS_TABLE[i^56]
            elif self.board.whiteKnights[i]:
                mg_value += self.MG_KNIGHT_POS_TABLE[i]
            elif self.board.blackKnights[i]:
                mg_value -= self.MG_KNIGHT_POS_TABLE[i^56]
            elif self.board.whiteBishops[i]:
                mg_value += self.MG_BISHOP_POS_TABLE[i]
            elif self.board.blackBishops[i]:
                mg_value -= self.MG_BISHOP_POS_TABLE[i^56]
            elif self.board.whiteRooks[i]:
                mg_value += self.MG_ROOK_POS_TABLE[i]
            elif self.board.blackRooks[i]:
                mg_value -= self.MG_ROOK_POS_TABLE[i^56]
            elif self.board.whiteQueens[i]:
                mg_value += self.MG_QUEEN_POS_TABLE[i]
            elif self.board.blackQueens[i]:
                mg_value -= self.MG_QUEEN_POS_TABLE[i^56]
            elif self.board.whiteKing[i]:
                mg_value += self.MG_KING_POS_TABLE[i]
            elif self.board.blackKing[i]:
                mg_value -= self.MG_KING_POS_TABLE[i^56]
        eg_value = 0
        for i in range(64):
            if self.board.whitePawns[i]:
                eg_value += self.EG_PAWN_POS_TABLE[i]
            elif self.board.blackPawns[i]:
                eg_value -= self.EG_PAWN_POS_TABLE[i^56]
            elif self.board.whiteKnights[i]:
                eg_value += self.EG_KNIGHT_POS_TABLE[i]
            elif self.board.blackKnights[i]:
                eg_value -= self.EG_KNIGHT_POS_TABLE[i^56]
            elif self.board.whiteBishops[i]:
                eg_value += self.EG_BISHOP_POS_TABLE[i]
            elif self.board.blackBishops[i]:
                eg_value -= self.EG_BISHOP_POS_TABLE[i^56]
            elif self.board.whiteRooks[i]:
                eg_value += self.EG_ROOK_POS_TABLE[i]
            elif self.board.blackRooks[i]:
                eg_value -= self.EG_ROOK_POS_TABLE[i^56]
            elif self.board.whiteQueens[i]:
                eg_value += self.EG_QUEEN_POS_TABLE[i]
            elif self.board.blackQueens[i]:
                eg_value -= self.EG_QUEEN_POS_TABLE[i^56]
            elif self.board.whiteKing[i]:
                eg_value += self.EG_KING_POS_TABLE[i]
            elif self.board.blackKing[i]:
                eg_value -= self.EG_KING_POS_TABLE[i^56]
        return (mg_value*(24-phase)+eg_value*phase)/24
            
    def evalDoubledPawns(self, penalty=30):
        value = 0
        for i in range(8):
            file = bitarray('1000000010000000100000001000000010000000100000001000000010000000') >> i
            value -= penalty * ((file & self.board.whitePawns).count()- 1)
            value += penalty * ((file & self.board.blackPawns).count()- 1)
        return value
    
    def evalMobility(self, phase, weight=2):
        value = len(self.board.generatePseudoLegalMoves())
        self.board.toPlay = colour.Colour.opposite(self.board.toPlay)
        value -= len(self.board.generatePseudoLegalMoves())
        self.board.toPlay = colour.Colour.opposite(self.board.toPlay)
        value *= weight*(24-phase)/24
        if self.board.toPlay == colour.Colour.WHITE:
            return value
        else:
            return -value

    def calcPhase(self):
        phase = 24
        phase -= self.board.whiteKnights.count()
        phase -= self.board.whiteBishops.count()
        phase -= 2*self.board.whiteRooks.count()
        phase -= 4*self.board.whiteQueens.count()
        phase -= self.board.blackBishops.count()
        phase -= self.board.blackKnights.count()
        phase -= 2*self.board.blackRooks.count()
        phase -= 4*self.board.blackQueens.count()
        return phase


    def heuristicEval(self, moves=None):
        if self.board.gameOver(moves):
            return self.board.getResult(moves)*10000
        phase = self.calcPhase()
        mat_eval = self.evalMaterial()
        pos_eval = self.evalPositioning(phase)
        pawn_eval = self.evalDoubledPawns()
        mob_eval = self.evalMobility(phase)
        return int(mat_eval + pos_eval + pawn_eval + mob_eval)
    
    def orderMoves(self, moves):
        reversed = False
        if self.board.toPlay == colour.Colour.WHITE:
            reversed = True
        evaluatedPositions = []
        boundedPositions = []
        unknownPositions = []
        for move in moves:
            self.board.applyMove(move)
            key = self.board.generateTTKey()
            self.board.unmake(move)
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

    def eval_iterative_deepening(self, eval_depth, quiescenceDepth=10):
        moves = self.board.generateMoves()
        for depth in range(eval_depth+1):
            moves = self.orderMoves(moves)
            self.board.applyMove(moves[0])
            bestEval = self.eval(depth, quiescenceDepth=quiescenceDepth)
            self.board.unmake(moves[0])
            for move in moves[1:]:
                self.board.applyMove(move)
                if self.board.toPlay == colour.Colour.BLACK:
                    eval = self.eval(depth, alpha=bestEval, quiescenceDepth=quiescenceDepth)
                    if eval > bestEval:
                        bestEval = eval
                else:
                    eval = self.eval(depth, beta=bestEval, quiescenceDepth=quiescenceDepth)
                    if eval < bestEval:
                        bestEval = eval
                self.board.unmake(move)
        return bestEval

    def eval(self, depth, alpha=-float('inf'), beta=float('inf'), quiescenceDepth=10):
        key = self.board.generateTTKey()
        transpositionEntry = None
        if key in self.transpositionTable:
            transpositionEntry = self.transpositionTable[key]
            if transpositionEntry.type == 1 and transpositionEntry.depth >= depth:
                return transpositionEntry.value

        if depth == 0:
            value = self.quiescenceEval(quiescenceDepth, alpha, beta)
            newEntry = ttentry.TTEntry(0, value, 1, self.board.age())
            self.transpositionTable[key] = newEntry
            return value
        
        moves = self.board.generateMoves()
        moves = self.orderMoves(moves)

        if len(moves) == 0:
            value = self.heuristicEval(moves)
            newEntry = ttentry.TTEntry(0, value, 1, self.board.age())
            self.transpositionTable[key] = newEntry
            return value
        
        if self.board.toPlay == colour.Colour.WHITE:
            value = -float('inf')
            beatAlpha = False
            for move in moves:
                self.board.applyMove(move)
                value = max(value, self.eval(depth-1, alpha, beta, quiescenceDepth))
                self.board.unmake(move)
                if value > beta:
                    newEntry = ttentry.TTEntry(depth, value, 2, self.board.age())
                    self.transpositionTable[key] = newEntry
                    return value
                if value > alpha:
                    alpha = value
                    beatAlpha = True
            if beatAlpha:
                newEntry = ttentry.TTEntry(depth, value, 1, self.board.age())
            else:
                newEntry = ttentry.TTEntry(depth, value, 3, self.board.age())
            self.transpositionTable[key] = newEntry
            return value
        else:
            value = float('inf')
            beatBeta = False
            for move in moves:
                self.board.applyMove(move)
                value = min(value, self.eval(depth-1, alpha, beta, quiescenceDepth))
                self.board.unmake(move)
                if value < alpha:
                    newEntry = ttentry.TTEntry(depth, value, 3, self.board.age())
                    self.transpositionTable[key] = newEntry
                    return value
                if value < beta:
                    beta = value
                    beatBeta = True
            if beatBeta:
                newEntry = ttentry.TTEntry(depth, value, 1, self.board.age())
            else:
                newEntry = ttentry.TTEntry(depth, value, 2, self.board.age())
            self.transpositionTable[key] = newEntry
            return value
        
    def quiescenceEval(self, depth, alpha=-float('inf'), beta=float('inf')):
        allMoves = self.board.generateMoves()
        moves = self.board.generateQuiescenceMoves(allMoves)
        moves = self.orderMoves(moves)

        key = self.board.generateTTKey()
        transpositionEntry = None
        if key in self.transpositionTable:
            transpositionEntry = self.transpositionTable[key]
            if transpositionEntry.type == 1:
                return transpositionEntry.value

        if depth == 0 or len(moves) == 0:
            value = self.heuristicEval(allMoves)
            newEntry = ttentry.TTEntry(0, value, 1, self.board.age())
            self.transpositionTable[key] = newEntry
            return value
        
        if self.board.toPlay == colour.Colour.WHITE:
            value = self.heuristicEval(allMoves)
            beatAlpha = False
            for move in moves:
                self.board.applyMove(move)
                value = max(value, self.quiescenceEval(depth-1, alpha, beta))
                self.board.unmake(move)
                if value >= beta:
                    newEntry = ttentry.TTEntry(0, value, 2, self.board.age())
                    self.transpositionTable[key] = newEntry
                    return value
                if value > alpha:
                    alpha = value
                    beatAlpha = True
            if beatAlpha:
                newEntry = ttentry.TTEntry(0, value, 1, self.board.age())
            else:
                newEntry = ttentry.TTEntry(0, value, 3, self.board.age())
            self.transpositionTable[key] = newEntry
            return value
        else:
            value = self.heuristicEval(allMoves)
            beatBeta = False
            for move in moves:
                self.board.applyMove(move)
                value = min(value, self.quiescenceEval(depth-1, alpha, beta))
                self.board.unmake(move)
                if value <= alpha:
                    newEntry = ttentry.TTEntry(0, value, 3, self.board.age())
                    self.transpositionTable[key] = newEntry
                    return value
                if value < beta:
                    beta = value
                    beatBeta = True
            if beatBeta:
                newEntry = ttentry.TTEntry(0, value, 1, self.board.age())
            else:
                newEntry = ttentry.TTEntry(0, value, 2, self.board.age())
            self.transpositionTable[key] = newEntry
            return value
        
    # Remove old entries in the transposition table
    def gcTranspositionTable(self):
        age = self.board.age()
        keys = list(self.transpositionTable.keys())
        for key in keys:
            if self.transpositionTable[key].age <= age:
                self.transpositionTable.pop(key)

    def bestMove(self, eval_depth=3, quiescenceDepth=10, perMove=10):
        self.gcTranspositionTable()
        start = time.time()
        moves = self.board.generateMoves()
        for depth in range(eval_depth+1):
            moves = self.orderMoves(moves)
            bestMove = moves[0]
            self.board.applyMove(bestMove)
            bestEval = self.eval(depth, quiescenceDepth=quiescenceDepth)
            self.board.unmake(bestMove)
            for move in moves[1:]:
                self.board.applyMove(move)
                if self.board.toPlay == colour.Colour.BLACK:
                    eval = self.eval(depth, alpha=bestEval, quiescenceDepth=quiescenceDepth)
                    if eval > bestEval:
                        bestEval = eval
                        bestMove = move
                else:
                    eval = self.eval(depth, beta=bestEval, quiescenceDepth=quiescenceDepth)
                    if eval < bestEval:
                        bestEval = eval
                        bestMove = move
                self.board.unmake(move)
                if time.time() - start > perMove:
                    return bestMove, bestEval
        return bestMove, bestEval

    def playGame(self, eval_depth=3, moves=-1, quiescenceDepth=10, perMove=10):
        while not self.gameOver() and moves != 0:
            moves -= 1
            bestMove, bestEval = self.bestMove(eval_depth, quiescenceDepth=quiescenceDepth, perMove=perMove)
            self.board.applyMove(bestMove)
            print(self.getString())
            print(bestEval)
        print(self.getResult())
    
def playAgainstEngine(FEN=None):
    engine = Engine(FEN)
    print(engine.board.getString())
    chosen = colour.Colour.fromString(input("play as white(w) or black(b)?"))
    if  engine.board.toPlay == chosen:
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

def playXBoard():
    engine = Engine()
    while True:
        try:
            command = input().strip()

            if command == "xboard":
                # Respond to xboard command
                print("feature done=0")
                print("feature myname=\"ExplainableEngine\"")
                print("feature ping=1")
                print("feature setboard=1")

            elif command == "new":
                # Respond to new game command
                engine = Engine()
                engine.playing = colour.Colour.BLACK

            elif command.startswith("force"):
                # Respond to force mode command
                pass

            elif command.startswith("protover"):
                # Respond to protocol version command
                print("feature usermove=1")
                print("feature done=1")

            elif command.startswith("quit"):
                # Respond to quit command
                break

            elif command.startswith("time"):
                engine.remaining_time = int(command.split()[1])

            elif command.startswith("otim"):
                engine.opp_remaining_time = int(command.split()[1])

            elif command.startswith("go"):
                if engine.playing == engine.board.toPlay:
                    # Compute best response move
                    move, eval = engine.bestMove(4, 10, engine.remaining_time/4000)
                    engine.board.applyMove(move)
                    if move[2] >= 8:
                        algebraic_move = indexToPos(move[0])+indexToPos(move[1])+["n", "b", "r", "q"][move[2]]
                    else:
                        algebraic_move = indexToPos(move[0])+indexToPos(move[1])
                    print("Responded with -: move", algebraic_move, file=sys.stderr)
                    print("Evaluation -:", eval, file=sys.stderr)
                    print("move", algebraic_move)

            elif command.startswith("usermove"):
                # Handle user move
                algebraic_move = command.split()[1]
                move = engine.board.findMove(algebraic_move)
                print("Responding to move -:", algebraic_move, file=sys.stderr)
                if move != None:
                    engine.board.applyMove(move)
                else:
                    print("Illegal move:", move)

                if engine.board.gameOver():
                    print("Game over", file=sys.stderr)
                    result = engine.board.getResult()
                    if result == -1:
                        print("0-1")
                    elif result == 1:
                        print("1-0")
                    else:
                        print("1/2-1/2")
                else:                
                    # Compute best response move
                    move, eval = engine.bestMove(4, 10, engine.remaining_time/4000)
                    engine.board.applyMove(move)
                    if move[2] >= 8:
                        algebraic_move = indexToPos(move[0])+indexToPos(move[1])+["n", "b", "r", "q"][move[2] % 4]
                    else:
                        algebraic_move = indexToPos(move[0])+indexToPos(move[1])
                    print("Responded with -: move", algebraic_move, file=sys.stderr)
                    print("Evaluation -:", eval, file=sys.stderr)
                    print("move", algebraic_move)

            elif command.startswith("ping"):
                # Respond to ping command
                print("pong", command.split()[1])

            elif command.startswith("setboard"):
                # Set the board to the given position
                fen = " ".join(command.split()[1:])
                engine = Engine(fen)
                engine.playing = colour.Colour.BLACK

            elif command.startswith("random"):
                pass

            elif command.startswith("black"):
                engine.playing = colour.Colour.BLACK

            elif command.startswith("white"):
                engine.playing = colour.Colour.WHITE

            else:
                # Unknown command, send "Error" response
                print("Error")

        except KeyboardInterrupt:
            pass


def main():
    # Redirect stderr to a file
    sys.stderr = open('xboard_interface.log', 'w')
    playXBoard()

if __name__ == "__main__":
    main()
