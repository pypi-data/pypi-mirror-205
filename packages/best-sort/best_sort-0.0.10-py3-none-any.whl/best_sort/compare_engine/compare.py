from best_sort.sort_algos import selection_sort
from best_sort.sort_algos import insertion_sort
from best_sort.sort_algos import bubble_sort
import time
from typing import Callable as function_call


sample_data = [9, 3, 1, 3, 2, 9, 7, 1, 3, 1, 1, 0, 0, 9, 8]

sorting_algorithms = {
        'selection': selection_sort.sort,
        'insertion': insertion_sort.sort,
        'bubble   ': bubble_sort.sort
    }

n_trials = 100000


def get_runtime(sort_algo: function_call[[list], list], data: list) -> float:
    '''
    Returns the runtime of a sort algorithm against a data set.
    Value is in seconds.

    sort_algo - A sorting algorithm function that sorts a list of data.
    data - A list of unsorted data.  Pass by Value.
    '''
    start_time = time.time()
    sort_algo(data.copy())
    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time


def trials(algos: dict[str, function_call[[list], list]], data: list, n_trials: int = 1) -> dict: # noqa : E501
    '''
    Runs each sorting algorithm function against a set of data n times.

    algos - The map of sorting algorithm keys and their functions as values.
    data - A list of data for the algorithms to sort.  ex. [9,4,8,1,0]
    n_trials - The number of times each algorithm should be run.

    The higher the number of trials, the more repeatable the results.
    '''
    results: dict[str, list] = {}

    for algorithm_name, algorithm_function in algos.items():

        if algorithm_name not in results:
            results[algorithm_name] = []

        for i in range(n_trials):
            runtime = get_runtime(algorithm_function, data.copy())
            results[algorithm_name].append(runtime)

    return results


def find_avg_times(results: dict[str, list]) -> dict:
    '''
    Finds the average runtime from a dict containing arrays of runtimes.

    results - dict of raw times of sorting algos.  Pass by value.
    '''
    report = results.copy()

    for algorithm_name, list_of_results in report.items():
        report[algorithm_name] = sum(list_of_results) / len(list_of_results)

    return report


def generate_report(result: dict[str, list[float]], n_trials: int, sample_data: list) -> None:  # noqa: E501
    '''
    Generates a report out of the test performed.

    result - dict generated from trials after finding means.
    n_trials - number of trials for test
    sample_data - This is the list that was sorted by each algorithm.
    '''
    print('Algorithms Tested:')
    for algo_name, avg_runtime in result.items():
        print(algo_name)
    print()
    print(f'Number of Times each was tested: {n_trials}')
    print(f'Number of elements in data: {len(sample_data)}')
    print()
    print('Average Runtimes of Each Algorithm (fastest to slowest):')
    sorted_results = sorted(result.items(), key=lambda x: x[1])
    for algorithm_name, avg_runtime in sorted_results:
        print(f"{algorithm_name} : {avg_runtime:.8f} seconds")
    print()
    fastest_algo = min(result.items(), key=lambda x: x[1])[0]
    print(f'Fastest Algorithm: {fastest_algo}')


if __name__ == "__main__":
    result = find_avg_times(trials(sorting_algorithms, sample_data, n_trials))
    generate_report(result, n_trials, sample_data)
