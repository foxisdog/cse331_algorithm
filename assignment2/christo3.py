import numpy as np
import pandas as pd
import math
import networkx as nx
import heapq # 노트북 셀 5에서 사용되었으나, networkx의 MST로 대체 가능. 여기서는 networkx 사용
import time
import argparse
import os

def calculate_distance_matrix(points):
    """점들의 좌표로부터 거리 행렬을 계산합니다."""
    diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    distance_matrix = np.sqrt(np.sum(diff ** 2, axis=-1))
    return distance_matrix

def christofides_algorithm(points, distance_matrix_original):
    """크리스토피데스 알고리즘을 사용하여 TSP 근사 해를 구합니다."""
    inputsize = len(points)
    
    # 노트북 셀[4]와 같이 거리에 1을 더합니다.
    # 이는 특정 데이터셋이나 문제 조건에 따른 것일 수 있습니다.
    # 일반적인 크리스토피데스 알고리즘에서는 이 단계가 없을 수 있습니다.
    distance_matrix = distance_matrix_original.copy() + 1

    # 1. 그래프 생성
    graph = nx.from_numpy_array(distance_matrix, create_using=nx.Graph)

    # 2. 최소 신장 트리 (MST) 생성
    mst = nx.minimum_spanning_tree(graph, weight='weight')
    
    # 3. MST에서 홀수 차수 정점 찾기 (O)
    odd_degree_nodes = [n for n, d in mst.degree() if d % 2 != 0]

    # 4. 홀수 차수 정점들로 이루어진 부분 그래프에서 최소 가중치 완벽 매칭 (M) 찾기
    #    networkx는 음수 가중치가 없는 완전 그래프에서만 min_weight_matching을 직접 지원.
    #    여기서는 홀수 차수 노드들로만 구성된 그래프를 새로 만들어 매칭을 찾습니다.
    odd_nodes_graph = nx.Graph()
    for i in range(len(odd_degree_nodes)):
        for j in range(i + 1, len(odd_degree_nodes)):
            u, v = odd_degree_nodes[i], odd_degree_nodes[j]
            # 원본 distance_matrix (1을 더한)에서 가중치를 가져옴
            weight = distance_matrix[u, v]
            odd_nodes_graph.add_edge(u, v, weight=weight)
            
    # nx.min_weight_matching은 max_cardinality=True일 때 완벽 매칭을 찾으려고 시도합니다.
    # 홀수 정점의 개수는 항상 짝수이므로 완벽 매칭이 존재합니다.
    min_weight_matching_edges = nx.min_weight_matching(odd_nodes_graph, weight='weight')

    # 5. 다중 그래프 (MST U M) 생성 (H)
    multigraph = nx.MultiGraph()
    multigraph.add_nodes_from(mst.nodes())
    multigraph.add_edges_from(mst.edges(data=True))
    
    for u, v in min_weight_matching_edges:
        # 원본 distance_matrix (1을 더한)에서 가중치를 가져옴
        weight = distance_matrix[u,v] # graph[u][v]['weight'] 대신 distance_matrix 사용
        multigraph.add_edge(u, v, weight=weight)

    # 6. 오일러 경로 찾기
    # 시작 노드를 지정하지 않으면 networkx가 임의로 선택 (보통 0번)
    # 모든 노드의 차수가 짝수이므로 오일러 회로가 존재
    eulerian_circuit_edges = list(nx.eulerian_circuit(multigraph, source=0)) # source=0으로 지정

    # 7. 해밀턴 경로 생성 (Shortcutting)
    tsp_path = []
    visited_nodes = np.full(inputsize, False)
    
    for u, v_unused in eulerian_circuit_edges: # 오일러 경로는 (u,v) 튜플의 리스트
        if not visited_nodes[u]:
            tsp_path.append(u)
            visited_nodes[u] = True
            
    # 시작점으로 돌아오는 경로 완성
    if tsp_path and tsp_path[0] != tsp_path[-1]:
         tsp_path.append(tsp_path[0])
    
    if not tsp_path and inputsize > 0 : # 점이 하나라도 있으면 경로에 시작점 추가
        tsp_path.append(0)
        if inputsize > 1 : # 자기 자신으로 돌아오는 경로
             tsp_path.append(0)
    elif not tsp_path and inputsize ==0: # 점이 없으면 빈 경로
        return 0, []


    # 8. 총 거리 계산 (원본 거리 행렬 사용, 1을 더하기 전 또는 더한 후의 거리 사용 여부 확인 필요)
    # 노트북에서는 'graph.edges[(prev , x)]['weight']'를 사용했고, 이는 1이 더해진 거리.
    # 최종 결과에서는 inputsize를 빼주므로, 1이 더해진 거리를 사용하는 것이 노트북의 의도.
    total_distance = 0
    if len(tsp_path) > 1:
        for i in range(len(tsp_path) - 1):
            u, v = tsp_path[i], tsp_path[i+1]
            total_distance += distance_matrix[u, v] # 1이 더해진 거리 사용

    # 노트북 셀[16]과 같이 결과에서 inputsize를 <0xC2><0xC8>니다.
    # 이는 distance_matrix += 1 에 대한 보정일 수 있습니다.
    final_distance = total_distance - inputsize
    
    # 노트북 셀[21] `sum - len(odd_rows)` 부분은 matching 가중치 합계에 대한 조정으로 보이며,
    # 최종 TSP 경로 거리 계산과는 별개로 보입니다. 여기서는 최종 경로 거리만 반환합니다.

    return final_distance, tsp_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Christofides algorithm for TSP.")
    parser.add_argument("input_file", help="Path to the input CSV file containing coordinates (columns 'x', 'y').")
    parser.add_argument("-o", "--output_file", help="Path to save the output CSV file.", default=None)

    args = parser.parse_args()

    # 입력 파일 읽기
    try:
        df = pd.read_csv(args.input_file)
        if 'x' not in df.columns or 'y' not in df.columns:
            raise ValueError("Input CSV must contain 'x' and 'y' columns.")
        points = np.array(df[['x', 'y']])
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
        exit(1)

    # 원본 거리 행렬 계산 (1을 더하기 전)
    distance_matrix_original = calculate_distance_matrix(points)

    start_time = time.time()
    calculated_distance, path = christofides_algorithm(points, distance_matrix_original)
    end_time = time.time()

    execution_time = end_time - start_time

    print(f"Input File: {os.path.basename(args.input_file)}")
    print(f"Calculated Distance (Christofides): {calculated_distance}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    # print(f"Path: {path}") # 경로 출력 (선택 사항)

    # 결과 저장
    if args.output_file:
        output_filename = args.output_file
    else:
        base, ext = os.path.splitext(os.path.basename(args.input_file))
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_filename = os.path.join(script_dir, "result", f"{base}_christofides_output.csv")

    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    results_df = pd.DataFrame({
        'input_file': [os.path.basename(args.input_file)],
        'distance': [calculated_distance],
        'execution_time_seconds': [execution_time]
    })

    try:
        results_df.to_csv(output_filename, index=False)
        print(f"결과를 '{output_filename}'에 저장했습니다.")
    except Exception as e:
        print(f"오류: 결과를 CSV 파일에 저장하는 중 문제 발생 - {e}")
