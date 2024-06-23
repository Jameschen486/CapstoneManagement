CREATE TABLE channels (
  channelid     serial PRIMARY KEY
);

CREATE TABLE users (
  userid        serial PRIMARY KEY,
  email         varchar NOT NULL,
  firstName     varchar,
  lastName      varchar,
  password      varchar,
  role          integer,
  groupid       integer
);

CREATE TABLE projects (
  projectid     serial PRIMARY KEY,
  ownerid       integer REFERENCES users(userid),
  channel       integer REFERENCES channels(channelid),
  groupno       varchar,
  spec          text,
  description   text,
  req           text,
  reqKnowledge  text,
  outcomes      text,
  additional    text
);


CREATE TABLE groups(
  groupid       serial PRIMARY KEY,
  groupowner    integer REFERENCES users(userid),
  groupname     varchar,
  assign        integer REFERENCES projects(projectid),
  channel       integer REFERENCES channels(channelid)
);


CREATE TABLE preferences (
  userid        integer REFERENCES users(userid),
  projectid     integer REFERENCES projects(projectid),
  level         integer
);

CREATE TABLE notifications (
  notifid       serial PRIMARY KEY,
  userid        integer REFERENCES users(userid),
  content       text
);

CREATE TABLE messages (
  messageid     serial PRIMARY KEY,
  channelid     integer REFERENCES channels(channelid),
  ownerid       integer REFERENCES users(userid),
  content       text,
  posttime      timestamp
);

CREATE TABLE accesschannels (
  channelid     integer REFERENCES channels(channelid),
  userid        integer REFERENCES users(userid)
);

ALTER TABLE users ADD FOREIGN KEY (groupid) REFERENCES groups(groupid);

