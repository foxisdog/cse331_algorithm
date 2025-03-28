import filecmp
import sys

def compare_files(file1, file2):
    # 파일 비교
    if filecmp.cmp(file1, file2, shallow=False):
        print("두 파일의 내용이 동일합니다.")
    else:
        print("두 파일의 내용이 다릅니다.")

    # 차이점 출력 (선택사항)
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    for i, (line1, line2) in enumerate(zip(lines1, lines2), 1):
        if line1 != line2:
            print(f"라인 {i}에서 차이가 발견되었습니다:")
            print(f"파일1: {line1.strip()}")
            print(f"파일2: {line2.strip()}")
            print()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python compare_files.py <파일1> <파일2>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    compare_files(file1, file2)
