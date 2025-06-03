import numpy as np
import pandas as pd
import math
import heapq # 노트북에 포함되어 있었으나, 현재 코드에서는 직접 사용되지 않는 것으로 보임
import matplotlib.pyplot as plt # 노트북에 포함되어 있었으나, CLI 환경에서는 주석 처리 또는 제거
from decimal import Decimal # 노트북에 포함되어 있었으나, 현재 코드에서는 직접 사용되지 않는 것으로 보임
import networkx as nx # 노트북에 포함되어 있었으나, 현재 코드에서는 직접 사용되지 않는 것으로 보임

# KMeans 및 거리 계산 관련 import
from sklearn.cluster import KMeans
import itertools
from scipy.spatial.distance import pdist, squareform

import time
import argparse
import os

# 노트북 셀 [41] - 옵티멀 값 (현재 스크립트에서는 직접 사용되지 않음)
opt_a280 = 2586.76964756316
opt_kz9976 = 1061882
opt_xql662 = 2513
opt_mona = 100000

floaterr = 1.0e-8 # 노트북 셀 [40]

# --- 노트북 셀 [43]의 함수 정의 시작 ---
def calculate_distance_matrix_optimized(coords):
    """numpy 벡터화를 사용한 고속 거리 행렬 계산"""
    if len(coords) <= 1:
        return np.zeros((len(coords), len(coords)))
    distances = pdist(coords, metric='euclidean')
    return squareform(distances)

def pairwise_distances_optimized(coords1, coords2):
    """두 좌표 집합 간의 모든 쌍 거리를 벡터화로 계산"""
    diff = coords1[:, np.newaxis, :] - coords2[np.newaxis, :, :]
    return np.sqrt(np.sum(diff**2, axis=2))

def held_karp_optimized(dist_matrix):
    """최적화된 Held-Karp 알고리즘"""
    n = len(dist_matrix)
    if n == 0:
        return []
    if n == 1:
        return [0] # 단일 노드 경로는 자기 자신
    if n == 2: # 두 노드 경로는 0-1-0
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
                min_cost_for_current_end = float('inf')
                best_prev_node = -1
                for prev_node in subset_indices:
                    if prev_node == end_node or not (prev_mask & (1 << prev_node)):
                        continue
                    cost = dp.get((prev_mask, prev_node), float('inf')) + dist_matrix[prev_node, end_node]
                    if cost < min_cost_for_current_end:
                        min_cost_for_current_end = cost
                        best_prev_node = prev_node
                if best_prev_node != -1:
                    dp[(mask, end_node)] = min_cost_for_current_end
                    parent[(mask, end_node)] = best_prev_node
    
    final_mask = (1 << n) - 2 # 0번 노드를 제외한 모든 노드 방문
    min_total_cost = float('inf')
    last_node_of_tour = -1

    for end_node in range(1, n):
        cost_to_complete_tour = dp.get((final_mask, end_node), float('inf')) + dist_matrix[end_node, 0]
        if cost_to_complete_tour < min_total_cost:
            min_total_cost = cost_to_complete_tour
            last_node_of_tour = end_node

    if last_node_of_tour == -1: # 경로를 찾지 못한 경우 (n이 매우 작거나 예외 상황)
        # 기본 경로 반환 (예: 0-1-2-...-0), 실제 Held-Karp에서는 거의 발생 안함
        return list(range(n)) + [0] 

    tour = [0] # 시작은 항상 0번 노드
    current_mask = final_mask
    current_last_node = last_node_of_tour

    path_reconstruction = []
    while current_last_node != 0 : # 0번으로 돌아올 때까지
        path_reconstruction.append(current_last_node)
        prev_node_in_tour = parent[(current_mask, current_last_node)]
        current_mask &= ~(1 << current_last_node)
        current_last_node = prev_node_in_tour
        if current_last_node == 0 and current_mask != 0: # 아직 방문할 노드가 남았는데 0으로 돌아가면 오류 가능성 (작은 n)
            # 이 경우는 경로 구성에 문제가 있거나 n이 매우 작을 때 발생 가능
            # Held-Karp 기본 가정은 시작(0)으로 돌아오는 것이므로, 마지막에 0 추가로 처리
            break


    tour.extend(reversed(path_reconstruction))
    tour.append(0) # 마지막으로 시작 노드 0 추가하여 사이클 완성
    
    return tour


def find_cluster_connections_optimized(clusters, coords):
    """클러스터 간 연결점을 벡터화 연산으로 고속 계산"""
    n_clusters = len(clusters)
    cluster_dist_matrix = np.full((n_clusters, n_clusters), np.inf)
    cluster_connections = {}
    
    for i in range(n_clusters):
        for j in range(i + 1, n_clusters):
            if not clusters[i] or not clusters[j]: # 빈 클러스터 예외 처리
                continue
                
            coords_i = coords[clusters[i]]
            coords_j = coords[clusters[j]]
            
            distances = pairwise_distances_optimized(coords_i, coords_j)
            
            if distances.size == 0: # 두 클러스터 중 하나가 비어있으면 거리가 없음
                continue

            min_idx = np.unravel_index(np.argmin(distances), distances.shape)
            min_dist = distances[min_idx]
            
            best_pair = (clusters[i][min_idx[0]], clusters[j][min_idx[1]])
            
            cluster_dist_matrix[i, j] = min_dist
            cluster_dist_matrix[j, i] = min_dist
            cluster_connections[(i, j)] = best_pair
            cluster_connections[(j, i)] = (best_pair[1], best_pair[0]) # 반대 방향도 저장
    
    return cluster_dist_matrix, cluster_connections

def solve_tsp_recursive_optimized(coords, max_cluster_size=15):
    """완전 최적화된 재귀적 TSP 해결"""
    n = len(coords)
    
    if n == 0:
        return []
    
    # 기본 케이스: 작은 문제는 직접 해결
    if n <= max_cluster_size:
        dist_matrix = calculate_distance_matrix_optimized(coords)
        tour = held_karp_optimized(dist_matrix)
        # Held-Karp는 [0, ..., 0] 형태의 순환 경로를 반환하므로, 마지막 복귀 제거하여 리스트로 만듦
        if len(tour) > 1 and tour[0] == tour[-1]:
            tour = tour[:-1] 
        # 모든 노드가 포함되었는지 확인 (단일 노드인 경우도 고려)
        # assert len(set(tour)) == n, f"기본 케이스 노드 누락! 입력: {n}, 경로: {tour}, 유니크: {len(set(tour))}"
        return tour

    # K-means 클러스터링
    # n_clusters 설정: max_cluster_size를 넘지 않도록, 최소 2개 또는 n // max_cluster_size
    # 클러스터 개수가 너무 적거나 많아지지 않도록 조정
    num_clusters_to_form = min(max_cluster_size, max(2, (n + max_cluster_size -1) // max_cluster_size )) # 올림 효과

    # KMeans 실행 시 UserWarning을 피하기 위해 환경변수 설정 (선택 사항, 스크립트 실행 환경에 따라 다름)
    # import os
    # os.environ['OMP_NUM_THREADS'] = '1' # 또는 적절한 스레드 수
    kmeans = KMeans(n_clusters=num_clusters_to_form, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(coords)
    
    clusters = [[] for _ in range(num_clusters_to_form)]
    for i, label in enumerate(labels):
        clusters[label].append(i)
    
    clusters = [cluster for cluster in clusters if cluster] # 빈 클러스터 제거
    actual_n_clusters = len(clusters)

    # 클러스터링 후 모든 노드가 포함되었는지 확인
    # clustered_nodes_set = set(node for cluster in clusters for node in cluster)
    # assert clustered_nodes_set == set(range(n)), "클러스터링 후 노드 누락!"

    if actual_n_clusters == 1: # 모든 점이 하나의 클러스터에 속한 경우
        dist_matrix = calculate_distance_matrix_optimized(coords)
        tour = held_karp_optimized(dist_matrix)
        if len(tour) > 1 and tour[0] == tour[-1]:
            tour = tour[:-1]
        # assert len(set(tour)) == n, "단일 클러스터 케이스 노드 누락!"
        return tour

    cluster_dist_matrix, cluster_connections = find_cluster_connections_optimized(clusters, coords)
    
    cluster_level_tour_indices = held_karp_optimized(cluster_dist_matrix)
    if len(cluster_level_tour_indices) > 1 and cluster_level_tour_indices[0] == cluster_level_tour_indices[-1]:
        cluster_level_tour_indices = cluster_level_tour_indices[:-1]

    final_tour = []
    visited_global_nodes = set()

    for i in range(len(cluster_level_tour_indices)):
        current_cluster_original_idx = cluster_level_tour_indices[i]
        
        # 클러스터 내부 경로 해결
        nodes_in_current_cluster = clusters[current_cluster_original_idx]
        coords_of_current_cluster = coords[nodes_in_current_cluster]

        # 내부 경로 해결 (재귀 또는 직접)
        if len(nodes_in_current_cluster) > max_cluster_size :
             internal_tour_local_indices = solve_tsp_recursive_optimized(coords_of_current_cluster, max_cluster_size)
        else:
            if len(nodes_in_current_cluster) == 1:
                internal_tour_local_indices = [0] # 로컬 인덱스 0
            else:
                internal_dist_matrix = calculate_distance_matrix_optimized(coords_of_current_cluster)
                internal_tour_local_indices = held_karp_optimized(internal_dist_matrix)
                if len(internal_tour_local_indices) > 1 and internal_tour_local_indices[0] == internal_tour_local_indices[-1]:
                    internal_tour_local_indices = internal_tour_local_indices[:-1]
        
        # 로컬 인덱스를 전역 인덱스로 변환
        internal_path_global_indices = [nodes_in_current_cluster[local_idx] for local_idx in internal_tour_local_indices]

        # 클러스터 간 연결점 찾기
        entry_node_global = None
        exit_node_global = None

        if len(cluster_level_tour_indices) > 1 : # 클러스터가 둘 이상일 때만 연결점 의미 있음
            prev_cluster_original_idx = cluster_level_tour_indices[(i - 1 + len(cluster_level_tour_indices)) % len(cluster_level_tour_indices)]
            next_cluster_original_idx = cluster_level_tour_indices[(i + 1) % len(cluster_level_tour_indices)]
            
            # 현재 클러스터로 들어오는 노드 (entry_node_global)
            if (prev_cluster_original_idx, current_cluster_original_idx) in cluster_connections:
                _, entry_node_global = cluster_connections[(prev_cluster_original_idx, current_cluster_original_idx)]
            
            # 현재 클러스터에서 나가는 노드 (exit_node_global)
            if (current_cluster_original_idx, next_cluster_original_idx) in cluster_connections:
                 exit_node_global, _ = cluster_connections[(current_cluster_original_idx, next_cluster_original_idx)]
        
        # 내부 경로를 entry_node에서 시작하여 exit_node로 끝나도록 조정
        adjusted_internal_path = []
        if not internal_path_global_indices: # 내부 경로가 비어있으면 (단일 노드 클러스터 등)
            pass
        elif entry_node_global is None or exit_node_global is None or entry_node_global == exit_node_global : # 연결점이 없거나 같으면 기존 경로 유지
            adjusted_internal_path = internal_path_global_indices
        else:
            try:
                entry_idx_local = internal_path_global_indices.index(entry_node_global)
                exit_idx_local = internal_path_global_indices.index(exit_node_global)

                path_len = len(internal_path_global_indices)
                current = entry_idx_local
                while True:
                    adjusted_internal_path.append(internal_path_global_indices[current])
                    if internal_path_global_indices[current] == exit_node_global:
                        break
                    current = (current + 1) % path_len # 순환적으로 다음 노드
                    if len(adjusted_internal_path) > path_len : # 무한 루프 방지
                         # 이 경우 경로 조정 실패, 원본 경로 사용
                         adjusted_internal_path = internal_path_global_indices
                         break
            except ValueError: # entry/exit 노드가 내부 경로에 없는 예외 케이스
                adjusted_internal_path = internal_path_global_indices # 원본 경로 사용

        # 최종 경로에 추가 (중복 방지)
        for node_global_idx in adjusted_internal_path:
            if node_global_idx not in visited_global_nodes:
                final_tour.append(node_global_idx)
                visited_global_nodes.add(node_global_idx)
        
        # 만약 클러스터의 모든 노드가 이미 방문되었다면 (예: exit_node가 다음 클러스터의 entry_node와 동일),
        # 그리고 현재 클러스터가 단일 노드 클러스터가 아니라면, exit_node를 명시적으로 추가 (경로 연결 보장)
        if exit_node_global is not None and exit_node_global not in visited_global_nodes and len(nodes_in_current_cluster) > 0 :
             # 다음 클러스터의 entry가 될 수 있으므로, 다음 반복에서 처리될 수 있음.
             # 여기서는 일단 추가하지 않고, 누락 노드 복구 단계에서 처리하도록 함.
             pass


    # 모든 원본 노드가 포함되었는지 확인 및 누락된 노드 추가
    all_original_nodes = set(range(n))
    missing_nodes = all_original_nodes - visited_global_nodes
    
    if missing_nodes:
        # print(f"Warning: {len(missing_nodes)}개 노드 누락됨. 추가 삽입 시도: {missing_nodes}")
        for missing_node in sorted(list(missing_nodes)): # 정렬하여 일관성 유지
            if not final_tour:
                final_tour.append(missing_node)
                visited_global_nodes.add(missing_node)
                continue

            min_increase = float('inf')
            best_insert_idx = 0
            # 가장 적은 비용 증가로 삽입할 위치 찾기
            for k in range(len(final_tour) + 1):
                temp_tour = final_tour[:k] + [missing_node] + final_tour[k:]
                current_increase = 0
                if k == 0: # 맨 앞에 삽입
                     if len(final_tour) > 0: # final_tour가 비어있지 않을 때
                        current_increase = np.linalg.norm(coords[missing_node] - coords[final_tour[0]])
                elif k == len(final_tour): # 맨 뒤에 삽입
                    current_increase = np.linalg.norm(coords[final_tour[-1]] - coords[missing_node])
                else: # 중간에 삽입
                    current_increase = (np.linalg.norm(coords[final_tour[k-1]] - coords[missing_node]) +
                                        np.linalg.norm(coords[missing_node] - coords[final_tour[k]]) -
                                        np.linalg.norm(coords[final_tour[k-1]] - coords[final_tour[k]]))
                
                if current_increase < min_increase:
                    min_increase = current_increase
                    best_insert_idx = k
            
            final_tour.insert(best_insert_idx, missing_node)
            visited_global_nodes.add(missing_node)

    # assert len(set(final_tour)) == n, f"최종 경로에 모든 노드가 포함되지 않음! 입력: {n}, 경로: {len(set(final_tour))}"
    return final_tour
# --- 노트북 셀 [43]의 함수 정의 끝 ---


def calculate_total_distance(coords, tour):
    """경로의 총 거리 계산"""
    if not tour or len(coords) == 0: # tour나 coords가 비어있으면 거리 0
        return 0.0
    
    total_dist = 0
    num_points_in_tour = len(tour)
    if num_points_in_tour < 2: # 점이 하나거나 없으면 거리 0
        return 0.0

    for i in range(num_points_in_tour):
        u = tour[i]
        v = tour[(i + 1) % num_points_in_tour] # 마지막 점에서 시작점으로 돌아옴
        total_dist += np.linalg.norm(coords[u] - coords[v])
    return total_dist


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run K-means + Held-Karp TSP solver.")
    parser.add_argument("input_file", help="Path to the input CSV file containing coordinates (columns 'x', 'y').")
    parser.add_argument("-o", "--output_file", help="Path to save the output CSV file.", default=None)
    parser.add_argument("--max_cluster_size", type=int, default=15, help="Maximum cluster size for Held-Karp.")

    args = parser.parse_args()

    # sklearn KMeans UserWarning 관련 OMP_NUM_THREADS 설정 (메모리 누수 경고 방지용)
    # 해당 경고는 성능에 직접적인 영향을 주지 않을 수 있으나, 필요시 활성화
    # os.environ['OMP_NUM_THREADS'] = '1' 

    # 입력 파일 읽기
    try:
        df = pd.read_csv(args.input_file)
        if 'x' not in df.columns or 'y' not in df.columns:
            raise ValueError("Input CSV must contain 'x' and 'y' columns.")
        points = np.array(df[['x', 'y']], dtype=np.float64) # float64로 타입 명시
    except FileNotFoundError:
        print(f"오류: 입력 파일 '{args.input_file}'을(를) 찾을 수 없습니다.")
        exit(1)
    except ValueError as ve:
        print(f"오류: 입력 파일 형식 문제 - {ve}")
        exit(1)
    except Exception as e:
        print(f"오류: 입력 파일을 읽는 중 문제 발생 - {e}")
        exit(1)

    if points.shape[0] == 0:
        print("오류: 입력 파일에 좌표 데이터가 없습니다.")
        calculated_distance = 0.0
        execution_time = 0.0
    else:
        start_time = time.time()
        # solve_tsp_recursive_optimized는 인덱스 리스트를 반환 (순환 경로 X)
        tsp_tour_indices = solve_tsp_recursive_optimized(points, max_cluster_size=args.max_cluster_size)
        end_time = time.time()

        execution_time = end_time - start_time
        
        # 경로의 총 거리 계산
        calculated_distance = calculate_total_distance(points, tsp_tour_indices)

    print(f"\nInput File: {os.path.basename(args.input_file)}")
    print(f"Calculated Distance (K-means + Held-Karp): {calculated_distance:.4f}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    if points.shape[0] > 0:
        print(f"Nodes in tour: {len(tsp_tour_indices)}, Unique nodes: {len(set(tsp_tour_indices))}, All nodes included: {len(set(tsp_tour_indices)) == len(points)}")
    # print(f"Path: {tsp_tour_indices}") # 경로가 길 수 있으므로 주석 처리

    # 결과 저장
    if args.output_file:
        output_filename = args.output_file
    else:
        base, ext = os.path.splitext(os.path.basename(args.input_file))
        output_filename = f"{base}_kmeans_hk_output.csv"

    results_df = pd.DataFrame({
        'input_file': [os.path.basename(args.input_file)],
        'num_nodes': [len(points)],
        'distance': [round(calculated_distance, 4) if calculated_distance is not None else None],
        'execution_time_seconds': [round(execution_time, 4)]
    })

    try:
        results_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print(f"결과를 '{output_filename}'에 저장했습니다.")
    except Exception as e:
        print(f"오류: 결과를 CSV 파일에 저장하는 중 문제 발생 - {e}")