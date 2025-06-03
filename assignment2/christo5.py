import numpy as np
import pandas as pd
import math
# import heapq # 노트북에 있었으나 networkx로 대체하여 직접 사용되지 않음
# import matplotlib.pyplot as plt # CLI 환경에서는 주석 처리
from decimal import Decimal # 노트북에 있었으나 현재 코드에서 직접 사용되지 않음
import networkx as nx
import time
import argparse
import os

# 노트북 셀 [4]: distance_matrix += 1 와 같은 조정을 위한 값
# floaterr = 1.0e-8 # 노트북에 있었으나 현재 코드에서 직접 사용되지 않음

def calculate_distance_matrix(points):
    """점들의 좌표로부터 거리 행렬을 계산합니다."""
    if points.shape[0] == 0:
        return np.array([])
    # diff = points[:, np.newaxis, :] - points[np.newaxis, :, :] # 노트북 방식
    # distance_matrix = np.sqrt(np.sum(diff ** 2, axis=-1))
    
    # scipy의 pdist + squareform 사용 (노트북 kmeans_heldkarp.ipynb 참고)
    # 만약 scipy가 설치되지 않았다면 위의 numpy 방식으로 대체 가능
    try:
        from scipy.spatial.distance import pdist, squareform
        if points.shape[0] == 1: # 점이 하나일 경우 pdist가 빈 배열 반환
             return np.array([[0.0]])
        distances = pdist(points, metric='euclidean')
        distance_matrix = squareform(distances)
    except ImportError:
        # scipy가 없을 경우 numpy 방식으로 대체
        diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
        distance_matrix = np.sqrt(np.sum(diff ** 2, axis=-1))

    return distance_matrix

def christofides_tsp_solver(points):
    """크리스토피데스 알고리즘을 사용하여 TSP 근사 해를 구하고 거리를 반환합니다."""
    inputsize = len(points)
    if inputsize == 0:
        return 0.0, []
    if inputsize == 1:
        return 0.0, [0]

    # 1. 거리 행렬 계산
    distance_matrix_original = calculate_distance_matrix(points)

    # 2. 노트북의 셀 [4]와 같이 거리에 1을 더합니다.
    distance_matrix_adjusted = distance_matrix_original.copy() + 1.0

    # 3. 그래프 생성 (조정된 거리 행렬 사용)
    graph = nx.from_numpy_array(distance_matrix_adjusted, create_using=nx.Graph)

    # 4. 최소 신장 트리 (MST) 생성
    mst = nx.minimum_spanning_tree(graph, weight='weight')
    
    # 5. MST에서 홀수 차수 정점 찾기 (O)
    odd_degree_nodes = [n for n, d in mst.degree() if d % 2 != 0]

    # 6. 홀수 차수 정점들로 이루어진 부분 그래프에서 최소 가중치 완벽 매칭 (M) 찾기
    if odd_degree_nodes: # 홀수 차수 노드가 있을 때만 매칭 수행
        odd_nodes_subgraph = graph.subgraph(odd_degree_nodes)
        # min_weight_matching은 가중치가 음수가 아닌 그래프에서 작동합니다.
        # 모든 간선에 1을 더했으므로 음수 가중치는 없습니다.
        min_weight_matching_edges = nx.min_weight_matching(odd_nodes_subgraph, weight='weight')
    else: # 홀수 차수 노드가 없으면 (이미 오일러 경로가 가능한 경우) 매칭은 비어있음
        min_weight_matching_edges = set()


    # 7. 다중 그래프 (MST U M) 생성 (H)
    multigraph = nx.MultiGraph()
    multigraph.add_nodes_from(mst.nodes()) # 모든 노드 추가
    multigraph.add_edges_from(mst.edges(data=True)) # MST 간선 추가
    
    for u, v in min_weight_matching_edges:
        # 조정된 거리 행렬에서 매칭 간선의 가중치를 가져옴
        weight = distance_matrix_adjusted[u, v]
        multigraph.add_edge(u, v, weight=weight)

    # 8. 오일러 경로 찾기
    # 시작 노드를 0으로 지정 (또는 첫 번째 노드)
    eulerian_circuit_nodes = []
    if multigraph.number_of_nodes() > 0:
        # 모든 노드의 차수가 짝수이므로 오일러 회로가 존재
        # nx.eulerian_circuit는 간선 리스트를 반환
        eulerian_circuit_edge_list = list(nx.eulerian_circuit(multigraph, source=points_map[0] if points_map else 0))
        if eulerian_circuit_edge_list:
            # 간선 리스트에서 노드 순서 추출
            eulerian_circuit_nodes.append(eulerian_circuit_edge_list[0][0]) # 첫 간선의 첫 노드
            for u_edge, v_edge in eulerian_circuit_edge_list:
                eulerian_circuit_nodes.append(v_edge) # 각 간선의 두 번째 노드 추가


    # 9. 해밀턴 경로 생성 (Shortcutting)
    tsp_path_indices = []
    visited_nodes_in_path = set()
    
    for node_idx in eulerian_circuit_nodes:
        if node_idx not in visited_nodes_in_path:
            tsp_path_indices.append(node_idx)
            visited_nodes_in_path.add(node_idx)
            
    # 시작점으로 돌아오는 경로 완성 (TSP는 보통 순환 경로)
    if tsp_path_indices and tsp_path_indices[0] != tsp_path_indices[-1]:
         tsp_path_indices.append(tsp_path_indices[0])
    
    if not tsp_path_indices and inputsize > 0 : # 경로가 비었고 점이 있으면
        tsp_path_indices = [0]
        if inputsize > 1:
             tsp_path_indices.append(0) # 자기 자신으로 돌아오는 경로
    elif not tsp_path_indices and inputsize == 0:
        return 0.0, []


    # 10. 총 거리 계산 (조정된 거리 행렬 사용)
    total_distance_adjusted = 0
    if len(tsp_path_indices) > 1:
        for i in range(len(tsp_path_indices) - 1): # 마지막 돌아오는 간선 제외하고 계산 후, 마지막에 추가
            u, v = tsp_path_indices[i], tsp_path_indices[i+1]
            total_distance_adjusted += distance_matrix_adjusted[u, v]

    # 노트북 셀[16], [18]과 같이 결과에서 inputsize를 <0xC2><0xC8>니다.
    final_calculated_distance = total_distance_adjusted - inputsize
    
    # 경로 반환 시, 실제 노드 인덱스 사용 (points_map이 있으면 변환)
    # 이 스크립트에서는 points_map을 사용하지 않고 0부터 inputsize-1까지의 인덱스를 직접 사용

    return final_calculated_distance, tsp_path_indices


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Christofides algorithm for TSP (based on n5 notebook).")
    parser.add_argument("input_file", help="Path to the input CSV file containing coordinates (columns 'x', 'y').")
    parser.add_argument("-o", "--output_file", help="Path to save the output CSV file.", default=None)

    args = parser.parse_args()

    # 입력 파일 읽기
    try:
        df = pd.read_csv(args.input_file)
        if 'x' not in df.columns or 'y' not in df.columns:
            raise ValueError("Input CSV must contain 'x' and 'y' columns.")
        # NetworkX는 정수형 노드 레이블을 선호하므로, 인덱스를 그대로 사용
        points_coords = np.array(df[['x', 'y']], dtype=np.float64)
        points_map = list(range(len(points_coords))) # 노드 인덱스 0, 1, 2, ...

    except FileNotFoundError:
        print(f"오류: 입력 파일 '{args.input_file}'을(를) 찾을 수 없습니다.")
        exit(1)
    except ValueError as ve:
        print(f"오류: 입력 파일 형식 문제 - {ve}")
        exit(1)
    except Exception as e:
        print(f"오류: 입력 파일을 읽는 중 문제 발생 - {e}")
        exit(1)

    if points_coords.shape[0] == 0:
        print("오류: 입력 파일에 좌표 데이터가 없습니다.")
        calculated_distance = 0.0
        execution_time = 0.0
    else:
        start_time = time.time()
        calculated_distance, path_indices = christofides_tsp_solver(points_coords)
        end_time = time.time()
        execution_time = end_time - start_time

    print(f"\nInput File: {os.path.basename(args.input_file)}")
    print(f"Calculated Distance (Christofides n5): {calculated_distance:.4f}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    # print(f"Path (indices): {path_indices}") # 경로가 길 수 있으므로 주석 처리

    # 결과 저장
    if args.output_file:
        output_filename = args.output_file
    else:
        base, ext = os.path.splitext(os.path.basename(args.input_file))
        output_filename = f"{base}_christofides_n5_output.csv"

    results_df = pd.DataFrame({
        'input_file': [os.path.basename(args.input_file)],
        'distance': [round(calculated_distance, 4) if calculated_distance is not None else None],
        'execution_time_seconds': [round(execution_time, 4)]
    })

    try:
        results_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print(f"결과를 '{output_filename}'에 저장했습니다.")
    except Exception as e:
        print(f"오류: 결과를 CSV 파일에 저장하는 중 문제 발생 - {e}")