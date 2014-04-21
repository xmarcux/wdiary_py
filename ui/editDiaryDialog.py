#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

"""
This class is the dialog
to edit an diary entry.
Is opened from main window.
"""

class EditDiaryDialog(wx.Dialog):

    """Init method."""
    def __init__(self, *args, **kw):
        super(EditDiaryDialog, self).__init__(*args, **kw)

        self.createView()
        self.SetTitle(_('Edit diary entry'))


    """Method creates the view of the dialog."""
    def createView(self):
        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        staticBox = wx.StaticBox(panel, wx.ID_ANY,  _('Edit diary entry:'))
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        staticBoxSizer.Add(topSizer, 0, wx.ALL | wx.EXPAND, 5)

        labelSizer = wx.BoxSizer(wx.VERTICAL)
        dateLbl = wx.StaticText(panel, wx.ID_ANY, _('Date:'))
        labelSizer.Add(dateLbl, 0, wx.ALL | wx.EXPAND, 5)
        hourLbl = wx.StaticText(panel, wx.ID_ANY, _('Hour:'))
        labelSizer.Add(hourLbl, 0, wx.ALL | wx.EXPAND, 5)
        titleLbl = wx.StaticText(panel, wx.ID_ANY, _('Title:'))
        labelSizer.Add(titleLbl, 0, wx.ALL | wx.EXPAND, 5)
        activityLbl = wx.StaticText(panel, wx.ID_ANY, _('Activity:'))
        labelSizer.Add(activityLbl, 0, wx.ALL | wx.EXPAND, 5)

        inputSizer = wx.BoxSizer(wx.VERTICAL)
        self.dateCtrl = wx.DatePickerCtrl(panel, wx.ID_ANY)
        inputSizer.Add(self.dateCtrl, 0, wx.ALL | wx.EXPAND, 5)

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
        inputSizer.Add(timeSizer, 0, wx.ALL | wx.EXPAND, 5)

        act = [_('Documentation'), _('Project leading'), _('Programming'), _('Graphics')]
        self.actCombo = wx.ComboBox(panel, wx.ID_ANY, choices=act)
        inputSizer.Add(self.actCombo, 0, wx.ALL | wx.EXPAND, 5)

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
        topSizer.Add(inputSizer, 1, wx.EXPAND)
        mainSizer.Add(staticBoxSizer, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(buttonSizer, 0, wx.ALL |  wx.ALIGN_CENTER, 5)

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    """Is triggered when cancel button is clicked."""
    def onCancel(self, event):
        self.Destroy()

    """Is triggered when save button is clicked."""
    def onSave(self, event):
        print('Dialog saved')
        self.Destroy()
