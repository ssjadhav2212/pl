#reading csv file
pima.indians.diabetes <- read.csv("~/BE/DA/Assign2/pima-indians-diabetes.csv", header=FALSE, comment.char="#")
library(e1071)
library(caTools)

#converted last column from num to factor
pima.indians.diabetes$V9 <- as.factor(pima.indians.diabetes$V9)
levels(pima.indians.diabetes$V9) <- c("No","Yes")

#splitting data into training and test data set
sample1 = sample.split(pima.indians.diabetes,SplitRatio = 0.7)
train = subset(pima.indians.diabetes,sample1==TRUE)
test = subset(pima.indians.diabetes,sample1==FALSE)
train
test
#summarry of train data set
summary(train)
model = naiveBayes(train[,1:8],train[,9])
model
table(predict(model,test[,1:8]),test[,9])
zz <- merge(test[,],predict(model,test[,1:8]))
zz