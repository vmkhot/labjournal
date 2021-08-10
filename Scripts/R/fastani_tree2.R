library(reshape2)
library(ape)
library(dendextend)
library(dplyr)
library(tidyr)
library(vegan)
library(dendextend)
library(cowplot)

setwd("/home/varadakhot/Documents/R_Practice/")
f <- read.delim("./fastani14_cp_trimmed.out", header=FALSE,sep="\t")
#create matrix from the list using acast from reshape2
m <- acast(f,V1 ~ V2)
m <- replace_na(m,0)
d <- vegdist(m,method = "bray")
h <- hclust(d, method = "average")
# plot(h)
dend <- as.dendrogram(h)
dend_2 <- dend %>% set("labels_cex",0.57) %>% set("branches_lwd",0.5) %>% set("hang_leaves")
# tree <- as.phylo(h)
# write.tree(phy=tree, file='vcontact.tree')

p1 <- ggplot(dend_2, horiz=T)+theme(plot.margin = unit(c(3,1,3,1),"lines"))
plot(p1)
# ggsave(file="fastani_dendro.png",width=15,height=5*2.5)

contigs <- read.table("viral_contigs_depths.txt", sep="\t", header=TRUE)
contigs_labels <- contigs$contigName #factor contig labels into a list and delet from dataframe
contigs$contigName <- NULL
rownames(contigs) <- contigs_labels # add rownames to data.frame from labels list
contigs$contigName= contigs_labels #add contig labels back
contigs$contigName <- factor(contigs$contigName,levels=labels(dend))
C <- gather(contigs,key="samples",value = "values", -contigName)
C <- na.omit(C)

p2 <-ggplot(C,aes(y=sqrt(C$values),x=C$contigName,fill=factor(C$samples))) +
  geom_bar(stat="identity")+ coord_flip()+
  theme(axis.text.y=element_blank(),axis.title.y = element_blank(),plot.title=element_text(hjust=0.5, size=11),legend.text=element_text(size=12),legend.title=element_text(size=12))+
  scale_fill_discrete(name="Samples", breaks=c("C_8_6_Ammonium", "T1_8_6_Nitrate", "T10_10_3_Urea","T2_10_3_Nitrate"),labels=c("Ammonium","8_Nitrate","Urea","10_Nitrate"))+
  ylab("Normalized Coverage") +
  ylim(0,2)#+
#labs(title="Virus Contig Coverage")+
# plot(p2)
# ggsave(file="abundances.svg",dpi=600,width=5,height=5*2.5)

plot_grid(p1,p2,align="h",scale = c(1.025,1),rel_widths = c(2,1))
ggsave(file="fastani_abundance.svg",width=16,height=9)
