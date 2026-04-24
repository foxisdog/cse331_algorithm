# Assignment 1

정렬 알고리즘을 직접 구현하고 입력 분포별 성능을 비교한 과제다. 기본 정렬들에 더해 `Timsort` 구현이 포함되어 있다는 점이 이 디렉토리의 특징이다.

## 핵심 파일

- `Makefile`: 정렬 실행 파일과 `monitor`를 빌드한다.
- `sort.cc`, `sort.h`: 공통 정렬 유틸리티
- `quick.cc`, `insert.cc`, `merge.cc`, `bubble.cc`, `heap.cc`, `select.cc`, `tournament.cc`, `shaker.cc`, `comb.cc`, `intro.cc`, `library.cc`, `tim.cc`: 알고리즘별 구현
- `monitor.cc`: 실행 결과 측정용 도구

## 디렉토리 구조

- `docs/`: 메모와 초안 문서
- `testfiles/`: 기본 입력 데이터
- `testfilesfast/`: 더 촘촘한 부분정렬 입력 데이터
- `result/`: 알고리즘별 원시 결과 CSV
- `results_processed/`: 후처리된 결과 CSV

## 실행

```bash
cd assignment1
make
./test.sh
```

개별 테스트 스크립트도 그대로 유지했다.

- `testbubble.sh`
- `testinsert.sh`
- `testlibrary.sh`
- `testselect.sh`
- `testshaker.sh`
- `testfast.sh`

## 참고

- 대량 실험 결과 파일이 많아서, 결과 분석은 `result/`와 `results_processed/`를 기준으로 보는 편이 낫다.
- 제출 보고서는 루트의 [reports/CSE331___Assignment_1.pdf](../reports/CSE331___Assignment_1.pdf)에서 확인할 수 있다.
