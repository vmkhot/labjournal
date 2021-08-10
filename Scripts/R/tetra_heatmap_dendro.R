library(reshape2)
library(ape)
library(phangorn)
library(dplyr)
library(tidyr)
library(cowplot)
library(ggplot2)
library(gplots)
library(dendextend)

setwd("/home/varadakhot/Documents/Virus_visuals/")
f <- read.delim("./tetra_cosines_hosts_w_taxon.csv", header=TRUE,se="\t")

#filter and dendrogram of just the bins_dataset
f_bins <-filter(f,!grepl('virus',Bin1_Taxon),!grepl('virus',Bin2_Taxon))
f_bins_mat <- acast(f_bins,Bin1 ~ Bin2,value.var = 'Cosine',fun.aggregate=mean)
f_bins_mat <- replace_na(f_bins_mat,0)
d <- dist(f_bins_mat,method="euclidean")
h <- as.dendrogram(hclust(d,method = "average"))
bins_dendro <- as.ggdend(h)
plot(h)

#filtered data for heatmap
f_unique <- filter(f,!grepl('virus',Bin1_Taxon),grepl('virus',Bin2_Taxon))
keeps <- c("Bin1_Taxon","Bin2_Taxon","Cosine")
f_unique <- f_unique[keeps]
bins_factor <- factor(bins_dendro$labels$label)

#heatmap of filtered data for virus v. bins
f_unique$Bin1_Taxon <- factor(f_unique$Bin1_Taxon,levels =bins_factor )

my_breaks= c(0.8,1)
my_palette <- c("#ffffff","#d8d6ff","#0800ff")


ggplot(data=f_unique,aes(x=Bin2_Taxon,y=Bin1_Taxon),fill=Cosine) + geom_tile(aes(fill=Cosine))+theme(axis.text.x.bottom = element_text(angle=90, size=12)) + scale_fill_gradientn(colours=my_palette,breaks=my_breaks)
plot(p1)


