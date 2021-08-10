library(sunburstR)

setwd("./Virus Research/ForUSB/R_Practice/sunburst_virus_enviro/")
sequences <- read.csv("./virus_enviro_3",
                      header=F,
                      stringsAsFactors = FALSE)
sunburst(sequences)
