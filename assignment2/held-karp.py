import numpy as np
from numba import njit
import pandas as pd

a = pd.read_csv("./datasets/test20.txt")
points = np.array(a[['x','y']])
inputsize = len(points)

# distance matrix 만들기
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
distance_matrix = np.sqrt(np.sum(diff ** 2, axis=-1))
len(distance_matrix)

S = distance_matrix
v = 0

memo = np.full((1 << len(S), len(S)), np.inf) # 비트마스킹으로 10001 이면 두개 원소 있는거임

def dp(S, v=0): #v 는 인덱스 S 는 리스트
    Min = np.inf
    size = len( S )
    minindex=0
    if size == 1:
        memo[0][v]=distance_matrix[0][v]
        return distance_matrix[0][v]
    Sbitmask = 0
    for x in S:
        Sbitmask += 1<<x
    if np.isfinite( memo[Sbitmask][v] ):
        return memo[Sbitmask][v]
    for i in S:
        if i == v:
            continue
        new_s = S.copy()
        new_s.remove(v)
        cost = dp( new_s, i ) + distance_matrix[i][v]
        if cost < Min:
            Min = cost
            minindex = i
    memo[Sbitmask][v] = Min
    return Min


x = [x for x in range(len(S))]
b = np.array(x)
print(dp(x))