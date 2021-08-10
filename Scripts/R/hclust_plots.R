  setwd("/home/varadakhot/Documents/R_Practice/")
  contigs <- read.table("viral_contigs_depths.txt", sep="\t", header=TRUE)
  contigs_labels <- contigs$contigName #factor contig labels into a list and delet from dataframe
  contigs$contigName <- NULL
  rownames(contigs) <- contigs_labels # add rownames to data.frame from labels list
  
  #at this point dataframe should only have values to create dist matrix
  library(vegan)
  library(ggplot2)
  library(dplyr)
  library(tidyr)
  dist_mat <- vegdist(contigs,method = "bray")
  hclust_avg <- hclust(dist_mat,method = "complete")
  plot(hclust_avg)
  rect.hclust(hclust_avg,k=20,border = 2:6) #draws boxes around the clusters. k=#of clu    sters, change k to see clusters
  #create clusters by cutting the tree
  cut_avg <- cutree(hclust_avg,k=20)
  contigs_cl <- mutate(contigs,cluster=cut_avg) # create new dataframe with clusters identified
  count(contigs_cl,cluster) # count number of contigs assigned to each cluster  
  contigs_cl$names= contigs_labels #add co  ntig labels back
  #convert from wide to long format using gather(), clusters and names will be used to factor
  C <- gather(contigs_cl,key="samples",value = "values", -cluster, -names)
  #plot
  ggplot(C,aes(x=reorder(C$names,C$cluster),y=C$values,fill=factor(C$samples))) +
    geom_bar(stat="identity")+
    theme(axis.text.x.bottom = element_text(angle=90, size=12),axis.text.y=element_text(size=12),axis.title=element_text(size=18),plot.title=element_text(hjust=0.5, size=18),legend.text=element_text(size=12),legend.title=element_text(size=12))+
    #annotate("rect",xmin=c(0,22.5,35.5,36.5,38.5,68.5,69.5,78.5,79.5,80.5,83.5,89.5,93.5,95.5,96.5),xmax=c(22.5,35.5,36.5,38.5,68.5,69.5,78.5,79.5,80.5,83.5,89.5,93.5,95.5,96.5,97.5),ymin = 0,ymax = 2.25,alpha=0.2,color="black",fill="pink")
    scale_fill_discrete(name="Samples", breaks=c("C_8_6_Ammonium", "T1_8_6_Nitrate", "T10_10_3_Urea","T2_10_3_Nitrate"),labels=c("Ammonium","8_Nitrate","Urea","10_Nitrate"))+
    xlab("Contigs") + ylab("Normalized Coverage") +
    labs(title="Viral Contig Coverage by Sample")+
    ylim(0,2.25)
  
  # 
  
  
