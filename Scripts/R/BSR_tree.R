library(reshape2)
library(ape)
library(dendextend)
library(dplyr)
library(tidyr)
library(vegan)
library(cowplot)

setwd("C:\Users\varde\Documents\Virus Research\viral_prop_mgs")
f <- read.delim("../../../", header=TRUE,sep="\t")
f[c(3)] <- lapply(f[3],function(x) 1/x)
is.na(f) <- sapply(f, is.infinite)
#create matrix from the list using acast from reshape2
m <- acast(f,contig1 ~ contig2)
m <- replace_na(m,0)
d <- dist(m)
h <- hclust(d, method = "average")
# plot(h)
dend <- as.dendrogram(h)
dend_2 <- dend %>% set("labels_cex",0.57) %>% set("branches_lwd",0.5) %>% set("hang_leaves")
tree <- as.phylo(h)
write.tree(phy=tree, file='BSR.tree')

p1 <- ggplot(dend, horiz=T)+theme(plot.margin = unit(c(3,1,3,1),"lines"))
plot(p1)
# ggsave(file="fastani_dendro.png",width=15,height=5*2.5)
