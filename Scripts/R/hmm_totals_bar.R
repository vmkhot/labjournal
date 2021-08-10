setwd("./alkanes_hackathon/validation/Metagenomes/normalized_metagenome_hmmsearch_results/")
library(dplyr)
library(tidyr)
library(ggplot2)

f <- read.table("./hmm_total_hits_0.8.csv", header=TRUE,sep="\t")


ggplot(f,aes(x=HMM,y=total)) +
  geom_bar(stat="identity", colour="black") +
  labs(x="",y="total nor domain score > 0.8",fill="",title="Summed hits/readCounts by HMM(METAGENOMES)")+
  theme(axis.text.x = element_text(colour="black", vjust=0.5,face="bold",size=12,angle=90,hjust=1),
        axis.text.y=element_text(colour="black",face="bold",size=12),
        axis.title.y=element_text(colour="black",face="bold",size=12),
        strip.text = element_text(colour="black",face="bold",size=10),
        legend.text = element_text(size = 10, face ="bold", colour ="black"), 
        legend.title = element_text(size = 12, face = "bold"), 
        panel.background = element_blank(), panel.border = element_rect(colour = "grey95", fill = NA, size = 0.1),panel.grid.major.y = element_line(colour = "grey95"),legend.position = "right")+
  facet_grid(. ~ oxygen + hc_type,space="free", scales="free",switch = "x")
  

