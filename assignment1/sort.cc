#include "sort.h"

void insertionsort(int* arr, int n){
    int tmp;
    for(int i=1; i<n; i++){
        tmp = arr[i];
        for(int j=i-1; j>=0; j--){
            if( arr[j] > tmp ){
                arr[j+1] = arr[j];
            }else{
                arr[j+1] = tmp;
                break;
            }
        }
        if(arr[0]>tmp){
            arr[0] = tmp;
        }
    }
}

void selectionsort(int* arr, int n){
    int tmp; // 현재 값을 기억하기 위함
    int minval; // 최소값
    int p;  //최소값을 가진 index

    for(int i=0; i<n-1; i++){
        tmp = arr[i]; // 현재 위치 기억
        minval = arr[i];
        p=i;
        // arr[i] = max( 나머지 arr)
        for(int j=i+1; j<n; j++){
            if( minval > arr[j] ){
                minval = arr[j];
                p = j;
            }
        }

        if( minval != tmp ){
            arr[i] = minval;
            arr[p] = tmp;
        }
    }
}

void merge(int* arr, int l, int m, int r){
    int p1=l;
    int p2=m+1;
    int p3=l;
    int sorted[MAXSIZE];

    while( p1 != m+1 && p2 != r+1){
        if( arr[p1] > arr[p2] ){
            sorted[ p3 ] = arr[p2];
            p2++;
            p3++;
        }else{
            sorted[ p3 ] = arr[p1];
            p1++;
            p3++;
        }
    }

    while( p1 != m+1 ){
        sorted[ p3 ] = arr[p1];
        p1++;
        p3++;
    }
    while( p2 != r+1 ){
        sorted[ p3 ] = arr[p2];
        p2++;
        p3++;
    }

    for(int i=l; i<=r; i++){
        arr[i] = sorted[i];
    }
}

void mergesort(int* arr, int l, int r){
    if(l>=r) return;
    int m = (l+r)/2;
    mergesort(arr, l, m);
    mergesort(arr, m+1, r);
    merge(arr, l, m, r);
}

void bubblesort(int* arr, int n){
    bool cond=1;
    int tmp;
    while(cond){
        cond = 0;
        for(int i=0; i<n-1; i++){
            if(arr[i] > arr[i+1]){
                tmp = arr[i];
                arr[i] = arr[i+1];
                arr[i+1]= tmp;
                cond = 1;
            }
        }
    }
}

void heapify(int* heap, int max_index, int current){
    int left;
    int right;
    int cur = current;
    int tmp;

    while ( 2*cur <= max_index){ // 자식노드가 존재하는가?
        if( 2*cur +1 <= max_index){ //오른쪽도 있나요?
            left = 2 * cur;
            right = 2 * cur + 1;
            if( heap[left] < heap[right]){// 왼쪽이 더작음
                if(heap[left] < heap[cur]){
                    tmp = heap[left];
                    heap[left] = heap[cur];
                    heap[cur] = tmp;
                    cur = left;
                }else{
                    break;
                }
            }else{//오른쪽이 더작음
                if(heap[right] < heap[cur]){
                    tmp = heap[right];
                    heap[right] = heap[cur];
                    heap[cur] =tmp;
                    cur =right;
                }else{
                    break;
                }
            }
            
        }else{
            left = 2 * cur;
            if( heap[left] < heap[cur] ){
                tmp = heap[cur];
                heap[cur] = heap[left];
                heap[left] = tmp;
                cur = left;
            }else{
                break;
            }
        }
    }
}

void heapsort(int* arr, int n){
    int* heap = arr - 1; // min heap
    for(int i= n/2; i>=1; i--){
        heapify(heap, n, i);
    }
    // build heap done
    int sorted[MAXSIZE];

    int i=n; // 가지고 있는 원소 개수 i
    while( i >= 1){
        sorted[n-i] = heap[1];
        heap[1] = heap[i];
        i--;
        heapify(heap,i,1);
    }

    for(int i=0; i<n; i++){
        arr[i] = sorted[i];
    }
}

void quicksort(int* arr, int n){
    if(n<=1) return;
    int p=arr[n-1];
    int tmp;
    int partition=0;
    for(int i=0; i<n-1; i++){
        if(arr[i] < p){
            tmp = arr[partition];
            arr[partition] = arr[i];
            arr[i] = tmp;
            partition++;
        }
    }
    arr[n-1] = arr[partition];
    arr[partition] = p;
    quicksort(arr, partition);
    quicksort(arr+(partition+1), n - (partition+1));
}