library(reshape2)
library(ape)
library(phangorn)
library(dplyr)
library(tidyr)
library(cowplot)
library(ggplot2)
library(gplots)
library(dendextend)

setwd("../alkanes_hackathon/validation/Metagenomes/normalized_metagenome_hmmsearch_results/")
f <- read.table("./metagenomes_norCutoff_heatmap.tsv", header=TRUE,sep="\t")

rownames(f) <- f$Metagenome
d <- dist(f,method="euclidean")
h <- as.dendrogram(hclust(d,method = "average"))
mg_dendro <- as.ggdend(h)
#plot(h, hang=-1, cex=0.6)
dend_2 <- h %>% set("labels_cex",0.5) %>% set("branches_lwd",0.5) #%>% set("hang_leaves")
p1 <- ggplot(dend_2, horiz=T)+theme(plot.margin = unit(c(3,1,3,1),"lines"))#+ labs(title = "metagenomes clustered)

p1

f$Metagenome <- factor(f$Metagenome,levels=labels(h))




f_m <- melt(f,id=c("Metagenome"))

my_breaks= c(0,0.25,0.5,0.75,1)
my_palette <- c("#fff7df","#bfcfff","#809fff","#0000ff","#002db3")

p2 <- ggplot(f_m,aes(x=variable,y=Metagenome), fill=value)+
  geom_tile(aes(fill=value))+
  theme(axis.text.x.bottom = element_text(angle=90, size=8),
        axis.text.y.left=element_text(size=8))+
  scale_fill_gradientn(colours=my_palette,breaks=my_breaks)


plot_grid(p1,p2,align="h",scale = c(1.055,1),rel_widths = c(1,3.5))
