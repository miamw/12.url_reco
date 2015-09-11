-- Create DB
CREATE DATABASE IF NOT EXISTS url_reco1
	LOCATION '/user/hive/warehouse/url_reco1';

use url_reco1;

-- Create 1_trf

CREATE TABLE IF NOT EXISTS 1_trf (
	imei string,
	uid string,
	site string,
	url string
) PARTITIONED BY (dt string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'
LOCATION '/user/hive/warehouse/url_reco1/1_trf';

-- Create 0_list
CREATE TABLE IF NOT EXISTS 0_list (
	key string
) PARTITIONED BY (dt string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'
LOCATION '/user/hive/warehouse/url_reco1/0_list';

-- Create 2_site_user
CREATE TABLE IF NOT EXISTS 12_site_user_weight (
	site string,
	user string,
	weight int
) PARTITIONED BY (dt string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'
LOCATION '/user/hive/warehouse/url_reco1/12_site_user_weight';
