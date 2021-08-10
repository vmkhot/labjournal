library(tidyr)
library(dplyr)
dvf_results <- read.table("Virus Research/files_from_server/dvf_results_filtered_5000bp.txt", sep="\t", header=TRUE)
str(dvf_results)
dvf_results_sorted <- dvf_results[order(-dvf_results$score),]
plot(dvf_results_sorted$name,dvf_results_sorted$score)

#filtering by score
quantile(dvf_results$score, c(0.5,0.75,0.90,0.99))
#  50%        75%        90%        99% 
#0.05712931 0.14946900 0.35384628 0.91907613 
dvf_results_filtered <- dvf_results %>% filter(score >= 0.91)


#filtering by pvalue
quantile(dvf_results$pvalue, c(0.5,0.25,0.10,0.01))
#50%        25%        10%         1% 
#0.22596118 0.16480663 0.10716822 0.01640135 
dvf_results_filtered2 <- dvf_results %>% filter(pvalue <= 0.0164)

write.csv(dvf_results_filtered, "Virus Research/files_from_server/dvf_results_filtered_5000bp_99percen.txt",row.names = FALSE)
