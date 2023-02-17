library(ROSE)
require(patchwork)
require(dplyr)
require(magrittr)
require(tidyverse)
library(readr)
library(factoextra)
require(ggplot2)
require(ggalt)
require(ggpubr)
require(cluster)
require(flextable)
require(Rtsne)
library(rgl)
library(umap)
library(plotly)
require(class)
require(e1071)
require(randomForest)
require(caret)
require(rfviz)
require(loon)
library(rstatix)
library(reprtree)
library(reprtree)
require(rattle)
require(rpart.plot)
require(VanillaICE)

source("dsq_functions.R")
rm(data)
#To compare with Unsupervised Machine Learning, I import only the data usable for the 54 item k-means clustering
initial.import <- read.csv("DSQ-1 108 items with NAs removed.csv")
#initial.import <- read.csv("108 dsq items imputed.csv")


data <- read.csv("MECFS VS OTHERS BINARY.csv")

items.list14 <- c(1, 2, 5, 6, 9, 10, 13, 14, 25, 26, 33, 34, 47, 48, 49, 50, 
                  67, 68, 71, 72, 87, 88, 91, 92, 105, 106, 107, 108)

items.list54f <- c(seq(from = 1, to = 107, by = 2))
items.list54s <- c(seq(from = 2, to = 108, by = 2))

items.list14f <- c(1, 5, 9, 13, 25, 33, 47, 49, 67, 71, 87, 91, 105, 107)
items.list14s <- c(2, 6, 10, 14, 26, 34, 48, 50, 68, 72, 88, 92, 106, 108)

items.list4c <- c(1, 2, 9, 10, 13, 14, 47, 48)
items.list4f <- c(1, 9, 13, 47)
items.list4s <- c(2, 10, 14, 48)

#items.listr <- sample(1:ncol(initial.import), 1)

items.top.pem <- c(3, 5, 6, 21)
items.4comp <- c(1, 5, 7, 24, 53)
items.14comp <- c(1, 3, 5, 7, 13, 17, 24, 25, 34, 36, 44, 46, 53, 54)
new.items <- c(53, 7, 22, 51, 49, 20, 36)

#initial.import %<>% filter(1:nrow(initial.import) %in% (1:nrow(data)))


data <- read.csv('DSQ 1 Composite MECFS and Controls.csv')
dx <- data$dx %>% as.factor()
data <- subset(data, select = -`dx`)
data <- subset(data, select = c(new.items))
data <- cbind(dx, data)
#data <- data %>% relocate(dx, .before = data$nausea47f)

#write.csv(data, file = "MECFS CONTROLS 1.17.23 COMP.csv", row.names = FALSE)

#data <- subset(data, select = -dx)

data.balanced.over <- ovun.sample(dx~., data = data, method = "over", N = 4624)
data.balanced.over <- data.balanced.over$data
table(data.balanced.over$dx)
data <- data.balanced.over

#set.seed(222)
ind <- sample(2, nrow(data), replace = TRUE, prob = c(0.7, 0.3))
train <- data[ind==1,]
test <- data[ind == 2,]

data <- train

#### Random Forest ####





rf.model <- randomForest(dx~., data = data, mtry = 3, ntree=1000)
print(rf.model)



#### prediction and confusion matrix ####

p1 <- predict(rf.model, data) 
confusionMatrix(p1, data$dx)

p2 <- predict(rf.model, test)
confusionMatrix(p2, test$dx)


# Variable Importance Plot:

data_x <- data[, 2:ncol(data)]
data_y <- data$dx

rfpref <- rf_prep(data_x, data_y)
varImpPlot(rfpref$rf, main="90% Acc. Ranked variables - ME/CFS vs all, 14 items")

