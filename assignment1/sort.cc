#include "sort.h"

void insertionsort(int* arr, int n){
    int tmp;
    for(int i=1; i<n; i++){
        tmp = arr[i];
        for(int j=i-1; j>=0; j--){
            if( arr[j] < tmp ){
                arr[j+1] = tmp;
            }else{
                arr[j+1] = arr[j];
            }
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
    int sorted[INPUT_SIZE];

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

void heapsort(int* arr, int n){

}

void bubblesort(int* arr, int n){

}

void quicksort(int* arr, int n){

}