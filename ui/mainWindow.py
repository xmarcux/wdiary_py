#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import datetime
import sys
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin

import editDiaryDialog
import optionDialog
import exportDialog
import autoSortListCtrl

import db.db_connection
import diary

class MainWindow (wx.Frame):
    """Main Window for application."""

    def __init__(self):
        """Init function"""

        wx.Frame.__init__(self, None, title=_('WDiary'), size=(400, 200))
        
        self.CreateStatusBar()

        self.SetMenuBar(self.createMenu())
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.createSizers()
        self.createTopView()
        self.createBottomView()
        self.createBottomListView()

        self.setupAboutInfo()

        image = wx.Image('img/wdiary.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(image)
        self.SetIcon(icon)

        """Init flags for saving a diary."""
        self.hourComboValueOk = False
        self.minComboValueOk = False
        self.titleComboValueOk = False
        self.actComboValueOk = False
        self.dateCtrlValueOk = False

        self.panel.SetSizerAndFit(self.mainSizer)
        self.Fit()
        self.SetMinSize(self.GetEffectiveMinSize())
        self.Center()
        self.Show(True)

    def createMenu(self):
        """ Function that creates menu."""

        # Create file menu
        fileMenu = wx.Menu()
        fileExit = fileMenu.Append(wx.ID_EXIT, _('E&xit'), _('Terminate application'))
        self.Bind(wx.EVT_MENU, self.onExit, fileExit)        

        # Create tools menu
        toolsMenu = wx.Menu()
        exportTools = toolsMenu.Append(wx.ID_ANY, _('&Export entries...\tCtrl+E'), 
                                       _('Export selected items to a textfile.'))
        self.Bind(wx.EVT_MENU, self.onExport, exportTools)

        toolsMenu.AppendSeparator()
        optionTools = toolsMenu.Append(wx.ID_ANY, _('&Options...\tCtrl+O'), 
                                       _('Change behavior for application.'))
        self.Bind(wx.EVT_MENU, self.onOptions, optionTools)

        # Create help menu
        helpMenu = wx.Menu()
        aboutHelp = helpMenu.Append(wx.ID_ABOUT, _('&About WDiary...\tCtrl+A'),
                                      _('Information about application.'))
        self.Bind(wx.EVT_MENU, self.onAbout, aboutHelp)
        
        # Create menubar
        menubar = wx.MenuBar()
        menubar.Append(fileMenu, _('&File'))
        menubar.Append(toolsMenu, _('&Tools'))
        menubar.Append(helpMenu, _('&Help'))

        # Create accelerator table
        exportKeyId = wx.NewId()
        optionKeyId = wx.NewId()
        aboutKeyId = wx.NewId()

        self.Bind(wx.EVT_MENU, self.onExport, id=exportKeyId)
        self.Bind(wx.EVT_MENU, self.onOptions, id=optionKeyId)
        self.Bind(wx.EVT_MENU, self.onAbout, id=aboutKeyId)

        self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('E'), exportKeyId),
                                              (wx.ACCEL_CTRL, ord('O'), optionKeyId),
                                              (wx.ACCEL_CTRL, ord('A'), aboutKeyId)])

        return menubar

    def createSizers(self):
        """Create containers for widgets"""

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        box = wx.StaticBox(self.panel, wx.ID_ANY, _('Add new diary entry:'))
        self.topSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bottomBox = wx.StaticBox(self.panel, wx.ID_ANY, _('Current diary entries:'))
        self.bottomSizer = wx.StaticBoxSizer(bottomBox, wx.VERTICAL)
        
        self.mainSizer.Add(self.topSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(self.bottomSizer, 1, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)

    def createTopView(self):
        """Creates items for the upper view in main window."""

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        descSizer = wx.BoxSizer(wx.VERTICAL)
        inputSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer.Add(hSizer, 1, wx.EXPAND)
        hSizer.Add(descSizer, 0, wx.EXPAND)
        hSizer.Add(inputSizer, 1, wx.EXPAND)

        desc_date = wx.StaticText(self.panel, wx.ID_ANY, _('Date:'))
        descSizer.Add(desc_date, 1, wx.ALL | wx.EXPAND, 5)
        self.dateCtrl = wx.DatePickerCtrl(self.panel, wx.ID_ANY)
        self.Bind(wx.EVT_DATE_CHANGED, self.onDateChanged, self.dateCtrl)
        inputSizer.Add(self.dateCtrl, 1, wx.ALL | wx.EXPAND, 5)

        desc_hour = wx.StaticText(self.panel, wx.ID_ANY, _('Hour:'))
        descSizer.Add(desc_hour, 1, wx.ALL | wx.EXPAND, 5)
        hours = []
        for h in range(25):
            hours.append(str(h))
        self.hourCombo = wx.ComboBox(self.panel, wx.ID_ANY, style=wx.CB_READONLY, value=hours[0], choices=hours)
        self.Bind(wx.EVT_TEXT, self.onHourChange, self.hourCombo)

        desc_min = wx.StaticText(self.panel, wx.ID_ANY, _('Minute:'))
        min = []
        for m in range(0, 60, 5):
            min.append(str(m))
        self.minCombo = wx.ComboBox(self.panel, wx.ID_ANY, style=wx.CB_READONLY, value=min[0], choices=min)
        self.Bind(wx.EVT_TEXT, self.onMinuteChange, self.minCombo)
        timeSizer = wx.BoxSizer(wx.HORIZONTAL)
        timeSizer.Add(self.hourCombo, 0, wx.ALL, 5)
        timeSizer.Add(desc_min, 0, wx.ALL, 5)
        timeSizer.Add(self.minCombo, 0, wx.ALL, 5)
        inputSizer.Add(timeSizer, 1)

        descTitle = wx.StaticText(self.panel, wx.ID_ANY, _('Title:'))
        descSizer.Add(descTitle, 1, wx.ALL | wx.EXPAND, 5)

        titleItems = db.db_connection.read_titles()
        self.titleCombo = wx.ComboBox(self.panel, wx.ID_ANY, choices=titleItems)
        self.Bind(wx.EVT_TEXT, self.onTitleChange, self.titleCombo)
        inputSizer.Add(self.titleCombo, 1, wx.ALL | wx.EXPAND, 5)

        descAct = wx.StaticText(self.panel, wx.ID_ANY, _('Activity:'))
        descSizer.Add(descAct, 1, wx.ALL | wx.EXPAND, 5)

        act = db.db_connection.read_activities()
        #act = [_('Documentation'), _('Project leading'), _('Programming'), _('Graphics')]
        self.actCombo = wx.ComboBox(self.panel, wx.ID_ANY, choices=act)
        self.Bind(wx.EVT_TEXT, self.onActivityChange, self.actCombo)
        inputSizer.Add(self.actCombo, 1, wx.ALL | wx.EXPAND, 5)


        descDesc = wx.StaticText(self.panel, wx.ID_ANY, _('Description of work performed:'))
        self.descText = wx.TextCtrl(self.panel, wx.ID_ANY, style=wx.TE_MULTILINE)

        self.addButton = wx.Button(self.panel, wx.ID_ANY, _('A&dd new entry'))
        self.Bind(wx.EVT_BUTTON, self.onAddNewClicked, self.addButton)
        self.addButton.Disable()

        self.topSizer.Add(descDesc, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        self.topSizer.Add(self.descText, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        self.topSizer.Add(wx.StaticLine(self.panel), 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        self.topSizer.Add(self.addButton, 0, wx.ALL | wx.ALIGN_CENTER, 5)

    def createBottomView(self):
        """Creates and layout items for bottom view."""

        radioSizerBase = wx.BoxSizer(wx.HORIZONTAL)
        radioSizerLeft = wx.BoxSizer(wx.VERTICAL)
        radioSizerMiddle = wx.BoxSizer(wx.VERTICAL)
        radioSizerRight = wx.BoxSizer(wx.VERTICAL)
        radioSizerBase.Add(radioSizerLeft, 1, wx.ALL, 5)
        radioSizerBase.Add(radioSizerMiddle, 1, wx.ALL, 5)
        radioSizerBase.Add(radioSizerRight, 1, wx.ALL, 5)
        self.bottomSizer.Add(radioSizerBase, 0, wx.ALL | wx.EXPAND, 5)

        self.radioToday = wx.RadioButton(self.panel, label=_('To&days entries'), style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioToday, self.radioToday)
        self.radioYesterday = wx.RadioButton(self.panel, label=_('&Yesterdays entries'))
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioYesterday, self.radioYesterday)
        radioSizerLeft.Add(self.radioToday, 1)
        radioSizerLeft.Add(self.radioYesterday, 1)

        self.radioWeek = wx.RadioButton(self.panel, label=_('This &weeks entries'))
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioWeek, self.radioWeek)
        self.radioLastWeek =wx.RadioButton(self.panel, label=_('&Last weeks entries'))
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioLastWeek, self.radioLastWeek)
        radioSizerMiddle.Add(self.radioWeek, 1)
        radioSizerMiddle.Add(self.radioLastWeek, 1)

        self.radioMonth = wx.RadioButton(self.panel, label=_('This &months entries'))
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioMonth, self.radioMonth)
        self.radioLastMonth = wx.RadioButton(self.panel, label=_('Last months &entries'))
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioLastMonth, self.radioLastMonth)
        radioSizerRight.Add(self.radioMonth, 1)
        radioSizerRight.Add(self.radioLastMonth, 1)

        today = datetime.date.today()
        self.radioDesc = wx.StaticText(self.panel, wx.ID_ANY, _('Current date:') + ' ' + today.isoformat())
        radioDescSizer = wx.BoxSizer(wx.VERTICAL)
        radioDescSizer.Add(self.radioDesc, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        self.bottomSizer.Add(radioDescSizer, 0, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT, 5)

    def createBottomListView(self):
        """
        Creates the table list that shows 
        current entries in bottom view.
        """

        self.list = autoSortListCtrl.AutoSortListCtrl(self.panel)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightListItem, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDoubleListItem, self.list)

        self.updateListItems()
        self.bottomSizer.Add(self.list, 1, wx.ALL | wx.EXPAND, 5)

    def setupAboutInfo(self):
        self.aboutInfo = wx.AboutDialogInfo()
        self.aboutInfo.SetName('WDiary')
        self.aboutInfo.SetVersion('1.0.0')
        self.aboutInfo.SetDevelopers(['Marcus Pedersén'])
        self.aboutInfo.SetCopyright('WDiary (C) 2014 Marcus Pedersén')
        self.aboutInfo.SetDescription('A work diary to keep track of what you have done when.')
        self.aboutInfo.SetLicense('This program is free software: you can redistribute it and/or modify\n'
                                  'it under the terms of the GNU General Public License as published by\n'
                                  'the Free Software Foundation, either version 3 of the License, or\n'
                                  '(at your option) any later version.\n'
                                  '\n'
                                  'This program is distributed in the hope that it will be useful,\n'
                                  'but WITHOUT ANY WARRANTY; without even the implied warranty of\n'
                                  'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n'
                                  'GNU General Public License for more details.\n'
                                  '\n'
                                  'You should have received a copy of the GNU General Public License\n'
                                  'along with this program. If not, see http://www.gnu.org/licenses/\n'
                                  '\n' 
                                  'Contact: marcux@marcux.org\n'
                                  'Repro: https://github.com/xmarcux/wdiary_py\n')

    def updateCombos(self):
        """
        Updates both title and activity combo. 
        Properties file is read and number of saved
        items is adjusted.
        Titles and activities are saved to file.
        """

        titles = self.titleCombo.GetItems()
        activity = self.actCombo.GetItems()

        properties = db.db_connection.read_properties()

        if(properties and properties['TitleNo']):
            no = int(properties['TitleNo'])
            if(len(titles) > no):
                diff = len(titles) - no
                for i in range(diff):
                    del titles[0]
        else:
            if(len(titles) > 100):
                diff = len(titles) - 100
                for i in range(diff):
                    del titles[0]

        self.titleCombo.SetItems(titles)
        db.db_connection.save_titles(titles)

        if(properties and properties['ActivitiesNo']):
            no = int(properties['ActivitiesNo'])
            if(len(activity) > no):
                diff = len(activity) - no
                for i in range(diff):
                    del activity[0]
        else:
            if(len(activity) > 100):
                diff = len(activity) - 100
                for i in range(diff):
                    del activity[0]

        self.actCombo.SetItems(activity)
        db.db_connection.save_activities(activity)

    def clearTitles(self):
        """Clear all titles in combo and on file for reuse."""

        self.titleCombo.SetItems([])
        db.db_connection.save_titles([])

    def clearActivities(self):
        """Clear all activities in combo and on file for reuse."""

        self.actCombo.SetItems([])
        db.db_connection.save_activities([])

    def appendTitleCombo(self, text):
        """Appends text to title combo box."""

        if text not in self.titleCombo.GetItems():
            self.titleCombo.Append(text)

    def appendActivityCombo(self, text):
        """Appends text to activity combo box."""
        
        if text not in self.actCombo.GetItems():
            self.actCombo.Append(text)

    def onAddNewClicked(self, event):
        """Is triggered when add new diary
        button is clicked."""

        date = self.dateCtrl.GetValue()
        new_diary = diary.Diary(int(date.Format("%Y")), int(date.Format("%m")), int(date.Format("%d")))
        new_diary.set_hour(int(self.hourCombo.GetValue()))
        new_diary.set_minute(int(self.minCombo.GetValue()))
        new_diary.set_title(self.titleCombo.GetValue())
        new_diary.set_activity(self.actCombo.GetValue())
        new_diary.set_description(self.descText.GetValue())

        db.db_connection.save_to_db(new_diary)

        self.appendTitleCombo(self.titleCombo.GetValue())
        self.appendActivityCombo(self.actCombo.GetValue())
        self.updateCombos()
        self.updateListItems()

    def enableAddButton(self):
        """If all inputs has a valid value enable add button, else disable."""
        if self.dateCtrl.GetValue().IsValid():
            self.dateCtrlValueOk = True
        else:
            self.dateCtrlValueOk = False

        if (self.hourComboValueOk or self.minComboValueOk) and \
            self.titleComboValueOk and self.actComboValueOk and \
            self.dateCtrlValueOk:
            self.addButton.Enable()
        else:
            self.addButton.Disable()

    def onMinuteChange(self, event):
        """Is triggered when combo box for minutes is changed."""

        if self.minCombo.GetSelection() != 0:
            self.minComboValueOk = True
        else:
            self.minComboValueOk = False

        self.enableAddButton()

    def onHourChange(self, event):
        """Is triggered when combo box for hours is changed."""

        if self.hourCombo.GetSelection() != 0:
            self.hourComboValueOk = True
        else:
            self.hourComboValueOk = False

        self.enableAddButton()

    def onTitleChange(self, event):
        """Is triggered when combo box for title is changed."""

        if self.titleCombo.GetValue() != '':
            self.titleComboValueOk = True
        else:
            self.titleComboValueOk = False

        self.enableAddButton()

    def onActivityChange(self, event):
        """Is triggered when combo box for activity is changed."""

        if self.actCombo.GetValue() != '':
            self.actComboValueOk = True
        else:
            self.actComboValueOk = False

        self.enableAddButton()

    def onDateChanged(self, event):
        """Is triggered when date is changed."""

        if self.dateCtrl.GetValue().IsValid():
            self.dateCtrlValueOk = True
        else:
            self.dateCtrlValueOk = False

        self.enableAddButton()

    def onRadioToday(self, event):
        """Is triggered when radiobutton today is clicked."""

        today = datetime.date.today()
        self.radioDesc.SetLabel(_('Current date:') + ' ' + today.isoformat())
        self.updateListItems()

    def onRadioYesterday(self, event):
        """Is triggered when radiobutton yesterday is clicked."""

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        self.radioDesc.SetLabel(_('Current date:') + ' ' + yesterday.isoformat())
        self.updateListItems()
        """
        #Get yesterdays diary entries
        db_items = db.db_connection.search_db_date(yesterday, yesterday)
        items = dict(zip(range(1, len(db_items)), db_items))
        items = items.items()
        self.list.DeleteAllItems()
        for key, data in items:
            i = self.list.InsertStringItem(sys.maxint, data.date_str())
            self.list.SetStringItem(i, 1, data.time_str())
            self.list.SetStringItem(i, 2, data.title())
            self.list.SetStringItem(i, 3, data.description())
            self.list.SetItemData(i, key)
        """

    def onRadioWeek(self, event):
        """Is triggered when radiobutton week is clicked"""

        today = datetime.date.today()
        firstDay = today - datetime.timedelta(today.weekday())
        lastDay = today + datetime.timedelta(6 - today.weekday())
        self.radioDesc.SetLabel(_('Current dates:') + ' ' + firstDay.isoformat() \
                                + ' ' + _('to') + ' ' + lastDay.isoformat())
        self.updateListItems()
        """
        #Get this weeks diary entries
        db_items = db.db_connection.search_db_date(firstDay, lastDay)
        items = dict(zip(range(1, len(db_items)), db_items))
        items = items.items()
        self.list.DeleteAllItems()
        for key, data in items:
            i = self.list.InsertStringItem(sys.maxint, data.date_str())
            self.list.SetStringItem(i, 1, data.time_str())
            self.list.SetStringItem(i, 2, data.title())
            self.list.SetStringItem(i, 3, data.description())
            self.list.SetItemData(i, key)
        """

    def onRadioLastWeek(self, event):
        """Is triggered when radiobutton last week is clicked."""

        today = datetime.date.today()
        firstDay = today - datetime.timedelta(7 + today.weekday())
        lastDay = firstDay + datetime.timedelta(6)
        self.radioDesc.SetLabel(_('Current dates:') + ' ' + firstDay.isoformat() \
                                + ' ' + _('to') + ' ' + lastDay.isoformat())
        self.updateListItems()

    def onRadioMonth(self, event):
        """Is triggered when radiobutton month is clicked."""

        today = datetime.date.today()
        self.radioDesc.SetLabel(_('Current date:') + ' ' + str(today.year) \
                                + ' ' + self.strMonth(today.month))
        self.updateListItems()

    def onRadioLastMonth(self, event):
        """Is triggered when radiobutton last month is clicked."""

        today = datetime.date.today()
        if today.month == 1:
            year = today.year - 1
            month = 12
        else:
            year = today.year
            month = today.month - 1

        self.radioDesc.SetLabel(_('Current date:') + ' ' + str(year) \
                                + ' ' + self.strMonth(month))
        self.updateListItems()

    def onRightListItem(self, event):
        """Is triggered when a list item is right clicked."""

        if self.list.GetFirstSelected() != -1:
            popupMenu = wx.Menu()
            editMenu = popupMenu.Append(wx.ID_EDIT, _('Edit item...'), _('Edit selected item.'))
            self.Bind(wx.EVT_MENU, self.onEdit, editMenu)
            popupMenu.AppendSeparator()
            deleteMenu = popupMenu.Append(wx.ID_DELETE, _('Delete'), _('Deletes the selected item.'))
            self.Bind(wx.EVT_MENU, self.onDelete, deleteMenu)

            self.list.PopupMenu(popupMenu, event.GetPosition())

    def onDoubleListItem(self, event):
        """Is triggered when a list item is double clicked or enter is hit."""

        dataId = event.GetItem().GetData()
        dialog = editDiaryDialog.EditDiaryDialog(self)
        dialog.addDiary(self.list.itemDataMap[dataId][4])
        dialog.ShowModal()
        dialog.Destroy()

    def updateListItems(self):
        """Updates list view for diaries"""

        startDate = datetime.date.today()
        endDate = datetime.date.today()

        if self.radioYesterday.GetValue():
            startDate = endDate - datetime.timedelta(1)
            endDate = endDate - datetime.timedelta(1)
        if self.radioWeek.GetValue():
            startDate = endDate - datetime.timedelta(endDate.weekday())
            endDate = endDate + datetime.timedelta(6 - endDate.weekday())
        if self.radioLastWeek.GetValue():
            startDate = endDate - datetime.timedelta(7 + endDate.weekday())
            endDate = startDate + datetime.timedelta(6)
        if self.radioMonth.GetValue():
            startDate = datetime.date(startDate.year, startDate.month, 1)
            endDate = datetime.date(endDate.year, endDate.month, 
                                    self.__lastDayMonth(endDate.year, endDate.month))
        if self.radioLastMonth.GetValue():
            year = startDate.year
            month = startDate.month - 1
            if month == 0:
                month = 12
                year -= 1
            startDate = datetime.date(year, month, 1)
            endDate = datetime.date(year, month, self.__lastDayMonth(year, month))
 
        db_items = db.db_connection.search_db_date(startDate, endDate)
        itemsDict = dict(zip(range(1, len(db_items) + 1), db_items))
        items = itemsDict.items()
        mapDict = {}
        self.list.DeleteAllItems()
        for key, data in items:
            i = self.list.InsertStringItem(sys.maxint, data.date_str())
            self.list.SetStringItem(i, 1, data.time_str())
            self.list.SetStringItem(i, 2, data.title())
            self.list.SetStringItem(i, 3, data.description())
            self.list.SetItemData(i, key)
            mapDict[key] = (data.date_str(), data.time_str(), data.title(), data.description(), data) 

        self.list.itemDataMap = mapDict

    def __lastDayMonth(self, year, month):
        """
        Returns the last day of specified month as a number.
        Need year if it is a leap year.
        """
        
        lastDay = 31
        if month == 4 or month == 6 or month == 9 or month == 11:
            lastDay = 30

        if month == 2:
            if year % 4 == 0:
                lastDay = 29
            else:
                lastDay = 28

        return lastDay
        

    def onExit(self, event):
        """Exit command trigged"""

        self.Close()

    def onExport(self, event):
        """Export command trigged"""

        dialog = exportDialog.ExportDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def onOptions(self, event):
        """Options command trigged"""

        dialog = optionDialog.OptionDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def onAbout(self, event):
        """About comand trigged"""

        wx.AboutBox(self.aboutInfo)

    def onDelete(self, event):
        """
        Is triggered when delete is clicked
        on popup menu in list.
        """
        dialog = wx.MessageDialog(self, _('Are you sure that you want to delete selected item?'),
                                  _('Delete'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
        if dialog.ShowModal() == wx.ID_YES:
            dataId = self.list.GetFirstSelected() + 1
            db.db_connection.delete_from_db(self.list.itemDataMap[dataId][4])
            self.updateListItems()

        dialog.Destroy()

    def onEdit(self, event):
        """
        Is triggered when edit item is
        clicked on popup menu in list.
        """

        dataId = self.list.GetFirstSelected() + 1
        dialog = editDiaryDialog.EditDiaryDialog(self)
        dialog.addDiary(self.list.itemDataMap[dataId][4])
        dialog.ShowModal()
        dialog.Destroy()


    def strMonth(self, monthNumber):
        """Returns string representing month number 1-12."""
    
        month = ''

        if monthNumber == 1:
            month = _('January')
        elif monthNumber == 2:
            month = _('February')
        elif monthNumber == 3:
            month = _('March')
        elif monthNumber == 4:
            month = _('April')
        elif monthNumber == 5:
            month = _('May')
        elif monthNumber == 6:
            month = _('June')
        elif monthNuber == 7:
            month = _('July')
        elif monthNumber == 8:
            month = _('August')
        elif monthNumber == 9:
            month = _('September')
        elif monthNumber == 10:
            month = _('October')
        elif monthNumber == 11:
            month = _('November')
        elif monthNumber == 12:
            month = _('December')
        else:
            month = _('Invalid date')

        return month
