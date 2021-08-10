library(reshape2)
library(dplyr)
library(tidyr)
library(ggplot2)

setwd("alkanes_hackathon/validation/Metagenomes/normalized_metagenome_hmmsearch_results/")

f <- read.table("./allMG_above_0.8_wide.csv", header=TRUE,sep="\t")

f_m <- melt(f,id=c("Metagenome","Environment"))

write.csv(f_m,"allMG_above_0.8_long.csv")
f_m_new <- read.csv("allMG_above_0.8_long.csv")


#keep order same as original data
f_m_new$Metagenome <- factor(f_m_new$Metagenome,levels = unique(f_m_new$Metagenome))

#~~~~~~~~~~~~~~~~~~~~~~~~~~BUBBLE PLOT~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

p2 <- ggplot(f_m_new,aes(x=HMM_new_name,y=Metagenome)) +
  geom_point(aes(size = value, colour = Environment),alpha=0.75)+
  facet_grid(class ~ . ,scales = "free",space="free")+
  scale_size_continuous(limits=c(0.00001,375),range = c(1.5,12),breaks=c(0.1,1,10,100))+
  labs(size="# of Hits > 0.8/Total Gene Count",colour="Environments")  + 
  theme(axis.text.y=element_text(colour="#31393C",size=12),
        axis.ticks.y=element_blank(),
        axis.title=element_blank(),
        axis.text.x=element_text(angle=90,hjust=1,vjust=0.3, colour="#31393C",size=12),
        legend.title = element_text(size = 12), panel.background = element_blank(),
        legend.text = element_text(size=12,color = "#31393C"),
        panel.border = element_rect(colour = "#e6e6e6ff", fill = NA, size = 1.2), 
        legend.position = "right",
        panel.grid.major.y = element_line(colour = "#fafafaff"),
        panel.grid.major.x = element_line(colour="#fafafaff"),
        strip.text.y = element_text(colour="black",size=12,angle=0),
        strip.background = element_rect(fill = "#f2f2f2ff",color = "#fafafaff"))+
  scale_color_manual(values = c("#EC8609","#325D9E","#ADDAFF","#FED872","#3381FF"), guide = guide_legend(override.aes = list(size=5)))+coord_flip()

p2

