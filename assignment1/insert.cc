#include <iostream>
#include <chrono>
#include "sort.h"

using namespace std;

int main() {
    int arr[MAXSIZE];
    int inputsize;
    
    // 입력 시간 제외
    cin >> inputsize;
    for(int i=0; i<inputsize; i++){
        cin >> arr[i];
    }

    // 순수 정렬 시간 측정 시작
    auto start = std::chrono::steady_clock::now();
    insertionsort(arr,inputsize);

    auto end = std::chrono::steady_clock::now();

    // 결과 출력 (모니터 프로그램에서 파싱)
    std::chrono::duration<double, std::milli> elapsed = end - start;
    std::cout << "SORT_TIME:" << elapsed.count() << " ms\n";

    return 0;
}
