#include<iostream>
#include<vector>
#include<omp.h>
#include<time.h>
#include <algorithm>
#define SIZE 1<<5

using namespace std;

vector<int> initialize(vector<int>,int);
void serial_binary_search(int*,int low,int high,int to_search);


int main()
{
    vector<int> v;
     v = initialize(v,SIZE);
    vector<int>::iterator ip;

   // for binary search array should be sorted so call sort
    sort(v.begin(),v.end());

    int* arr = &v[0];

        double start_time = omp_get_wtime();
        serial_binary_search(arr,0,v.size()-1,arr[4]);
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



void serial_binary_search(int* arr,int low,int high,int to_search)
{
    if(low<high){
     //cout<<"low = "<<low<<" and high = "<<high<<endl;
    int mid = (low+high)/2;
    if(arr[mid] == to_search)
    {

        cout<<"element found at index = "<<mid<<endl;
        cout<<"element at index mid = "<<arr[mid]<<endl;
        return;
    }
    else if(arr[mid]>to_search)
    {
        serial_binary_search(arr,low,mid,to_search);
    }
    else if(arr[mid]<to_search)
    {
        serial_binary_search(arr,mid+1,high,to_search);
    }


    }

}

