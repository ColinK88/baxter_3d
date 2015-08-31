#!/usr/bin/env python

import cv2
import wx
from capture import *
from calib import *
from gui import *
from ros import initTopics, ROSPublish
from multiprocessing import Pool
import rospy
import os

cams = ( cv2.VideoCapture(0), cv2.VideoCapture(1) )

os.system('v4l2-ctl -d 0 -c focus_auto=0')
os.system('v4l2-ctl -d 0 -c focus_absolute=20')
os.system('v4l2-ctl -d 1 -c focus_auto=0')
os.system('v4l2-ctl -d 1 -c focus_absolute=20')

# all of this needs tidied
sevenTwenty = (1280, 720)
tenEighty = (1920,1080)
resolutions = (sevenTwenty, tenEighty)

setResolution(sevenTwenty, cams)


rospy.init_node('image_capture', anonymous=True)
initTopics()



image = None

modeChoices = ("Anaglyph", "Red", "Green", "Side By Side")
resChoices = ("720", "1080")

class UI(wx.Frame):
	def __init__(self, parent, title, processPool):
		wx.Frame.__init__(self, parent, title=title)
		self.Maximize()
		self.pool = processPool
		self.InitUI()
		
	def InitUI(self):

		panel = self.panel = VideoStream(self, cams)
		#infoPanel = wx.Panel(self)
		self.captureButton = wx.ToggleButton(panel, label='Start Capture', pos=(20,40))
		self.calibButton = wx.ToggleButton(panel, label='Start Calibration', pos=(20,80))

		box = wx.BoxSizer(wx.VERTICAL)

		menuBar = wx.MenuBar()

		fileMenu = wx.Menu()
		quit = fileMenu.Append(wx.ID_EXIT, "E&xit", "Exit the program")
		menuBar.Append(fileMenu,"&File")

		calibMenu = wx.Menu()
		imageMenu = wx.Menu()
		menuBar.Append(calibMenu,"Calibration")

		self.changeMode = wx.ComboBox(panel, pos=(20, 100), choices=modeChoices, style=wx.CB_READONLY)
		self.changeRes = wx.ComboBox(panel, pos=(20, 150), choices =resChoices, style=wx.CB_READONLY )
		
		self.changeMode.Bind(wx.EVT_COMBOBOX, self.OnSelectMode)
		self.changeRes.Bind(wx.EVT_COMBOBOX, self.OnSelectRes)

		box.Add(self.changeMode, flag=wx.TOP, border=10)
		box.Add(self.changeRes, flag=wx.BOTTOM, border=10)
		box.Add(self.captureButton, flag=wx.TOP, border=10)
		box.Add(self.calibButton, flag=wx.TOP, border=10)

		self.SetMenuBar(menuBar)
		
		self.captureButton.Bind(wx.EVT_TOGGLEBUTTON, self.OnCapture)
		
		self.Bind(wx.EVT_MENU, self.OnQuit, quit)
		panel.SetupScrolling()
		self.panel.SetSizer(box)
		self.panel.Layout()

		ROSPublish(cams)


		self.Show(True)

	def StartCalibration():
		FindPoints()
	
	def OnCalibrate(self, evt):
		print "calibrate"

	def OnCapture(self, evt):
		toggle = self.captureButton.GetValue()

		#ToggleCapture(toggle)


	def OnSelectRes(self, evt):
		pass
		#setResolution( resolutions[self.changeRes.GetCurrentSelection()], cams)

	def OnSelectMode(self, evt):
		setCaptureMode(self.changeMode.GetCurrentSelection() )

	def OnQuit(self, evt):
		self.Close()
		cams[0].release()
		cams[1].release()	
		cv2.destroyAllWindows()



if __name__ == '__main__':
	try:
		app = wx.App()
		processPool = Pool()
		cap = UI(None, "Project", processPool)
		#rospy.init_node('baxter_3d', anonymous=True)
		app.MainLoop()
	except KeyboardInterrupt:
		self.Close()
		cams[0].release()
		cams[1].release()	
		cv2.destroyAllWindows()
