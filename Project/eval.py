import engine
import csv

def main():
    test_data_path = "/Users/kaitannashah/Documents/University/II/Project/explainable-chess/Project/data/stockfish_evals/chessData.csv"
    with open(test_data_path, newline='') as test_data_file:
        reader = csv.reader(test_data_file)
        correct = 0
        for i, row in enumerate(reader):
            if (i % 10000 == 1 and i < 1000000):
                fen = row[0]
                eng = engine.Engine(fen)
                evaluation = eng.eval_iterative_deepening(5)
                test_eval = row[1]
                if test_eval[0] == "#":
                    if test_eval[1] == "+" and evaluation > 100:
                        correct += 1
                    elif test_eval[1] == "-" and evaluation < -100:
                        correct += 1
                else:
                    test_eval = int(test_eval)
                    if test_eval <= 100 and test_eval >= -100:
                        if evaluation <= 100 and evaluation >= -100:
                            correct += 1
                    elif test_eval > 100 and evaluation > 100:
                        correct += 1
                    elif test_eval < -100 and evaluation < -100:
                        correct += 1
        print(correct)

if __name__ == "__main__":
    main()