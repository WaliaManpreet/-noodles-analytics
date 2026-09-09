CREATE DATABASE noodles_dw;
USE noodles_dw;


SELECT * FROM factsocialengagement;
USE noodles_dw;
SHOW FULL TABLES WHERE Table_type = 'VIEW';

SELECT COUNT(*) AS cnt FROM vw_ExecutiveDashboard;
SELECT COUNT(*) AS cnt FROM vw_TimeSeries;
SELECT COUNT(*) AS cnt FROM vw_SocialAnalytics;
SELECT COUNT(*) AS cnt FROM vw_PlatformDaily;