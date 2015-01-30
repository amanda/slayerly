drop table if exists slayer;
create table slayer (
	id integer primary key autoincrement,
	url text not null,
	shortened text not null
);
