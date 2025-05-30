import numpy as np
import pandas as pd
import math
import heapq
import matplotlib.pyplot as plt
from decimal import Decimal
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
        
    edges = edges + edges
    # print(len(edges))
    # print(nodes)

    e_path = find_eulerian_circuit(nodes, edges)

    short_cutting = []
    for i in range(len(e_path) - 1):
        if e_path[i] not in short_cutting:
            short_cutting.append(e_path[i])

    dist = 0
    for i in range(len(short_cutting) -1):
        dist += distance_matrix[short_cutting[i]][short_cutting[i+1]]

    return dist

import numpy as np
import pandas as pd
import math
import heapq
import matplotlib.pyplot as plt
import time
from decimal import Decimal

floaterr = 1.0e-8

def find_eulerian_circuit(nodes, edges):
    stack = [nodes[0]]
    result = []
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
    # distance matrix 만들기
    diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    distance_matrix = np.sqrt(np.sum(diff ** 2, axis=-1))
    
    inputsize = len(points)
    
    # MST 찾기(프림 알고리즘 사용)
    visited = [False] * len(points)
    minheap = []
    mstgraph = np.full((inputsize, inputsize), np.inf)
    
    # 0 추가
    for x in range(inputsize):
        heapq.heappush(minheap, (distance_matrix[0][x], 0, x))
    visited[0] = True
    
    while minheap:
        Weight, From, To = heapq.heappop(minheap)
        if not visited[To]:
            visited[To] = True
            mstgraph[From, To] = Weight
            mstgraph[To, From] = Weight
            for x in range(inputsize):
                next_to, next_weight = x, distance_matrix[To][x]
                if not visited[next_to]:
                    heapq.heappush(minheap, (next_weight, To, next_to))
    
    nodes = []
    edges = []
    for x in range(len(mstgraph)):
        for y in range(len(mstgraph)):
            if x >= y:
                continue
            if mstgraph[x][y] != np.inf:
                edges.append((x, y))
    for x in range(len(mstgraph)):
        nodes.append(x)
    
    edges = edges + edges  # MST의 각 간선을 두 번 복사
    
    e_path = find_eulerian_circuit(nodes, edges)
    
    short_cutting = []
    for i in range(len(e_path) - 1):
        if e_path[i] not in short_cutting:
            short_cutting.append(e_path[i])
    
    dist = 0
    for i in range(len(short_cutting) - 1):
        dist += distance_matrix[short_cutting[i]][short_cutting[i + 1]]
    
    return dist, short_cutting

def run_tsp_benchmark():
    """3개 데이터셋에 대한 2-approximation TSP 벤치마크 실행"""
    
    datasets = [
        {"file": "./datasets/a280.csv", "name": "a280"},
        {"file": "./minidatasets/kz9976.csv", "name": "kz9976"},
        {"file": "./datasets/xql662.csv", "name": "xql662"}
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
            total_distance, tour = twoapp(points)
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            # 순환 경로로 만들기 위해 마지막에 시작점 추가
            if len(tour) > 0 and tour[-1] != tour[0]:
                # 마지막 노드에서 시작점까지의 거리 추가
                diff = points[tour[-1]] - points[tour[0]]
                last_distance = np.sqrt(np.sum(diff ** 2))
                total_distance += last_distance
            
            results.append({
                'dataset': dataset['name'],
                'num_nodes': num_nodes,
                'execution_time_sec': round(execution_time, 6),
                'total_distance': round(total_distance, 6),
                'tour_length': len(tour),
                'algorithm': '2-approximation'
            })
            
            print(f"실행 시간: {execution_time:.6f}초")
            print(f"총 경로 거리: {total_distance:.6f}")
            print(f"투어 길이: {len(tour)}개 노드")
            
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {dataset['file']}")
            results.append({
                'dataset': dataset['name'],
                'num_nodes': None,
                'execution_time_sec': None,
                'total_distance': None,
                'tour_length': None,
                'algorithm': '2-approximation',
                'error': 'File not found'
            })
        except Exception as e:
            print(f"오류 발생 ({dataset['name']}): {str(e)}")
            results.append({
                'dataset': dataset['name'],
                'num_nodes': None,
                'execution_time_sec': None,
                'total_distance': None,
                'tour_length': None,
                'algorithm': '2-approximation',
                'error': str(e)
            })
    
    # 결과를 DataFrame으로 변환
    results_df = pd.DataFrame(results)
    
    # CSV 파일로 저장
    output_filename = 'tsp_2approximation_results.csv'
    results_df.to_csv(output_filename, index=False, encoding='utf-8')
    
    print(f"\n=== 결과 요약 ===")
    print(results_df.to_string(index=False))
    print(f"\n결과가 '{output_filename}' 파일로 저장되었습니다.")
    
    return results_df

# 개별 데이터셋 테스트 함수 (디버깅용)
def test_single_dataset(dataset_path, dataset_name):
    """단일 데이터셋 테스트"""
    try:
        print(f"\n=== {dataset_name} 단일 테스트 ===")
        data = pd.read_csv(dataset_path)
        points = np.array(data[['x', 'y']])
        
        start_time = time.time()
        total_distance, tour = twoapp(points)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        print(f"노드 수: {len(points)}")
        print(f"실행 시간: {execution_time:.6f}초")
        print(f"총 거리: {total_distance:.6f}")
        print(f"투어: {tour[:10]}..." if len(tour) > 10 else f"투어: {tour}")
        
        return True
    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        return False

# 실행
if __name__ == "__main__":
    # 전체 벤치마크 실행
    benchmark_results = run_tsp_benchmark()