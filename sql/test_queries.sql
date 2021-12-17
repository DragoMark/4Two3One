/* displaying player records from a certain club */
SELECT * FROM player WHERE club_name='PSG';

/* Display matches of a certain club */
SELECT * FROM match WHERE home_team='PSG' OR away_team='PSG';

-- Display all transfers
SELECT * FROM player_transfer;

/* Display matches a user follows */
SELECT * FROM match as m WHERE m.match_id = 
(SELECT u.match_id FROM user_match as u WHERE u.usr_id=7002);

/* Return the club that the highest paid coach manages */
SELECT club_name FROM clubs 
WHERE manager_id = (SELECT manager_id FROM manager 
WHERE salary = (SELECT max(salary) FROM clubs NATURAL JOIN manager));

-- Return national team that the highest paid manager manages
SELECT nat_name FROM national_team
WHERE manager_id = (SELECT manager_id FROM manager 
WHERE salary = (SELECT max(salary) FROM national_team NATURAL JOIN manager));

-- Return goals scored by captain of national team for all users
SELECT u.usr_id,foo.captain_id,foo.nat_name,foo.goals from user_nat_team as u natural join 
(select n.captain_id,n.nat_name,s.goals from national_team as n, stats as s 
where n.captain_id = s.player_id) as foo;

CREATE USER admin WITH PASSWORD 'chu';
GRANT ALL PRIVILEGES ON DATABASE "four2three1" to admin;

CREATE USER statmaster WITH PASSWORD 'meLikesNumbers';
GRANT SELECT , INSERT , UPDATE ON TABLE "stats"
TO statmaster;


