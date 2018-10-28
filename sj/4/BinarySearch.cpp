#include<iostream>
#include<vector>
#include<omp.h>
#include<time.h>
#include <algorithm>
#define SIZE 1<<5

using namespace std;

vector<int> initialize(vector<int>,int);
void serial_binary_search(int*,int low,int high,int to_search,bool found);
void parallel_binary_search(int*,int low,int high,int to_search,int);




int main()
{
    vector<int> v;
    int no_of_cores=8;

    //initializing large array with random numbers
    v = initialize(v,SIZE);
    vector<int>::iterator ip;

   // for binary search array should be sorted so call sort
    sort(v.begin(),v.end());


    /*for(ip= v.begin();ip!=v.end();ip++)

    {
        cout<<*ip<<"\t";
    }*/

    //getting no of cores
          #pragma omp parallel
          {
              #pragma omp master
              {
                  no_of_cores = omp_get_num_threads();



              }
          }

        int* arr = &v[0];

        double start_time = omp_get_wtime();
        parallel_binary_search(arr,0,v.size()-1,arr[4],no_of_cores);
        double time = omp_get_wtime() - start_time;
        cout<<"time required = "<<time<<endl;






}



vector<int> initialize(vector<int> v,int n)
{
    srand(time(0));
    for(int i=0;i<SIZE;i++)
        v.push_back(rand());
    vector<int>::iterator ip;
    ip = std::unique(v.begin(), v.begin() + n);
    v.resize(std::distance(v.begin(), ip));

    return v;

}



void serial_binary_search(int* arr,int low,int high,int to_search,bool found)
{
    if(!found && low<high){
     //cout<<"low = "<<low<<" and high = "<<high<<endl;
    int mid = (low+high)/2;
    if(arr[mid] == to_search)
    {
        found = true;
        cout<<"element found at index = "<<mid<<endl;
        cout<<"element at index mid = "<<arr[mid]<<endl;
        return;
    }
    else if(arr[mid]>to_search)
    {
        serial_binary_search(arr,low,mid,to_search,found);
    }
    else if(arr[mid]<to_search)
    {
        serial_binary_search(arr,mid+1,high,to_search,found);
    }


    }

}


void parallel_binary_search(int* arr,int low,int high,int to_search,int threadCount)
{        bool found = false;
        if(threadCount<=1){
            //call to serial merge sort

            serial_binary_search(arr,low,high,to_search,found);
        }

        else{
            #pragma omp parallel sections shared(found)
            {


                #pragma omp section
                parallel_binary_search(arr,low,(low+high)/2,to_search,threadCount/2);
                #pragma omp section
                parallel_binary_search(arr,(low+high)/2+1,high,to_search,threadCount/2);

            }

        }
}
