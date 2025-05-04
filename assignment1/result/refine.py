import pandas as pd
import sys
import os.path
import glob

def process_csv_file(input_file):
    try:
        # 출력 파일명 생성 (파일명_processed.확장자)
        file_name, file_ext = os.path.splitext(input_file)
        output_file = f"{file_name}_processed{file_ext}"
        
        # CSV 파일 불러오기
        print(f'파일 읽는 중: {input_file}')
        data = pd.read_csv(input_file)
        
        # 첫 두 열을 100행까지 추출
        extracted_data = data.iloc[:10, 1:3]
        
        # 추출한 데이터를 새 CSV 파일로 저장
        extracted_data.to_csv(output_file, index=False)
        
        print(f'처리 완료: {output_file} (처음 {len(extracted_data)}행, 첫 2열)')
        return True
        
    except FileNotFoundError:
        print(f'오류: {input_file} 파일을 찾을 수 없습니다.')
        return False
    except Exception as e:
        print(f'파일 {input_file} 처리 중 오류 발생: {e}')
        return False

def main():
    # 명령줄 인자 확인
    if len(sys.argv) < 2:
        print('사용법: python3 program.py 파일.csv [파일2.csv ...]')
        print('       python3 program.py *.csv')
        sys.exit(1)

    # 처리할 파일 목록
    files_to_process = []
    
    # 인자 분석
    for arg in sys.argv[1:]:
        # 와일드카드가 확장되지 않은 경우를 처리
        if '*' in arg:
            matched_files = glob.glob(arg)
            if matched_files:
                files_to_process.extend(matched_files)
            else:
                print(f'경고: {arg}와 일치하는 파일이 없습니다.')
        else:
            files_to_process.append(arg)
    
    if not files_to_process:
        print('처리할 CSV 파일이 없습니다.')
        sys.exit(1)
    
    # 각 파일 처리
    success_count = 0
    for file_path in files_to_process:
        # CSV 파일인지 확인
        if not file_path.lower().endswith('.csv'):
            print(f'건너뜀: {file_path} (CSV 파일이 아님)')
            continue
        
        if process_csv_file(file_path):
            success_count += 1
    
    # 결과 요약
    print(f'\n처리 완료: {success_count}/{len(files_to_process)} 파일 성공적으로 처리됨')

if __name__ == "__main__":
    main()
