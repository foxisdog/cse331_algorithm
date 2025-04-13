import random

def generate_partially_sorted_array(size, shuffle_ratio):
    """
    부분적으로 정렬된 배열 생성
    :param size: 배열 크기
    :param shuffle_ratio: 무작위로 섞을 비율 (0.0 ~ 1.0)
    :return: 부분적으로 정렬된 배열
    """
    # 1. 정렬된 배열 생성
    array = list(range(size))
    
    # 2. 섞을 요소 개수 계산
    num_to_shuffle = int(size * shuffle_ratio)
    
    # 3. 섞을 인덱스 선택
    indices = list(range(size))
    random.shuffle(indices)
    shuffle_indices = indices[:num_to_shuffle]
    
    # 4. 선택된 인덱스만 Fisher-Yates Shuffle 적용
    for i in range(len(shuffle_indices) - 1, 0, -1):
        j = random.randint(0, i)
        # 인덱스에 해당하는 요소 교환
        idx1, idx2 = shuffle_indices[i], shuffle_indices[j]
        array[idx1], array[idx2] = array[idx2], array[idx1]
    
    return array