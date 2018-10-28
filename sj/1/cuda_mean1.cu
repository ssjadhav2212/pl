#include<stdio.h>
#include<time.h>
#include<iostream>
#define w 256
#define h 256

#define N w*h

using namespace std;

__global__ void reduce(int*,int*);

int main(void)
{
	int* hostA = (int*)malloc(N*sizeof(int));
	int* hostB = (int*)malloc(N*sizeof(int));

	int* deviceA,*deviceB;

	cudaMalloc(&deviceA,sizeof(int)*N);
	cudaMalloc(&deviceB,sizeof(int)*N);


	//randomly generate array hostA
	srand(time(0));
	int i;

	//initialize host vector by random elements
	for(i=0;i<N;i++)
	{
		hostA[i] = i;
	}

	hostB[0]=0;

	cudaMemcpy(deviceA,hostA,N*sizeof(int),cudaMemcpyHostToDevice);

	cudaMemcpy(deviceB,hostB,N*sizeof(int),cudaMemcpyHostToDevice);

	dim3 blocksize(256);
	dim3 gridsize(N/blocksize.x);

	reduce<<<gridsize,blocksize>>>(deviceA,deviceB);

	cudaDeviceSynchronize();

	cudaMemcpy(hostB,deviceB,sizeof(int),cudaMemcpyDeviceToHost);

	int mean = hostB[0]/(N);
	cout<<"Reduced array mean  is = "<<mean<<endl;

	printf("Actual value of mean should be: %d \n", (N-1)/2);


	cudaFree(deviceA);
	cudaFree(deviceB);


	delete[] hostB;
	delete[] hostA;









}


__global__ void reduce(int* input,int* output)
{
	__shared__ int shared_data[256];

	int  i = blockIdx.x*blockDim.x+threadIdx.x;

	shared_data[threadIdx.x]=input[i];

	__syncthreads();

	for(int s=1;s<blockDim.x;s*=2)
	{
		int index = 2 * s * threadIdx.x;;

        if (index < blockDim.x)
        {
            shared_data[index] += shared_data[index + s];
        }
        __syncthreads();
	}

	if (threadIdx.x == 0)
        atomicAdd(output,shared_data[0]);
}