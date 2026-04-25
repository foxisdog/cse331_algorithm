import sys

def check_csv(file_name):
    try:
        # 파일 읽기
        with open(file_name, 'r') as file:
            lines = file.readlines()
        
        # Statistics 섹션 찾기
        stats_start = None
        for i, line in enumerate(lines):
            if "Statistics:" in line:
                stats_start = i
                break
        
        if stats_start is None:
            return f"Error: Statistics section not found in file {file_name}"
        
        # Statistics 섹션 파싱
        stats_lines = lines[stats_start + 1:]
        stats_dict = {}
        for line in stats_lines:
            if ',' in line:
                key, value = line.strip().split(',')
                stats_dict[key.strip()] = value.strip()
        
        # Average Time 확인
        if "Average Time" in stats_dict and stats_dict["Average Time"] == "0.000 ms":
            return f"Error: Average Time is 0ms in file {file_name}"
        
        # 오류가 없으면 None 반환
        return None
    except Exception as e:
        return f"Error processing file {file_name}: {e}"

if __name__ == "__main__":
    # 명령줄 인자로 파일 이름들 받기
    if len(sys.argv) > 1:
        file_names = sys.argv[1:]  # 첫 번째 인자는 스크립트 이름이므로 제외
        for file_name in file_names:
            result = check_csv(file_name)
            if result:  # 결과가 있을 때만 출력
                print(result)
    else:
        print("Please provide one or more CSV file names as arguments.")
