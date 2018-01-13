use  spider;
create table if not exists originurl 
(	url_id int  not null auto_increment,
	url char(255) not null,
    stars int default 0,
    primary key ( url_id )
) engine = myisam;
insert into originurl( url ) values( 'test http' );
delete from originurl where url_id != 1;
select  count(url) , count( distinct url) from originurl;
select * from originurl;