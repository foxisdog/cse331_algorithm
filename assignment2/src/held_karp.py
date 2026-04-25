import argparse
import itertools
import os
import time

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform


def calculate_distance_matrix(coords):
    """Compute a dense Euclidean distance matrix."""
    if len(coords) <= 1:
        return np.zeros((len(coords), len(coords)))
    distances = pdist(coords, metric="euclidean")
    return squareform(distances)


def held_karp(dist_matrix):
    """Solve TSP exactly with Held-Karp DP and return a cyclic tour."""
    n = len(dist_matrix)
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1, 0]

    dp = {}
    parent = {}

    for j in range(1, n):
        dp[(1 << j, j)] = dist_matrix[0, j]
        parent[(1 << j, j)] = 0

    for size in range(2, n):
        for subset_indices in itertools.combinations(range(1, n), size):
            mask = sum(1 << bit for bit in subset_indices)
            for end_node in subset_indices:
                prev_mask = mask & ~(1 << end_node)
                min_cost_for_current_end = float("inf")
                best_prev_node = -1
                for prev_node in subset_indices:
                    if prev_node == end_node or not (prev_mask & (1 << prev_node)):
                        continue
                    cost = dp.get((prev_mask, prev_node), float("inf")) + dist_matrix[prev_node, end_node]
                    if cost < min_cost_for_current_end:
                        min_cost_for_current_end = cost
                        best_prev_node = prev_node
                if best_prev_node != -1:
                    dp[(mask, end_node)] = min_cost_for_current_end
                    parent[(mask, end_node)] = best_prev_node

    final_mask = (1 << n) - 2
    min_total_cost = float("inf")
    last_node_of_tour = -1

    for end_node in range(1, n):
        cost_to_complete_tour = dp.get((final_mask, end_node), float("inf")) + dist_matrix[end_node, 0]
        if cost_to_complete_tour < min_total_cost:
            min_total_cost = cost_to_complete_tour
            last_node_of_tour = end_node

    if last_node_of_tour == -1:
        return list(range(n)) + [0]

    tour = [0]
    current_mask = final_mask
    current_last_node = last_node_of_tour
    path_reconstruction = []

    while current_last_node != 0:
        path_reconstruction.append(current_last_node)
        prev_node_in_tour = parent[(current_mask, current_last_node)]
        current_mask &= ~(1 << current_last_node)
        current_last_node = prev_node_in_tour
        if current_last_node == 0 and current_mask != 0:
            break

    tour.extend(reversed(path_reconstruction))
    tour.append(0)
    return tour


def calculate_total_distance(coords, tour):
    """Calculate the total cyclic length of a tour."""
    if not tour or len(coords) == 0:
        return 0.0
    if len(tour) < 2:
        return 0.0

    total_dist = 0.0
    for i in range(len(tour) - 1):
        u = tour[i]
        v = tour[i + 1]
        total_dist += np.linalg.norm(coords[u] - coords[v])
    return total_dist


def run_cli():
    parser = argparse.ArgumentParser(description="Run Held-Karp exact TSP solver.")
    parser.add_argument("input_file", help="Path to the input CSV file containing coordinates (columns 'x', 'y').")
    parser.add_argument("-o", "--output_file", help="Path to save the output CSV file.", default=None)
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.input_file)
        if "x" not in df.columns or "y" not in df.columns:
            raise ValueError("Input CSV must contain 'x' and 'y' columns.")
        points = np.array(df[["x", "y"]], dtype=np.float64)
    except FileNotFoundError:
        print(f"오류: 입력 파일 '{args.input_file}'을(를) 찾을 수 없습니다.")
        raise SystemExit(1)
    except ValueError as exc:
        print(f"오류: 입력 파일 형식 문제 - {exc}")
        raise SystemExit(1)
    except Exception as exc:
        print(f"오류: 입력 파일을 읽는 중 문제 발생 - {exc}")
        raise SystemExit(1)

    if points.shape[0] == 0:
        print("오류: 입력 파일에 좌표 데이터가 없습니다.")
        calculated_distance = 0.0
        execution_time = 0.0
        tsp_tour_indices = []
    else:
        dist_matrix = calculate_distance_matrix(points)
        start_time = time.time()
        tsp_tour_indices = held_karp(dist_matrix)
        end_time = time.time()
        execution_time = end_time - start_time
        calculated_distance = calculate_total_distance(points, tsp_tour_indices)

    print(f"\nInput File: {os.path.basename(args.input_file)}")
    print(f"Calculated Distance (Held-Karp): {calculated_distance:.4f}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    if points.shape[0] > 0:
        print(f"Tour length: {len(tsp_tour_indices)}, Unique nodes: {len(set(tsp_tour_indices[:-1]))}")

    if args.output_file:
        output_filename = args.output_file
    else:
        base, _ = os.path.splitext(os.path.basename(args.input_file))
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_filename = os.path.join(project_dir, "result", f"{base}_held_karp_output.csv")

    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    results_df = pd.DataFrame(
        {
            "input_file": [os.path.basename(args.input_file)],
            "num_nodes": [len(points)],
            "distance": [round(calculated_distance, 4)],
            "execution_time_seconds": [round(execution_time, 4)],
        }
    )

    try:
        results_df.to_csv(output_filename, index=False, encoding="utf-8-sig")
        print(f"결과를 '{output_filename}'에 저장했습니다.")
    except Exception as exc:
        print(f"오류: 결과를 CSV 파일에 저장하는 중 문제 발생 - {exc}")


if __name__ == "__main__":
    run_cli()
