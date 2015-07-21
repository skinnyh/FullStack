#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def updateDB(cmd):
    """Connect to DB and do update query"""
    db = connect()
    cursor = db.cursor()
    cursor.execute(cmd)
    db.commit()
    db.close()


def deleteMatches():
    """Remove all the match records from the database."""
    query = "DELETE FROM matches"
    db = connect()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    query = "DELETE FROM players"
    db = connect()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT count(*) FROM players"
    db = connect()
    cursor = db.cursor()
    cursor.execute(query)
    ret = cursor.fetchone()
    db.close()
    return int(ret[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    name = bleach.clean(name)  # avoid script injection
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))  # avoid SQL injection
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = "SELECT * FROM standings"
    db = connect()
    cursor = db.cursor()
    cursor.execute(query)
    ret = cursor.fetchall()
    db.close()
    return ret


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    ret = []
    for i in range(0, len(standings), 2):
        pair = (standings[i][0], standings[i][1], standings[i + 1][0], standings[i + 1][1])
        ret.append(pair)
    return ret
