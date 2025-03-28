#ifndef SORT_H
#define SORT_H

#define INPUT_SIZE 1000

void insertionsort(int* arr, int n);
void selectionsort(int* arr, int n);
void merge(int* arr, int left, int mid, int right);
void mergesort(int* arr, int left, int right);
void heapsort(int* arr, int n);
void bubblesort(int* arr, int n);
void quicksort(int* arr, int n);

#endif
