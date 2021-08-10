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
f <- read.table("./mixed_MG_dataset.tsv", header=TRUE,sep="\t")



f_m <- melt(f,id=c("Metagenome"))
f_m_new <- separate(data=f_m,col=variable,into=c("hmm","oxygen","hc"),sep="\\.")

write.csv(f_m_new,"mixed_MG_dataset_long.csv")

#keep order same as original data
f_m_new$Metagenome <- factor(f_m_new$Metagenome,levels = unique(f_m_new$Metagenome))

#~~~~~~~~~Heatmap~~~~~~~~~~~~~~~~~~~~~~~#
my_breaks= c(0,0.1,0.25,0.5,0.75)
my_palette <- c("#ffffff","#bbe1fa","#3282b8","#265D82","#1b262c")

p1 <- ggplot(f_m_new,aes(x=hmm,y=Metagenome), fill=value)+
  geom_tile(aes(fill=value))+
  theme(axis.title=element_blank(),
        axis.text.x = element_text(angle=90, size=10,colour="black",hjust=1,vjust=0.3),
        axis.text.y = element_text(size=8,colour="black"),
        legend.text=element_text(size=8,colour="black"))+
  scale_fill_gradientn(colours=my_palette,breaks=my_breaks)+
  coord_flip()+
  labs(title = "Mixed Metagenomes, norcutoff >=0.8",value="Counts of gene expression")

p1

#~~~~~~~~~BUBBLE~~~~~~~~~~~~~~~~~~~~~~~#

p2 <- ggplot(f_m_new,aes(x=hmm,y=value)) +
  geom_point(aes(size = value, fill = Metagenome), alpha = 0.75, shape = 21)+
  facet_grid(. ~ oxygen ,scales = "free",space="free")+
  scale_size_continuous(limits = c(0.00001, 0.75), range = c(1,15), breaks = c(0,0.25,0.5,0.75))+
  labs(title = "Mixed Metagenomes, norcutoff >=0.8",size="Counts of gene expression",fill="Metagenomes")  + 
  theme(axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        axis.title=element_blank(),
        axis.text.x=element_text(angle=90,hjust=1,vjust=0.3, colour="black"),
        legend.title = element_text(size = 11), panel.background = element_blank(), 
        panel.border = element_rect(colour = "black", fill = NA, size = 1.2), 
        legend.position = "right", panel.grid.major.y = element_line(colour = "grey95"),
        panel.grid.major.x = element_line(colour="grey95"))+
  scale_fill_manual(values = c("darkorange", "skyblue","deeppink2","seagreen","turquoise3","slateblue3","tomato2"), guide = guide_legend(override.aes = list(size=5)))
p2
