#!/bin/bash

## Training: url similarity matrix
function run_urls_sim() {
        # mr 0
        hd -rmr $mr_dir/2_mr0
        hstream \
        -file $work_dir/cos0_mapper.py -mapper 'cos0_mapper.py' \
        -file $work_dir/cos0_reducer.py -reducer 'cos0_reducer.py' \
        -input $mr_dir/mat_site_user_valid.loose -output $mr_dir/2_mr0

        # mr 1
        hd -rmr $mr_dir/2_mr1
        hstream \
        -file $work_dir/cos1_mapper.py -mapper 'cos1_mapper.py' \
        -file $work_dir/cos1_reducer.py -reducer 'cos1_reducer.py' \
        -input $mr_dir/mat_site_user_valid.loose -output $mr_dir/2_mr1

        # mr 2
        hd -rmr $mr_dir/2_mr2
        hstream \
        -file $work_dir/cos2_mapper.py -mapper 'cos2_mapper.py' \
        -file $work_dir/cos2_reducer.py -reducer 'cos2_reducer.py' \
        -input $mr_dir/2_mr1 -output $mr_dir/2_mr2

        # mr 3
        hd -rmr $mr_dir/2_mr3
        hstream \
        -file $work_dir/cos3_mapper.py -mapper 'cos3_mapper.py' \
        -file $work_dir/cos3_reducer.py -reducer 'cos3_reducer.py' \
        -input $mr_dir/2_mr0 -input $mr_dir/2_mr2 -output $mr_dir/2_mr3
}

## Test: reco for user
function run_reco() {
        ## Run mr job
        #hd -cat $mr_dir/2_mr3/part* > $local_dir/mat_site_sim.loose

        hd -rmr $mr_dir/3_reco
        hstream \
        -file $work_dir/reco_mapper.py -mapper 'reco_mapper.py' \
        -file $work_dir/reco_reducer.py -reducer 'reco_reducer.py' \
        -file $local_dir/mat_site_sim_top.loose \
        -input $mr_dir/mat_site_user_valid.loose -output $mr_dir/3_reco

        hd -cat $mr_dir/3_reco/part* > $local_dir_tmp/mat_user_site.loose
}
