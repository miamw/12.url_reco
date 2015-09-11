use url_reco1;

LOAD DATA LOCAL INPATH '${f}' INTO TABLE ${t}
	PARTITION (dt='${dt}');
