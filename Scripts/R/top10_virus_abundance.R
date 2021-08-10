setwd("~/Virus Research/bioreactor_viruses_manuscript/abundance_figure/")

VC <- read.csv("viral_contigs_wide.csv",sep=",",header=TRUE)
library(ggplot2)
library(reshape2)
library(tidyr)
library(RColorBrewer)
library(colorRamps)

VCm <- melt(VC,id=c("Sample","pH"))

#VCm_new <- separate(data=VCm,col=variable,into=c("variable","Organism"),sep="_")

#save and add organism column into the long format in excel, read back into program
write.csv(VCm,"viral_contigs_long.csv")
VCm_new <- read.csv("viral_contigs_long.csv",header=TRUE)
VCm_new$Sample <- factor(VCm_new$Sample,levels=unique(VCm_new$Sample))



#bubble plot
xx = ggplot(VCm_new,aes(x=Sample,y=variable)) +
  geom_point(aes(size = value, fill = organism), alpha = 0.75, shape = 21)+
  scale_size_continuous(limits = c(0.01, 2000), range = c(1,19), breaks = c(1,10,200,2000))+
 # scale_fill_manual(values = colours, guide = FALSE) + 
  scale_y_discrete(limits = rev(levels(VCm_new$variable)))+
  facet_grid(. ~ organism ,scale = "free_x")+coord_flip()

xx

labels <- c(host="Bacterial Populations", virus="Viral Contigs")

#expanding colour palette
n_col<- 23
colours <- colorRampPalette(brewer.pal(8,"Accent"))(n_col)

#stacked/grouped bar graph
xs= ggplot(VCm_new,aes(x=organism,y=value,fill=factor(variable))) +
  geom_bar(stat="identity", colour="black",position="stack") +
  scale_fill_manual(values = colours)+
  labs(x="Organism",y="Sequencing depth",fill="Populations")+
  theme(axis.text.x = element_text(colour="black", vjust=0.5,face="bold",size=12),
      axis.text.y=element_text(colour="black",face="bold",size=12),
      axis.title=element_text(colour="black",face="bold",size=12),
      strip.text = element_text(colour="black",face="bold",size=10),
      legend.text = element_text(size = 10, face ="bold", colour ="black"), 
      legend.title = element_text(size = 12, face = "bold"), 
      panel.background = element_blank(), panel.border = element_rect(colour = "grey95", fill = NA, size = 0.1),panel.grid.major.y = element_line(colour = "grey95"),legend.position = "right")+
  facet_grid(. ~ Sample,scales = "free",labeller =labeller(Organism=labels))

xs
