setwd("./alkanes_hackathon/validation/Metagenomes/normalized_metagenome_hmmsearch_results/")
library(dplyr)
library(tidyr)

hmm_result_antartic <- read.table("normalized_hmmsearch_result_antarcticOcean_VK_3300029631.tblout", header=FALSE)
hmm_result_antartic <- rename(hmm_result_antartic,gene_name=V1,hmm=V3,normalized_score=V20,deg_type=V21)
hmm_result_antartic <- hmm_result_antartic[,-(18:19),drop=FALSE]

hmm_result_HC_napdc <- read.table("normalized_hmmsearch_result_HCenrichmentnapdc_AC_SRR634687_filter.tblout", header=FALSE)
hmm_result_HC_napdc <- rename(hmm_result_HC_napdc,gene_name=V1,hmm=V3,normalized_score=V18,deg_type=V19)

hmm_result_childgut <- read.table("normalized_hmmsearch_result_childgut_VK_3300023490.tblout", header=FALSE)
hmm_result_childgut <- rename(hmm_result_childgut,gene_name=V1,hmm=V3,normalized_score=V20,deg_type=V21)
hmm_result_childgut <- hmm_result_childgut[,-(18:19),drop=FALSE]

hmm_result_yucatan <- read.table("normalized_hmmsearch_result_yucatanmarine_VK_3300001969.tblout", header=FALSE)
hmm_result_yucatan <- rename(hmm_result_yucatan,gene_name=V1,hmm=V3,normalized_score=V20,deg_type=V21)
hmm_result_yucatan <- hmm_result_yucatan[,-(18:19),drop=FALSE]

hmm_result_coral <- read.table("normalized_hmmsearch_result_coral_VK_3300010032.tblout", header=FALSE)
hmm_result_coral <- rename(hmm_result_coral,gene_name=V1,hmm=V3,normalized_score=V20,deg_type=V21)
hmm_result_coral <- hmm_result_coral[,-(18:19),drop=FALSE]



hmm_result_antartic['environment']='antartic_ocean'
hmm_result_HC_napdc['environment']='HC_enrichment_napdc'
hmm_result_childgut['environment']='childgut'
hmm_result_yucatan['environment']='yucatan'
hmm_result_coral['environment']='coral'


hmm_result_combined<- rbind(hmm_result_antartic,hmm_result_HC_napdc,hmm_result_coral, hmm_result_yucatan, hmm_result_childgut)



write.csv(hmm_result_combined,"hmm_result_antartic_HCnapdc_coral_gut_yucatan.csv")
hmm_result_combined <- read.table("hmm_result_antartic_HCnapdc_coral_gut_yucatan.csv",header=TRUE, sep=',')


#filter results by score
hmm_result_combined_filtered <- filter(hmm_result_combined, normalized_score > 0.2)

hmm_result_combined_filtered$hmm <- factor(hmm_result_combined_filtered$hmm,levels = unique(hmm_result_combined_filtered$hmm))
                                       
                                      

library(ggplot2)

ggplot(hmm_result_combined, aes(x=hmm,y=normalized_score,color=factor(environment))) +
  geom_point(alpha=0.5)+theme(axis.text.x.bottom = element_text(angle=90))+ 
  xlab("HMM_genes") + 
  ylab("Normalized Domain Score") + 
  labs(title="HC degradation genes in 5 metagenomes")+ 
  theme(axis.text.x.bottom = element_text(vjust=0.5))+
  facet_grid(metabolism ~ HC_type,scales = "free_x", space="free")

ggplot(hmm_result_combined_filtered, aes(x=hmm,y=normalized_score,color=factor(environment))) +
  geom_point(alpha=0.5)+theme(axis.text.x.bottom = element_text(angle=90))+ 
  xlab("HMM_genes") + 
  ylab("Normalized Domain Score") + 
  labs(title="HC degradation genes in 5 metagenomes")+
  facet_grid(metabolism ~ HC_type, scales = "free_x")
