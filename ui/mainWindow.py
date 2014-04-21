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


test_dict = {
1 : ('2014-03-17', '2:45', 'A little title that is the first', 'This is the first job to be described in this first python version of wdiary.'),
2 : ('2014-03-18', '0:30', 'A short little title', 'A shoert description.'),
3 : ('2014-03-20', '3:0', 'A1123-1 Fieing up the second pan', 'As the first pan does not give power enough to ahndle the heat. A second fire is started and the system will run fine all night.')
}


"""Main Window for application."""
class MainWindow (wx.Frame):

    """Init function"""
    def __init__(self):
        wx.Frame.__init__(self, None, title=_('WDiary'), size=(400, 200))
        
        self.CreateStatusBar()

        self.SetMenuBar(self.createMenu())
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.createSizers()
        self.createTopView()
        self.createBottomView()
        self.createBottomListView()

        self.setupAboutInfo()
        
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

    """ Function that creates menu."""
    def createMenu(self):

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

    """Create containers for widgets"""
    def createSizers(self):
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        box = wx.StaticBox(self.panel, wx.ID_ANY, _('Add new diary entry:'))
        self.topSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bottomBox = wx.StaticBox(self.panel, wx.ID_ANY, _('Current diary entries:'))
        self.bottomSizer = wx.StaticBoxSizer(bottomBox, wx.VERTICAL)
        
        self.mainSizer.Add(self.topSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(self.bottomSizer, 1, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)

    """Creates items for the upper view in main window."""
    def createTopView(self):
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
        self.titleCombo = wx.ComboBox(self.panel, wx.ID_ANY)
        self.Bind(wx.EVT_TEXT, self.onTitleChange, self.titleCombo)
        inputSizer.Add(self.titleCombo, 1, wx.ALL | wx.EXPAND, 5)

        descAct = wx.StaticText(self.panel, wx.ID_ANY, _('Activity:'))
        descSizer.Add(descAct, 1, wx.ALL | wx.EXPAND, 5)
        act = [_('Documentation'), _('Project leading'), _('Programming'), _('Graphics')]
        self.actCombo = wx.ComboBox(self.panel, wx.ID_ANY, choices=act)
        self.Bind(wx.EVT_TEXT, self.onActivityChange, self.actCombo)
        inputSizer.Add(self.actCombo, 1, wx.ALL | wx.EXPAND, 5)


        descDesc = wx.StaticText(self.panel, wx.ID_ANY, _('Description of work performed:'))
        descText = wx.TextCtrl(self.panel, wx.ID_ANY, style=wx.TE_MULTILINE)

        self.addButton = wx.Button(self.panel, wx.ID_ANY, _('A&dd new entry'))
        self.addButton.Disable()

        self.topSizer.Add(descDesc, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        self.topSizer.Add(descText, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        self.topSizer.Add(wx.StaticLine(self.panel), 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        self.topSizer.Add(self.addButton, 0, wx.ALL | wx.ALIGN_CENTER, 5)

    """Creates and layout items for bottom view."""
    def createBottomView(self):
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

    """
    Creates the table list that shows 
    current entries in bottom view.
    """
    def createBottomListView(self):
        self.list = autoSortListCtrl.AutoSortListCtrl(self.panel)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightListItem, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDoubleListItem, self.list)

        items = test_dict.items()
        for key, data in items:
            i = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetStringItem(i, 1, data[1])
            self.list.SetStringItem(i, 2, data[2])
            self.list.SetStringItem(i, 3, data[3])
            self.list.SetItemData(i, key)


        """
        i1 = self.list.InsertStringItem(sys.maxint, '2014-03-17')
        self.list.SetStringItem(i1, 1, '2:45')
        self.list.SetStringItem(i1, 2, 'A little title that is the first')
        self.list.SetStringItem(i1, 3, 'This is the first job to be described in this first python version of wdiary.')
        self.list.SetItemData(i1, 1)

        i1 = self.list.InsertStringItem(sys.maxint, '2014-03-18')
        self.list.SetStringItem(i1, 1, '0:30')
        self.list.SetStringItem(i1, 2, 'A short little title')
        self.list.SetStringItem(i1, 3, 'A shoert description.')
        self.list.SetItemData(i1, 2)

        i1 = self.list.InsertStringItem(sys.maxint, '2014-03-20')
        self.list.SetStringItem(i1, 1, '3:0')
        self.list.SetStringItem(i1, 2, 'A1123-1 Fieing up the second pan')
        self.list.SetStringItem(i1, 3, 'As the first pan does not give power enough to ahndle the heat. A second fire is started and the system will run fine all night.')
        self.list.SetItemData(i1, 3)
        """

        self.bottomSizer.Add(self.list, 1, wx.ALL | wx.EXPAND, 5)

    def setupAboutInfo(self):
        self.aboutInfo = wx.AboutDialogInfo()
        self.aboutInfo.SetName('WDiary')
        self.aboutInfo.SetVersion('Alpha')
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

    """If all inputs has a valid value enable add button, else disable."""
    def enableAddButton(self):
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

    """Is triggered when combo box for minutes is changed."""
    def onMinuteChange(self, event):
        if self.minCombo.GetSelection() != 0:
            self.minComboValueOk = True
        else:
            self.minComboValueOk = False

        self.enableAddButton()

    """Is triggered when combo box for hours is changed."""
    def onHourChange(self, event):
        if self.hourCombo.GetSelection() != 0:
            self.hourComboValueOk = True
        else:
            self.hourComboValueOk = False

        self.enableAddButton()

    """Is triggered when combo box for title is changed."""
    def onTitleChange(self, event):
        if self.titleCombo.GetValue() != '':
            self.titleComboValueOk = True
        else:
            self.titleComboValueOk = False

        self.enableAddButton()

    """Is triggered when combo box for activity is changed."""
    def onActivityChange(self, event):
        if self.actCombo.GetValue() != '':
            self.actComboValueOk = True
        else:
            self.actComboValueOk = False

        self.enableAddButton()

    """Is triggered when date is changed."""
    def onDateChanged(self, event):
        if self.dateCtrl.GetValue().IsValid():
            self.dateCtrlValueOk = True
        else:
            self.dateCtrlValueOk = False

        self.enableAddButton()

    """Is triggered when radiobutton today is clicked."""
    def onRadioToday(self, event):
        today = datetime.date.today()
        self.radioDesc.SetLabel(_('Current date:') + ' ' + today.isoformat())

    """Is triggered when radiobutton yesterday is clicked."""
    def onRadioYesterday(self, event):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        self.radioDesc.SetLabel(_('Current date:') + ' ' + yesterday.isoformat())

    """Is triggered when radiobutton week is clicked"""
    def onRadioWeek(self, event):
        today = datetime.date.today()
        firstDay = today - datetime.timedelta(today.weekday())
        lastDay = today + datetime.timedelta(6 - today.weekday())
        self.radioDesc.SetLabel(_('Current dates:') + ' ' + firstDay.isoformat() \
                                + ' ' + _('to') + ' ' + lastDay.isoformat())

    """Is triggered when radiobutton last week is clicked."""
    def onRadioLastWeek(self, event):
        today = datetime.date.today()
        firstDay = today - datetime.timedelta(7 + today.weekday())
        lastDay = firstDay + datetime.timedelta(6)
        self.radioDesc.SetLabel(_('Current dates:') + ' ' + firstDay.isoformat() \
                                + ' ' + _('to') + ' ' + lastDay.isoformat())

    """Is triggered when radiobutton month is clicked."""
    def onRadioMonth(self, event):
        today = datetime.date.today()
        self.radioDesc.SetLabel(_('Current date:') + ' ' + str(today.year) \
                                + ' ' + self.strMonth(today.month))

    """Is triggered when radiobutton last month is clicked."""
    def onRadioLastMonth(self, event):
        today = datetime.date.today()
        if today.month == 1:
            year = today.year - 1
            month = 12
        else:
            year = today.year
            month = today.month - 1

        self.radioDesc.SetLabel(_('Current date:') + ' ' + str(year) \
                                + ' ' + self.strMonth(month))

    """Is triggered when a list item is right clicked."""
    def onRightListItem(self, event):
        if self.list.GetFirstSelected() != -1:
            popupMenu = wx.Menu()
            editMenu = popupMenu.Append(wx.ID_EDIT, _('Edit item...'), _('Edit selected item.'))
            self.Bind(wx.EVT_MENU, self.onEdit, editMenu)
            popupMenu.AppendSeparator()
            deleteMenu = popupMenu.Append(wx.ID_DELETE, _('Delete'), _('Deletes the selected item.'))
            self.Bind(wx.EVT_MENU, self.onDelete, deleteMenu)

            self.list.PopupMenu(popupMenu, event.GetPosition())

    """Is triggered when a list item is double clicked or enter is hit."""
    def onDoubleListItem(self, event):
        print("double click on item.")
        dataId = event.GetItem().GetData()
        print(self.list.itemDataMap[dataId])

    """Exit command trigged"""
    def onExit(self, event):
        self.Close()

    """Export command trigged"""
    def onExport(self, event):
        dialog = exportDialog.ExportDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    """Options command trigged"""
    def onOptions(self, event):
        dialog = optionDialog.OptionDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    """About comand trigged"""
    def onAbout(self, event):
        wx.AboutBox(self.aboutInfo)

    """
    Is triggered when delete is clicked
    on popup menu in list.
    """
    def onDelete(self, event):
        dialog = wx.MessageDialog(self, _('Are you sure that you want to delete selected item?'),
                                  _('Delete'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
        if dialog.ShowModal() == wx.ID_YES:
            print('Delete item')
        dialog.Destroy()

    """
    Is triggered when edit item is
    clicked on popup menu in list.
    """
    def onEdit(self, event):
        dialog = editDiaryDialog.EditDiaryDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    """Returns string representing month number 1-12."""
    def strMonth(self, monthNumber):
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
