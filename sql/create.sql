DROP DATABASE four2three1;
CREATE database four2three1; 

\c four2three1

CREATE TABLE player
( player_id INT PRIMARY KEY,
  p_name VARCHAR(20) NOT NULL,
  position VARCHAR(20) NOT NULL,
  agent_id INT,
  nat_team VARCHAR(20),
  club_name VARCHAR(20),
  salary INT NOT NULL,
  term INT NOT NULL,
  join_date DATE
);

CREATE TABLE stats
(
    player_id INT PRIMARY KEY,
    goals INT NOT NULL,
    assists INT NOT NULL,
    tackles INT NOT NULL,
    mins INT NOT NULL,
    duels_won INT NOT NULL
);

CREATE TABLE agent
(
    agent_id INT PRIMARY KEY,
    agent_name VARCHAR(20) NOT NULL,
    nationality VARCHAR(20) NOT NULL
);

CREATE TABLE national_team
(
    nat_name VARCHAR(20) PRIMARY KEY,
    captain_id INT,
    manager_id INT
);

CREATE TABLE manager
(
    manager_id INT PRIMARY KEY,
    mgr_name VARCHAR(20) NOT NULL,
    nationality VARCHAR(20) NOT NULL,
    salary INT NOT NULL,
    term INT NOT NULL,
    join_date date
);

CREATE TABLE clubs
(
    club_name VARCHAR(20) PRIMARY KEY,
    manager_id INT,
    city VARCHAR(20) NOT NULL,
    league VARCHAR(20) NOT NULL,
    stadium_name VARCHAR(20)
);

CREATE TABLE match
(
    match_id INT PRIMARY KEY,
    home_team VARCHAR(20),
    away_team VARCHAR(20),
    venue VARCHAR(20),
    league VARCHAR(20),
    score VARCHAR(10),
    match_date date
);

CREATE TABLE journalist
(
	j_name VARCHAR(20) PRIMARY KEY,
    article_id INT 
);

CREATE TABLE articles
(
    article_id INT PRIMARY KEY,
    publish_date date NOT NULL,
    publish_time time NOT NULL,
    info varchar
);

CREATE TABLE player_transfer
(
    transfer_id INT PRIMARY KEY,
    player_id INT, 
    from_club VARCHAR(20),
    to_club VARCHAR(20),
    transfer_fee INT NOT NULL,
    transfer_terms VARCHAR(100),
    agent_fee INT DEFAULT 0
);

CREATE TABLE our_user 
(
    usr_id INT PRIMARY KEY,
    username VARCHAR(20),
    dob date CHECK (dob < '2022-01-01')
);

CREATE TABLE user_player
(
    usr_id INT,
    player_id INT,
    PRIMARY KEY(usr_id,player_id)
);

CREATE TABLE user_club
(
    usr_id INT ,
    club_name VARCHAR(20),
    PRIMARY KEY(usr_id,club_name)
);

CREATE TABLE user_match
(
    usr_id INT,
    match_id INT,
    PRIMARY KEY(usr_id,match_id)
);

CREATE TABLE user_journalist
(
    usr_id INT ,
    journalist_name VARCHAR(20),
    PRIMARY KEY(usr_id,journalist_name)
);

CREATE TABLE user_nat_team
(
    usr_id INT,
    nat_name VARCHAR(20),
    PRIMARY KEY(usr_id,nat_name)
);
