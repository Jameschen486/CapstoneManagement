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
  channel       integer REFERENCES channels(channelid) ON DELETE SET NULL
);


CREATE TABLE groups(
  groupid       serial PRIMARY KEY,
  ownerid       integer REFERENCES users(userid),
  groupname     varchar,
  assign        integer REFERENCES projects(projectid) ON DELETE SET NULL,
  channel       integer REFERENCES channels(channelid) ON DELETE SET NULL
);

CREATE TABLE grouprequests(
  userid        integer REFERENCES users(userid),
  groupid       integer REFERENCES groups(groupid) ON DELETE CASCADE
);

CREATE TABLE preferences (
  userid        integer REFERENCES users(userid) ON DELETE CASCADE,
  projectid     integer REFERENCES projects(projectid) ON DELETE CASCADE,
  rank          integer
);

CREATE TABLE skills (
  skillid       serial PRIMARY KEY,
  skillname     varchar
);

CREATE TABLE userskills (
  userid        integer REFERENCES users(userid) ON DELETE CASCADE,
  skillid       integer REFERENCES skills(skillid) ON DELETE CASCADE
);

CREATE TABLE projectskills (
  projectid     integer REFERENCES projects(projectid) ON DELETE CASCADE,
  skillid       integer REFERENCES skills(skillid) ON DELETE CASCADE
);

CREATE TABLE resetcodes (
  userid        integer REFERENCES users(userid) ON DELETE CASCADE,
  code          varchar,
  created       timestamp,
  PRIMARY KEY (userid)
);

CREATE TABLE notifications (
  notifid       serial PRIMARY KEY,
  userid        integer REFERENCES users(userid) ON DELETE CASCADE,
  created       timestamp,
  isnew         boolean,
  content       text
);

CREATE TABLE messages (
  messageid     serial PRIMARY KEY,
  channelid     integer REFERENCES channels(channelid) ON DELETE CASCADE,
  ownerid       integer REFERENCES users(userid) ON DELETE SET NULL,
  created       timestamp DEFAULT current_timestamp,
  content       text
);

CREATE TABLE accesschannels (
  channelid     integer REFERENCES channels(channelid) ON DELETE CASCADE,
  userid        integer REFERENCES users(userid) ON DELETE CASCADE
);

ALTER TABLE users ADD FOREIGN KEY (groupid) REFERENCES groups(groupid);

