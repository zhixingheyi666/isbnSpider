-- -- truncate table preIsbn;
-- select * from preisbn;


-- '验证replace函数的用法'
-- select replace(isbn,'-','') from attbooklist;
-- select bl.isbn, bl.title, pr.isbn from attbooklist bl, preisbn pr where pr.isbn = replace(bl.isbn,'-','');

-- select * from booklist;
-- select * from attbooklist;
-- select * into atttt from attbooklist where id >1000;
-- select * from atttt;
-- delete from attbooklist where id=67;

-- -------------------------------------------------------------------------------------
-- select * from lendwork where loperator = '王_00';
-- delete  from lendwork where loperator = '王_00';