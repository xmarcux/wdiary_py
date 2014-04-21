#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.calendar
import autoSortListCtrl

"""
This class is a dialog
to export data to a text file.
It is opened from Tool->Export entries... menu.
"""
class ExportDialog(wx.Dialog):

    """Init method."""
    def __init__(self, *args, **kw):
        super(ExportDialog, self).__init__(*args, **kw)

        self.createView()
        self.SetTitle(_('Export'))

    """Method creates the view of the dialog."""
    def createView(self):
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

        notebook = wx.Notebook(panel, wx.ID_ANY)
        self.pageDate = wx.Panel(notebook)
        notebook.AddPage(self.pageDate, _('&Date'))
        self.createDatePage()
        self.pageSearch = wx.Panel(notebook)
        notebook.AddPage(self.pageSearch, _('S&earch'))
        self.createSearchPage()
        mainSizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)

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

    """Creates content for date page view."""
    def createDatePage(self):
        dateSizer = wx.BoxSizer(wx.VERTICAL)
        descLbl = wx.StaticText(self.pageDate, wx.ID_ANY,
                                _('Select day/week/month and choose with calendar:'))
        dateSizer.Add(descLbl, 0, wx.ALL | wx.EXPAND, 5)

        radioSizer = wx.BoxSizer(wx.HORIZONTAL)
        radioDay = wx.RadioButton(self.pageDate, wx.ID_ANY, label=_('&Day'),
                                  style=wx.RB_GROUP)
        radioSizer.Add(radioDay, 1, wx.ALL, 5)
        radioWeek = wx.RadioButton(self.pageDate, wx.ID_ANY, label=_('&Week'))
        radioSizer.Add(radioWeek, 1, wx.ALL, 5)
        radioMonth = wx.RadioButton(self.pageDate, wx.ID_ANY, label=_('&Month'))
        radioSizer.Add(radioMonth, 1, wx.ALL, 5)
        dateSizer.Add(radioSizer, 0, wx.ALL | wx.EXPAND, 5)

        calendar = wx.calendar.CalendarCtrl(self.pageDate, wx.ID_ANY, 
                                            style=wx.calendar.CAL_MONDAY_FIRST |
                                            wx.calendar.CAL_SHOW_HOLIDAYS)
        dateSizer.Add(calendar, 1, wx.ALL | wx.EXPAND, 5)

        self.pageDate.SetSizer(dateSizer)

    """Creates content for search page view."""
    def createSearchPage(self):
        searchSizer = wx.BoxSizer(wx.VERTICAL)
        searchLbl = wx.StaticText(self.pageSearch, wx.ID_ANY, _('Enter serach text:'))
        searchSizer.Add(searchLbl, 0, wx.ALL | wx.EXPAND, 5)

        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.searchTxt = wx.TextCtrl(self.pageSearch, wx.ID_ANY)
        inputSizer.Add(self.searchTxt, 1, wx.ALL | wx.EXPAND, 5)
        searchBtn = wx.Button(self.pageSearch, wx.ID_ANY, _('&Search'))
        inputSizer.Add(searchBtn, 0, wx.ALL, 5)
        searchSizer.Add(inputSizer, 0, wx.ALL | wx.EXPAND, 5)

        searchResult = autoSortListCtrl.AutoSortListCtrl(self.pageSearch)
        searchSizer.Add(searchResult, 1, wx.ALL | wx.EXPAND, 5)

        self.pageSearch.SetSizer(searchSizer)

    """Is triggered when browse button is clicked."""
    def onBrowse(self, event):
        fileDialog = wx.FileDialog(self, 'Choose export file:', '', '', '*', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return

        self.fileInput.SetValue(fileDialog.GetPath())

    """Is triggered when export button is clicked."""
    def onExport(self, event):
        print('Export...')
        self.Destroy()

    """Is triggered when cancel button is clicked."""
    def onCancel(self, event):
        self.Destroy()
