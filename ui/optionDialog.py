#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

"""
This class is a dialog
to change options for 
the application.
Is opened from Tool->Options... menu
"""
class OptionDialog(wx.Dialog):

    """Init method."""
    def __init__(self, *args, **kw):
        super(OptionDialog, self).__init__(*args, **kw)

        self.createView()
        self.SetTitle(_('Options'))

    """Method creates the view of the dialog."""
    def createView(self):
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

        content = []
        for c in range(0, 51, 5):
            content.append(str(c))

        for c in range(60, 101, 10):
            content.append(str(c))

        self.titleCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY, 
                                      value=content[-1], choices=content)
        actionSizer.Add(self.titleCombo, 0, wx.ALL | wx.EXPAND, 5)
        self.titleClearBtn = wx.Button(panel, wx.ID_ANY, _('Clear titles'))
        self.Bind(wx.EVT_BUTTON, self.onTitleClear, self.titleClearBtn)
        actionSizer.Add(self.titleClearBtn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.actCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY,
                                    value=content[-1], choices=content)
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

    """Is triggered when clear title button is clicked."""
    def onTitleClear(self, event):
        print('Title cleared.')

    """Is triggered when clear activity is clicked."""
    def onActivityClear(self, event):
        print('Activity cleared')

    """Is triggered when cancel button is clicked."""
    def onCancel(self, event):
        self.Destroy()

    """Is triggered when ok button is clicked."""
    def onOk(self, event):
        print('Ok clicked')
        self.Destroy()

