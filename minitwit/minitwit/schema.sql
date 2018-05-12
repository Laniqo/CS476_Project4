drop table if exists user;
create table user (
  user_id GUID primary key,
  username text not null,
  email text not null,
  pw_hash text not null
);

drop table if exists follower;
create table follower (
  who_id GUID,
  whom_id GUID
);

drop table if exists message;
create table message (
  message_id integer primary key autoincrement,
  author_id GUID,
  text text not null,
  pub_date integer
);
