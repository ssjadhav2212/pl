library(datasets)

#get data
data("iris")  

#read data
names(iris)   #attribute names
dim(iris)     #rows and col
str(iris)     #details of dataset

min(iris$Sepal.Length)    #gives minimum value. $ acts like dor operator
max(iris$Sepal.Length)    #gives max value. $ acts like dor operator

summary(iris)

#--------------Histogram--------------
hist(iris$Petal.Length)     #pass any column of your choice

#--------------Boxplot----------------
boxplot(iris$Sepal.Length)
boxplot(iris[,-5])    #exclude fifth column


