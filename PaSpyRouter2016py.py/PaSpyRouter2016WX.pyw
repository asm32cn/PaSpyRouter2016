#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 2.7
# PaSpyRouter2016WX.pyw

import wx
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO, base64, urllib2, re


conf__strCookies = 'Authorization=Basic%20YWRtaW46cGFzc3dk; ChgPwdSubTag='
conf__strCaptain = 'PaSpyRouter2016WX.pyw'
conf__strLinkPrefix = 'http://192.168.1.1/userRpm/'

strFrameIcon = 'R0lGODlhIAAgAJEAAAAAAMDAwP//AAAAACH5BAQUAP8ALAAAAAAgACAAAAJcjI+py+0PIwNAzpqoXTrj' \
	'jXThBxricZZpsG5ra72kOrO1W8OSXI6KHuH1TLlbrDgk/ow7ZFI4hPZOlKr1is1Wbdqu9+sVCABi8rgM' \
	'1pbX53H6neXCwcm6/Y6XFAAAOw=='

A_strIconData = (
	'R0lGODlhEAAPAIAAAAAAAP///yH5BAUUAAEALAAAAAAQAA8AAAIkjA2px9gBHmTRUXnqxNlmbYFe+IiV' \
	'uHUpklxj2aDvLLNKzTEFADs=',
	'R0lGODlhEAAPAIAAAAAAAP///yH5BAUUAAEALAAAAAAQAA8AAAIijI+py50Ao4QIOHsw08H6B3pRVl0V' \
	'hnbqOY1Z277w5NR2AQA7',
	'R0lGODlhEAAPAIAAAAAAAP///yH5BAUUAAEALAAAAAAQAA8AAAInjI9pwO19nmQRqIjoXXVp33mfBSbk' \
	'SG4pZbVBu06PCm3vW9OzzQcFADs=',
	'R0lGODlhEAAPAIAAAAAAAP///yH5BAUUAAEALAAAAAAQAA8AAAIkjI+py3AAowuyTmqgmjrfh3Vd4pQe' \
	'c1Lfxq1ka1moy1bojSsFADs=',
	'R0lGODlhEAAPAIAAAAAAAP///yH5BAUUAAEALAAAAAAQAA8AAAIcjI+py40Ao4nSLQontncHDHAKqFFi' \
	'Qn7eybZGAQA7',
	'R0lGODlhEAAPAJEAAAAAANTQyICAgP///yH5BAUUAAMALAAAAAAQAA8AAAIqnI+pywgPAZOJVvUwFtZ0' \
	'L3DOJh7fAIQfELRtWpqum57sHGRLBDX+3ygAADs=',
	'R0lGODlhEAAPAIAAAAAAAP///yH5BAUUAAEALAAAAAAQAA8AAAIojI+pwK3XIngOslRRDpdOy3HSZ1yT' \
	'FIKn05Uk9m7uK8atNtJ49PRKAQA7',
)

conf_dictMemo = {
	'DC-6D-CD-75-B9-79': u'理发店',
	'F6-D0-10-96-DC-E2': u'酷派.我',
	'A0-93-47-96-B7-70': u'OPPO.蒋',
	'F4-29-81-92-4B-D0': u'玉米.女',
	'24-09-95-63-7F-64': u'鸡柳.女',
	'F4-29-81-C7-DD-A7': u'叶刚.vo',
	'E8-BB-A8-A8-42-26': u'奶茶.邻',
}

strDataSufix = '\n0,0 );\n'
strCrlf = '\n' # 0D 0A

A_strKeys1 = ('id', 'strClientName', 'strMacAddress', 'strIpAddress', 'strTimeout', 'strMemo')
A_strKeys2 = ('id', 'strMacAddress', 'nStatus', 'nReceive', 'nSend', 'strIpAddress', 'strClientName', 'strMemo')
A_strKeys3 = ('@', 'strBrief')

A_strKeys1n = ('@',) + A_strKeys1
A_strKeys2n = ('@',) + A_strKeys2

strKey1 = A_strKeys1[2] # strMacAddress
strKey2 = A_strKeys1[1] # strClientName
strKey3 = A_strKeys1[3] # strIpAddress
strKey4 = A_strKeys2[3] # nReceive
strKey5 = A_strKeys2[4] # nSend

class enumAlignment():
	left = wx.LIST_FORMAT_LEFT
	center = wx.LIST_FORMAT_CENTER
	right = wx.LIST_FORMAT_RIGHT

conf_nWidth = {
	'@':(30, enumAlignment.right),
	'strClientName':(175, enumAlignment.left),
	'strMacAddress':(125, enumAlignment.left),
	'strIpAddress':(105, enumAlignment.left),
	'strTimeout':(85, enumAlignment.center),
	'strMemo':(65, enumAlignment.left),
	'nStatus':(65, enumAlignment.center),
	'nReceive':(65, enumAlignment.right),
	'nSend':(65, enumAlignment.right),
	'id':(30, enumAlignment.right),
	'strBrief':(683, enumAlignment.left)}

conf__dictActions = [
	{'text':u'设备状态', 'tip':u'查看设备状态'},
	{'text':u'报表', 'tip':u'查看综合报表'},
	{'text':u'DHCP', 'tip':u'查看DHCP列表'},
	{'text':u'数据包', 'tip':u'统计无线数据包'},
	{'text':u'日志', 'tip':u'查看设备日志'},
	{'text':u'清除日志', 'tip':u'清除日志'},
	{'text':u'重启设备', 'tip':u'重启设备'}]


class PaSpyRouter2016WX(wx.Frame):
	def __init__(self, parent=None):
		wx.Frame.__init__(self, parent, title=conf__strCaptain, size=(780, 450))
		self.Center()
		self.SetIcon( self.getIcon() )

		statusBar = self.CreateStatusBar()
		toolbar = self.CreateToolBar()
		self.objToolbarIcon = []
		self.objButtons = []
		for i in xrange(7):
			self.objToolbarIcon.append( self.getToolbarIcon(i) )
			nActionID = wx.NewId()
			self.objButtons.append( toolbar.AddSimpleTool(nActionID, self.objToolbarIcon[i],
				conf__dictActions[i]['text'], conf__dictActions[i]['tip']) )

			if i in (0, 3, 5):
				toolbar.AddSeparator()
		toolbar.Realize()

		self.Bind(wx.EVT_MENU, self.PA_DoDisplayDevInfo, self.objButtons[0])
		self.Bind(wx.EVT_MENU, self.PA_DoDisplayReport, self.objButtons[1])
		self.Bind(wx.EVT_MENU, self.PA_DoDisplayHosts, self.objButtons[2])
		self.Bind(wx.EVT_MENU, self.PA_DoDisplayStations, self.objButtons[3])
		self.Bind(wx.EVT_MENU, self.PA_DoDisplaySysLog, self.objButtons[4])

		self.Bind(wx.EVT_MENU, self.PA_DoClearSysLog, self.objButtons[5])
		self.Bind(wx.EVT_MENU, self.PA_DoRebootDevice, self.objButtons[6])

		self.listDisplay = wx.ListCtrl(self, size=(-1,-1), style=wx.LC_REPORT|wx.BORDER_SUNKEN) #|wx.LC_HRULES|wx.LC_VRULES)
		#self.listDisplay.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))

	def getToolbarIcon(self, i):
		return BitmapFromImage( ImageFromStream( cStringIO.StringIO( base64.b64decode( A_strIconData[i] ) ) ) )

	def getIcon(self):
		icon = EmptyIcon()
		icon.CopyFromBitmap( BitmapFromImage( ImageFromStream( cStringIO.StringIO( base64.b64decode( strFrameIcon ) ) ) ) )
		return icon

	def Do_DownloadData(self, strParam):
		objRequest = urllib2.Request(conf__strLinkPrefix + strParam)
		objRequest.add_header('Cookie', conf__strCookies)
		objRequest.add_header('Referer', conf__strLinkPrefix + 'MenuRpm.htm')
		return urllib2.urlopen(objRequest).read()

	def GetConfigList(self, strData, strPrefix, strSufix):
		nPosStart = strData.find(strPrefix)
		if nPosStart>=0:
			nPosStart += len(strPrefix)
			nPosEnd = strData.find(strSufix, nPosStart)
			if nPosEnd>=0:
				A_strLines = strData[nPosStart:nPosEnd].replace('\\/', '/').split(strCrlf)
				for i in xrange(len(A_strLines)):
					A_strLines[i] = A_strLines[i][1:-2].strip() if A_strLines[i][0]=='"' else A_strLines[i][0:-1]
				return A_strLines
		return None


	def PA_DoReport(self, A_strKeys, oData):
		nLen = len(A_strKeys)
		self.listDisplay.DeleteAllItems()
		self.listDisplay.DeleteAllColumns()
		for i in xrange(nLen):
			strKey = A_strKeys[i]
			self.listDisplay.InsertColumn(i, A_strKeys[i], conf_nWidth[strKey][1], conf_nWidth[strKey][0])

		if oData:
			nRow = 0
			for o in oData:
				nItemID = self.listDisplay.InsertStringItem(nRow, o[A_strKeys[0]])
				for i in xrange(1, nLen):
					strKey = A_strKeys[i]
					self.listDisplay.SetStringItem(nItemID, i, o[strKey])
				nRow += 1


	def PA_DoFetchClientData(self):
		self.data1 = []

		strData = self.Do_DownloadData('AssignedIpAddrListRpm.htm')
		A_strLines = self.GetConfigList(strData, 'var DHCPDynPara=new Array(\n', strDataSufix)
		if A_strLines==None:
			print 'PA_DoFetchClientData() fail.'
			return
		nCount = int(A_strLines[0])
		A_strLines = self.GetConfigList(strData, 'var DHCPDynList=new Array(\n', strDataSufix)
		if A_strLines==None:
			print 'PA_DoFetchClientData() fail.'
			return
		nCount = len(A_strLines) / 4

		for i in xrange(nCount):
			n = i * 4
			oItem = {
				'@':str(i),
				A_strKeys1[0]:str(i+1),
				A_strKeys1[1]:A_strLines[n],
				A_strKeys1[2]:A_strLines[n+1],
				A_strKeys1[3]:A_strLines[n+2],
				A_strKeys1[4]:u'永久' if A_strLines[n+3]=='Permanent' else A_strLines[n+3],
				A_strKeys1[5]:''}

			# strMemo
			for strKey in conf_dictMemo:
				if strKey == oItem[strKey1]:
					oItem['strMemo'] = conf_dictMemo[strKey]
					break

			self.data1.append(oItem)

	def PA_DoFetchWLanStations(self):
		self.data2 = []

		strData = self.Do_DownloadData('WlanStationRpm.htm?Page=1')
		A_strLines = self.GetConfigList(strData, 'var wlanHostPara=new Array(\n', strDataSufix)
		if A_strLines==None:
			print 'PA_DoFetchWLanStations() fail.'
			return
		nCount = int(A_strLines[0])

		A_strLines = self.GetConfigList(strData, 'var hostList=new Array(\n', strDataSufix)
		if A_strLines==None:
			print 'PA_DoFetchWLanStations() fail.'
			return
		nCount = len(A_strLines) / 7

		for i in xrange(nCount):
			n = i * 7
			oItem = {
				'@':str(i),
				A_strKeys2[0]:str(i+1),
				A_strKeys2[1]:A_strLines[n],
				A_strKeys2[2]:A_strLines[n+1],
				strKey4:A_strLines[n+5],
				strKey5:A_strLines[n+6],
				A_strKeys2[5]:'',
				A_strKeys2[6]:'',
				A_strKeys2[7]:'',
				'flag':0}

			# strClientName, strIpAddress
			for o in self.data1:
				if oItem[strKey1] == o[strKey1]:
					oItem[strKey2] = o[strKey2] # strClientName
					oItem[strKey3] = o[strKey3] # strIpAddress
					break

			# strMemo
			for strKey in conf_dictMemo:
				if strKey == oItem[strKey1]:
					oItem['strMemo'] = conf_dictMemo[strKey]
					break

			self.data2.append(oItem)

	def PA_DoFetchSysLog(self):
		data3 = []

		strData = self.Do_DownloadData('SystemLogRpm.htm')
		A_strLines = self.GetConfigList(strData, 'var logList=new Array(\n', strDataSufix)
		if A_strLines==None:
			print 'PA_DoFetchSysLog() fail.'
			return data3

		nCount = len(A_strLines)
		for i in xrange(nCount):
			n = nCount - i - 1
			data3.append({
				A_strKeys3[0]:str(n),
				A_strKeys3[1]:A_strLines[n]})
		return data3

	def PA_DoDisplayDevInfo(self, e):
		A_strInfoKeys = ('', '', '')
		A_nInfoWidth = (90, 110, 390)
		nLen = len(A_strInfoKeys)

		self.listDisplay.DeleteAllItems()
		self.listDisplay.DeleteAllColumns()
		for i in xrange(nLen):
			self.listDisplay.InsertColumn(i, A_strInfoKeys[i], wx.LIST_FORMAT_LEFT, A_nInfoWidth[i])

		sectionId = []
		_row = [0]
		def addRowEx(*v):
			nRow = _row[0]
			nItemID = self.listDisplay.InsertStringItem(nRow, v[0])
			for i in xrange(1, len(v)):
				self.listDisplay.SetStringItem(nItemID, i, v[i])
			_row[0] += 1

		def addSection(s):
			sectionId.append(_row[0])
			addRowEx(s)
		
		def addRow(strKey, s):
			addRowEx('', strKey, s)

		nSeconds = -1
		strData = self.Do_DownloadData('StatusRpm.htm')
		A_strLines = self.GetConfigList(strData, "var statusPara=new Array(\n", strDataSufix)
		if A_strLines!=None:
			addSection(u'版本信息')
			addRow(u'当前软件版本：', A_strLines[5])
			addRow(u'当前硬件版本：', A_strLines[6])
			nSeconds = int(A_strLines[4])
		A_strLines = self.GetConfigList(strData, "var lanPara=new Array(\n", strDataSufix)
		if A_strLines!=None:
			addSection(u'LAN口状态')
			addRow(u'MAC地址：', A_strLines[0])
			addRow(u'IP地址：', A_strLines[1])
			addRow(u'子网掩码：', A_strLines[2])
		A_strLines = self.GetConfigList(strData, "var wlanPara=new Array(\n", strDataSufix)
		if A_strLines!=None:
			addSection(u'无线状态')
			addRow(u'无线功能：', A_strLines[0])
			addRow(u'SSID号：', A_strLines[1])
			addRow(u'MAC地址：', A_strLines[4])
		A_strLines = self.GetConfigList(strData, "var wanPara=new Array(\n", strDataSufix)
		if A_strLines!=None:
			addSection(u'WAN口状态')
			addRow(u'MAC地址：', A_strLines[1])
			addRow(u'IP地址：', A_strLines[2])
			addRow(u'子网掩码：', A_strLines[4])
			addRow(u'网关：', A_strLines[7])
			addRow(u'DNS服务器：', A_strLines[11])
			addRow(u'上网时间：', A_strLines[12])
		A_strLines = self.GetConfigList(strData, "var statistList=new Array(\n", strDataSufix)
		if A_strLines!=None:
			addSection(u'WAN口状态')
			addRow(u'字节数：', u'接收 %s, 发送 %s' % (A_strLines[0], A_strLines[1]))
			addRow(u'数据包数：', u'接收 %s, 发送 %s' % (A_strLines[2], A_strLines[3]))
		if nSeconds>=0:
			s = u'%s 天 %02d:%02d:%02d' % (nSeconds/86400, nSeconds%86400/3600, nSeconds%3600/60, nSeconds%60)
			addSection('')
			addRow(u'运行时间：', s)

		for nRow  in sectionId:
			self.listDisplay.SetItemTextColour(nRow, '#FFFFFF')
			self.listDisplay.SetItemBackgroundColour(nRow, '#006699')


	def PA_DoDisplayReport(self, e):
		self.PA_DoFetchClientData()
		self.PA_DoFetchWLanStations()

		data3 = []
		n = 0
		for i in self.data1:
			oItem = {
				'@':str(n),
				A_strKeys1[0]:i[A_strKeys1[0]],
				A_strKeys1[1]:i[A_strKeys1[1]],
				A_strKeys1[2]:i[A_strKeys1[2]],
				A_strKeys1[3]:i[A_strKeys1[3]],
				A_strKeys1[4]:i[A_strKeys1[4]],
				A_strKeys1[5]:i[A_strKeys1[5]],
				strKey4:'',
				strKey5:''}

			for o in self.data2:
				if o[strKey1] == i[strKey1]:
					oItem[strKey4] = o[strKey4] # nReceive
					oItem[strKey5] = o[strKey5] # nSend
					o['flag']=1

			data3.append(oItem)
			n += 1

		for o in self.data2:
			if o['flag']==0:
				data3.append({
					'@':str(n),
					A_strKeys1[0]:'@'+o[A_strKeys1[0]],
					A_strKeys1[1]:'',
					A_strKeys1[2]:o[A_strKeys1[2]],
					A_strKeys1[3]:'',
					A_strKeys1[4]:'',
					A_strKeys1[5]:'',
					strKey4:o[strKey4],
					strKey5:o[strKey5]})

		A_strKeys3n = ('@',) + A_strKeys1 + (strKey4, strKey5)
		self.PA_DoReport(A_strKeys3n, data3)

	def PA_DoDisplayHosts(self, e):
		self.PA_DoFetchClientData()
		self.PA_DoReport(A_strKeys1n, self.data1)

	def PA_DoDisplayStations(self, e):
		self.PA_DoFetchClientData()
		self.PA_DoFetchWLanStations()
		self.PA_DoReport(A_strKeys2n, self.data2)

	def PA_DoDisplaySysLog(self, e):
		self.PA_DoReport(A_strKeys3, self.PA_DoFetchSysLog())

	def PA_DoClearSysLog(self, e):
		if wx.MessageBox(u'清空设备日志么 ?', conf__strCaptain, \
				wx.YES_NO | wx.ICON_QUESTION | wx.NO_DEFAULT ) == wx.YES:
			self.Do_DownloadData('SystemLogRpm.htm?ClearLog=%C7%E5%B3%FD%CB%F9%D3%D0%C8%D5%D6%BE')
			self.PA_DoDisplaySysLog(0)

	def PA_DoRebootDevice(self, e):
		if wx.MessageBox(u'确定要重启设备么 ?', conf__strCaptain, \
				wx.YES_NO | wx.ICON_QUESTION | wx.NO_DEFAULT ) == wx.YES:
			self.Do_DownloadData('SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7')
			wx.MessageBox(u"正在重启，请等待15秒。", conf__strCaptain, wx.OK | wx.ICON_INFORMATION)



if __name__ == '__main__':
	app = wx.App()
	ex = PaSpyRouter2016WX()
	ex.Show()
	app.MainLoop()
