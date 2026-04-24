import numpy as np
import pandas as pd
import math
import networkx as nx
import sys
import time
import os

start_time = time.perf_counter()

if len(sys.argv) < 2:
    print("Usage: python christofides.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = os.path.splitext(input_file)[0] + ".output"



a = pd.read_csv(input_file)
points = np.array(a[['x','y']])
inputsize = len(points)

# # distance matrix 만들기
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
distance_matrix = np.sqrt(np.sum(diff ** 2, axis=-1))
distance_matrix += 1

# minimum weight perfect matching Blossom 알고리즘
graph = nx.from_numpy_array(distance_matrix)
mst = nx.minimum_spanning_tree(graph, weight='weight')

oddnodeindex = [n for n, d in mst.degree() if d % 2 == 0]
oddnode = graph.copy()
oddnode.remove_nodes_from(oddnodeindex)

matching = nx.algorithms.matching.min_weight_matching( oddnode, weight='weight' )

multigraph = nx.MultiGraph()
multigraph.add_nodes_from(mst.nodes(data=True))
multigraph.add_edges_from(mst.edges(data=True))

for u,v in matching:
    w = graph[u][v]['weight']
    multigraph.add_edge( u, v, weight = w)

circuit = nx.eulerian_circuit(multigraph, source=None)

path = []
visited=np.full( inputsize, False )

for x in circuit:
    if not visited[x[0]]:
        path.append(x[0])
        visited[x[0]] = True

distsum = 0

prev = None
for x in path:
    if prev == None:
        prev = x
        continue
    distsum += graph.edges[(prev , x)]['weight']
    prev = x
distsum += graph.edges[(x , 0)]['weight']

final_result = distsum - inputsize
# 실행 시간 측정 종료 (ms 단위)
end_time = time.perf_counter()
elapsed_ms = int((end_time - start_time) * 1000)  # ms 단위로 변환[2][3][4][6]

# 결과 파일로 저장
with open(output_file, 'w') as f:
    f.write(f"Final result: {final_result}\n")
    f.write(f"Execution Time: {elapsed_ms} ms\n")

print(f"Result saved to {output_file}")
print(f"Execution Time: {elapsed_ms} ms")
