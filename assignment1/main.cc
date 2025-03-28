#include <iostream>
#include "sort.h"

using namespace std;

int main(){
    int arr[INPUT_SIZE];
    for(int i=0; i<INPUT_SIZE; i++){
        arr[i] = rand();
    }

    // selectionsort(arr, INPUT_SIZE);

    // insertionsort(arr,INPUT_SIZE);

    // mergesort(arr,0,INPUT_SIZE-1);

    // bubblesort(arr,INPUT_SIZE);

    // heapsort(arr,INPUT_SIZE);
    quicksort(arr,INPUT_SIZE);

    for(int i=0; i<INPUT_SIZE; i++){
        cout << arr[i] << '\n';
    }
    
    return 0;
}