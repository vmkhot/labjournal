setwd("Virus Research/ForUSB/R_Practice")
contigs <- read.table("./virus_bins_abundances.txt", sep="\t", header=TRUE)
contigs_labels <- contigs$Contig.id #factor contig labels into a list and delet from dataframe
contigs$Contig.id <- NULL
rownames(contigs) <- contigs_labels # add rownames to data.frame from labels list

#at this point dataframe should only have values to create dist matrix
library(vegan)
library(ggplot2)
library(dplyr)
library(tidyr)
library(dendextend)

dist_mat <- vegdist(contigs,method = "bray")
hclust_avg <- hclust(dist_mat,method = "average")
plot(hclust_avg)
# ggsave("dendro_viral_hits.svg")
dend <- as.dendrogram(hclust_avg)
dend_2 <- dend %>% set("labels_cex",0.5) %>% set("branches_lwd",0.5) %>% set("hang_leaves")

contigs$Contig.id= contigs_labels #add contig labels back
contigs$Contig.id <- factor(contigs$Contig.id,levels=labels(dend))
C <- gather(contigs,key="samples",value = "values", -Contig.id)

p1 <- ggplot(dend_2, horiz=T)+theme(plot.margin = unit(c(3,1,3,1),"lines"))+ labs(title = "bray-curtis dissimilarity")
 plot(p1)
# ggsave(file="dendro_viral_hits.svg",width=20,height=10*1.25)

p2 <-ggplot(C,aes(y=C$values,x=C$Contig.id,fill=factor(C$samples))) +
  geom_bar(stat="identity")+ coord_flip()+
  theme(axis.text.y=element_blank(),axis.title.y = element_blank(),plot.title=element_text(hjust=0.5, size=11),legend.text=element_text(size=12),legend.title=element_text(size=12))+
  scale_fill_discrete(name="Samples", breaks=c("C_8_6_Ammonium", "T1_8_6_Nitrate", "T10_10_3_Urea","T2_10_3_Nitrate"),labels=c("Ammonium","8_Nitrate","Urea","10_Nitrate"))+
  ylab("Normalized Coverage") +
  labs(title="Viral Contig Coverage")+
  ylim(0,7.5)
plot(p2)
# ggsave(file="abundances.svg",dpi=600,width=5,height=5*2.5)
library(cowplot)

plot_grid(p1,p2,align="h",scale = c(1.07,1),rel_widths = c(1.5,1))
# ggsave("test.png",plot=last_plot())