from engine import *
import time

class Tutor():
    def __init__(self, filename, depth=4):
        self.filename=filename
        self.last_line_read = ""
        self.engine = Engine()
        self.depth=depth

    def read_new_messages(self):
        with open(self.filename, "r") as file:
            file.seek(0, 2)
            file.seek(0 if self.last_line_read == "" else file.tell() - len(self.last_line_read), 0)

            new_messages = file.readlines()
            self.last_line_read = new_messages[-1] if new_messages else self.last_line_read

        return new_messages

    def process_command(self, message):
        command = message.strip()
        if command == "new":
            self.engine = Engine()
            self.bestMove, self.bestEval, self.bestReason = self.engine.bestMoveReason(self.depth, quiescenceDepth=12)

        elif command.startswith("quit"):
            # Respond to quit command
            quit()

        elif command.startswith("user"):
            # Handle user move
            algebraic_move = command.split()[1]
            move = self.engine.board.findMove(algebraic_move)
            self.engine.board.applyMove(move)

            if self.engine.board.gameOver():
                print("\nGame over")
                result = self.engine.board.getResult()
                if result == -1:
                    print("0-1")
                elif result == 1:
                    print("1-0")
                else:
                    print("1/2-1/2")
            else:                
                # Compute evaluation and reason
                userEval, userReason = self.engine.evalReason(self.depth, quiescenceDepth=12)
                if move == self.bestMove or userEval == self.bestEval:
                    print("\nYou played the best move!")
                    self.printEvalReason(userEval, userReason)
                else:
                    print("\nThe move", moveToAlgebraic(self.bestMove), "was better than your move:")
                    self.printEvalReason(self.bestEval, self.bestReason)
                    print("\nCompared to your move:")
                    self.printEvalReason(userEval, userReason)

        elif command.startswith("engine"):
            # Handle user move
            algebraic_move = command.split()[1]
            move = self.engine.board.findMove(algebraic_move)
            self.engine.board.applyMove(move)

            if self.engine.board.gameOver():
                print("\nGame over")
                result = self.engine.board.getResult()
                if result == -1:
                    print("0-1")
                elif result == 1:
                    print("1-0")
                else:
                    print("1/2-1/2")
            else:                
                # Compute evaluation and reason
                self.bestMove, self.bestEval, self.bestReason = self.engine.bestMoveReason(self.depth, quiescenceDepth=12)


    def mainLoop(self):
        while True:
            new_messages = self.read_new_messages()
            if new_messages:
                for message in new_messages:
                    self.process_command(message)
            time.sleep(0.1)

    def printEvalReason(self, eval, reason):
        heuristic_reasons = ["Game result: ", "Material score: ", "Piece positioning: ", "Pawn structure: ", "Mobility score: "]
        print("Overall evaluation: ", eval)
        for i in range(len(heuristic_reasons)):
            print(heuristic_reasons[i], reason[i])

def main():
    filename = "communication.txt"
    tutor = Tutor(filename)
    tutor.mainLoop()


if __name__ == "__main__":
    main()