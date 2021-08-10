library(reshape2)
library(ape)
library(phangorn)
library(dplyr)
library(tidyr)
library(cowplot)
library(ggplot2)


setwd("../bioreactor_viruses_manuscript/")
f <- read.table("./CRISPRarray_comparison_table_4plotting.csv", header=TRUE,sep=",")


f_m <- melt(f,id=c("ï..CRISPRArrays"))


f_m <- melt(f,id=c("ï..CRISPRArrays","Phormidium_Genome_spacers","PBR_AF_Day0_spacers","PBR_Nitrogen_Exp_spacers","PBR_Fresh_Biomass_spacers","Probe_Lake_spacers","X_Good_Enough_Lake_spacers"))
#f_m_new <- separate(data=f_m,col=variable,into=c("hmm","oxygen","hc"),sep="\\.")

write.csv(f_m,"CRISPRarray_comparison_table_4plotting_long.csv")
f_m_long <- read.csv("CRISPRarray_comparison_table_4plotting_long.csv")

#keep order same as original data
f_m_long$variable <- factor(f_m_long$variable,levels = unique(f_m_long$variable))

#~~~~~~~~~Heatmap~~~~~~~~~~~~~~~~~~~~~~~#
p1 <- ggplot(f_m_long,aes(x=variable,y=ï..CRISPRArrays),fill=value)+
  geom_tile(aes(fill=value))+
  geom_text(aes(label=round(spacers,1),size=11,fontface="bold"))+
  scale_x_discrete(position="top")+
  scale_y_discrete(limits=rev)+
  theme(axis.title=element_blank(),
        axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        panel.background =element_blank())+
  scale_fill_gradient(high="#ecf8f8", low="#7cb192",trans="reverse")#+
  #labs(title = "Cyano CRISPR arrays across multiple metagenomes",value="Counts of gene expression")

p1
