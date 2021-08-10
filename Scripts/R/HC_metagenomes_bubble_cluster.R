library(reshape2)
library(ape)
library(phangorn)
library(dplyr)
library(tidyr)
library(cowplot)
library(ggplot2)
library(gplots)
library(dendextend)
library(ggdendro)

setwd("alkanes_hackathon/validation/Metagenomes/normalized_metagenome_hmmsearch_results/")
f <- read.table("./pet_res_enrich_MG_dataset.txt", header=TRUE,sep="\t")

#~~~~~~~~~PLOT 1~~~~~~~~~~~~~~~~~~~~~~~#
rownames(f) <- f$Metagenome

d <- dist(f,method="euclidean")
h <- as.dendrogram(hclust(d,method = "average"))

mg_dendro <- ggdendrogram(data=h,rotate=TRUE)+
  theme(axis.text.y=element_text(size=8,colour = "black"))

mg_dendro

#plot(h)
#dend_2 <- h %>% set("labels_cex",0) %>% set("branches_lwd",0.5) #%>% set("hang_leaves")
#p1 <- ggplot(dend_2, horiz=T)+theme(plot.margin = unit(c(3,1,3,1),"lines"))#+ labs(title = "metagenomes clustered)

#p1

#~~~~~~~~~PLOT 2~~~~~~~~~~~~~~~~~~~~~~~#

f_m <- melt(f,id=c("Metagenome"))
f_m_new <- separate(data=f_m,col=variable,into=c("hmm","oxygen","hc"),sep="\\.")


f_m_new$Metagenome <- factor(f_m_new$Metagenome,levels=labels(h),ordered = TRUE)


p2 <- ggplot(f_m_new,aes(x=hmm,y=Metagenome)) +
  geom_point(aes(size = value, fill = oxygen), alpha = 0.75, shape = 21)+
  facet_grid(. ~ oxygen ,scales = "free",space="free")+
  scale_size_continuous(limits = c(0.00001, 1), range = c(1,10), breaks = c(0,0.25,0.5,0.75,1))+
  labs(title = "Petroleum Res. and Enrichment Metagenomes, norcutoff >=0.8",size="Counts of gene expression",fill="Oxygen Use")  + 
  theme(axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        axis.title=element_blank(),
        axis.text.x=element_text(angle=90,hjust=1,vjust=0.3, colour="black"),
        legend.title = element_text(size = 11), panel.background = element_blank(), 
        panel.border = element_rect(colour = "black", fill = NA, size = 1.2), 
        legend.position = "top", panel.grid.major.y = element_line(colour = "grey95"),panel.grid.major.x = element_line(colour="grey95"))

library(grid)
p2
grid.newpage()
print(p2,vp=viewport(x = 0.4, y = 0.5, width = 0.8, height = 1.0))
print(mg_dendro, vp = viewport(x = 0.90, y = 0.623, width = 0.2, height = 0.54))
