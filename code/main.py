import os
import sys
import argparse
from utils.utils import load_dataset, save_solution, save_trace
from algorithms.branch_and_bound import BranchAndBound
from algorithms.approximation import ApproximationAlgorithm
from algorithms.local_search_1 import LocalSearch1
from algorithms.local_search_2 import LocalSearch2

# Assume that utils and algorithms are in the same directory as main.py or adjust sys.path accordingly.
def parse_args():
    parser = argparse.ArgumentParser(description="Run algorithms for the Knapsack Problem")
    parser.add_argument("-inst", "--instance", type=str, required=True, help="Dataset filepath")
    parser.add_argument("-alg", "--algorithm", type=str, choices=['BnB', 'Approx', 'LS1', 'LS2'], required=True,
                        help="Algorithm to use: BnB, Approx, LS1, or LS2")
    parser.add_argument("-time", "--cutoff_time", type=int, required=True, help="Cut-off time in seconds")
    parser.add_argument("-seed", "--random_seed", type=int, required=False, default=None,
                        help="Random seed for the algorithm (optional for BnB and Approx)")
    return parser.parse_args()

def main():

    args = parse_args()

    if args.algorithm in ['LS1', 'LS2'] and args.random_seed is None:
        print("Error: LS1 and LS2 algorithms require a random seed.")
        sys.exit(1)

    dataset_path = args.instance
    algorithm_choice = args.algorithm
    cut_off_time = args.cutoff_time
    random_seed = args.random_seed

    items, capacity = load_dataset(dataset_path)

    algorithms = {
        'BnB': BranchAndBound(items, capacity),
        'Approx': ApproximationAlgorithm(items, capacity),
        'LS1': LocalSearch1(items, capacity, random_seed),
        'LS2': LocalSearch2(items, capacity, random_seed)
    }

    if algorithm_choice not in algorithms:
        print(f"Error: Unknown algorithm choice '{algorithm_choice}'.")
        print("Valid options are: BnB, Approx, LS1, LS2.")
        sys.exit(1)

    algorithm = algorithms.get(algorithm_choice)

    solution, trace = algorithm.solve(cut_off_time)

    # Ensure output directories exist
    os.makedirs(f"Output/solution_files/{algorithm_choice}", exist_ok=True)
    os.makedirs(f"Output/trace_files/{algorithm_choice}", exist_ok=True)

    save_solution(dataset_path, algorithm_choice, cut_off_time, random_seed, solution)
    save_trace(dataset_path, algorithm_choice, cut_off_time, random_seed, trace)

if __name__ == "__main__":
    main()