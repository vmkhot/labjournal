library(igraph)
library(reshape2)
edges <- read.csv("Virus Research/network_visual/host_predict_network.csv", header=TRUE, sep=',')
g <- graph.data.frame(edges,directed =F)
V(g)$type <- V(g)$name %in% edges[,2]
E(g)$weight <- as.numeric(edges[,3])
g
get.incidence(g, attr = "weight")
#plot
V(g)$color <- V(g)$type
V(g)$color=gsub("FALSE","red",V(g)$color)
V(g)$color=gsub("TRUE","blue",V(g)$color)
plot(g, edge.color="gray30",edge.width=E(g)$weight, layout=layout_as_bipartite)