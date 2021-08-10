ggarrange(ggplot(data=new$bin05A.contig0138,aes(new$bin05A.contig0138$position,new$bin05A.contig0138$C_8_6_Ammonium)) + geom_line() + ylim(0,40) + labs(title="C_8_6_Ammonium",x="Position",y="Coverage"),
          ggplot(data=new$bin05A.contig0138,aes(new$bin05A.contig0138$position,new$bin05A.contig0138$T10_10_3_Urea)) + geom_line() + ylim(0,40)+ labs(title="T10_10_3_Urea",x="Position",y="Coverage"),
          ggplot(data=new$bin05A.contig0138,aes(new$bin05A.contig0138$position,new$bin05A.contig0138$T1_8_6_Nitrate)) + geom_line()+ylim(0,40) + labs(title="T1_8_6_Nitrate",x="Position",y="Coverage"),
          ggplot(data=new$bin05A.contig0138,aes(new$bin05A.contig0138$position,new$bin05A.contig0138$T2_10_3_Nitrate)) + geom_line() + ylim(0,40) + labs(title="T2_10_3_Nitrate",x="Position",y="Coverage"), nrow=4, align="h")







