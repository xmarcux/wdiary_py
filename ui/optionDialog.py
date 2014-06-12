#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import db.db_connection

class OptionDialog(wx.Dialog):
    """
    This class is a dialog
    to change options for 
    the application.
    Is opened from Tool->Options... menu
    """

    def __init__(self, *args, **kw):
        """Init method."""
        super(OptionDialog, self).__init__(*args, **kw)

        self.createView()
        self.SetTitle(_('Options'))

    def createView(self):
        """Method creates the view of the dialog."""

        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        labelSizer = wx.BoxSizer(wx.VERTICAL)
        actionSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(labelSizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(actionSizer, 1, wx.ALL, 5)
        mainSizer.Add(topSizer, 0, wx.ALL | wx.EXPAND, 5)

        titleLbl = wx.StaticText(panel, wx.ID_ANY, _('Number of titles saved for reuse:'))
        labelSizer.Add(titleLbl, 1, wx.ALL, 5)
        clearTitleLbl = wx.StaticText(panel, wx.ID_ANY, _('Clear all buffered titles:'))
        labelSizer.Add(clearTitleLbl, 1, wx.ALL, 5)
        
        actLbl = wx.StaticText(panel, wx.ID_ANY, _('Number of activities saved for reuse:'))
        labelSizer.Add(actLbl, 1, wx.ALL, 5)
        clearActLbl = wx.StaticText(panel, wx.ID_ANY, _('Clear all buffered activities:'))
        labelSizer.Add(clearActLbl, 1, wx.ALL, 5)

        prop = db.db_connection.read_properties()

        content = []
        for c in range(0, 51, 5):
            content.append(str(c))

        for c in range(60, 101, 10):
            content.append(str(c))

        self.titleCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY, 
                                      value=content[-1], choices=content)
        if(prop and prop['TitleNo'] in content):
            self.titleCombo.SetValue(prop['TitleNo'])

        actionSizer.Add(self.titleCombo, 0, wx.ALL | wx.EXPAND, 5)
        self.titleClearBtn = wx.Button(panel, wx.ID_ANY, _('Clear titles'))
        self.Bind(wx.EVT_BUTTON, self.onTitleClear, self.titleClearBtn)
        actionSizer.Add(self.titleClearBtn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.actCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY,
                                    value=content[-1], choices=content)
        if(prop and prop['ActivitiesNo'] in content):
            self.actCombo.SetValue(prop['ActivitiesNo'])
 
        actionSizer.Add(self.actCombo, 0, wx.ALL | wx.EXPAND, 5)
        self.actClearBtn = wx.Button(panel, wx.ID_ANY, _('Clear activities'))
        self.Bind(wx.EVT_BUTTON, self.onActivityClear, self.actClearBtn)
        actionSizer.Add(self.actClearBtn, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        mainSizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.okButton = wx.Button(panel, wx.ID_ANY, _('&OK'))
        self.Bind(wx.EVT_BUTTON, self.onOk, self.okButton)
        self.cancelButton = wx.Button(panel, wx.ID_ANY, _('&Cancel'))
        self.Bind(wx.EVT_BUTTON, self.onCancel, self.cancelButton)
        buttonSizer.Add(self.okButton, 0, wx.ALL, 5)
        buttonSizer.Add(self.cancelButton, 0, wx.ALL, 5)
        mainSizer.Add(buttonSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def onTitleClear(self, event):
        """Is triggered when clear title button is clicked."""

        dialog = wx.MessageDialog(self, _('Are you sure that you want to clear title buffer?'),
                                  _('Clear title buffer'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
        if dialog.ShowModal() == wx.ID_YES:
            self.GetParent().clearTitles()
        dialog.Destroy()

    def onActivityClear(self, event):
        """Is triggered when clear activity is clicked."""

        dialog = wx.MessageDialog(self, _('Are you sure that you want to clear activity buffer?'),
                                  _('Clear activity buffer'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
        if dialog.ShowModal() == wx.ID_YES:
            self.GetParent().clearActivities()
        dialog.Destroy()

    def onCancel(self, event):
        """Is triggered when cancel button is clicked."""
        self.Destroy()

    def onOk(self, event):
        """Is triggered when ok button is clicked."""

        prop = {}
        prop['TitleNo'] = self.titleCombo.GetValue()
        prop['ActivitiesNo'] = self.actCombo.GetValue()
        db.db_connection.save_properties(prop)
        self.GetParent().updateCombos()
        self.Destroy()

