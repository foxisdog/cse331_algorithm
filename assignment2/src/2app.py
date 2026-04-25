import numpy as np
import pandas as pd
import math
import heapq
import matplotlib.pyplot as plt
from decimal import Decimal
import time
import argparse # 터미널 인자 처리를 위해 추가
import os # 파일 경로 처리를 위해 추가

floaterr = 1.0e-8

def find_eulerian_circuit(nodes, edges):
    stack = [nodes[0]]
    result =[]
    while stack:
        node = stack[-1]
        found = False
        for edge in edges:
            if edge[0] == node:
                stack.append(edge[1])
                edges.remove(edge)
                found = True
                break
            elif edge[1] == node:
                stack.append(edge[0])
                edges.remove(edge)
                found = True
                break
        if not found:
            result.append(stack.pop())
    return result

def twoapp(points):
    inputsize = len(points) # points 길이를 inputsize로 사용
    # distance matrix 만들기
    diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    distance_matrix = np.sqrt(np.sum(diff ** 2, axis=-1))

    # MST 찾기( 프림 알고리즘 사용)
    visited = [False] * len(points)
    minheap = []
    mstgraph = np.full( ( inputsize, inputsize ), np.inf)

    # 0 추가
    for x in range(inputsize):
        heapq.heappush(minheap, ( distance_matrix[0][x] , 0, x ) )
    visited[ 0 ] = True

    while minheap:
        Weight, From, To = heapq.heappop( minheap )
        if not visited[To]:
            visited[To] = True
            mstgraph[ From, To ] = Weight
            mstgraph[ To, From ] = Weight
            for x in range(inputsize):
                next_to, next_weight = x, distance_matrix[To][x]
                if not visited[ next_to ]:
                    heapq.heappush( minheap, ( next_weight, To, next_to ) )

    nodes = []
    edges=[]
    for x in range( len(mstgraph) ):
        for y in range( len(mstgraph) ):
            if x >= y:
                continue
            if mstgraph[x][y] != np.inf:
                edges.append( (x,y) )
    for x in range(len(mstgraph)):
        nodes.append(x)
        
    edges = edges + edges # 오일러 경로를 위해 간선 복제 (두 배로 만듦)

    e_path = find_eulerian_circuit(nodes, list(edges)) # edges를 list로 복사하여 전달

    short_cutting = []
    visited_nodes_in_shortcut = set() # 중복 방문 방지를 위한 set
    for node in e_path:
        if node not in visited_nodes_in_shortcut:
            short_cutting.append(node)
            visited_nodes_in_shortcut.add(node)
    
    # TSP 경로는 시작점으로 돌아와야 하므로, 마지막 노드를 시작 노드로 추가
    if short_cutting and short_cutting[0] != short_cutting[-1]:
        short_cutting.append(short_cutting[0])


    dist = 0
    for i in range(len(short_cutting) -1):
        dist += distance_matrix[short_cutting[i]][short_cutting[i+1]]

    return dist, short_cutting # 경로도 반환하도록 수정 (선택 사항)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run 2-approximation algorithm for TSP.")
    parser.add_argument("input_file", help="Path to the input CSV file containing coordinates.")
    # 출력 파일 이름을 위한 인자 추가 (선택 사항)
    parser.add_argument("-o", "--output_file", help="Path to save the output CSV file.", default=None)


    args = parser.parse_args()

    # 입력 파일 읽기
    try:
        a = pd.read_csv(args.input_file)
        points = np.array(a[['x','y']])
    except FileNotFoundError:
        print(f"오류: 입력 파일 '{args.input_file}'을(를) 찾을 수 없습니다.")
        exit(1)
    except Exception as e:
        print(f"오류: 입력 파일을 읽는 중 문제 발생 - {e}")
        exit(1)


    start_time = time.time()
    # inputsize를 twoapp 함수 내부에서 points 길이로 계산하도록 변경했으므로, 여기서 넘겨줄 필요 없음
    dist, path = twoapp(points) # 경로도 반환 받음
    end_time = time.time()

    execution_time = end_time - start_time

    print(f"Input File: {args.input_file}")
    print(f"Calculated Distance (2-approximation): {dist}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    # print(f"Path: {path}") # 경로 출력 (선택 사항)

    # 결과 저장
    if args.output_file:
        output_filename = args.output_file
    else:
        # 기본 산출물은 result/ 아래로 모아 저장한다.
        base, ext = os.path.splitext(os.path.basename(args.input_file))
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_filename = os.path.join(project_dir, "result", f"{base}_2app_output.csv")

    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    results_df = pd.DataFrame({
        'input_file': [os.path.basename(args.input_file)],
        'distance': [dist],
        'execution_time_seconds': [execution_time]
    })

    try:
        results_df.to_csv(output_filename, index=False)
        print(f"결과를 '{output_filename}'에 저장했습니다.")
    except Exception as e:
        print(f"오류: 결과를 CSV 파일에 저장하는 중 문제 발생 - {e}")
