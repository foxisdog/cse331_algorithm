import sys
import random

def generate_partially_sorted_array(size, shuffle_ratio=0.75):
    """
    부분적으로 정렬된 배열 생성
    :param size: 배열 크기
    :param shuffle_ratio: 무작위로 섞을 비율 (기본값: 20%)
    :return: 부분적으로 정렬된 배열
    """
    # 정렬된 배열 생성
    array = list(range(size))
    
    # 섞을 요소 개수 계산
    num_to_shuffle = int(size * shuffle_ratio)
    
    # 섞을 인덱스 선택
    indices = list(range(size))
    random.shuffle(indices)
    shuffle_indices = indices[:num_to_shuffle]
    
    # 선택된 인덱스만 셔플 수행
    for i in range(len(shuffle_indices) - 1, 0, -1):
        j = random.randint(0, i)
        idx1, idx2 = shuffle_indices[i], shuffle_indices[j]
        array[idx1], array[idx2] = array[idx2], array[idx1]
    
    return array

def main():
    # 명령줄에서 입력받기
    if len(sys.argv) != 2:
        print("사용법: python3 프로그램이름 size")
        sys.exit(1)
    
    try:
        size = int(sys.argv[1])
        if size <= 0:
            raise ValueError("size는 양수여야 합니다.")
        
        # 부분적으로 정렬된 배열 생성 및 출력
        result = generate_partially_sorted_array(size)
        for x in result:
            print(x,end=" ")
        
    
    except ValueError as e:
        print(f"오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

