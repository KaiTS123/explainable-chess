import colour
import board
import ttentry
from bitarray import bitarray
import time
import sys
from bitarray_masks import *

class Engine:
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
    
    def evalPositioning(self):
        value = 0
        for i in range(64):
            if self.board.whitePawns[i]:
                value += self.PAWN_POS_TABLE[i]
            elif self.board.blackPawns[i]:
                value -= self.PAWN_POS_TABLE[i^56]
            elif self.board.whiteKnights[i]:
                value += self.KNIGHT_POS_TABLE[i]
            elif self.board.blackKnights[i]:
                value -= self.KNIGHT_POS_TABLE[i^56]
            elif self.board.whiteBishops[i]:
                value += self.BISHOP_POS_TABLE[i]
            elif self.board.blackBishops[i]:
                value -= self.BISHOP_POS_TABLE[i^56]
            elif self.board.whiteRooks[i]:
                value += self.ROOK_POS_TABLE[i]
            elif self.board.blackRooks[i]:
                value -= self.ROOK_POS_TABLE[i^56]
            elif self.board.whiteQueens[i]:
                value += self.QUEEN_POS_TABLE[i]
            elif self.board.blackQueens[i]:
                value -= self.QUEEN_POS_TABLE[i^56]
            elif self.board.whiteKing[i]:
                value += self.KING_POS_TABLE[i]
            elif self.board.blackKing[i]:
                value -= self.KING_POS_TABLE[i^56]
        return value
            
    def evalDoubledPawns(self, penalty=30):
        value = 0
        for i in range(8):
            file = bitarray('1000000010000000100000001000000010000000100000001000000010000000') >> i
            value -= penalty * ((file & self.board.whitePawns).count()- 1)
            value += penalty * ((file & self.board.blackPawns).count()- 1)
        return value

    def heuristicEval(self, moves=None):
        if self.board.gameOver(moves):
            return self.board.getResult(moves)*10000
        mat_eval = self.evalMaterial()
        pos_eval = self.evalPositioning()
        pawn_eval = self.evalDoubledPawns()
        return mat_eval+pos_eval+pawn_eval
    
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
            self.gcTranspositionTable()
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
            print("Received command -:", command, file=sys.stderr)

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
                    move, eval = engine.bestMove(4, 10, max(engine.remaining_time/40, (engine.opp_remaining_time-engine.remaining_time)/2)/100)
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
                    move, eval = engine.bestMove(4, 10, max(engine.remaining_time/40, (engine.opp_remaining_time-engine.remaining_time)/2)/100)
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
            print("Keyboard interrupt", file=sys.stderr)
            pass


def main():
    playXBoard()

        
# Redirect stderr to a file
sys.stderr = open('xboard_interface.log', 'w')

if __name__ == "__main__":
    main()
