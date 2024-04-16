from engine import *

def playXBoard():
    engine = Engine()
    while True:
        try:
            command = input().strip()

            if command == "xboard":
                # Respond to xboard command
                print("feature done=0")

            elif command == "new":
                # Respond to new game command
                engine = Engine()
                engine.playing = colour.Colour.BLACK

            elif command.startswith("protover"):
                # Respond to protocol version command
                print("feature myname=\"ExplainableEngine\"")
                print("feature ping=1")
                print("feature setboard=1")
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
                    move, eval, reason = engine.bestMoveReason(5, 10, engine.remaining_time/(120*(45-(engine.board.fullMoves%40))))
                    engine.board.applyMove(move)
                    print("Played move -:", moveToAlgebraic(move), file=sys.stderr)
                    printEvalReason(eval, reason, file=sys.stderr)
                    print("move", moveToAlgebraic(move))

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
                    move, eval, reason = engine.bestMoveReason(5, 10, engine.remaining_time/(120*(45-(engine.board.fullMoves%40))))
                    engine.board.applyMove(move)
                    print("Played move -:", moveToAlgebraic(move), file=sys.stderr)
                    printEvalReason(eval, reason, file=sys.stderr)
                    print("move", moveToAlgebraic(move))

            elif command.startswith("ping"):
                # Respond to ping command
                print("pong", command.split()[1])

            elif command.startswith("setboard"):
                # Set the board to the given position
                fen = " ".join(command.split()[1:])
                engine = Engine(fen)
                engine.playing = colour.Colour.BLACK

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
    # Redirect stderr to a file for debugging with xboard
    sys.stderr = open('xboard_reasons.log', 'w')
    playXBoard()

if __name__ == "__main__":
    main()