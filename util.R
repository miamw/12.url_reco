
#getHist(input=fea, fea='cnt_trf', if_log=0, if_zero=0, xmax=1000000, xstep=10, xlim=300, ylim=0.8, if_table=0, xlab='monthly traffic', main='Overall Site Traffic Distribution')
getHist = function(input,fea,xstep,xlim,ylim,if_log,if_zero,if_table,xmax=1000000,xlab,main) {
	if( if_log==1 ) {
		inp_tmp <- cbind(input[,1],log(input[,fea]))
	} else {
		inp_tmp <- cbind(input[,1],input[,fea])
	}
	ind = inp_tmp[,2] > xlim
	inp_tmp[ind,2] = xlim

	axis_x <- seq(0,xmax,by=xstep)
	breaks <- seq(-xstep,xmax,by=xstep)
	
	hist0 <- hist(inp_tmp[,2],breaks=breaks,plot=F);        perc0 <- hist0$counts/sum(hist0$counts)
	perc_tmp <- cbind(axis_x,perc0)
	if( if_zero==1 ) {
		perc <- perc_tmp[c(1:(xlim/xstep+1)),]
	}else {
		perc <- perc_tmp[c(2:(xlim/xstep+1)),]
	}
	plot(perc, type="l", col=1, xlim=c(0,xlim), ylim=c(0,ylim), xlab=xlab,ylab="probability",main=main)
	
	if(if_table==1) {
		return(cbind(perc_tmp[,1],cumsum(perc_tmp[,2])))
	}
}
