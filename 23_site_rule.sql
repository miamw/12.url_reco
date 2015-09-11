use url_reco;

-- Insert
INSERT OVERWRITE TABLE 2_site_fea
	PARTITION(dt=106)
SELECT
	*
FROM
	1_trf
WHERE
	dt=6 AND
	NOT (site~"^www.") AND NOT(site in skip) AND
		cnt_trf>=300 AND cnt_trf<100000 AND
		cnt_uid>=30 AND
		uid_trf_avg>=30 AND
		did_uidcnt_avg<1.2 )	
