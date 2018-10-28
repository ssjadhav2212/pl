#include<stdio.h>
#include<time.h>
#include<iostream>

#define w 256
#define h 256

#define N w*h

using namespace std;

__global__ void reduce(int*,int*,int*);

int main(void)
{
	int* hostA = (int*)malloc(N*sizeof(int));
	int* hostB = (int*)malloc(N*sizeof(int));

	int* hostMean = (int*)malloc(sizeof(int));

	*hostMean = 32767;

	int* deviceA; int *deviceB;int*deviceMean;

	cudaMalloc(&deviceA,sizeof(int)*N);
	cudaMalloc(&deviceB,sizeof(int)*N);
	cudaMalloc(&deviceMean,sizeof(int));


	//randomly generate array hostA
	srand(time(0));
	int i;

	//initialize host vector by random elements
	for(i=0;i<N;i++)
	{
		hostA[i] = i;
	}

	hostB[0]=0.0;

	cudaMemcpy(deviceA,hostA,N*sizeof(int),cudaMemcpyHostToDevice);

	cudaMemcpy(deviceB,hostB,N*sizeof(int),cudaMemcpyHostToDevice);

	cudaMemcpy(deviceMean,hostMean,sizeof(int),cudaMemcpyHostToDevice);

	dim3 blocksize(256);
	dim3 gridsize(N/blocksize.x);

	float gpu_elapsed_time;
	cudaEvent_t gpu_start,gpu_stop;

	cudaEventCreate(&gpu_start);
	cudaEventCreate(&gpu_stop);

	cudaEventRecord(gpu_start,0);


	reduce<<<gridsize,blocksize>>>(deviceA,deviceB,deviceMean);

	cudaDeviceSynchronize();

	cudaMemcpy(hostB,deviceB,sizeof(int),cudaMemcpyDeviceToHost);

	cudaEventRecord(gpu_stop, 0);
	cudaEventSynchronize(gpu_stop);
	cudaEventElapsedTime(&gpu_elapsed_time, gpu_start, gpu_stop);
	cudaEventDestroy(gpu_start);
	cudaEventDestroy(gpu_stop);

    
    
	

	double std_dev = pow(hostB[0]/(N),0.5);
	cout<<"Reduced array standard deviation   is = "<<std_dev<<endl;

	std::cout<<"The gpu took: "<<gpu_elapsed_time<<" milli-seconds"<<std::endl;

	



     clock_t cpu_start = clock();

	int sum=0;
	for(int i=0;i<N;i++){
	sum = sum  + int(pow((hostA[i] - (*hostMean)),2.0));
	}

	//cout<<"sum == "<<sum<<endl;

	double std_dev_actual = pow(sum/(N),0.5);

	printf("Actual value of standard deviation should be: %f \n", std_dev_actual);

	clock_t cpu_stop = clock();
	clock_t cpu_elapsed_time = 1000*(cpu_stop - cpu_start)/CLOCKS_PER_SEC;

	

	std::cout<<"The cpu took: "<<cpu_elapsed_time<<" milli-seconds"<<std::endl;



	cudaFree(deviceA);
	cudaFree(deviceB);


	delete[] hostB;
	delete[] hostA;









}


__global__ void reduce(int* input,int* output,int* mean)
{
	__shared__ int shared_data[256];

	int  i = blockIdx.x*blockDim.x+threadIdx.x;

	shared_data[threadIdx.x] = int( pow(double(input[i]- *mean),2.0));

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