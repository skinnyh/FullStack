-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


--clean up and connect to database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\connect tournament

--create tables and view
CREATE TABLE players (
	id serial primary key,
	name text
);

CREATE TABLE matches (
	id serial primary key,
	winner integer references players (id),
	loser integer references players (id)
);

CREATE VIEW standings AS
SELECT p.id, name,
	(SELECT count(*) FROM matches WHERE winner = p.id) AS wins,
	(SELECT count(*) FROM matches WHERE p.id IN (winner, loser)) AS matches
FROM players p
ORDER BY wins DESC