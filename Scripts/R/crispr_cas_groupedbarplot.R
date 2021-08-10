setwd("~/Virus Research/ForUSB/Virus_visuals/")

VC <- read.csv("crispr_cas.tsv",sep="\t",header=TRUE)
library(ggplot2)
library(ggrepel)
library(reshape2)
library(tidyr)

VCm <- melt(VC,id=c("bin","organism","cas_label"))

write.table(VCm,"crispr_cas_long.tsv",sep='\t')
VCm_new <-read.table("crispr_cas_long.tsv",sep='\t',header=TRUE)

VCm_new$bin <- factor(VCm_new$bin,levels=unique(VCm_new$bin))


labels <- c(cas_num="Cas Systems", crispr="CRISPR Arrays")

#stacked bar graph
xs= ggplot(VCm_new,aes(x=bin,y=value,fill=variable,label=cas_label)) +
  geom_bar(stat="identity", colour="black", position="dodge")+
  xlab("Bins")+labs(x="Bins",y="",fill="")+
  theme(axis.text.x = element_text(colour="black", vjust=0.5,face="bold",size=12),
        axis.text.y=element_text(colour="black",face="bold",size=12),
        axis.title.y=element_blank(),
        strip.text = element_text(colour="black",face="bold",size=10),
        legend.text = element_text(size = 10, face ="bold", colour ="black"), 
        legend.title = element_text(size = 12, face = "bold"), 
        panel.background = element_blank(), panel.border = element_rect(colour = "grey95", fill = NA, size = 0.1),panel.grid.major.y = element_line(colour = "grey95"),legend.position = "right")+
  facet_grid(. ~ organism,labeller =labeller(variable=labels),space="free", scales="free",switch = "x")+
  geom_text_repel(vjust=-0.75,fontface="bold")
  
xs



