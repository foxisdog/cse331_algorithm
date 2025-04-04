#include <iostream>
#include <chrono>
#include "sort.h"

using namespace std;
// ulimit -s unlimited
int main() {
    int arr[MAXSIZE];
    int inputsize;
    
    // 입력 시간 제외
    cin >> inputsize;
    for(int i=0; i<inputsize; i++){
        cin >> arr[i];
    }

    // 순수 정렬 시간 측정 시작
    auto start = std::chrono::high_resolution_clock::now();
    timsort(arr, inputsize);
    auto end = std::chrono::high_resolution_clock::now();

    // 결과 출력 (모니터 프로그램에서 파싱)
    std::chrono::duration<double, std::milli> elapsed = end - start;
    std::cout << "SORT_TIME:" << elapsed.count() << " ms\n";

    // for(int i=0; i<inputsize; i++){
    //     std::cout << arr[i] <<'\n';
    // }

    return 0;
}