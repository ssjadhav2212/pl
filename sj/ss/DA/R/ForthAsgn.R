

data1 <- read.csv(file.choose())

View(data1)

subset_mydata <- data1[,c(1,5)]

View(subset_mydata)


which.max(subset_mydata$snowfall)

subset_mydata[21,]

# or

subset(subset_mydata, snowfall == max(snowfall))
