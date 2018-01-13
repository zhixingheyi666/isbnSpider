use fortest;
select * from bookmurl 
	where utext regexp '正则';
select line from fline_code where hashid = 29;
select namepath from fmate_code where hashid in (select hashid from fline_code where line regexp 'sys.path');
select hashid from fline_code where line regexp 'sys.path';
select hashid ,line from fline_code where line regexp 'connSql';
select line ,hashid from fline_code where line regexp 'href';
SELECT * FROM fortest.bookmurl;
select  count(distinct url )  from fortest.bookmurl ;-- where url regexp 'github';
select  distinct url  from fortest.bookmurl where url regexp 'github';
select  distinct *  from fortest.bookmurl order by url;