"""Example of how to use wx tooltips on a matplotlib figure window.
Adapted from http://osdir.com/ml/python.matplotlib.devel/2006-09/msg00048.html"""

import matplotlib as mpl
mpl.use('WXAgg')
mpl.interactive(False)

import pylab as pl
from pylab import get_current_fig_manager as gcfm
import wx
import numpy as np
import random


class wxToolTipExample(object):
    def __init__(self):
        self.figure = pl.figure()
        self.axis = self.figure.add_subplot(111)

        # create a long tooltip with newline to get around wx bug (in v2.6.3.3)
        # where newlines aren't recognized on subsequent self.tooltip.SetTip() calls
        self.tooltip = wx.ToolTip(tip='tip with a long %s line and a newline\n' % (' '*100))
        gcfm().canvas.SetToolTip(self.tooltip)
        self.tooltip.Enable(False)
        self.tooltip.SetDelay(0)
        self.figure.canvas.mpl_connect('motion_notify_event', self._onMotion)

        self.dataX = np.arange(0, 100)
        self.dataY = [random.random()*100.0 for x in xrange(len(self.dataX))]
        self.axis.plot(self.dataX, self.dataY, linestyle='-', marker='o', markersize=10, label='myplot')

    def _onMotion(self, event):
        collisionFound = False
        if event.xdata != None and event.ydata != None: # mouse is inside the axes
            for i in xrange(len(self.dataX)):
                radius = 1
                if abs(event.xdata - self.dataX[i]) < radius and abs(event.ydata - self.dataY[i]) < radius:
                    top = tip='x=%f\ny=%f' % (event.xdata, event.ydata)
                    self.tooltip.SetTip(tip)
                    self.tooltip.Enable(True)
                    collisionFound = True
                    break
        if not collisionFound:
            self.tooltip.Enable(False)



example = wxToolTipExample()
pl.show()