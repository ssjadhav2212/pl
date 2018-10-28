import pandas as pd
import os
import matplotlib.pyplot as plt
import math

path_to_file = 'C:\\Users\\Amruta K\\Downloads\\Iris.csv'
data = pd.read_csv(path_to_file,encoding='utf-8')


'''print('\n\n\nNo of features in Iris flower dataset are : ',len(data.columns)-1,'\n\n\n\n')

print('Types of features are as follows\n')
print(data.dtypes)
'''
print('\nDescribing data as follows \n')
cols = data.columns;

print(len(cols))
full_data = []

for i in range(1,6):
	feature = cols[i]
	Series_feature = ((data[feature]))
	full_data.insert(0,Series_feature)
	mean = 0;
	count = len(Series_feature)
	print('count = ',count)
	type_of_data = type(Series_feature[2])
	#print('type of data = ',type_of_data)
	
	if Series_feature.dtype.name == 'float64' or Series_feature.dtype.name == 'int64':
		print('Attribute type is numerical')

	if type(Series_feature[1]) == type('amruta'):
		print('attribute type is nominal')
	#elif type(Series_feature[2]) == type(1)  or type(Series_feature[2] )== type(1.1):

		
    
	if i!=5:
		for element in Series_feature:
			mean+=element
		print('summation = ',mean)
		print('mean = ',mean/count)
		mean = mean/count

		x_x2_sum=0;
		for element in Series_feature:
			x_x2_sum+=(element - mean)**2
		val = x_x2_sum/(count-1)
		std_dev = math.sqrt(val)
		print('standard deviation = ',std_dev)

		min = 5
		max = -1
		for element in Series_feature:
			if element < min:
				min = element

		print('min = ',min)

		for element in Series_feature:
			if element > max:
				max = element
		print('max = ',max)


		Series_feature = Series_feature.sort_values(ascending=True)

		k = 0.25

		index = k*count
		print('index = ',index)
		if index.is_integer():
			percentile = (Series_feature[index-1]+Series_feature[index])/2
		else:
			index = int(index)
			percentile = Series_feature[index-1]
		print(k,'th percentile is = ',Series_feature.quantile(0.25))

		k = 0.50
		index = k*count
		if index.is_integer():
			percentile = (Series_feature[index-1]+Series_feature[index])/2
		else:
			index = int(index)
			percentile = Series_feature[index-1]
		print(k,'th percentile is = ',Series_feature.quantile(0.50))

		k = 0.75

		index = k*count
		if index.is_integer():
			percentile = (Series_feature[index-1]+Series_feature[index])/2
		else:
			index = int(index)
			percentile = Series_feature[index-1]
		print(k,'th percentile is = ',Series_feature.quantile(0.75))


	
	print('\n\n')

List = []
print('\n\n')



for i in range(1,5):
	feature = cols[i]
	data[feature].plot(kind='hist',bins=150)
	plt.title(feature+' distribution')
	plt.xlabel(feature)
	plt.show()


print('now printing boxplot')

data.plot.box()
#pd.options.display.mpl_style = 'default'

