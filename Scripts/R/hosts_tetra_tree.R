library(reshape2)
library(dplyr)
library(tidyr)
library(cowplot)
library(ggplot2)
library(gplots)


setwd("/home/varadakhot/Documents/Virus_visuals/")
f <- read.delim("./tetra_cosines_hosts_w_taxon.csv", header=TRUE,se="\t")

#create matrix and dendrogram from the list using acast from reshape2
m <- acast(f,Bin1_Taxon ~ Bin2_Taxon,value.var = 'Cosine',fun.aggregate=mean)
m <- replace_na(m,0)
d <- dist(m,method="euclidean")
hclust_avg <- hclust(d,method = "average")
plot(hclust_avg)
#tree <- as.phylo(hclust_avg)
#write.tree(phy=tree, file='./host_tetra_cosine.tree')

#heatmap option
f_filtered <-filter(f,grepl('virus',Bin2_Taxon),!grepl('virus',Bin1_Taxon))
sort1.f_filtered <- f_filtered[order(-f_filtered$Cosine), ]
sort1.f_filtered_matrix <- acast(sort1.f_filtered,Bin1_Taxon ~ Bin2_Taxon,value.var = 'Cosine',fun.aggregate=mean)
colors= c(seq(0,0.8,length=200),seq(0.81,1,length=200))
my_palette <- colorRampPalette(c("#ffffff","#b0adff","#0800ff"))

#print heatmap and save to file as svg
svg(filename = "heatmap_tetra", width=20, height=10)
heatmap.2(sort1.f_filtered_matrix,col=my_palette(399),breaks=colors,density.info="none", trace="none",symm=F,symkey=F,symbreaks=T,scale="none",Colv=TRUE,Rowv=TRUE, dendrogram = "row",margins = c(12,30))
dev.off()
