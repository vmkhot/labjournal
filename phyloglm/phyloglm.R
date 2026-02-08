# install.packages("phylolm")
# install.packages("ggtree")
library(ape)
library(phylolm)
library(dplyr)
library(ggplot2)

setwd('OneDrive - Friedrich-Schiller-Universität Jena/MCP_struct/Microviridae_analysis/multiple_cluster_analysis/combined_model_phyloglm/')

# df_100 <- read.csv("phyloglm_test_data_all.tsv",header = TRUE, sep = '\t', check.names = FALSE)
df_100 <- read.csv("phyloglm_test_data_new_alignment.tsv",header = TRUE, sep = '\t', check.names = FALSE)
rownames(df_100) <- df_100[,1]
df_100[,1] <- NULL

# Replace "mytree.nwk" with your tree file path
tree <- read.tree("cluster_0_1_mixed_MSTA_aa_plus_ec6098ref_2.tree")
class(tree)           # should be "phylo"
# tree$tip.label        # shows the tip names


# Features to test (columns 2 onward)
features <- names(df_100)[-c(1)]

# Function to fit phyloglm for a single feature
fit_phyloglm <- function(feature) {
  print(feature)  # track progress
  
  # Prepare data
  dat <- df_100[, c(1, which(names(df_100) == feature))]
  names(dat) <- c("y", "x")
  
  # Fit model with error handling
  m1 <- tryCatch(
    phyloglm(
      formula = y ~ x,
      data = dat,
      phy = tree,
      method = "logistic_IG10",
      boot = 2
    ),
    error = function(e) list(coefficients = NA)
  )
  
  # Extract results
  if (is.na(coef(m1)[1])) {
    return(data.frame(
      feature = feature,
      Estimate = NA,
      SE = NA,
      z.value = NA,
      p.value = NA,
      alpha = NA
    ))
  } else {
    m1.sum <- summary(m1)
    return(data.frame(
      feature = feature,
      Estimate = m1.sum$coefficients["x", 1],
      SE = m1.sum$coefficients["x", 2],
      z.value = m1.sum$coefficients["x", 3],
      p.value = m1.sum$coefficients["x", 6],
      alpha = m1$alpha
    ))
  }
}



# Apply to all features
Res_100_pruned <- lapply(features, fit_phyloglm) %>% bind_rows()

# View results
head(Res_100_pruned, n=10)

# adjust the pvalues (Benjamini-Hochberg)
Res_100_pruned$padj <- p.adjust(Res_100_pruned$p.value, method = "fdr")

Res_100_pruned_filt <- filter(Res_100_pruned, padj < 0.01)

write.csv(Res_100_pruned,"phyloglm_results_combined_model_pruned_full_01_new.csv")

# plot
p <- ggplot(Res_100_pruned, aes(x = Estimate, y = z.value, label=feature)) +
  geom_point(aes(color = alpha), alpha = 0.2,size=1.5) +   # base layer
  geom_point(
    data = subset(Res_100_pruned, -log10(padj) > 3),
    aes(color = alpha), size=1.5) +# highlight significant ones
  geom_text(
    data =subset(Res_100_pruned, z.value <= -8),
    size = 3, hjust=1.2)+
  geom_text(
      data =subset(Res_100_pruned, z.value >= 5),
      size = 3, hjust=1.2)+
  geom_hline(yintercept = 3.9, linetype = "dashed", color = "black") +
  geom_hline(yintercept = -3.9, linetype = "dashed", color = "black") +
  #scale_color_gradientn(colours = c("#364B9AFF", "#4A7BB7FF", "#6EA6CDFF", "#98CAE1FF", "#C2E4EFFF", "#EAECCCFF", "#FEDA8BFF", "#FDB366FF", "#F67E4BFF", "#DD3D2DFF", "#A50026FF"),name = "alpha") +
  scale_color_gradient(name = "Phylogenetic\nsignal (alpha)", low = "#82e9e9ff", high = "#0d4d4dff")+
  theme_minimal()+
  theme(
    axis.text = element_text(size=14),
    axis.title = element_text(size=14),
    legend.text = element_text(size=14),
    legend.title = element_text(size=14)
    
  )



p
ggsave("zvalue_v_estimate.svg")
print(-log10(0.005))

