#!/bin/bash

source ~/.bash_profile

#alias python=python
alias python=python3

work_dir=`pwd`
#local_dir='/nh/backlog/mw'
local_dir='../data'
hdfs_dir='/user/hive/warehouse/url_reco1'


# **************************** Func ****************************

# Upload traffic data
function upload_trf() {
	_server=$1

	if [[ $_server == "ufs37" ]]
	then
		fld='NF-1'
	elif [[ $_server == "nh604" ]]
	then
		#fld='NF-2'
		fld='NF-1'
	else
		echo "Wrong Server Name!"
		exit -1
	fi

	_dir=$local_dir/turbo2/$_server
	for f in `ls -1 $_dir`
	do
		dt=`echo $f | awk -F"." '{print $('$fld')}' | sed 's/-//g'`
		hive -f 11_load.sql -d f=$_dir/$f -d t=1_trf -d dt=$dt
	done
}

function upload_sitelist() {
	# get site only
	cut -f1 $local_dir/list_site_fea.v1 > $local_dir/list_site.v1
	hive -f 11_load.sql -d f=$local_dir/list_site.v1 -d t=0_list -d dt='f1'
}


# Download data
function dl_data() {
	_f=$1
	_dt=$2

	hd -cat $hdfs_dir/$_f/dt=$_dt/* > $local_dir/$_f.$_dt
}

# Run python
function run_py() {
	_f=$1
	_param=$2
	_import=$3

	python -c "from url_reco import $_import $_f; $_f($_param)"
}

# Add score
function add_score() {
	idx=$local_dir/idx_site
	score=$local_dir/idx_site_top_score
	idx_score=$local_dir/idx_site_score

	awk -F"\t" 'BEGIN{OFS="\t"}ARGIND==1{
		score[$1]=$3
	}ARGIND==2{
		if($1 in score)
			s=score[$1]
		else
			s=0
		print $1,$2,s
	}' $score $idx > $idx_score

	#rm -f $score
} 

# Diff new old reco result
function diff_reco() {
	cd $local_dir
	paste old/check_idx_user_sitelist new/check_idx_user_sitelist | cut -f1-4,8 > check.diff

	cd $work_dir
}

# **************************** Main ****************************

## ****** Data Prep: Filter Urls ******

## Create DB && tabels
#hive -f 10_create.sql

## Upload site list
#upload_sitelist

## Upload traffic
#upload_trf ufs37
#upload_trf nh604

## Get site_user_weight
#f=12_site_user_weight
#hive -f $f.sql
#dl_data $f f1

## Calculate user feature
#f=13_fea_user
#hive -f $f.sql | sort -nrk3 > $local_dir/$f

## Get site, user, weight matrix
#run_py prep_data" "'../data'" "util_tight_mat,"

## ****** Training: Get Url Relationship Matrix ******
#run_py train "'../data', start=0, end=20000"

## ****** Test: Get (user, url_list) ******
#run_py prep_test "'../data', site_cnt=1013" "util_load_idx,"
#add_score
#run_py test "'../data', top_k=100, user_top=400000"
#run_py filter_reco_list "'../data', viewed_th=10, listlen_th=20" "util_load_idx,"

offset=10
mod=1000
run_py manual_check "'../data', site_cnt=20, offset=$offset, mod=$mod" "util_load_idx,"

## Run diff
#diff_reco
