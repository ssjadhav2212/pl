#include<iostream>
#include<omp.h>
#include<time.h>
#include <stdio.h>
#include <string.h>
#include<malloc.h>
#include <stdlib.h>
using namespace std;

int* initialize(int size,int* arr)
{
    srand(time(0));
    for(int i=0;i<size;i++)
        arr[i]=rand();


    return arr;
}

void merge(int* X,int n,int* tmp)
{
    int i = 0;
   int j = n/2;
   int ti = 0;

   while (i<n/2 && j<n) {
      if (X[i] < X[j]) {
         tmp[ti] = X[i];
         ti++; i++;
      } else {
         tmp[ti] = X[j];
         ti++; j++;
      }
   }
   while (i<n/2) { /* finish up lower half */
      tmp[ti] = X[i];
      ti++; i++;
   }
      while (j<n) { /* finish up upper half */
         tmp[ti] = X[j];
         ti++; j++;
   }
   memcpy(X, tmp, n*sizeof(int));

}



void mergesort(int* X,int n,int* temp)
{
    if(n<2)
        return;
    mergesort(X,n/2,temp);
    mergesort(X+(n/2),n-(n/2),temp);

    merge(X,n,temp);
}



int main()
{
    double start,stop;
    int size = 1000;
    for(int i=4;i<=13;i++)
    {

        cout<<"size = "<<size<<endl;
        int* arr;
        arr = (int*) malloc(size*4);
        arr = initialize(size,arr);
        int temp[size];
        start = omp_get_wtime();
        mergesort(arr,size,temp);
        stop = omp_get_wtime();

        cout<<"sorting time = "<<stop-start<<endl;
        size*=2;


    }
}

