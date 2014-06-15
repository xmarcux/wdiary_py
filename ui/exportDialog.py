#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.calendar
import autoSortListCtrl
import datetime
import os.path
import math
import string
import sys
import db

class ExportDialog(wx.Dialog):
    """
    This class is a dialog
    to export data to a text file.
    It is opened from Tool->Export entries... menu.
    """

    def __init__(self, *args, **kw):
        """Init method."""
        super(ExportDialog, self).__init__(*args, **kw)

        self.createView()
        self.SetTitle(_('Export'))

    def createView(self):
        """Method creates the view of the dialog."""
        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        mainLbl = wx.StaticText(panel, wx.ID_ANY, 
                                _('Export selected options to a specified text file'))
        mainSizer.Add(mainLbl, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(wx.StaticLine(panel, wx.ID_ANY), 0, wx.ALL | wx.EXPAND, 5)

        fileLbl = wx.StaticText(panel, wx.ID_ANY, _('Enter export file path:'))
        mainSizer.Add(fileLbl, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        fileSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fileInput = wx.TextCtrl(panel, wx.ID_ANY)
        fileSizer.Add(self.fileInput, 1, wx.ALL | wx.EXPAND, 5)
        browseBtn = wx.Button(panel, wx.ID_ANY, _('&Browse...'))
        self.Bind(wx.EVT_BUTTON, self.onBrowse, browseBtn)
        fileSizer.Add(browseBtn, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(fileSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.notebook = wx.Notebook(panel, wx.ID_ANY)
        self.pageDate = wx.Panel(self.notebook)
        self.notebook.AddPage(self.pageDate, _('&Date'))
        self.createDatePage()
        self.pageSearch = wx.Panel(self.notebook)
        self.notebook.AddPage(self.pageSearch, _('S&earch'))
        self.createSearchPage()
        mainSizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(wx.StaticLine(panel, wx.ID_ANY), 0, wx.ALL | wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        exportBtn = wx.Button(panel, wx.ID_ANY, _('&Export'))
        self.Bind(wx.EVT_BUTTON, self.onExport, exportBtn)
        buttonSizer.Add(exportBtn, 0, wx.ALL, 5)
        cancelBtn = wx.Button(panel, wx.ID_ANY, _('&Cancel'))
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)
        buttonSizer.Add(cancelBtn, 0, wx.ALL, 5)
        mainSizer.Add(buttonSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def createDatePage(self):
        """Creates content for date page view."""
        dateSizer = wx.BoxSizer(wx.VERTICAL)
        descLbl = wx.StaticText(self.pageDate, wx.ID_ANY,
                                _('Select day/week/month and choose with calendar:'))
        dateSizer.Add(descLbl, 0, wx.ALL | wx.EXPAND, 5)

        radioSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.radioDay = wx.RadioButton(self.pageDate, wx.ID_ANY, label=_('&Day'),
                                  style=wx.RB_GROUP)
        radioSizer.Add(self.radioDay, 1, wx.ALL, 5)
        self.radioWeek = wx.RadioButton(self.pageDate, wx.ID_ANY, label=_('&Week'))
        radioSizer.Add(self.radioWeek, 1, wx.ALL, 5)
        self.radioMonth = wx.RadioButton(self.pageDate, wx.ID_ANY, label=_('&Month'))
        radioSizer.Add(self.radioMonth, 1, wx.ALL, 5)
        dateSizer.Add(radioSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.calendar = wx.calendar.CalendarCtrl(self.pageDate, wx.ID_ANY, 
                                                 style=wx.calendar.CAL_MONDAY_FIRST |
                                                 wx.calendar.CAL_SHOW_HOLIDAYS)
        dateSizer.Add(self.calendar, 1, wx.ALL | wx.EXPAND, 5)

        self.pageDate.SetSizer(dateSizer)

    def createSearchPage(self):
        """Creates content for search page view."""
        searchSizer = wx.BoxSizer(wx.VERTICAL)
        searchLbl = wx.StaticText(self.pageSearch, wx.ID_ANY, _('Enter serach text:'))
        searchSizer.Add(searchLbl, 0, wx.ALL | wx.EXPAND, 5)

        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.searchTxt = wx.TextCtrl(self.pageSearch, wx.ID_ANY)
        inputSizer.Add(self.searchTxt, 1, wx.ALL | wx.EXPAND, 5)
        searchBtn = wx.Button(self.pageSearch, wx.ID_ANY, _('&Search'))
        self.Bind(wx.EVT_BUTTON, self.onSearch, searchBtn)
        inputSizer.Add(searchBtn, 0, wx.ALL, 5)
        searchSizer.Add(inputSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.searchResult = autoSortListCtrl.AutoSortListCtrl(self.pageSearch)
        searchSizer.Add(self.searchResult, 1, wx.ALL | wx.EXPAND, 5)

        self.pageSearch.SetSizer(searchSizer)

    def onBrowse(self, event):
        """Is triggered when browse button is clicked."""
        fileDialog = wx.FileDialog(self, 'Choose export file:', '', '', '*', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return

        self.fileInput.SetValue(fileDialog.GetPath())

    def onSearch(self, event):
        """Is triggered when search button is clicked."""
        
        items = db.db_connection.search_db(self.searchTxt.GetValue())
        items = dict(zip(range(1, len(items) + 1), items))
        items = items.items()
        mapDict = {}
        self.searchResult.DeleteAllItems()
        for key, data in items:
            i = self.searchResult.InsertStringItem(sys.maxint, data.date_str())
            self.searchResult.SetStringItem(i, 1, data.time_str())
            self.searchResult.SetStringItem(i, 2, data.title())
            self.searchResult.SetStringItem(i, 3, data.description())
            self.searchResult.SetItemData(i, key)
            mapDict[key] = (data.date_str(), data.time_str(), data.title(), data.description())

        self.searchResult.itemDataMap = mapDict
        

    def onExport(self, event):
        """Is triggered when export button is clicked."""
        
        if self.fileInput.GetValue() == "":
            dialog = wx.MessageDialog(self, _('Please specify file name.'), 
                                      _('No file name'), wx.OK | wx.ICON_WARNING)
            dialog.ShowModal()
        else:
            if self.notebook.GetSelection() == 0:
                date = self.calendar.GetDate()
                startdate = datetime.date(date.GetYear(), date.GetMonth() + 1, date.GetDay())
                if self.radioDay.GetValue():
                    enddate = startdate
                elif self.radioWeek.GetValue():
                    startdate = datetime.date(startdate.year, startdate.month,
                                              startdate.day - startdate.weekday())
                    enddate = datetime.date(startdate.year, startdate.month, 
                                            startdate.day + 6)
                else:
                    startdate = datetime.date(startdate.year, startdate.month, 1)
                    if (startdate.month == 4 or startdate.month == 6 or
                        startdate.month == 9 or startdate.month == 11):
                        enddate = datetime.date(startdate.year, startdate.month, 30)
                    elif startdate.month == 2:
                        if (startdate.year % 4) == 0:
                            enddate = datetime.date(startdate.year, startdate.month, 29)
                        else:
                            enddate = datetime.date(startdate.year, startdate.month, 28)
                    else:
                        enddate = datetime.date(startdate.year, startdate.month, 31)

                diaries = db.db_connection.search_db_date(startdate, enddate)
                self.__export_to_file(self.fileInput.GetValue(), diaries, startdate, enddate)
            else:
                diaries = db.db_connection.search_db(self.searchTxt.GetValue())
                self.__export_to_file(self.fileInput.GetValue(), diaries, '', '')


    def __export_to_file(self, filename, diaries, startdate, enddate):
        """
        Exports all diaries in a formated way
        to specified file in filename.
        Warns user if file already exists
        or if error occures.
        """

        date = datetime.datetime.now().isoformat(' ')
        if os.path.exists(filename):
            dialog = wx.MessageDialog(self, _('File already exists.\nDo you want to replace it?'),
                                      _('File exists'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
            if dialog.ShowModal() == wx.ID_NO:
                return

        write_str = '*' * 90 + '\n'
        write_str += '*' + (' ' * 35) + 'Export from WDiary' + (' ' * 35) + '*' + '\n'
        write_str += '*' + (' ' * 31) + date + (' ' * 31) + '*' + '\n'
        write_str += '*' * 90 + '\n'

        if self.notebook.GetSelection() == 0:
            write_str += '*' + (' ' *37) + 'Export by date' + (' ' * 37) + '*' + '\n'
            write_str += '*' + (' ' * 26) + 'Diary entries from date: ' + str(startdate.year) + '-'
            if startdate.month < 10:
                write_str += '0' + str(startdate.month)
            else:
                write_str += str(startdate.month)
            write_str += '-'
            if startdate.day < 10:
                write_str += '0' + str(startdate.day)
            else:
                write_str += str(startdate.day)
            write_str += (' ' *27) + '*' + '\n'

            write_str += '*' + (' ' * 26) + 'Diary entries to date: ' + str(enddate.year) + '-'
            if enddate.month < 10:
                write_str += '0' + str(enddate.month)
            else:
                write_str += str(enddate.month)
            write_str += '-'
            if enddate.day < 10:
                write_str += '0' + str(enddate.day)
            else:
                write_str += str(enddate.day)
            write_str += (' ' * 29) + '*' + '\n'
        else:
            write_str += '*' + (' ' * 32) + 'Export by search string' + (' ' * 33) + '*' + '\n'
            search_str = self.searchTxt.GetValue()
            search_str_nl = ""
            times_bks_left = int(math.floor((88 - len(search_str) - 32)/2))
            times_bks_right = 88 - 32 - len(search_str) - times_bks_left 
            if times_bks_left <= 0:
                times_bks_left = 28
                times_bks_right = 28
                if len(search_str) > 85:
                    search_str_nl = search_str[:85] + '...'
                else:
                    search_str_nl = search_str
                search_str = ""

            write_str += ('*' + (' ' * times_bks_left) + 'Diary entries for search string:' + 
                          search_str + (' ' * times_bks_right) + '*' + '\n')
            if search_str_nl:
                no_blank = 88 - len(search_str_nl)
                write_str += '*' + search_str_nl + (' ' * no_blank) + '*' + '\n'

        write_str += '*' * 90 + '\n'
        write_str += '\n' + '*' * 90 + '\n'
        write_str += '*' + (' ' * 37) + 'Diary entries:' + ( ' ' * 37) + '*\n'
        write_str += '*' * 90 + '\n\n'

        write_str += self.__diary_export_str(diaries)
        write_str += '\n\n\n' + ('*' * 38) + 'End of export' + ('*' * 39)

        try:
            abs_path = os.path.abspath(filename)
            abs_path = abs_path[:abs_path.rfind(os.sep)+1]
            if not os.path.exists(abs_path):
                os.makedirs(abs_path) 

            file = open(filename, 'w')
            file.write(write_str)
            file.flush()
            file.close()
        except Exception, e:
            dialog = wx.MessageDialog(self, _('Error writing to file: ') + '\n' + repr(e), 
                                      _('File error'), wx.OK | wx.ICON_ERROR)
            dialog.ShowModal()
            return

        dialog = wx.MessageDialog(self, _('Successfully exported diaries to:') + '\n' +
                                  os.path.abspath(filename), _('Successfull export'), 
                                  wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        self.Destroy()

    def __diary_export_str(self, diaries):
        """Function takes a list of diaries 
           and append the diaries in a formated
           way on to the append_str.
           Appended string is returned."""

        str = ""
        for d in diaries:
            str += '*' * 90 + '\n'
            str += 'Date: ' + d.date_str() + '\n'
            str += 'Time: ' + d.time_str() + '\n'
            str += 'Title: ' + self.__format_multirows(d.title()) + '\n'
            str += 'Activity: ' + self.__format_multirows(d.activity()) + '\n'
            str += 'Description: ' + self.__format_multirows(d.description()) + '\n' 

        str += '*' * 90 + '\n'
        return str

    def __format_multirows(self, str):
        """Formats given string into
           multiple rows.
           New string is returned."""

        tmp_str = str
        if len(str) <= 76:
            return tmp_str

        rows = tmp_str.split('\n')
        i = 0
        for r in rows:
            tot_row = ""
            rest = r
            while len(rest) > 90:
            #if len(r) > 90:
                if (rest.rfind(' ') != -1 and
                    rest.rfind(' ') > 90):
                    tmp1 = rest[:90]
                    tmp2 = rest[90:]
                    tot_row += tmp1[:tmp1.rfind(' ') + 1] + '\n'
                    rest = tmp1[tmp1.rfind(' '):] + tmp2
                else:
                    tot_row = r[:91] + '\n' 
                    rest = r[90:]
            rows[i] = tot_row + rest
            i += 1

        tmp_str = '\n' + string.join(rows, '\n')
        return tmp_str

    def onCancel(self, event):
        """Is triggered when cancel button is clicked."""
        self.Destroy()
