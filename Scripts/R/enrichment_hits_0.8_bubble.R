library(reshape2)
library(dplyr)
library(tidyr)
library(ggplot2)

setwd("Metagenomes/normalized_metagenome_hmmsearch_results/")

f <- read.table("./enrichment_MG_dataset_2.csv", header=TRUE,sep="\t")

f$HMM <- factor(f$HMM,levels = unique(f$HMM))



p2 <- ggplot(f,aes(x=HMM,y=Normalized_Domain_Score))+
  geom_point(aes(fill = Enrichment ), alpha = 0.75, shape = 21,size=5)+
  facet_grid(Oxygen_Use ~ HC_Type ,scales = "free",space="free")+
  labs(title = "HMM Hits to Enrichment Metagenomes > 0.8",y="Normalized Domain Score",fill="Enrichment Conditions")+ 
  theme(axis.text.y=element_text(color="black",size=11),
        axis.title.y=element_text(color="black",size=12,face="bold"),
        axis.ticks.y=element_blank(),
        axis.title.x=element_blank(),
        axis.text.x=element_text(angle=90,hjust=1,vjust=0.3, colour="black",size=10),
        legend.title = element_text(size = 11), panel.background = element_blank(),
        legend.text = element_text(size=11,color = "black"),
        panel.border = element_rect(colour = "black", fill = NA, size = 1.2), 
        legend.position = "right", panel.grid.major.y = element_line(colour = "grey95"),
        panel.grid.major.x = element_line(colour="grey95"),
        strip.text = element_text(colour="black",face="bold",size=10))+
  scale_fill_manual(values = c("#FED872", "#EC8609","#FED872","#EC8609","#FED872","#3381FF","#ADDAFF","#ADDAFF"), guide = guide_legend(override.aes = list(size=5)))+geom_jitter()

p2

