#include "sort.h"
#include <random>
#include <algorithm>
#include <iostream>
#include <stdlib.h> 


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
    bool is_swap=1;
    int tmp;
    for(int index=0; is_swap && index <n-1; index++){
        is_swap = 0;

        for(int i=0; i<n-1-index; i++){
            if(arr[i] > arr[i+1]){
                tmp = arr[i];
                arr[i] = arr[i+1];
                arr[i+1]= tmp;
                is_swap = 1;
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
    int tmp;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, n-1);
    int pindex = dist(gen);
    tmp = arr[n-1];
    arr[n-1] = arr[pindex];
    arr[pindex] = tmp;
    // pivot 을 범위내 랜덤하게 선택
    
    int p=arr[n-1];
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

void tournament(int* arr, int n){

    int size=1;
    while( size < n){
        size = size*2;
    } // 2의 거듭제곱 찾아서 트리 꽉채우기

    int cur;
    int left,right;
    int tree[2*size]; //1부터 시작
    for(int i=0; i<n; i++){
        tree[size+i] = arr[i];
    } // 리프노드에 박음
    for(int i=size+n; i<2*size; i++){
        tree[i] = INT32_MAX;
    }

    for(int i=size-1; i>=1; i--){
        tree[i] = tree[2*i] < tree[2*i+1] ? tree[2*i] : tree[2*i + 1];
    } // 1번 토너먼트 진행함

    for(int i=0; i<n; i++){ //n개 뽑으면 끝
        // 하나 뽑고
        cur = 1;
        arr[i] = tree[1];

        // 뽑은 경로를 찾아가서
        while( cur < size){
            left = cur * 2;
            right = cur * 2 + 1;
            if( tree[left] == tree[1] ){
                cur = left;
            }else{
                cur = right;
            }
        }

        // 바꿔주고 그 경로만 토너먼트 진행시키기
        tree[cur] = INT32_MAX;
        
        while( cur != 1 ){
            cur = cur / 2; //위로 한칸 올라가서
            tree[cur] = tree[2*cur] < tree[2*cur+1] ? tree[2*cur] : tree[2*cur + 1];//토너먼트 결과 보기
        }
    }
}

void shaker(int* arr, int n){
    bool is_swap = true;

    // int picked=0;
    int tmp;
    int position = 0;
    int ub=n-1; //오른쪽에 정렬된놈수 -> 상한으로 수정
    int lb=0;  //왼쪽에 정렬된원소수 -> 하한으로 수정
    int last=0; //가장 최근 바꾼 위치 나중에 ub 와 lb 계산할 떄 쓸예정
    while(is_swap){
        is_swap = false;
        //오른쪽으로 밀기 position 0 에있고
        
        // picked = lb+1;
        while( position < ub){
            if( arr[position] > arr[position+1]){
                tmp = arr[position];
                arr[position] = arr[position+1];
                arr[position+1] = tmp; // 바꾸고
                last = position;
                is_swap = true;
            }
            position++;
        }
            // ub 업테이트
        ub = last;

        //왼쪽으로 밀기
        while( position > lb ){
            if( arr[position-1] > arr[position]){
                tmp = arr[position];
                arr[position] = arr[position-1];
                arr[position-1] = tmp;
                last = position;
                is_swap = true;
            }
            position--;
        }
        lb=last;
    }
}

void comb(int* arr, int n){
    float shrink = 1.3;

    bool is_swap = true;
    int gap = n;
    int tmp;

    while(is_swap || gap != 1){
        is_swap = false;

        gap = floor(gap/shrink);
        if(gap < 1){
            gap = 1;
        }
        for(int i=0; i+gap<n; i++){
            if(arr[i] > arr[i+gap]){
                tmp = arr[i];
                arr[i] = arr[i+gap];
                arr[i+gap] = tmp;
                is_swap = true;
            }
        }
    }
}

void intro(int* arr, int n, int max_depth, int threshold, int recur){
    if(n<=1) return;
    if( recur >= max_depth){
        heapsort(arr,n);
        return;
    }
    if( n <= threshold ){
        insertionsort(arr,n);
        return;
    }

    // quick sort
    
    int tmp;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, n-1);
    int pindex = dist(gen);
    tmp = arr[n-1];
    arr[n-1] = arr[pindex];
    arr[pindex] = tmp;
    // pivot 을 범위내 랜덤하게 선택
    
    int p=arr[n-1];
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
    intro(arr, partition, max_depth, threshold, recur+1);
    intro(arr+(partition+1), n - (partition+1), max_depth, threshold, recur+1);

}




void rebalance(int* arr, bool* is_gap, int end){ // 0 부터 end 까지 리밸런싱 해버리기 홀수는 전부 갭, 짝수는 아닐수도
    int p = end;
    while( p >=0){
        if(p%2 == 1){ //홀수는 갭이고고
            is_gap[p] = true;
            p--;
        }else{ //짝수는 진짜 있음
            is_gap[p] = is_gap[p/2];
            arr[p]=arr[p/2];
            p--;
        }
    }
    // printf("Rebalance end, lenth = %d\n", end);
}

int binarysearch(int key, int* arr, int end, bool* is_gap) {
    // printf("bs start \n");
    int ub,lb, mid;
    lb = 0;
    ub = end;
    mid = (lb+ub)/2;
    // std::cout << "lb : " << lb << "\nub : " << ub << "\nmid= "<< mid << "\n\n" << std::endl;

    while(lb<=ub){
        mid = (lb+ub)/2;
        
        // std::cout << "lb : " << lb << "\nub : " << ub << "\nmid= "<< mid << "\n\n" << std::endl;
        // std::cout << "is_gap[" << mid << "] =" << is_gap[mid] << std::endl; 
        if(is_gap[mid]){ //연속된 갭은 없다. mid가 갭일때 왼 오 중 이동해야함
            // std::cout << "mid is at gap" << std::endl;
            if(mid > lb){
                mid--;
            }else if(mid < ub){
                mid++;
            }else{ //lb == mid == ub
                
        // std::cout << "lb : " << lb << "\nub : " << ub << "\nmid= "<< mid << "\n\n" << std::endl;
        // std::cout << "bs done at " << lb << std::endl;
                return lb;
            }
        }

        if(arr[mid] < key){
            lb = mid+1;
        }else{
            ub = mid-1;
        }
        
        // std::cout << "lb : " << lb << "\nub : " << ub << "\nmid= "<< mid << "\n\n" << std::endl;
    }
    // std::cout << "bs done at " << lb << std::endl;
    return lb;
}


void insert(int* arr, bool* is_gap, int insertelem, int position, int end){ //작은걸 왼쪽으로 밀면됌
    // std::cout << "insert start" << std::endl;
    bool direction=true;
    int p=position;
    int prev=insertelem;
    int cur;
    int range=0;

    while(true){ //방향 확인
        if( p+range<=end && is_gap[p+range] ){ //+
            direction = 1;
            break;
        }
        if( p-range >= 0 && is_gap[p-range]){ //-
            direction=0;
            break;
        }
        range++;
    }

    if(direction){ //오른쪽으로 밀면서
        // p++;
        while(!is_gap[p]){
            cur = arr[p];
            arr[p]=prev;
            prev = cur;
            p++;
        }
    }else{ //왼쪽으로 밀면서서
        p--;
        while(!is_gap[p]){
            cur = arr[p];
            arr[p]=prev;
            prev = cur;
            p--;
        }
    }
    //마지막 넣고 끝
    arr[p] = prev;
    is_gap[p]=false;
}


void library(int* arr, int n){
    int* tmp = (int*)malloc(sizeof(int) * 2 * n);
    bool* is_gap = (bool*)malloc(sizeof(bool) * 2* n);
    // int tmp[2*MAXSIZE];
    // bool is_gap[2*MAXSIZE]={true,};

    int jend, jstart, balancedsize;

    tmp[0] = arr[0];
    is_gap[0] = false;

    for(int i=1; i<=floor(log2(n))+1; i++){
        //정렬되어있음
        // rebalance 하고 insert
        balancedsize = (1<<i)-1;
        rebalance(tmp,is_gap, balancedsize); // 2^i 승까지 rebalance
        
        jend= balancedsize < n-1 ? balancedsize : n-1;
        jstart = (1<<(i-1));
        for(int j= jstart; j<=jend; j++){ //jstart 부터 jend 까지 balanced 에 박아
            insert(tmp, is_gap, arr[j], binarysearch(arr[j],tmp,balancedsize, is_gap) , balancedsize);
        }
    }

    //복사
    int copy=0;
    for(int i=0; i<=balancedsize && copy<n; i++){
        if( !is_gap[i] ){
            arr[copy] = tmp[i];
            copy++;
        }
    }

    free(tmp);
    free(is_gap);
}



// void merge(int* arr, int l, int m, int r){
//     int p1=l;
//     int p2=m+1;
//     int p3=l;
//     int sorted[MAXSIZE];

//     while( p1 != m+1 && p2 != r+1){
//         if( arr[p1] > arr[p2] ){
//             sorted[ p3 ] = arr[p2];
//             p2++;
//             p3++;
//         }else{
//             sorted[ p3 ] = arr[p1];
//             p1++;
//             p3++;
//         }
//     }

//     while( p1 != m+1 ){
//         sorted[ p3 ] = arr[p1];
//         p1++;
//         p3++;
//     }
//     while( p2 != r+1 ){
//         sorted[ p3 ] = arr[p2];
//         p2++;
//         p3++;
//     }

//     for(int i=l; i<=r; i++){
//         arr[i] = sorted[i];
//     }
// }



void binaryinsert(int* arr, int start, int end, bool ascending){
    if(start>=end) return;
    int ub = end-1; // 넣고 싶은 원소는 end 에있고 상한은 end -1
    int lb = start;
    int mid=(ub+lb)/2;
    int key = arr[end];

    while(lb<=ub){
        mid=(ub+lb)/2;
        if((ascending && arr[mid]> arr[end] ) || (!ascending && arr[mid]<arr[end])){
            ub = mid -1;
        }else{
            lb=mid+1;
        }
    }
    for (int i = end-1; i>=lb; i--){
        arr[i + 1] = arr[i];
    }
    arr[lb] = key;
}

void  makerun(int* arr, int start, int end){
    int ub, lb;
    bool ascending;
    int prev;
    int cur;
    int tmp;
    if(start>=end) return;
    ascending = arr[start] < arr[start+1];


    for(int i=1; i<=end; i++){
        binaryinsert(arr,start,start+i,ascending);
    }
    if(!ascending){
        for(int i=0; i<(end-start)/2 + 1; i++){
            tmp = arr[end-i];
            arr[end-i] = arr[start+i];
            arr[start+i] = tmp;
        }
    }
}

void timsort(int* arr, int n){
    // https://www.perplexity.ai/search/timsort-seolmyeonghaejweo-1lIP4m6yTbGjWI2Okn1Tig
    //minirun 정하기
    int minirun = 64;

    //run 만들기
    for(int i=0; i<=log2(n); i++){
        int runend = minirun*(i+1)-1 < n-1 ? minirun*(i+1)-1 : n-1;
        makerun(arr, minirun*i,runend);
    }

    //merge
    for(int i=n/minirun; i>=0; i++){
        for(int j=0; j<i; j++){
            merge(arr,j*minirun*i,j*minirun*(i-1),runend);
        }
    }
}