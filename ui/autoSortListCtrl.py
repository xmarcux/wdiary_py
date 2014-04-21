#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin

"""A class that creates a table to show diary entries in."""
class AutoSortListCtrl (wx.ListCtrl, ColumnSorterMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self, 4)
        ListCtrlAutoWidthMixin.__init__(self)

        self.InsertColumn(0, _('Date'))
        self.InsertColumn(1, _('Time'))
        self.InsertColumn(2, _('Title'))
        self.InsertColumn(3, _('Description'))

        self.itemDataMap = {}

    def GetListCtrl(self):
        return self

