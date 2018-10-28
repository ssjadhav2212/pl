#Decision Tree for prediction. Used iris dataset

library(rpart)
library("rpart.plot")

data(iris)

#taking only '100' records out of 150.
s<-sample(150,100)

#split into training and testing dataset
train <- iris[s,]
test <- iris[-s,]

#model for decision tree. using variable, "dtm"
dtm = rpart(Species~., train, method = "class")

#plot decision tree
rpart.plot(dtm)

#addign various parameter.
#rpart.plot(dtm, type=4, extra=101)

p <-predict(dtm, test, type = "class")
table(test[,5], p)


