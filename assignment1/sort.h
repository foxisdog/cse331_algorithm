#ifndef SORT_H
#define SORT_H

#include <random>
#define MAXSIZE 1000000

void insertionsort(int* arr, int n);
void selectionsort(int* arr, int n);
void mergesort(int* arr, int left, int right);
void heapsort(int* arr, int n);
void bubblesort(int* arr, int n);
void quicksort(int* arr, int n, std::mt19937 gen);
void tournament(int* arr, int n);
void shaker(int* arr, int n);
void comb(int* arr, int n);
void intro(int* arr, int n, int max_depth, int threshold, int recur,std::mt19937 gen);
void library(int* arr, int n);
void timsort(int* arr, int n);
#endif
