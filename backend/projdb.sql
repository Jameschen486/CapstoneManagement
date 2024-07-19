CREATE TABLE channels (
  channelid     serial PRIMARY KEY,
  channelname   varchar
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
  rank          integer
);

CREATE TABLE skills (
  skillid       serial PRIMARY KEY,
  skillname     varchar
);

CREATE TABLE userskills (
  userid        integer REFERENCES users(userid),
  skillid       integer REFERENCES skills(skillid)
);

CREATE TABLE projectskills (
  projectid     integer REFERENCES projects(projectid),
  skillid       integer REFERENCES skills(skillid)
);

CREATE TABLE resetcodes (
  userid        integer REFERENCES users(userid) PRIMARY KEY,
  code          varchar,
  created       timestamp
);

CREATE TABLE notifications (
  notifid       serial PRIMARY KEY,
  userid        integer REFERENCES users(userid),
  created       timestamp,
  isnew         boolean,
  content       text
);

CREATE TABLE messages (
  messageid     serial PRIMARY KEY,
  channelid     integer REFERENCES channels(channelid),
  ownerid       integer REFERENCES users(userid),
  created       timestamp,
  content       text
);

CREATE TABLE accesschannels (
  channelid     integer REFERENCES channels(channelid),
  userid        integer REFERENCES users(userid)
);

ALTER TABLE users ADD FOREIGN KEY (groupid) REFERENCES groups(groupid);

