library(dplyr)
library(tidyr)
library(ggplot2)

setwd("Virus Research/network_visual/")
f <- read.table("./VC_summed_coverage_plot.csv", header=TRUE,sep=",")

p <- ggplot(f,aes(x=1,y=ï..VC)) +
  geom_point(aes(size = Coverage),colour="skyblue3",alpha=0.75)+
  scale_size_continuous(limits=c(0.00001,1389),range = c(1.5,15),breaks=c(1,10,100,1000))

p
