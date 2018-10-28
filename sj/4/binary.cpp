#include<cstdio>
#include<mpi.h>
#include<iostream>
#include<chrono>

using namespace std::chrono;
using namespace std;


int n=8000;

int key=4500;



void binary_search(int a[],int start,int end,int key)
{

	

	while(start<=end)
	{

		int m=(start+end)/2;

		if(a[m]==key)
		{

			cout<<"Found"<<endl;
			return;


		}
		else if(a[m]<key)
		{
			start=m+1;
		}
		else
		{
			end=m-1;
		}

	}

	
	cout<<"Not found"<<endl;


}




int main(int argc,char **argv)
{

	cout<<"Hello welcome to MPI World"<<endl;
	int a[n];

	for(int i=0;i<n;i++)
	{

	a[i]=i+1;


	}
	
	
	int rank,size;

	MPI_Init(&argc,&argv);


	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&size);
	
	
		

	float start1[4] = {0, 0, 0, 0}, end1[4] = {0, 0, 0, 0};
	float g_start[4] = {0, 0, 0, 0}, g_end[4] = {0, 0, 0, 0};

	int blocksize=n/4;


	MPI_Barrier(MPI_COMM_WORLD);

	start1[rank] = MPI_Wtime();

	
	if(rank==0)
	{
		
		binary_search(a,rank*blocksize,(rank+1)*blocksize-1,key);

	}

	else if(rank>=1)
	{

		
		binary_search(a,rank*blocksize,(rank+1)*blocksize-1,key);		

	}

	MPI_Barrier(MPI_COMM_WORLD);
	end1[rank] = MPI_Wtime();

	
	printf("%d, %f\n", rank, start1[rank]);

	MPI_Reduce(start1, g_start, 4, MPI_FLOAT, MPI_MIN, 0, MPI_COMM_WORLD);
	MPI_Reduce(end1, g_end, 4, MPI_FLOAT, MPI_MAX, 0, MPI_COMM_WORLD);

	MPI_Finalize();

	if(!rank) {
		
		printf("%f, %f, %f, %f, %f, %f, %f, %f\n", g_start[0], g_start[1], g_start[2], g_start[3], g_end[0], g_end[1], g_end[2], g_end[3]);
		printf("Time: %f\n", g_end[0]-g_start[0]);

	}



}
