#include<iostream>
#include<algorithm>
#include<omp.h>
#include<vector>
#include<time.h>

using namespace std;

vector<int> initialize(vector<int>,int);



int main()
{
    int inc = 2;
    for(int ii=2;ii<=15;ii++){
    int k = 1<<ii;

    vector<int> v;
    v = initialize(v,k);
    int arr[k];
    int x = 0;
    vector<int>::iterator ptr;
    for (ptr = v.begin(); ptr < v.end(); ptr++)
    {
        arr[x]=*ptr;
        x+=1;
    }

    double start_time = omp_get_wtime();
    cout<<"size = "<<x<<endl;
    int i,j;
    for(i=0;i<(x-1);i++)
    {
        int first = i % 2;
        //cout<<"ho"<<endl;
        #pragma omp parallel for default(none),shared(arr,first)
        for(j=0;j<(x-i-1);j+=2)
        {
            //cout<<"hola"<<endl;
            if(arr[j]>arr[j+1])
                {
                    int temp = arr[j];
                    arr[j] = arr[j+1];
                    arr[j+1]=temp;
                }
        }
    }
    double time = omp_get_wtime() - start_time;
    cout<<"time required = "<<time<<endl;

    }



}


vector<int> initialize(vector<int> v,int n)
{
    srand(time(0));
    for(int i=0;i<n;i++)
        v.push_back(rand());


    return v;

}
