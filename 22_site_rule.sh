#!/bin/bash

f_skip="/nh/backlog/mw/url.skip"
f_site_fea="/nh/backlog/mw/2_site_fea"

# normalize skip
awk -F"\t" '{print $2}' $f_skip | sed 's/^http:\/\///g' > $f_skip.nml

# filter www. and skip
awk -F"\t" 'ARGIND==1{
	skip[$1]
}ARGIND==2{
	site=$1
	cnt_trf=$2
	cnt_did=$3
	cnt_uid=$4
	cnt_url=$5
	did_trf_avg=$6
	uid_trf_avg=$7
	did_uidcnt_avg=$8

	if( !(site~"^www.") && !(site in skip) &&
		cnt_trf>=300 && cnt_trf<100000 &&
		cnt_uid>=30 &&
		uid_trf_avg>=30 &&
		did_uidcnt_avg<1.2 )
	{
		print $1
	}
}' $f_skip.nml $f_site_fea > $f_site_fea.flt 
