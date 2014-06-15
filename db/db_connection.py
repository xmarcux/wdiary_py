#!/usr/bin/env python

import sqlite3
import diary
import os
import cPickle

def init_db():
    """Initializes the database.
    If correct tables does not exist
    they will be created."""

    conn = sqlite3.connect('db' + os.sep + 'wdiary.db')
    cur = conn.cursor()

    #create main table
    cur.execute("""CREATE TABLE IF NOT EXISTS diary
                   (diaryID INTEGER PRIMARY KEY AUTOINCREMENT, year INT, month INT, day INT, 
                    hour INT, minute INT, title text, activity text, description text)""")
    conn.commit()
    conn.close()


def save_to_db(d):
    """Saves the diary to database.
    If diary already exists it will be updated."""

    conn = sqlite3.connect('db' + os.sep + 'wdiary.db')
    cur = conn.cursor()

    if not d.id():
        cur.execute("""INSERT INTO diary (year, month, day, hour, minute, title, activity, description)
                       VALUES (?,?,?,?,?,?,?,?)""", d.sql_insert_tuple())
    else:
        cur.execute("""UPDATE diary SET 
                       year = ?, month = ?, day = ?, hour = ?, minute = ?,
                       title = ?, activity = ?, description = ?
                       WHERE diaryID == ?""", d.sql_insert_tuple() + (d.id(),))

    conn.commit()
    conn.close()

def delete_from_db(d):
    """Deletes the diary from database.
    If diary does not exist, nothing happens."""

    conn = sqlite3.connect('db' + os.sep + 'wdiary.db')
    cur = conn.cursor()

    if d.id():
        cur.execute("""DELETE FROM diary WHERE diaryID == ?""", (d.id(),))

    conn.commit()
    conn.close()

def search_db(search_str):
    """Searches the diary table.
    All diaries where  title, activity or description 
    contains search string is returned in a list of Diary."""

    conn = sqlite3.connect('db' + os.sep + 'wdiary.db')
    cur = conn.cursor()

    search_str = '%' + search_str + '%'
    l_diary = []
    for row in cur.execute("""SELECT * FROM diary 
                              WHERE title LIKE ?
                              OR activity LIKE ?
                              OR description LIKE ?""", (search_str, search_str, search_str)):
        l_diary.append(diary.Diary(row[1], row[2], row[3], row[4], 
                                   row[5], row[6], row[7], row[8], row[0]))

    conn.close()
    return l_diary

def search_db_date(startdate, enddate):
    """Searches the diary table.
    All diaries between and including start-
    and enddate is returned as a list of Diary."""

    syear = startdate.year
    smonth = startdate.month
    sday = startdate.day

    eyear = enddate.year
    emonth = enddate.month
    eday = enddate.day

    conn = sqlite3.connect('db' + os.sep + 'wdiary.db')
    cur = conn.cursor()

    l_diary = []

    if syear == eyear and smonth == emonth:
        for row in cur.execute("""SELECT * FROM diary WHERE
                                  year == ?
                                  AND month == ?
                                  AND day >= ?
                                  AND day <= ?""", (syear, smonth, sday, eday)):
            l_diary.append(diary.Diary(row[1], row[2], row[3], row[4], 
                                       row[5], row[6], row[7], row[8], row[0]))

    if syear == eyear and smonth < emonth:
        for row in cur.execute("""SELECT * FROM diary WHERE
                                  year == ?
                                  AND month == ?
                                  AND day >= ?""", (syear, smonth, sday)):
            l_diary.append(diary.Diary(row[1], row[2], row[3], row[4], 
                                       row[5], row[6], row[7], row[8], row[0]))

        for row in cur.execute("""SELECT * FROM diary WHERE
                                  year == ?
                                  AND month > ?
                                  AND month < ?""", (syear, smonth, emonth)):
            l_diary.append(diary.Diary(row[1], row[2], row[3], row[4],
                                       row[5], row[6], row[7], row[8], row[0]))

        for row in cur.execute("""SELECT * FROM diary WHERE
                                  year == ?
                                  AND month == ?
                                  AND day <= ?""", (eyear, emonth, eday)):
            l_diary.append(diary.Diary(row[1], row[2], row[3], row[4],
                                       row[5], row[6], row[7], row[8], row[0]))

    if syear < eyear:
        for row in cur.execute("""SELECT * FROM diary WHERE
                                  (year == ?
                                  AND month == ?
                                  AND day >= ?)
                                  OR
                                  (year == ?
                                   AND month > ?)
                                  OR
                                  (year > ?
                                   AND year < ?)
                                  OR
                                  (year == ?
                                   AND month < ?)
                                  OR
                                  (year == ?
                                   AND month == ?
                                   AND day <= ?)""", 
                               (syear, smonth, sday, syear, smonth, syear, eyear, 
                               eyear, emonth, eyear, emonth, eday)):
            l_diary.append(diary.Diary(row[1], row[2], row[3], row[4], 
                                   row[5], row[6], row[7], row[8], row[0]))

    conn.close()
    return l_diary

def save_properties(properties):
    """
    Saves properties for application.
    Properties are ordered as a dict
    and saved to file as a pickle.
    """

    file = open('db' + os.sep + 'wdiary.properties', 'w')
    cPickle.dump(properties, file)
    file.close()

def read_properties():
    """
    Read propeties file and 
    returns properties object that was saved.
    Should be a dict.
    """

    try:
        file = open('db' + os.sep + 'wdiary.properties')
        properties = cPickle.load(file)
        file.close()
    except:
        properties = {}

    return properties

def save_titles(titles):
    """
    Saves titles to be reused in main window.
    Titles are ordered in a list and
    saved to file as a pickle.
    """

    file = open('db' + os.sep + 'wdiary.titles', 'w')
    cPickle.dump(titles, file)
    file.close()

def read_titles():
    """
    Read titles file and
    returns title objects that was saved.
    Should be a list.
    """

    try:
        file = open('db' + os.sep + 'wdiary.titles')
        titles = cPickle.load(file)
        file.close()
    except:
        titles = []

    return titles

def save_activities(activity):
    """
    Saves activities to be reused in main window.
    Activities are oredered in a list and
    saved to file as a pickle.
    """

    file = open('db' + os.sep + 'wdiary.activities', 'w')
    cPickle.dump(activity, file)
    file.close()

def read_activities():
    """
    Read activities file and
    returns activity objects that was saved.
    Should be a list.
    """

    try:
        file = open('db' + os.sep + 'wdiary.activities')
        activity = cPickle.load(file)
        file.close()
    except:
        activity = []

    return activity
