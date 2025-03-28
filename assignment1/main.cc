#include <iostream>
#include "sort.h"
#include <chrono>
#include <sys/resource.h>

using namespace std;

int main(){
    struct rusage usage;
    
    int arr[MAXSIZE];
    int inputsize;
    cin >> inputsize;
    for(int i=0; i<inputsize; i++){
        cin >> arr[i];
    }
    auto start = chrono::high_resolution_clock::now();
    // selectionsort(arr, inputsize);
    // insertionsort(arr,inputsize);
    // mergesort(arr,0,inputsize-1);
    // bubblesort(arr,inputsize);
    // heapsort(arr,inputsize);
    quicksort(arr,inputsize);

    auto end = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &usage);  

    // for(int i=0; i<inputsize; i++){
    //     cout << arr[i] << '\n';
    // }
    auto elapsed = chrono::duration_cast<chrono::milliseconds>(end - start);
    cout << "Time : " << elapsed.count() << " ms" << endl;
    cout << "max mem : " << usage.ru_maxrss << " KB" << endl;

    return 0;
}