# Assignment 2

여러 TSP 근사 알고리즘과 `Held-Karp` 기반 정확해 접근을 비교한 과제다. 2-approximation, Christofides, K-means + Held-Karp 조합을 중심으로 구성되어 있다.

## 핵심 파일

- `2app.py`: MST 기반 2-approximation 실행 스크립트
- `christo3.py`: Christofides 알고리즘 실행 스크립트
- `held_karp.py`: 순수 Held-Karp 정확해 실행 스크립트 겸 공용 모듈
- `clustering_divide_conquer.py`: 클러스터링 기반 분할 정복 TSP 실행 스크립트
- `kmeans_heldkarp.py`: 기존 파일명을 유지하기 위한 호환용 진입점
- `test.sh`: 주요 데이터셋 일괄 실행 스크립트

## 디렉토리 구조

- `datasets/`: 실험 입력 CSV
- `opt/`: 비교용 최적해 또는 참조 투어 파일
- `result/`: 기본 실행 결과 CSV
- `result/legacy_root_runs/`: 과거에 루트에 생성되었던 CSV를 옮겨둔 보관용 결과
- `notebooks/`: 실험 과정에서 사용한 Jupyter Notebook
- `archive/ipynb_checkpoints/`: 체크포인트 보관 디렉토리

## 실행

```bash
cd assignment2
python3 ./2app.py ./datasets/a280.csv
python3 ./christo3.py ./datasets/a280.csv
python3 ./held_karp.py ./datasets/a280.csv
python3 ./clustering_divide_conquer.py ./datasets/a280.csv
```

배치 실행은 아래처럼 가능하다.

```bash
cd assignment2
./test.sh
```

현재 파이썬 스크립트는 기본 출력 파일을 `result/` 아래에 저장하도록 맞춰 두었다. 별도 경로가 필요하면 `-o` 옵션을 사용하면 된다.

## 참고

- 실험용 노트북은 재현 가능성을 위해 `notebooks/`로 분리했다.
- `clustering_divide_conquer.py`는 `held_karp.py`를 import해서 사용한다.
- 제출 보고서는 루트의 [reports/CSE331___Assignment_2.pdf](../reports/CSE331___Assignment_2.pdf)에서 확인할 수 있다.
