-- -- truncate table preIsbn;
-- select * from preisbn;
-- select count(*) from abkbooklist;


-- '��֤replace�������÷�'
-- select replace(isbn,'-','') from attbooklist;
-- select bl.isbn, bl.title, pr.isbn from attbooklist bl, preisbn pr where pr.isbn = replace(bl.isbn,'-','');

-- '��ÿ�λ�ȡ���鼮�ı�Ŀ��Ϣ���뵽������Ŀ����ȥ��ͬʱselect into�����ݱ�abklistbook��, Ȼ��ǵ����attbooklist�������ظ�'
-- insert into booklist(adds, BCid, Caste, Epitome,  extName, ISBN, keyword, PageMode, Pages, Price, PubID, publish, PublishDate, Title, translator, Version, Writer) 
-- 	select adds, BCid, Caste, Epitome,  extName, ISBN, keyword, PageMode, Pages, Price, PubID, publish, PublishDate, Title, translator, Version, Writer from attbooklist;
-- insert into abkbooklist(adds, BCid, Caste, Epitome,  extName, ISBN, keyword, PageMode, Pages, Price, PubID, publish, PublishDate, Title, translator, Version, Writer)
-- 	select adds, BCid, Caste, Epitome,  extName, ISBN, keyword, PageMode, Pages, Price, PubID, publish, PublishDate, Title, translator, Version, Writer from attbooklist;

-- -- truncate attbooklist;


-- '��ѯһ�������е�����'
-- select name from syscolumns where id=(select max(id) from sysobjects where xtype='u' and name='attbooklist')

-- select * from booklist;
-- select * from attbooklist;
-- select * into atttt from attbooklist where id >1000;
-- select * from atttt;
-- delete from attbooklist where id=67;

-- -------------------------------------------------------------------------------------
-- select * from lendwork where loperator = '��_00';
-- delete  from lendwork where loperator = '��_00';