# Naive Bayes

# Importing the dataset
dataset = read.csv('H:\FINAL LP1\DA\R\diabetes.csv')
dataset = dataset[,c(6,8,9)]

# Encoding the target feature as factor
dataset$Outcome = factor(dataset$Outcome, levels = c(0, 1))


#---------------Splitting the dataset-------------------
# install.packages('caTools')
library(caTools)

set.seed(123)
split = sample.split(dataset$Outcome, SplitRatio = 0.75)
train = subset(dataset, split == TRUE)
test = subset(dataset, split == FALSE)

# Feature Scaling
train[-3] = scale(train[-3])
test[-3] = scale(test[-3])

# Fitting SVM to the Training set
# install.packages('e1071')
library(e1071)
classifier = naiveBayes(x = train[-3],
                        y = train$Outcome)

# Predicting the Test set results
y_pred = predict(classifier, newdata = test[-3])

# Making the Confusion Matrix
confusionMatrix = table(test[, 3], y_pred)

#display confusion matrix
confusionMatrix
