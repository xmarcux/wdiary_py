#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import db.db_connection


class EditDiaryDialog(wx.Dialog):
    """
    This class is the dialog
    to edit an diary entry.
    Is opened from main window.
    """

    def __init__(self,  *args, **kw):
        """Init method."""
        super(EditDiaryDialog, self).__init__(*args, **kw)

        self.createView()
        self.SetTitle(_('Edit diary entry'))

    def addDiary(self, diary):
        self.diary = diary
        self.descText.SetValue(diary.description())

        date = wx.DateTime()
        date.SetYear(diary.year())
        date.SetMonth(diary.month()-1)
        date.SetDay(diary.day())
        self.dateCtrl.SetValue(date)

        self.titleCombo.SetValue(diary.title())
        self.actCombo.SetValue(diary.activity())
        self.hourCombo.SetValue(str(diary.hour()))
        self.minCombo.SetValue(str(diary.minute()))

    def createView(self):
        """Method creates the view of the dialog."""

        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        staticBox = wx.StaticBox(panel, wx.ID_ANY,  _('Edit diary entry:'))
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        staticBoxSizer.Add(topSizer, 1, wx.ALL | wx.EXPAND, 5)

        labelSizer = wx.BoxSizer(wx.VERTICAL)
        dateLbl = wx.StaticText(panel, wx.ID_ANY, _('Date:'))
        labelSizer.Add(dateLbl, 1, wx.ALL | wx.EXPAND, 5)
        hourLbl = wx.StaticText(panel, wx.ID_ANY, _('Hour:'))
        labelSizer.Add(hourLbl, 1, wx.ALL | wx.EXPAND, 5)
        titleLbl = wx.StaticText(panel, wx.ID_ANY, _('Title:'))
        labelSizer.Add(titleLbl, 1, wx.ALL | wx.EXPAND, 5)
        activityLbl = wx.StaticText(panel, wx.ID_ANY, _('Activity:'))
        labelSizer.Add(activityLbl, 1, wx.ALL | wx.EXPAND, 5)

        inputSizer = wx.BoxSizer(wx.VERTICAL)
        self.dateCtrl = wx.DatePickerCtrl(panel, wx.ID_ANY)
        inputSizer.Add(self.dateCtrl, 1, wx.ALL | wx.EXPAND, 5)

        timeSizer = wx.BoxSizer(wx.HORIZONTAL)
        hours = []
        for h in range(25):
            hours.append(str(h))
        self.hourCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY, value=hours[0], choices=hours)
        timeSizer.Add(self.hourCombo, 1, wx.ALL, 5)
        minLbl = wx.StaticText(panel, wx.ID_ANY, _('Minute:'))
        timeSizer.Add(minLbl, 0, wx.ALL, 5)
        min = []
        for m in range(0, 60, 5):
            min.append(str(m))
        self.minCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY, value=min[0], choices=min)
        timeSizer.Add(self.minCombo, 1, wx.ALL, 5)
        inputSizer.Add(timeSizer, 1, wx.ALL | wx.EXPAND, 5)

        titles = db.db_connection.read_titles()
        self.titleCombo = wx.ComboBox(panel, wx.ID_ANY, choices=titles)
        inputSizer.Add(self.titleCombo, 1, wx.ALL | wx.EXPAND, 5)

        act = db.db_connection.read_activities()
        self.actCombo = wx.ComboBox(panel, wx.ID_ANY, choices=act)
        inputSizer.Add(self.actCombo, 1, wx.ALL | wx.EXPAND, 5)

        self.descLbl = wx.StaticText(panel, wx.ID_ANY, _('Description of work performed:'))
        staticBoxSizer.Add(self.descLbl, 0, wx.ALL | wx.EXPAND, 5)
        self.descText = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE)
        staticBoxSizer.Add(self.descText, 1, wx.ALL | wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        saveButton = wx.Button(panel, wx.ID_ANY, _('&Save'))
        buttonSizer.Add(saveButton, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.Bind(wx.EVT_BUTTON, self.onSave, saveButton)
        cancelButton = wx.Button(panel, wx.ID_ANY, _('&Cancel'))
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelButton)

        buttonSizer.Add(cancelButton, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        topSizer.Add(labelSizer, 0, wx.EXPAND)
        topSizer.Add(inputSizer, 1, wx.BOTTOM | wx.EXPAND, 10)
        mainSizer.Add(staticBoxSizer, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(buttonSizer, 0, wx.ALL |  wx.ALIGN_CENTER, 5)

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def onCancel(self, event):
        """Is triggered when cancel button is clicked."""
        self.Destroy()

    def onSave(self, event):
        """Is triggered when save button is clicked."""
        
        error_msg = ""
        if not self.dateCtrl.GetValue().IsValid():
            error_msg = "Specify a valid date.\n"

        if self.hourCombo.GetValue() == "0" and self.minCombo.GetValue() == "0":
            error_msg += "Specify hours and/or minutes.\n"

        if self.titleCombo.GetValue() == "":
            error_msg += "Specify title.\n"
        
        if self.actCombo.GetValue() == "":
            error_msg += "Specify activity.\n"

        if error_msg:
            error_msg = "Error saving diary entry:\n\n" + error_msg
            dialog = wx.MessageDialog(self, error_msg, _('Error saving'), wx.OK | wx.ICON_WARNING)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            date = self.dateCtrl.GetValue()
            self.diary.set_year(date.GetYear())
            self.diary.set_month(date.GetMonth() + 1)
            self.diary.set_day(date.GetDay())

            self.diary.set_hour(int(self.hourCombo.GetValue()))
            self.diary.set_minute(int(self.minCombo.GetValue()))
            self.diary.set_title(self.titleCombo.GetValue())
            self.diary.set_activity(self.actCombo.GetValue())
            self.diary.set_description(self.descText.GetValue())

            db.db_connection.save_to_db(self.diary)

            self.GetParent().updateListItems()
            self.Destroy()
