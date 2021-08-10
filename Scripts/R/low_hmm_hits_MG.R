setwd("./alkanes_hackathon/validation/Metagenomes/normalized_metagenome_hmmsearch_results/")
library(dplyr)
library(tidyr)
library(ggplot2)

low_hits <- read.csv("hits_below_0.8._2csv.txt", header=TRUE, sep='\t')

low_hits_melt <- melt(low_hits,id=c("metagenome","environment"))

low_hits_melt$metagenome <- factor(low_hits_melt$metagenome,levels = unique(low_hits_melt$metagenome))


ggplot(low_hits_melt, aes(x=variable,y=metagenome)) +
  geom_point(aes(fill = environment,size=value),alpha=0.5,shape = 21)+
  scale_size_continuous(limits = c(0.00001, 1.6), range = c(1,15), breaks = c(0,0.01,0.1,0.5,1,1.6))+
  theme(axis.text.x.bottom = element_text(angle=90,vjust=0.5))+ 
  xlab("HMM_genes") + 
  ylab("Normalized Domain Score") + 
  labs(title="0.8 > hits > 0.1",fill="Environment", size="summedHits/readCounts")+
  guides(fill = guide_legend(override.aes = list(size = 5)))
  
  #facet_grid(oxygen ~ hc_type,scale = "free_x", space="free")+
  
#~~~~~~~~~~~~~~~~~~~~~~~~~hits plots~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

f <- read.table("./hits_below_0.8.csv", header=TRUE,sep="\t")

f$hmm <- factor(f$hmm,levels = unique(f$hmm))



p2 <- ggplot(f,aes(x=hmm,y=nor_score))+
  geom_point(aes(fill = environment ), alpha = 0.65, shape = 21,size=5)+
  facet_grid(oxygen ~ hc_type ,scales = "free",space="free")+
  labs(title = "HMM hits < 0.8",y="Normalized Domain Score",fill="Environment")+ 
  theme(axis.text.y=element_text(color="black",size=11),
        axis.title.y=element_text(color="black",size=12,face="bold"),
        axis.ticks.y=element_blank(),
        axis.title.x=element_blank(),
        axis.text.x=element_text(angle=90,hjust=1,vjust=0.3, colour="black",size=12,face="bold"),
        legend.title = element_text(size = 11), panel.background = element_blank(),
        legend.text = element_text(size=11,color = "black"),
        panel.border = element_rect(colour = "black", fill = NA, size = 1.2), 
        legend.position = "right", panel.grid.major.y = element_line(colour = "grey95"),
        panel.grid.major.x = element_line(colour="grey95"),
        strip.text = element_text(colour="black",face="bold",size=10))+
  scale_fill_manual(values = c("darkorange", "slateblue3","turquoise3","steelblue2","deeppink2","seagreen","tomato2","sienna3"), guide = guide_legend(override.aes = list(size=5)))

p2
