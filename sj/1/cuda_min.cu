#include<math.h>
#include<time.h>
#include<stdexcept>
#include<iostream>
#include<cstdlib> //for abs(x)
#include<stdio.h>
#include<math.h>


using namespace std;

__global__ void findMin(int* A,int* current_min,int* mutex,unsigned int n);



int main()
{
	const int NUMBER_OF_ELEMENTS = 1024*1024*20;

	int* hostA = (int*)malloc(NUMBER_OF_ELEMENTS*sizeof(int));

	int* hostMin = (int*)malloc(sizeof(int));

	*hostMin = 1230000;

	srand(time(0));
	int i;

	//initialize host vector by random elements
	for(i=0;i<NUMBER_OF_ELEMENTS;i++)
	{
		int temp = rand() % 1230000;
		if(temp<0){
		temp*=-1;
		temp = temp% 1230000;
		}
		else if(temp==0)
				temp=34;
		hostA[i] = temp;
		
	}
	int* deviceA,*deviceMin,*deviceMutex;

	cudaMalloc(&deviceA,NUMBER_OF_ELEMENTS*sizeof(int));
	cudaMalloc(&deviceMin,sizeof(int));
	cudaMalloc(&deviceMutex,sizeof(int));

	cudaMemcpy(deviceMin,hostMin,sizeof(int),cudaMemcpyHostToDevice);
	cudaMemset(deviceMutex,0,sizeof(int));

	cudaMemcpy(deviceA,hostA,NUMBER_OF_ELEMENTS*sizeof(int),cudaMemcpyHostToDevice);

	//set up timing variables

	float gpu_elapsed_time;
	cudaEvent_t gpu_start,gpu_stop;

	cudaEventCreate(&gpu_start);
	cudaEventCreate(&gpu_stop);

	cudaEventRecord(gpu_start,0);


	findMin<<<256,256>>>(deviceA,deviceMin,deviceMutex,NUMBER_OF_ELEMENTS);

	cudaDeviceSynchronize();

	cudaMemcpy(hostMin,deviceMin,sizeof(int),cudaMemcpyDeviceToHost);
	cudaEventRecord(gpu_stop, 0);
	cudaEventSynchronize(gpu_stop);
	cudaEventElapsedTime(&gpu_elapsed_time, gpu_start, gpu_stop);
	cudaEventDestroy(gpu_start);
	cudaEventDestroy(gpu_stop);

	cout<<"Answer by CUDA for MIN is = "<<*hostMin<<endl;
	std::cout<<"The gpu took: "<<gpu_elapsed_time<<" milli-seconds"<<std::endl;

	






	clock_t cpu_start = clock();

	int minn = 1230000;

	for(int i=0;i<NUMBER_OF_ELEMENTS;i++)
	{
	if(hostA[i]<minn)
	    minn = hostA[i];
	}

	clock_t cpu_stop = clock();
	clock_t cpu_elapsed_time = 1000*(cpu_stop - cpu_start)/CLOCKS_PER_SEC;

	cout<<"Expected min value is = "<<minn<<endl;

	std::cout<<"The cpu took: "<<cpu_elapsed_time<<" milli-seconds"<<std::endl;


	cudaFree(deviceA);

	delete[] hostA;

	return cudaDeviceSynchronize();
    	




    

    	



}
__global__ void findMin(int* A,int* current_min,int* mutex,unsigned int n)
{
		//printf("threadIdx.x = %d and blockIdx = %d and gridDim.x = %d\n",threadIdx.x,blockIdx.x,gridDim.x);

		unsigned int index = threadIdx.x + blockIdx.x*blockDim.x;
		unsigned int stride = gridDim.x*blockDim.x;

		unsigned int offset = 0;

		__shared__ int cache[256];

		int temp = 1230000;
		while(index+offset<n)
		{
		//printf("A[i] = %d and current temp = %d\n",A[index+offset],temp);
		temp = fminf(temp,A[index+offset]);
		//printf("temp == %d\n",temp);
		offset+=stride;
		}

		cache[threadIdx.x]=temp;

		__syncthreads();


		//reduction
		//printf("blockDim.x = %d\n",blockDim.x/2);
		unsigned int i=blockDim.x/2;
		while(i!=0)
		{
		if(threadIdx.x<i)
		{
		cache[threadIdx.x] = fminf(cache[threadIdx.x],cache[threadIdx.x+i]);

		}
		__syncthreads();
		i/=2;
		}

		if(threadIdx.x == 0)
		while(atomicCAS(mutex,0,1)!=0);
		//printf("current_min before = %d\n",*current_min);
		*current_min = fminf(*current_min,cache[0]);
		//printf("current_min = %d\n",*current_min);
		atomicExch(mutex,0);


}


