use url_reco1;

SELECT
	user,
	COUNT(DISTINCT site) AS cnt_site,
	SUM(weight) AS cnt_active
FROM
	12_site_user_weight
WHERE
	dt='f1'
GROUP BY
	user;
