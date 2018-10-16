-- -- truncate table preIsbn;
-- select * from preisbn;
-- select count(*) from abkbooklist;


-- '验证replace函数的用法'
-- select replace(isbn,'-','') from attbooklist;
-- select bl.isbn, bl.title, pr.isbn from attbooklist bl, preisbn pr where pr.isbn = replace(bl.isbn,'-','');

-- '将每次获取的书籍的编目信息并入到辅助编目库中去，同时select into到备份表abklistbook中, 然后记得清空attbooklist，避免重复'
-- insert into booklist(adds, BCid, Caste, Epitome,  extName, ISBN, keyword, PageMode, Pages, Price, PubID, publish, PublishDate, Title, translator, Version, Writer) 
-- 	select adds, BCid, Caste, Epitome,  extName, ISBN, keyword, PageMode, Pages, Price, PubID, publish, PublishDate, Title, translator, Version, Writer from attbooklist;
-- insert into abkbooklist(adds, BCid, Caste, Epitome,  extName, ISBN, keyword, PageMode, Pages, Price, PubID, publish, PublishDate, Title, translator, Version, Writer)
-- 	select adds, BCid, Caste, Epitome,  extName, ISBN, keyword, PageMode, Pages, Price, PubID, publish, PublishDate, Title, translator, Version, Writer from attbooklist;

-- -- truncate attbooklist;


-- '查询一个表所有的列名'
-- select name from syscolumns where id=(select max(id) from sysobjects where xtype='u' and name='attbooklist')

-- select * from booklist;
-- select * from attbooklist;
-- select * into atttt from attbooklist where id >1000;
-- select * from atttt;
-- delete from attbooklist where id=67;

-- -------------------------------------------------------------------------------------
-- select * from lendwork where loperator = '王_00';
-- delete  from lendwork where loperator = '王_00';