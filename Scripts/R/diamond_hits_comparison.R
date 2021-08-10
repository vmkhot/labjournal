setwd("./alkanes_hackathon/validation/")
library(dplyr)
library(tidyr)
library(ggplot2)

f <- read.csv("NorCutOff_hmmsearch_diamond_test_tmoB_alkanes_0.1.out", header=TRUE, sep='\t')

box <- ggplot(f, aes(x=HMM,y=Normalized_Domain_Score,fill=HMM)) + geom_boxplot()+ geom_jitter(alpha=0.1,aes(fill=HMM))+
  theme(axis.text.x.bottom = element_text(angle=90,vjust=0.5))+
  scale_fill_manual(values = c("darkorange", "darkorange4","darkorange","slateblue","slateblue3","deeppink4","deeppink","seagreen","seagreen","seagreen","seagreen1"))

box

scatter <- ggplot(f, aes(x=HMM,y=Domain_Score,fill=HMM)) + geom_point(position="dodge",alpha=0.5)+
  theme(axis.text.x.bottom = element_text(angle=90,vjust=0.5))+
  scale_fill_manual(values = c("darkorange", "darkorange4","darkorange","slateblue","slateblue3","deeppink2","deeppink2","seagreen","tomato2","tomato2","tomato2","tomato2",), guide = guide_legend(override.aes = list(size=5)))

scatter

