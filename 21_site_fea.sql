use url_reco;

-- Create
CREATE TABLE 2_site_fea (
	site string,
	actday int,
	trf_avg float,
	trf_median float,
	trf_cv float,
	uu_avg float,
	uu_median float,
	uu_cv float,
	uid_actday_avg float,
	uid_actday_median float,
	uid_trf_avg float,
	uid_trf_median float
) PARTITIONED BY (dt string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'
LOCATION '/user/hive/warehouse/url_reco/2_site_fea';

-- Insert
INSERT OVERWRITE TABLE 2_site_fea
	PARTITION(dt='overall')
SELECT
	site_dt.site AS site,
	actday,
	trf_avg,
	trf_median,
	trf_cv,
	uu_avg,
	uu_median,
	uu_cv,
	uid_actday_avg,
	uid_actday_median,
	uid_trf_avg,
	uid_trf_median
FROM (
	SELECT
		site,
		avg(uid_actday) AS uid_actday_avg,
		percentile(uid_actday, 0.5) AS uid_actday_median,
		avg(trf_avg) AS uid_trf_avg,
		percentile(cast(trf_avg as int), 0.5) AS uid_trf_median
	FROM (
		SELECT
			site,
			uid,
			count(DISTINCT dt) AS uid_actday,
			(count(*)/count(DISTINCT dt)) AS trf_avg
		FROM
			1_trf
		WHERE
			dt>='20150300' AND dt<'20150701'
		GROUP BY
			site, uid
	) by_site_uid
	GROUP BY
		site
) site_uid JOIN (
	SELECT
		site,
		count(DISTINCT dt) AS actday,
		avg(trf) AS trf_avg,
		percentile(trf, 0.5) AS trf_median,
		(stddev_pop(trf)/avg(trf)) AS trf_cv,
		avg(uu) AS uu_avg,
		percentile(uu, 0.5) AS uu_median,
		(stddev_pop(uu)/avg(uu)) AS uu_cv
	FROM (
		SELECT
			site,
			dt,
			count(*) AS trf,
			count(DISTINCT uid) AS uu
		FROM
			1_trf
		WHERE
			dt>='20150300' AND dt<'20150701'
		GROUP BY
			site, dt
	) by_site_dt
	GROUP BY
		site
) site_dt ON site_uid.site=site_dt.site;
