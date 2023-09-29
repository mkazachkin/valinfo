SET PGCLIENTENCODING=utf-8
chcp 65001
SET psql_path="C:\Program Files\PostgreSQL\14\bin\psql.exe"
SET psql_script_name=valinfo_start_db.sql
SET psql_script_path=%~dp0
SET db_name=valuation_info_2023_1
SET run_options=-U Kaz_MYu -h 192.168.1.2 -d %db_name% -f
%psql_path% %run_options% %psql_script_path%%psql_script_name% 

