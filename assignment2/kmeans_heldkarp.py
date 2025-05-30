import pandas as pd
import numpy as np
import time
from sklearn.cluster import KMeans
import itertools
from scipy.spatial.distance import pdist, squareform
import heapq

# 첨부된 파일의 최적화된 TSP 함수들을 그대로 사용
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
        return [0]
    if n == 2:
        return [0, 1, 0]
    
    dp = {}
    parent = {}
    
    # 초기화
    for j in range(1, n):
        dp[(1 << j, j)] = dist_matrix[0, j]
        parent[(1 << j, j)] = 0
    
    # DP 계산
    for size in range(2, n):
        for subset in itertools.combinations(range(1, n), size):
            mask = sum(1 << bit for bit in subset)
            
            for end in subset:
                dp[(mask, end)] = float('inf')
                prev_mask = mask & ~(1 << end)
                
                for prev_end in subset:
                    if prev_end == end or not (prev_mask & (1 << prev_end)):
                        continue
                    
                    cost = dp.get((prev_mask, prev_end), float('inf')) + dist_matrix[prev_end, end]
                    if cost < dp[(mask, end)]:
                        dp[(mask, end)] = cost
                        parent[(mask, end)] = prev_end
    
    # 최적 경로 찾기 및 재구성
    mask = (1 << n) - 2
    min_cost = float('inf')
    best_last = -1
    
    for end in range(1, n):
        if (mask, end) in dp:
            cost = dp[(mask, end)] + dist_matrix[end, 0]
            if cost < min_cost:
                min_cost = cost
                best_last = end
    
    if best_last == -1:
        return list(range(n)) + [0]
    
    # 경로 재구성
    tour = [0]
    mask = (1 << n) - 2
    end = best_last
    
    while end != 0 and (mask, end) in parent:
        tour.append(end)
        new_end = parent[(mask, end)]
        mask &= ~(1 << end)
        end = new_end
    
    if tour[-1] != 0:
        tour.append(0)
    
    return tour

def find_cluster_connections_optimized(clusters, coords):
    """클러스터 간 연결점을 벡터화 연산으로 고속 계산"""
    n_clusters = len(clusters)
    cluster_dist_matrix = np.full((n_clusters, n_clusters), np.inf)
    cluster_connections = {}
    
    for i in range(n_clusters):
        for j in range(i+1, n_clusters):
            if len(clusters[i]) == 0 or len(clusters[j]) == 0:
                continue
            
            coords_i = coords[clusters[i]]
            coords_j = coords[clusters[j]]
            
            distances = pairwise_distances_optimized(coords_i, coords_j)
            
            min_idx = np.unravel_index(np.argmin(distances), distances.shape)
            min_dist = distances[min_idx]
            
            best_pair = (clusters[i][min_idx[0]], clusters[j][min_idx[1]])
            
            cluster_dist_matrix[i, j] = min_dist
            cluster_dist_matrix[j, i] = min_dist
            cluster_connections[(i, j)] = best_pair
            cluster_connections[(j, i)] = (best_pair[1], best_pair[0])
    
    return cluster_dist_matrix, cluster_connections

def solve_tsp_recursive_optimized(coords, max_cluster_size=15):
    """완전 최적화된 재귀적 TSP 해결"""
    n = len(coords)
    
    if n == 0:
        return []
    
    if n <= max_cluster_size:
        dist_matrix = calculate_distance_matrix_optimized(coords)
        tour = held_karp_optimized(dist_matrix)
        if len(tour) > 1 and tour[-1] == tour[0]:
            tour = tour[:-1]
        return tour
    
    # K-means 클러스터링
    n_clusters = min(max_cluster_size, max(2, n // max_cluster_size))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(coords)
    
    # 클러스터 그룹화
    clusters = [[] for _ in range(n_clusters)]
    for i, label in enumerate(labels):
        clusters[label].append(i)
    
    # 빈 클러스터 제거
    clusters = [cluster for cluster in clusters if len(cluster) > 0]
    n_clusters = len(clusters)
    
    if n_clusters == 1:
        dist_matrix = calculate_distance_matrix_optimized(coords)
        tour = held_karp_optimized(dist_matrix)
        if len(tour) > 1 and tour[-1] == tour[0]:
            tour = tour[:-1]
        return tour
    
    # 클러스터 간 연결 계산
    cluster_dist_matrix, cluster_connections = find_cluster_connections_optimized(clusters, coords)
    
    # 클러스터 레벨 TSP
    cluster_tour = held_karp_optimized(cluster_dist_matrix)
    if len(cluster_tour) > 1 and cluster_tour[-1] == cluster_tour[0]:
        cluster_tour = cluster_tour[:-1]
    
    # 진입/출구 노드 결정
    entry_exit = {}
    for i in range(len(cluster_tour)):
        curr_cluster = cluster_tour[i]
        next_cluster = cluster_tour[(i + 1) % len(cluster_tour)]
        
        if (curr_cluster, next_cluster) in cluster_connections:
            exit_node, entry_node = cluster_connections[(curr_cluster, next_cluster)]
            
            if curr_cluster not in entry_exit:
                entry_exit[curr_cluster] = {"entry": None, "exit": exit_node}
            else:
                entry_exit[curr_cluster]["exit"] = exit_node
            
            if next_cluster not in entry_exit:
                entry_exit[next_cluster] = {"entry": entry_node, "exit": None}
            else:
                entry_exit[next_cluster]["entry"] = entry_node
    
    # 각 클러스터의 TSP 해결 및 경로 구성
    final_tour = []
    processed_nodes = set()
    
    for cluster_idx in cluster_tour:
        cluster_nodes = clusters[cluster_idx]
        cluster_coords = coords[cluster_nodes]
        
        # 재귀 호출로 클러스터 내부 해결
        if len(cluster_nodes) > max_cluster_size:
            cluster_tour_local = solve_tsp_recursive_optimized(cluster_coords, max_cluster_size)
            cluster_path = [cluster_nodes[local_idx] for local_idx in cluster_tour_local]
        else:
            if len(cluster_nodes) == 1:
                cluster_path = cluster_nodes
            else:
                cluster_dist_matrix = calculate_distance_matrix_optimized(cluster_coords)
                local_tour = held_karp_optimized(cluster_dist_matrix)
                if len(local_tour) > 1 and local_tour[-1] == local_tour[0]:
                    local_tour = local_tour[:-1]
                cluster_path = [cluster_nodes[local_idx] for local_idx in local_tour]
        
        # 진입/출구 노드에 맞게 경로 조정
        entry_node = entry_exit.get(cluster_idx, {}).get("entry")
        exit_node = entry_exit.get(cluster_idx, {}).get("exit")
        
        if entry_node is not None and exit_node is not None and entry_node != exit_node:
            if entry_node in cluster_path and exit_node in cluster_path:
                entry_idx = cluster_path.index(entry_node)
                exit_idx = cluster_path.index(exit_node)
                
                if entry_idx <= exit_idx:
                    cluster_path = cluster_path[entry_idx:exit_idx+1]
                else:
                    cluster_path = cluster_path[entry_idx:] + cluster_path[:exit_idx+1]
        
        # 중복 제거하면서 추가
        for node in cluster_path:
            if node not in processed_nodes:
                final_tour.append(node)
                processed_nodes.add(node)
    
    # 누락 노드 복구
    all_nodes = set(range(n))
    missing_nodes = all_nodes - processed_nodes
    
    if missing_nodes:
        for missing_node in sorted(missing_nodes):
            if len(final_tour) == 0:
                final_tour.append(missing_node)
                continue
            
            best_pos = 0
            min_cost_increase = float('inf')
            
            for pos in range(len(final_tour) + 1):
                cost_increase = 0
                
                if pos == 0:
                    if len(final_tour) > 0:
                        cost_increase = np.linalg.norm(coords[missing_node] - coords[final_tour[0]])
                elif pos == len(final_tour):
                    cost_increase = np.linalg.norm(coords[missing_node] - coords[final_tour[-1]])
                else:
                    prev_node = final_tour[pos-1]
                    next_node = final_tour[pos]
                    cost_increase = (
                        np.linalg.norm(coords[missing_node] - coords[prev_node]) +
                        np.linalg.norm(coords[missing_node] - coords[next_node]) -
                        np.linalg.norm(coords[prev_node] - coords[next_node])
                    )
                
                if cost_increase < min_cost_increase:
                    min_cost_increase = cost_increase
                    best_pos = pos
            
            final_tour.insert(best_pos, missing_node)
    
    return final_tour

def calculate_total_distance(coords, tour):
    """경로의 총 거리 계산"""
    total_distance = 0
    for i in range(len(tour)):
        curr = tour[i]
        next_node = tour[(i + 1) % len(tour)]
        total_distance += np.linalg.norm(coords[curr] - coords[next_node])
    return total_distance

# 3개 데이터셋에 대한 TSP 실행 및 결과 저장
def run_tsp_benchmark():
    """3개 데이터셋에 대한 TSP 벤치마크 실행"""
    
    datasets = [
        {"file": "./datasets/a280.csv", "name": "a280"},
        {"file": "./minidatasets/minitsp.csv", "name": "minitsp"},
        {"file": "./datasets/xql662.csv", "name": "xql662"} #,
        # {"file": "./datasets/mona-lisa100K.csv", "name": "mona-lisa100K"}
    ]
    
    results = []
    
    for dataset in datasets:
        try:
            print(f"\n=== {dataset['name']} 데이터셋 처리 중 ===")
            
            # 데이터 로드
            data = pd.read_csv(dataset['file'])
            points = np.array(data[['x', 'y']])
            num_nodes = len(points)
            
            print(f"노드 수: {num_nodes}")
            
            # TSP 실행 시간 측정
            start_time = time.time()
            tour = solve_tsp_recursive_optimized(points, max_cluster_size=15)
            end_time = time.time()
            
            execution_time = end_time - start_time
            total_distance = calculate_total_distance(points, tour)
            
            results.append({
                'dataset': dataset['name'],
                'num_nodes': num_nodes,
                'execution_time_sec': round(execution_time, 4),
                'total_distance': round(total_distance, 4),
                'nodes_in_tour': len(tour),
                'all_nodes_included': len(set(tour)) == num_nodes
            })
            
            print(f"실행 시간: {execution_time:.4f}초")
            print(f"총 경로 거리: {total_distance:.4f}")
            print(f"모든 노드 포함: {len(set(tour)) == num_nodes}")
            
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {dataset['file']}")
            results.append({
                'dataset': dataset['name'],
                'num_nodes': None,
                'execution_time_sec': None,
                'total_distance': None,
                'nodes_in_tour': None,
                'all_nodes_included': None,
                'error': 'File not found'
            })
        except Exception as e:
            print(f"오류 발생 ({dataset['name']}): {str(e)}")
            results.append({
                'dataset': dataset['name'],
                'num_nodes': None,
                'execution_time_sec': None,
                'total_distance': None,
                'nodes_in_tour': None,
                'all_nodes_included': None,
                'error': str(e)
            })
    
    # 결과를 DataFrame으로 변환
    results_df = pd.DataFrame(results)
    
    # CSV 파일로 저장
    output_filename = 'myown.csv'
    results_df.to_csv(output_filename, index=False, encoding='utf-8')
    
    print(f"\n=== 결과 요약 ===")
    print(results_df)
    print(f"\n결과가 '{output_filename}' 파일로 저장되었습니다.")
    
    return results_df

# 실행
if __name__ == "__main__":
    benchmark_results = run_tsp_benchmark()
