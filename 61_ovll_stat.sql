use url_reco;

INSERT OVERWRITE TABLE 2_site_fea
	PARTITION(dt=0)
SELECT
	COUNT(*) AS trf,
	COUNT(DISTINCT imei) AS cnt_imei,
	COUNT(DISTINCT uid) AS cnt_uid,
	COUNT(DISTINCT url) AS cnt_url,
	(COUNT(*)/COUNT(DISTINCT uid)) AS uid_trf_avg,
	(COUNT(DISTINCT uid)/COUNT(DISTINCT imei)) AS imei_uidcnt_avg
FROM
	1_trf
WHERE
	dt=0;
