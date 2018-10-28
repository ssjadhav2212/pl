import pandas as pd
import os
import matplotlib.pyplot as plt

path_to_file = 'C:\\Users\\Amruta K\\Downloads\\Iris.csv'
data = pd.read_csv(path_to_file,encoding='utf-8')


'''print('\n\n\nNo of features in Iris flower dataset are : ',len(data.columns)-1,'\n\n\n\n')

print('Types of features are as follows\n')
print(data.dtypes)
'''
print('\nDescribing data as follows \n')
cols = data.columns;

print(len(cols))

for i in range(1,6):
	feature = cols[i]
	Series_feature = ((data[feature]))
	
	print(data[feature].describe())
	print('\n\n')

List = []
print('\n\n')
for i in range(1,5):
	feature = cols[i]
	data[feature].plot(kind='hist',bins=150)
	plt.title(feature+' distribution')
	plt.xlabel(feature)
	plt.show()



	'''dof = data[cols[i]]
				List.append(dof)
			
			colors = ['blue','black','orange','green']
			
			plt.hist(List,colors)
			plt.xlabel("feature")
			plt.ylabel("frequency")
			plt.xticks(range(0, 7))
			plt.yticks(range(1, 20))
			plt.show()'''


'''

'''