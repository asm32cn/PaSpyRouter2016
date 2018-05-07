#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 2.7
# PaSpyRouter2016Qt.pyw

import sys, urllib2, re
from PyQt4 import QtGui, QtCore

conf__strCookies = 'Authorization=Basic%20YWRtaW46cGFzc3dk; ChgPwdSubTag='
conf__strCaptain = 'PaSpyRouter2016Qt.pyw'
conf__strLinkPrefix = 'http://192.168.1.1/userRpm/'

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
	left = QtCore.Qt.AlignLeft
	center = QtCore.Qt.AlignCenter
	right = QtCore.Qt.AlignRight

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
	{'icon':'res/res-button-01.png', 'text':u'设备状态', 'tip':u'查看设备状态'},
	{'icon':'res/res-button-02.png', 'text':u'报表', 'tip':u'查看综合报表'},
	{'icon':'res/res-button-03.png', 'text':u'DHCP', 'tip':u'查看DHCP列表'},
	{'icon':'res/res-button-04.png', 'text':u'数据包', 'tip':u'统计无线数据包'},
	{'icon':'res/res-button-05.png', 'text':u'日志', 'tip':u'查看设备日志'},
	{'icon':'res/res-button-06.png', 'text':u'清除日志', 'tip':u'清除日志'},
	{'icon':'res/res-button-07.png', 'text':u'重启设备', 'tip':u'重启设备'}]


class PaSpyRouter2016Qt(QtGui.QMainWindow):
	def __init__(self):
		super(PaSpyRouter2016Qt, self).__init__()

		self.setWindowTitle(conf__strCaptain)
		self.resize(780, 450)
		self.setWindowIcon(QtGui.QIcon('res/PaSpyRouter2016py-icon.gif'))

		self.initUI()
	
	def initUI(self):

		self.objDisplay = QtGui.QTreeView()
		self.objDisplay.setRootIsDecorated(False)
		self.objDisplay.setAlternatingRowColors(True)
		self.objDisplay.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.setCentralWidget(self.objDisplay)

		#self.objDisplay.setFont( QtGui.QFont('宋体', 10) )

		toolBar = self.addToolBar('ToolBar')
		for i in xrange(len(conf__dictActions)):
			cfgItem = conf__dictActions[i]
			objAction = QtGui.QAction(QtGui.QIcon(cfgItem['icon']), cfgItem['text'], self)
			objAction.setStatusTip(cfgItem['tip'])
			self.connect(objAction, QtCore.SIGNAL('triggered()'), lambda n=i:self.doToolbarClick(n))
			toolBar.addAction(objAction)
			if i in (0, 3, 5):
				toolBar.addSeparator()
		self.statusBar()


	def doToolbarClick(self, n):
		if n == 0:
			self.PA_DoDisplayDevInfo()
		elif n == 1:
			self.PA_DoDisplayReport()
		elif n == 2:
			self.PA_DoDisplayHosts()
		elif n == 3:
			self.PA_DoDisplayStations()
		elif n == 4:
			self.PA_DoDisplaySysLog()
		elif n == 5:
			self.PA_DoClearSysLog()
		elif n == 6:
			self.PA_DoRebootDevice()


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
		model = QtGui.QStandardItemModel(0, nLen, self)
		for i in xrange(nLen):
			strKey = A_strKeys[i]
			#columnItem = QtGui.QStandardItem(strKey)
			#columnItem.setTextAlignment(conf_nWidth[strKey][1])
			#model.setHorizontalHeaderItem(i, columnItem)
			model.setHeaderData(i, QtCore.Qt.Horizontal, A_strKeys[i])
			model.horizontalHeaderItem(i).setTextAlignment(conf_nWidth[strKey][1])

		if oData:
			nRow = 0
			for o in oData:
				model.insertRow(nRow)
				oItem = QtGui.QStandardItem(str(nRow))
				model.setItem(nRow, oItem)
				for i in xrange(nLen):
					strKey = A_strKeys[i]
					#oSubItem = QtGui.QStandardItem(o[strKey])
					#oSubItem.setTextAlignment(conf_nWidth[strKey][1])
					#model.setItem( nRow, i, oSubItem)
					model.setData( model.index(nRow, i), o[strKey])
					model.item(nRow, i).setTextAlignment(conf_nWidth[strKey][1])
				nRow += 1

		self.objDisplay.setModel(model);
		for i in xrange(nLen):
			strKey = A_strKeys[i]
			self.objDisplay.setColumnWidth(i, conf_nWidth[strKey][0])

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

	def PA_DoDisplayDevInfo(self):
		A_strInfoKeys = ('', '', '')
		A_nInfoWidth = (90, 110, 390)
		nLen = len(A_strInfoKeys)

		oSectionText = QtGui.QColor(255, 255, 255, 255)
		oSectionBack = QtGui.QColor(0, 102, 153, 255)

		model = QtGui.QStandardItemModel(0, nLen, self)
		for i in xrange(nLen):
			model.setHeaderData(i, QtCore.Qt.Horizontal, A_strInfoKeys[i])

		sectionId = []
		_row = [0]
		def addRowEx(*v):
			nRow = _row[0]
			model.insertRow(nRow)
			for i in xrange(len(v)):
				model.setData( model.index(nRow, i), v[i])
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

		self.objDisplay.setModel(model);
		for i in xrange(nLen):
			self.objDisplay.setColumnWidth(i, A_nInfoWidth[i])
		

		for nRow  in sectionId:
			for i in xrange(3):
				model.setData( model.index(nRow, i), oSectionText, QtCore.Qt.TextColorRole)
				model.setData( model.index(nRow, i), oSectionBack, QtCore.Qt.BackgroundRole)


	def PA_DoDisplayReport(self):
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

	def PA_DoDisplayHosts(self):
		self.PA_DoFetchClientData()
		self.PA_DoReport(A_strKeys1n, self.data1)

	def PA_DoDisplayStations(self):
		self.PA_DoFetchClientData()
		self.PA_DoFetchWLanStations()
		self.PA_DoReport(A_strKeys2n, self.data2)

	def PA_DoDisplaySysLog(self):
		self.PA_DoReport(A_strKeys3, self.PA_DoFetchSysLog())

	def PA_DoClearSysLog(self):
		if QtGui.QMessageBox.question(self, conf__strCaptain, u'清空设备日志么 ?', \
				QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
			self.Do_DownloadData('SystemLogRpm.htm?ClearLog=%C7%E5%B3%FD%CB%F9%D3%D0%C8%D5%D6%BE')
			self.PA_DoDisplaySysLog()

	def PA_DoRebootDevice(self):
		if QtGui.QMessageBox.question(self, conf__strCaptain, u'确定要重启设备么 ?', \
				QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
			self.Do_DownloadData('SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7')
			QtGui.QMessageBox.information(self, conf__strCaptain, u'正在重启，请等待15秒。')


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	wndMain = PaSpyRouter2016Qt()
	wndMain.show()
	app.exec_()
