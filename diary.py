#!/usr/bin/env python 

import datetime

class Diary():
    """This class contains functionality
    for a diary entry with date description and so on."""

    def __init__(self, year, month, day, hour=0, minute=0, title="", 
                 activity="", description="", id=None):
        """Initialization of object."""
        try:
            #if date is valid, else todays date is used.
            self.__date = datetime.date(year, month, day)
        except:
            self.__date = datetime.date.today()

        self.__hour = hour
        self.__minute = minute
        self.__title = title
        self.__activity = activity
        self.__desc = description

        if id:
            self.__id = id
        else:
            self.__id = None

    def year(self):
        """Returns year"""
        return self.__date.year

    def set_year(self, year):
        """Changes the year"""
        self.__date = datetime.date(year, self.__date.month, self.__date.day)

    def month(self):
        """Returns month"""
        return self.__date.month

    def set_month(self, month):
        """Changes the month"""
        self.__date = datetime.date(self.__date.year, month, self.__date.day)

    def day(self):
        """Returns day"""
        return self.__date.day

    def set_day(self, day):
        """Changes the day"""
        self.__date = datetime.date(self.__date.year, self.__date.month, day)

    def date(self):
        """Returns date"""
        return self.__date

    def date_str(self):
        """Returns date as a string in format YYYY-MM-DD:"""
        date_str = str(self.year()) + '-'

        if self.month() < 10:
            date_str += '0' + str(self.month())
        else:
            date_str += str(self.month())

        date_str += '-'

        if self.day() < 10:
            date_str += '0' + str(self.day())
        else:
            date_str += str(self.day())

        return date_str

    def set_date(self, date):
        """Changes the date"""
        self.__date = date

    def hour(self):
        """Returns hour"""
        return self.__hour

    def set_hour(self, hour):
        """Changes the hour"""
        self.__hour = hour

    def minute(self):
        """Returns minute"""
        return self.__minute

    def set_minute(self, minute):
        """Changes the minute"""
        self.__minute = minute

    def time_str(self):
        """Returns time as a string in format HH:MM."""
        time_str = ''
        
        if self.__hour < 10:
            time_str += '0'

        time_str += str(self.__hour) + ':'

        if self.__minute < 10:
            time_str += '0'

        time_str += str(self.__minute)
        return time_str

    def title(self):
        """Returns title"""
        return self.__title

    def set_title(self, title):
        """Changes the title"""
        self.__title = title

    def activity(self):
        """Returns activity"""
        return self.__activity

    def set_activity(self, activity):
        """Changes the activity"""
        self.__activity = activity

    def description(self):
        """Returns description"""
        return self.__desc

    def set_description(self, description):
        """Changes the description"""
        self.__desc = description

    def id(self):
        """Returns id"""
        return self.__id

    def set_id(self, id):
        """Changes the id"""
        self.__id = id

    def sql_insert_str(self):
        """Returns a string that is suitable
           to use with insert.
           Column names are asumed to be called 
           same as variable names.
           Use with INSERT INTO table_name plus 
           this string."""
        sql_str = "('year', 'month', 'day', 'hour', 'minute', 'title', 'activity', 'description') "
        sql_str += "VALUES ("
        sql_str += str(self.__date.year) + ', '
        sql_str += str(self.__date.month) + ', '
        sql_str += str(self.__date.day) + ', '
        sql_str += str(self.__hour) + ', '
        sql_str += str(self.__minute) + ', '
        sql_str += self.__title + ', '
        sql_str += self.__activity + ', '
        sql_str += self.__desc + ')'
        return sql_str

    def sql_insert_tuple(self):
        """Returns a tuple containing all
        values in the diary.
        Column order is:
        year, month, day, hour, minute, title, activity, description.
        Use with INSERT INTO."""
        return (self.year(), self.month(), self.day(), self.__hour, self.__minute,
                self.__title, self.__activity, self.__desc)
