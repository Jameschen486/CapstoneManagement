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
  projectname   varchar,
  ownerid       integer REFERENCES users(userid),
  title         text,
  clients       text,
  specials      text,
  groupcount    text,
  background    text,
  reqs          text,
  reqKnowledge  text,
  outcomes      text,
  supervision   text,
  additional    text,
  channel       integer REFERENCES channels(channelid)
);


CREATE TABLE groups(
  groupid       serial PRIMARY KEY,
  ownerid       integer REFERENCES users(userid),
  groupname     varchar,
  assign        integer REFERENCES projects(projectid) ON DELETE SET NULL,
  channel       integer REFERENCES channels(channelid)
);

CREATE TABLE grouprequests(
  userid        integer REFERENCES users(userid),
  groupid       integer REFERENCES groups(groupid)
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

