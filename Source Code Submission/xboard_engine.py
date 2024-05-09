from engine import *

filename="communication.txt"

def write_message(message):
    with open(filename, "a") as file:
        file.write(message+'\n')

def clear_file():
    with open(filename, "w") as file:
        file.write("")

def playXBoard():
    clear_file()
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
                write_message("new")

            elif command.startswith("protover"):
                # Respond to protocol version command
                print("feature myname=\"ExplainableEngine\"")
                print("feature ping=1")
                print("feature setboard=1")
                print("feature usermove=1")
                print("feature done=1")

            elif command.startswith("quit"):
                # Respond to quit command
                clear_file()
                time.sleep(1)
                quit()

            elif command.startswith("time"):
                engine.remaining_time = int(command.split()[1])

            elif command.startswith("otim"):
                engine.opp_remaining_time = int(command.split()[1])

            elif command.startswith("go"):
                if engine.playing == engine.board.toPlay:
                    # Compute best response move
                    move, _ = engine.bestMove(6, 10, engine.remaining_time/(120*(45-(engine.board.fullMoves%40))))
                    engine.board.applyMove(move)
                    print("move", moveToAlgebraic(move))
                    write_message("engine "+ moveToAlgebraic(move))

            elif command.startswith("usermove"):
                # Handle user move
                algebraic_move = command.split()[1]
                move = engine.board.findMove(algebraic_move)
                write_message("user "+ algebraic_move)
                if move != None:
                    engine.board.applyMove(move)
                else:
                    print("Illegal move:", move)

                if engine.board.gameOver():
                    result = engine.board.getResult()
                    if result == -1:
                        print("0-1")
                    elif result == 1:
                        print("1-0")
                    else:
                        print("1/2-1/2")
                else:                
                    # Compute best response move
                    move, _ = engine.bestMove(6, 10, engine.remaining_time/(120*(45-(engine.board.fullMoves%40))))
                    engine.board.applyMove(move)
                    print("move", moveToAlgebraic(move))
                    write_message("engine "+ moveToAlgebraic(move))

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
    playXBoard()

if __name__ == "__main__":
    main()