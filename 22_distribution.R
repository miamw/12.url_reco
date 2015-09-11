source('/Users/Meng/Work/workspace/UrlRecoSS/src/util.R')

####################### Func #######################

####################### Main #######################

######### site feature

## read data
#fea_dir = '/Users/Meng/Work/workspace/UrlRecoSS/data/2_site_fea'
#fea = read.table(fea_dir, na.strings = "NA", quote=NULL, comment='', sep = "\t", header=T)
#
#################### plot
##pdf(file = '/Users/Meng/Work/workspace/UrlRecoSS/data/site_dist.pdf')
#
#
## active day
#dis = getHist(input=fea, fea='actday', if_log=0, if_zero=0, xstep=1, xlim=130, ylim=0.6, if_table=1, xlab='active day', main='Site Distribution -- Active Days')
#fea_flt = fea[which(fea[,'actday']>=30),]
#
## uu
#dis = getHist(input=fea_flt, fea='uu_median', if_log=0, if_zero=0, xstep=10, xlim=1000, ylim=1, if_table=1, xlab='uniq user count(median)', main="Site Distribution -- Uniq User Count")
#fea_flt = fea[which(fea[,'actday']>=30 & fea[,'uu_median']>=10),]
#
#dis = getHist(input=fea_flt, fea='uid_actday_avg', xstep=0.05, xlim=5, ylim=0.15, if_log=0, if_zero=0, if_table=1, xlab="users' active days(average)", main="Site Distribution -- Users' Active Days")
#fea_flt = fea[which(fea[,'actday']>=30 & fea[,'uu_median']>=10 & fea[,'uu_median']<2000 & fea[,"uid_actday_avg"]>=1.2),]
#
######## loaded
#
#flted = fea[which(fea[,'actday']>=30 & fea[,'uu_median']>=10 & fea[,"uid_actday_avg"]>1 & fea[,"uid_actday_avg"]<1.05),]
#
#dev.off()

########## uid site count

#fea_dir = '/Users/Meng/Work/workspace/UrlRecoSS/data/2_site_fea'
#fea = read.table(fea_dir, na.strings = "NA", quote=NULL, comment='', sep = "\t", header=T)
#
#################### plot
##pdf(file = '/Users/Meng/Work/workspace/UrlRecoSS/data/site_dist.pdf')
#
#
## active day
#dis = getHist(input=fea, fea='actday', if_log=0, if_zero=0, xstep=1, xlim=130, ylim=0.6, if_table=1, xlab='active day', main='Site Distribution -- Active Days')

