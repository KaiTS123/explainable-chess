from engine import *
import time

class Tutor():
    def __init__(self, filename, depth=3):
        self.filename=filename
        self.last_position = 0
        self.engine = Engine()
        self.depth=depth

    def read_new_messages(self):
        with open(self.filename, "r") as file:
            file.seek(self.last_position)
        
            new_messages = file.readlines()
            
            self.last_position = file.tell()

        return new_messages

    def process_command(self, message):
        command = message.strip()
        if command == "new":
            self.engine = Engine()
            self.bestMove, self.bestEval, self.bestReason, self.bestCont = self.engine.bestMoveReason(self.depth, quiescenceDepth=12, perMove=20)

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
                userEval, userReason, userCont = self.engine.evalReason(self.depth, quiescenceDepth=12)
                if move == self.bestMove or userEval == self.bestEval:
                    print("\nYou played", moveToAlgebraic(move)+ ", the best move!")
                    self.printEvalReason(userEval, userReason, userCont)
                else:
                    print("\nThe move", moveToAlgebraic(self.bestMove), "was better than your move:")
                    self.printEvalReason(self.bestEval, self.bestReason, self.bestCont[1:])
                    print("\nCompared to your move", moveToAlgebraic(move), ":")
                    self.printEvalReason(userEval, userReason, userCont)

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
                self.bestMove, self.bestEval, self.bestReason, self.bestCont = self.engine.bestMoveReason(self.depth, quiescenceDepth=12, perMove=20)


    def mainLoop(self):
        while True:
            new_messages = self.read_new_messages()
            if new_messages:
                for message in new_messages:
                    self.process_command(message)
            time.sleep(0.1)

    def printEvalReason(self, eval, reason, cont):
        heuristic_reasons = ["Checkmate: ", "Material score: ", "Piece positioning: ", "Pawn structure: ", "Mobility score: "]
        max_values = [1, 9, 2, 2, 1]
        print_cont(cont)
        draw_eval_bar(15, eval/100, "Overall evaluation: ")
        if reason[0] == "N/A":
            reasons = list(zip(reason[1:], heuristic_reasons[1:]))
            reasons.sort(key=lambda x: abs(x[0]), reverse=True)
            for i in range(1, len(heuristic_reasons)):
                draw_eval_bar(max_values[i], reasons[i-1][0]/100, reasons[i-1][1])
        else:
            draw_eval_bar(1, reason[0], heuristic_reasons[0])

def draw_eval_bar(N, x, label):
    width = 80  # Maximum width of the evaluation bar
    scale_factor = width / (2 * N)  # Scale factor to adjust for negative and positive values

    label = label + str(x)
    padding = width // 2 - len(label) // 2
    print(" "* padding + label)

    # Draw the evaluation bar
    bar = ""
    for i in range(-width//2, width//2+1):
        if i == 0:
            bar += "|"
        elif i <= x * scale_factor:
            bar += "□"
        else:
            bar += "■"

    # Print the evaluation bar
    print(bar+"\n")

def print_cont(cont):
    res = "Best continuation: "
    for move in cont:
        res += moveToAlgebraic(move)+", "
    print(res[:-2])

def main():
    filename = "communication.txt"
    tutor = Tutor(filename)
    tutor.mainLoop()


if __name__ == "__main__":
    main()