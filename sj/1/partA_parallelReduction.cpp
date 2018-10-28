#include<iostream>
#include<time.h>
#include<omp.h>
#include<vector>
using namespace std;

vector<int> initialize(vector<int>,int);

int main()
{
    int SIZE = 1<<12;
    int arr[SIZE];

    vector<int> v;
    v = initialize(v,SIZE);
    
    int x = 0;
    vector<int>::iterator ptr;
    for (ptr = v.begin(); ptr < v.end(); ptr++)
    {
        arr[x]=*ptr;
        x+=1;
    }

    double start,end;
    start  =omp_get_wtime();

    cout<<"\n=====Reduction operation name = MAX=====\n";
    int max_val = 0;
    int j;
    #pragma omp parallel for reduction(max:max_val)
    for(j=0;j<SIZE;j++)
    {
        if(arr[j]>max_val)
            max_val=arr[j];
    }

    cout<<"\nMAX value from array is = "<<max_val<<endl;


    cout<<"\n=====Reduction operation name = MIN=====\n";
    int min_val = 100;
    
    #pragma omp parallel for reduction(min:min_val)
    for(j=0;j<SIZE;j++)
    {
        if(arr[j]<min_val)
            min_val=arr[j];
    }

    cout<<"\nMIN value from array is = "<<min_val<<endl;

    cout<<"\n=====Reduction operation name = SUM=====\n";
    int sum = 0;
    #pragma omp  parallel for reduction(+:sum)
    for(int i=0;i<SIZE;i++)
    {
        sum+=arr[i];
    }

    cout<<"\nSUM value from array is = "<<sum<<endl;

    cout<<"\n=====Reduction operation name = AVERAGE=====\n";
     sum = 0;
    #pragma omp  parallel for reduction(+:sum)
    for(int i=0;i<SIZE;i++)
    {
        sum+=arr[i];
    }
    int average = sum/SIZE;

    cout<<"\nAVERAGE value from array is = "<<average<<endl;


    end = omp_get_wtime();

    cout<<"execution time = "<<end-start<<endl;


}

vector<int> initialize(vector<int> v,int n)
{
    srand(time(0));
    for(int i=0;i<n;i++)
        v.push_back(rand());


    return v;

}
