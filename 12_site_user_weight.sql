use url_reco1;

INSERT OVERWRITE TABLE 12_site_user_weight
	PARTITION(dt='f1')
SELECT
	site,
	user,
	COUNT(DISTINCT dt) AS weight
FROM (
	SELECT
		1_trf.site AS site,
		1_trf.imei AS user,
		1_trf.dt AS dt
	FROM 1_trf JOIN 0_list ON 1_trf.site = 0_list.key
	WHERE
		1_trf.dt>='20150300' AND 1_trf.dt<='20151231' AND 0_list.dt='f1'
) site_user
GROUP BY site, user;	
