set hive.exec.dynamic.partition.mode=nonstrict;

use url_reco;

INSERT OVERWRITE TABLE 1_trf
	PARTITION(dt)
SELECT
	did,
	uid,
	parse_url(url, 'HOST') AS domain,
	url,
	dt
FROM
	0_ori_trf;
