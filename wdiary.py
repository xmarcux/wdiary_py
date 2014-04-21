#!/usr/bin/env python

import wx
import gettext
import ui.mainWindow as mw

gettext.install('wdiary', '/locale', unicode=False)

app = wx.App(False)
mw.MainWindow()
app.MainLoop()
