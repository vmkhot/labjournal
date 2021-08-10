library(qvalue)
setwd("/Users/varde/Documents/Virus Research/DVF_testing/")
result <- read.csv("dvfinitial_output.txt", sep = '\t')

result$qvalue <- qvalue(result$pvalue,pi0 = 1,)$qvalue
result[order(result$qvalue),]
plot(result$pvalue,result$qvalue)
write.csv(result,file="dvfinitial_output_qvalues.txt",sep = '\t')
