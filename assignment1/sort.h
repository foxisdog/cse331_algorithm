#ifndef SORT_H
#define SORT_H

#define MAXSIZE 1000000

void insertionsort(int* arr, int n);
void selectionsort(int* arr, int n);
void mergesort(int* arr, int left, int right);
void heapsort(int* arr, int n);
void bubblesort(int* arr, int n);
void quicksort(int* arr, int n);
void tournament(int* arr, int n);
void shaker(int* arr, int n);
void comb(int* arr, int n);
void intro(int* arr, int n, int max_depth, int threshold, int recur);
void library(int* arr, int n);
#endif
