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

void merge(int a[], int size, int temp[]) {
   // cout<<"inside merge"<<endl;
	int i1 = 0;
	int i2 = size / 2;
	int it = 0;

	while(i1 < size/2 && i2 < size) {
		if (a[i1] <= a[i2]) {
			temp[it] = a[i1];
			i1 += 1;
		}
		else {
			temp[it] = a[i2];
			i2 += 1;
		}
		it += 1;
	}

	while (i1 < size/2) {
	    temp[it] = a[i1];
	    i1++;
	    it++;
	}
	while (i2 < size) {
	    temp[it] = a[i2];
	    i2++;
	    it++;
	}

	memcpy(a, temp, size*sizeof(int));

}

void mergesort_serial(int a[], int size, int temp[]) {
	int i;
    //cout<<"in serial ms"<<endl;
    //cout<<"sizze = "<<size<<endl;
    //return;
	if (size == 2) {
		if (a[0] <= a[1])
			return;
		else {
			std::swap(a[0], a[1]);
			return;
		}
	}


	else if(size>2){
	mergesort_serial(a, size/2, temp);
	mergesort_serial(a + size/2, size - size/2, temp);
	merge(a, size, temp);
	}
}


void mergesort_parallel_omp(int a[], int size, int temp[], int threads) {
    //cout<<"no of threads = "<<threads<<endl;
    if ( threads == 1) {
        mergesort_serial(a, size, temp);
    }
    else if (threads > 1) {

        #pragma omp parallel sections
        {
            #pragma omp section
            mergesort_parallel_omp(a, size/2, temp, threads/2);
            #pragma omp section
            mergesort_parallel_omp(a + size/2, size-size/2,temp + size/2, threads-threads/2);
        }
        #pragma omp taskwait
        merge(a, size, temp);
        } // threads > 1
}


int main()
{
    double start,stop;
    int size = 1000;

    int no_of_cores;

    #pragma omp parallel
    {
        #pragma omp master
        {
            no_of_cores = omp_get_max_threads();
        }
    }

    cout<<"no of cores = "<<no_of_cores<<endl;
    for(int i=4;i<=13;i++)
    {

        cout<<"size = "<<size<<endl;
        int* arr;
        arr = (int*) malloc(size*4);
        arr = initialize(size,arr);
        int temp[size];
        start = omp_get_wtime();


        mergesort_parallel_omp(arr,size,temp,8);


        stop = omp_get_wtime();

        cout<<"sorting time = "<<stop-start<<endl;
        size*=2;


    }
}

