#!/usr/bin/python

import cv2
import wx
import wx.lib.scrolledpanel as scrolled
import sys
from capture import * #TODO this needs to be de-coupled properly at some point
from ros import 

class VideoStream(scrolled.ScrolledPanel):
	def __init__(self, parent, cams, fps=30):
		scrolled.ScrolledPanel.__init__(self, parent, size=(wx.GetDisplaySize() ))

		self.cams = cams

		img = getImage(cams)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		h,w = img.shape[:2]

		self.timer = wx.Timer(self)
		self.timer.Start(1000./fps)		

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_TIMER, self.NextFrame)

		self.bmp = wx.BitmapFromBuffer(w,h,img)
		wx.YieldIfNeeded()

	def OnPaint(self, evt):
		dc = wx.BufferedPaintDC(self)
		dc.DrawBitmap(self.bmp, 0, 0)
		wx.YieldIfNeeded()

	def NextFrame(self, evt):
		img = getImage(self.cams)
		h,w = img.shape[:2]

		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		if self.bmp.GetWidth() != w:
			self.bmp = wx.BitmapFromBuffer(w,h,img)

		self.bmp.CopyFromBuffer(img)
		wx.YieldIfNeeded()
		self.Refresh()


class DisparityStream(scrolled.ScrolledPanel):
	def __init__(self, parent, fps=30):
		scrolled.ScrolledPanel.__init__(self, parent, size=(wx.GetDisplaySize() ))

		self.cams = cams

		img = getImage(cams)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		h,w = img.shape[:2]

		self.timer = wx.Timer(self)
		self.timer.Start(1000./fps)		

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_TIMER, self.NextFrame)

		self.bmp = wx.BitmapFromBuffer(w,h,img)
		wx.YieldIfNeeded()

	def OnPaint(self, evt):
		dc = wx.BufferedPaintDC(self)
		dc.DrawBitmap(self.bmp, 0, 0)
		wx.YieldIfNeeded()

	def NextFrame(self, evt):
		img = getImage(self.cams)
		h,w = img.shape[:2]

		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		if self.bmp.GetWidth() != w:
			self.bmp = wx.BitmapFromBuffer(w,h,img)

		self.bmp.CopyFromBuffer(img)
		wx.YieldIfNeeded()
		self.Refresh()
