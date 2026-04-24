import argparse
import os
import time

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans

from held_karp import calculate_distance_matrix, calculate_total_distance, held_karp


def pairwise_distances_optimized(coords1, coords2):
    """두 좌표 집합 간의 모든 쌍 거리를 벡터화로 계산"""
    diff = coords1[:, np.newaxis, :] - coords2[np.newaxis, :, :]
    return np.sqrt(np.sum(diff**2, axis=2))


def find_cluster_connections_optimized(clusters, coords):
    """클러스터 간 연결점을 벡터화 연산으로 고속 계산"""
    n_clusters = len(clusters)
    cluster_dist_matrix = np.full((n_clusters, n_clusters), np.inf)
    cluster_connections = {}

    for i in range(n_clusters):
        for j in range(i + 1, n_clusters):
            if not clusters[i] or not clusters[j]:
                continue

            coords_i = coords[clusters[i]]
            coords_j = coords[clusters[j]]
            distances = pairwise_distances_optimized(coords_i, coords_j)

            if distances.size == 0:
                continue

            min_idx = np.unravel_index(np.argmin(distances), distances.shape)
            min_dist = distances[min_idx]
            best_pair = (clusters[i][min_idx[0]], clusters[j][min_idx[1]])

            cluster_dist_matrix[i, j] = min_dist
            cluster_dist_matrix[j, i] = min_dist
            cluster_connections[(i, j)] = best_pair
            cluster_connections[(j, i)] = (best_pair[1], best_pair[0])

    return cluster_dist_matrix, cluster_connections


def solve_tsp_recursive_optimized(coords, max_cluster_size=15):
    """K-means 분할 정복 방식으로 TSP tour를 구성한다."""
    n = len(coords)
    if n == 0:
        return []

    if n <= max_cluster_size:
        tour = held_karp(calculate_distance_matrix(coords))
        if len(tour) > 1 and tour[0] == tour[-1]:
            tour = tour[:-1]
        return tour

    num_clusters_to_form = min(max_cluster_size, max(2, (n + max_cluster_size - 1) // max_cluster_size))
    kmeans = KMeans(n_clusters=num_clusters_to_form, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(coords)

    clusters = [[] for _ in range(num_clusters_to_form)]
    for i, label in enumerate(labels):
        clusters[label].append(i)

    clusters = [cluster for cluster in clusters if cluster]
    actual_n_clusters = len(clusters)

    if actual_n_clusters == 1:
        tour = held_karp(calculate_distance_matrix(coords))
        if len(tour) > 1 and tour[0] == tour[-1]:
            tour = tour[:-1]
        return tour

    cluster_dist_matrix, cluster_connections = find_cluster_connections_optimized(clusters, coords)
    cluster_level_tour_indices = held_karp(cluster_dist_matrix)
    if len(cluster_level_tour_indices) > 1 and cluster_level_tour_indices[0] == cluster_level_tour_indices[-1]:
        cluster_level_tour_indices = cluster_level_tour_indices[:-1]

    final_tour = []
    visited_global_nodes = set()

    for i in range(len(cluster_level_tour_indices)):
        current_cluster_original_idx = cluster_level_tour_indices[i]
        nodes_in_current_cluster = clusters[current_cluster_original_idx]
        coords_of_current_cluster = coords[nodes_in_current_cluster]

        if len(nodes_in_current_cluster) > max_cluster_size:
            internal_tour_local_indices = solve_tsp_recursive_optimized(coords_of_current_cluster, max_cluster_size)
        else:
            if len(nodes_in_current_cluster) == 1:
                internal_tour_local_indices = [0]
            else:
                internal_tour_local_indices = held_karp(calculate_distance_matrix(coords_of_current_cluster))
                if len(internal_tour_local_indices) > 1 and internal_tour_local_indices[0] == internal_tour_local_indices[-1]:
                    internal_tour_local_indices = internal_tour_local_indices[:-1]

        internal_path_global_indices = [nodes_in_current_cluster[local_idx] for local_idx in internal_tour_local_indices]

        entry_node_global = None
        exit_node_global = None

        if len(cluster_level_tour_indices) > 1:
            prev_cluster_original_idx = cluster_level_tour_indices[(i - 1 + len(cluster_level_tour_indices)) % len(cluster_level_tour_indices)]
            next_cluster_original_idx = cluster_level_tour_indices[(i + 1) % len(cluster_level_tour_indices)]

            if (prev_cluster_original_idx, current_cluster_original_idx) in cluster_connections:
                _, entry_node_global = cluster_connections[(prev_cluster_original_idx, current_cluster_original_idx)]

            if (current_cluster_original_idx, next_cluster_original_idx) in cluster_connections:
                exit_node_global, _ = cluster_connections[(current_cluster_original_idx, next_cluster_original_idx)]

        adjusted_internal_path = []
        if not internal_path_global_indices:
            pass
        elif entry_node_global is None or exit_node_global is None or entry_node_global == exit_node_global:
            adjusted_internal_path = internal_path_global_indices
        else:
            try:
                entry_idx_local = internal_path_global_indices.index(entry_node_global)
                path_len = len(internal_path_global_indices)
                current = entry_idx_local
                while True:
                    adjusted_internal_path.append(internal_path_global_indices[current])
                    if internal_path_global_indices[current] == exit_node_global:
                        break
                    current = (current + 1) % path_len
                    if len(adjusted_internal_path) > path_len:
                        adjusted_internal_path = internal_path_global_indices
                        break
            except ValueError:
                adjusted_internal_path = internal_path_global_indices

        for node_global_idx in adjusted_internal_path:
            if node_global_idx not in visited_global_nodes:
                final_tour.append(node_global_idx)
                visited_global_nodes.add(node_global_idx)

    all_original_nodes = set(range(n))
    missing_nodes = all_original_nodes - visited_global_nodes

    if missing_nodes:
        for missing_node in sorted(list(missing_nodes)):
            if not final_tour:
                final_tour.append(missing_node)
                visited_global_nodes.add(missing_node)
                continue

            min_increase = float("inf")
            best_insert_idx = 0
            for k in range(len(final_tour) + 1):
                if k == 0:
                    current_increase = np.linalg.norm(coords[missing_node] - coords[final_tour[0]])
                elif k == len(final_tour):
                    current_increase = np.linalg.norm(coords[final_tour[-1]] - coords[missing_node])
                else:
                    current_increase = (
                        np.linalg.norm(coords[final_tour[k - 1]] - coords[missing_node])
                        + np.linalg.norm(coords[missing_node] - coords[final_tour[k]])
                        - np.linalg.norm(coords[final_tour[k - 1]] - coords[final_tour[k]])
                    )

                if current_increase < min_increase:
                    min_increase = current_increase
                    best_insert_idx = k

            final_tour.insert(best_insert_idx, missing_node)
            visited_global_nodes.add(missing_node)

    return final_tour


def run_cli():
    parser = argparse.ArgumentParser(description="Run clustering-based divide-and-conquer TSP solver.")
    parser.add_argument("input_file", help="Path to the input CSV file containing coordinates (columns 'x', 'y').")
    parser.add_argument("-o", "--output_file", help="Path to save the output CSV file.", default=None)
    parser.add_argument("--max_cluster_size", type=int, default=15, help="Maximum cluster size for Held-Karp.")
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
        start_time = time.time()
        tsp_tour_indices = solve_tsp_recursive_optimized(points, max_cluster_size=args.max_cluster_size)
        end_time = time.time()
        execution_time = end_time - start_time
        calculated_distance = calculate_total_distance(points, tsp_tour_indices + ([tsp_tour_indices[0]] if tsp_tour_indices else []))

    print(f"\nInput File: {os.path.basename(args.input_file)}")
    print(f"Calculated Distance (Clustering + Held-Karp): {calculated_distance:.4f}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    if points.shape[0] > 0:
        print(f"Nodes in tour: {len(tsp_tour_indices)}, Unique nodes: {len(set(tsp_tour_indices))}, All nodes included: {len(set(tsp_tour_indices)) == len(points)}")

    if args.output_file:
        output_filename = args.output_file
    else:
        base, _ = os.path.splitext(os.path.basename(args.input_file))
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_filename = os.path.join(script_dir, "result", f"{base}_kmeans_hk_output.csv")

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
