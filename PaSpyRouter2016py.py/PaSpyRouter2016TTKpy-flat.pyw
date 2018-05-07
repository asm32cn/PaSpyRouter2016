#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 2.7
# PaSpyRouter2016TTKpy-flat.pyw

from Tkinter import *
import urllib2, ttk, tkMessageBox as mb

conf__strCookies = 'Authorization=Basic%20YWRtaW46cGFzc3dk; ChgPwdSubTag='
conf__strCaptain = 'PaSpyRouter2016TTKpy.pyw'
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

conf_nWidth = {
	'@':(30, 'e'),
	'strClientName':(175, 'w'),
	'strMacAddress':(125, 'w'),
	'strIpAddress':(105, 'w'),
	'strTimeout':(85, 'center'),
	'strMemo':(65, 'w'),
	'nStatus':(65, 'center'),
	'nReceive':(65, 'e'),
	'nSend':(65, 'e'),
	'id':(30, 'e'),
	'strBrief':(683, 'w')}

def Do_DownloadData(strParam):
	objRequest = urllib2.Request(conf__strLinkPrefix + strParam)
	objRequest.add_header('Cookie', conf__strCookies)
	objRequest.add_header('Referer', conf__strLinkPrefix + 'MenuRpm.htm')
	return urllib2.urlopen(objRequest).read()

def GetConfigList(strData, strPrefix, strSufix):
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

def PA_DoReport(A_strKeys, oData):
	[objListview.delete(objItem) for objItem in objListview.get_children()]
	objListview['columns'] = A_strKeys
	for i in xrange(len(A_strKeys)):
		strColumnName, strKey = '#%s' % (i+1), A_strKeys[i]
		objListview.column(strColumnName, width=conf_nWidth[strKey][0], anchor=conf_nWidth[strKey][1])
		objListview.heading(strColumnName, text=strKey, anchor=conf_nWidth[strKey][1])
	ii = 0
	for i in oData:
		objListview.insert('', ii, values=[i[A_strKeys[n]]  for n in xrange(len(A_strKeys))] )
		ii += 1

def PA_DoFetchClientData():
	global data1
	data1 = []

	strData = Do_DownloadData('AssignedIpAddrListRpm.htm')
	A_strLines = GetConfigList(strData, 'var DHCPDynPara=new Array(\n', strDataSufix)
	if A_strLines==None:
		print 'PA_DoFetchClientData() fail.'
		return
	nCount = int(A_strLines[0])
	A_strLines = GetConfigList(strData, 'var DHCPDynList=new Array(\n', strDataSufix)
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

		for strKey in conf_dictMemo:
			if strKey == oItem[strKey1]:
				oItem['strMemo'] = conf_dictMemo[strKey]
				break

		data1.append(oItem)

def PA_DoFetchWLanStations():
	global data2
	data2 = []

	strData = Do_DownloadData('WlanStationRpm.htm?Page=1')
	A_strLines = GetConfigList(strData, 'var wlanHostPara=new Array(\n', strDataSufix)
	if A_strLines==None:
		print 'PA_DoFetchWLanStations() fail.'
		return
	nCount = int(A_strLines[0])

	A_strLines = GetConfigList(strData, 'var hostList=new Array(\n', strDataSufix)
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
		for o in data1:
			if oItem[strKey1] == o[strKey1]:
				oItem[strKey2] = o[strKey2] # strClientName
				oItem[strKey3] = o[strKey3] # strIpAddress
				break

		# strMemo
		for strKey in conf_dictMemo:
			if strKey==oItem[strKey1]:
				oItem['strMemo'] = conf_dictMemo[strKey]
				break

		data2.append(oItem)

def PA_DoFetchSysLog():
	data3 = []

	strData = Do_DownloadData('SystemLogRpm.htm')
	A_strLines = GetConfigList(strData, 'var logList=new Array(\n', strDataSufix)
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

def PA_DoDisplayDevInfo():
	[objListview.delete(objItem) for objItem in objListview.get_children()]
	A_strInfoKeys = ('', '', '')
	A_nInfoWidth = (90, 110, 352)
	objListview['columns'] = A_strInfoKeys
	for i in xrange(len(A_strInfoKeys)):
		strColumnName, strKey = '#%s' % (i+1), A_strInfoKeys[i]
		objListview.column(strColumnName, width=A_nInfoWidth[i], anchor='w')
		objListview.heading(strColumnName, text=strKey, anchor='w')
	n = 0
	nSeconds = -1
	strData = Do_DownloadData('StatusRpm.htm')
	A_strLines = GetConfigList(strData, "var statusPara=new Array(\n", strDataSufix)
	if A_strLines!=None:
		objListview.insert('', n, values=(u'版本信息', '', ''), tags=('section') );n += 1
		objListview.insert('', n, values=('', u'当前软件版本：', A_strLines[5]) );n += 1
		objListview.insert('', n, values=('', u'当前硬件版本：', A_strLines[6]) );n += 1
		nSeconds = int(A_strLines[4])
	A_strLines = GetConfigList(strData, "var lanPara=new Array(\n", strDataSufix)
	if A_strLines!=None:
		objListview.insert('', n, values=(u'LAN口状态', '', ''), tags=('section') );n += 1
		objListview.insert('', n, values=('', u'MAC地址：', A_strLines[0]) );n += 1
		objListview.insert('', n, values=('', u'IP地址：', A_strLines[1]) );n += 1
		objListview.insert('', n, values=('', u'子网掩码：', A_strLines[2]) );n += 1
	A_strLines = GetConfigList(strData, "var wlanPara=new Array(\n", strDataSufix)
	if A_strLines!=None:
		objListview.insert('', n, values=(u'无线状态', '', ''), tags=('section') );n += 1
		objListview.insert('', n, values=('', u'无线功能：', A_strLines[0]) );n += 1
		objListview.insert('', n, values=('', u'SSID号：', A_strLines[1]) );n += 1
		objListview.insert('', n, values=('', u'MAC地址：', A_strLines[4]) );n += 1
	A_strLines = GetConfigList(strData, "var wanPara=new Array(\n", strDataSufix)
	if A_strLines!=None:
		objListview.insert('', n, values=(u'WAN口状态', '', ''), tags=('section') );n += 1
		objListview.insert('', n, values=('', u'MAC地址：', A_strLines[1]) );n += 1
		objListview.insert('', n, values=('', u'IP地址：', A_strLines[2]) );n += 1
		objListview.insert('', n, values=('', u'子网掩码：', A_strLines[4]) );n += 1
		objListview.insert('', n, values=('', u'网关：', A_strLines[7]) );n += 1
		objListview.insert('', n, values=('', u'DNS服务器：', A_strLines[11]) );n += 1
		objListview.insert('', n, values=('', u'上网时间：', A_strLines[12]) );n += 1
	A_strLines = GetConfigList(strData, "var statistList=new Array(\n", strDataSufix)
	if A_strLines!=None:
		objListview.insert('', n, values=(u'WAN口流量统计', '', ''), tags=('section') );n += 1
		objListview.insert('', n, values=('', u'字节数：', '接收 %s, 发送 %s' % (A_strLines[0], A_strLines[1])) );n += 1
		objListview.insert('', n, values=('', u'数据包数：', '接收 %s, 发送 %s' % (A_strLines[2], A_strLines[3])) );n += 1
	if nSeconds>=0:
		s = '%s 天 %02d:%02d:%02d' % (nSeconds/86400, nSeconds%86400/3600, nSeconds%3600/60, nSeconds%60)
		objListview.insert('', n, values=(u'', '', ''), tags=('section') );n += 1
		objListview.insert('', n, values=('', u'运行时间：', s) );n += 1
	objListview.tag_configure('section', background='#006699', foreground='#FFFFFF')

def PA_DoDisplayReport():
	PA_DoFetchClientData()
	PA_DoFetchWLanStations()

	data3 = []
	n = 0
	for i in data1:
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
		for o in data2:
			if o[strKey1] == i[strKey1]:
				oItem[strKey4] = o[strKey4]
				oItem[strKey5] = o[strKey5]
				o['flag']=1
		data3.append(oItem)
		n += 1
	for o in data2:
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
	PA_DoReport(A_strKeys3n, data3)

def PA_DoDisplayHosts():
	PA_DoFetchClientData()
	PA_DoReport(A_strKeys1n, data1)

def PA_DoDisplayStations():
	PA_DoFetchClientData()
	PA_DoFetchWLanStations()
	PA_DoReport(A_strKeys2n, data2)

def PA_DoDisplaySysLog():
	PA_DoReport(A_strKeys3, PA_DoFetchSysLog())

def PA_DoClearSysLog():
	if mb.askyesno(conf__strCaptain, u'清空设备日志么 ?', default=mb.NO):
		Do_DownloadData('SystemLogRpm.htm?ClearLog=%C7%E5%B3%FD%CB%F9%D3%D0%C8%D5%D6%BE')
		PA_DoDisplaySysLog()

def PA_DoRebootDevice():
	if mb.askyesno(conf__strCaptain, u'确定要重启设备么 ?', default=mb.NO):
		Do_DownloadData('SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7')
		mb.showinfo(conf__strCaptain, '正在重启，请等待15秒。')

def buttonClick(n):
	#print n
	if n==0:
		PA_DoDisplayDevInfo()
	elif n==1:
		PA_DoDisplayReport()
	elif n==2:
		PA_DoDisplayHosts()
	elif n==3:
		PA_DoDisplayStations()
	elif n==4:
		PA_DoDisplaySysLog()
	elif n==5:
		PA_DoClearSysLog()
	elif n==6:
		PA_DoRebootDevice()


if __name__ == '__main__':
	frame1 = Tk()
	frame1.title(conf__strCaptain)

	frame1.tk.call('wm', 'iconphoto', frame1._w, PhotoImage(data=strFrameIcon))
	frame1.geometry('780x450+%s+%s' % (frame1.winfo_screenwidth()/2-394, frame1.winfo_screenheight()/2-238) )

	objToolbar = Frame(frame1)
	A_objIcons = []
	for i in xrange(7):
		A_objIcons.append(PhotoImage(data = A_strIconData[i]))
		Button(objToolbar, image=A_objIcons[i], width=16, bd=0,
			command=lambda n=i:buttonClick(n) ).pack(side=LEFT, padx=5, pady=5)
	objToolbar.pack(side=TOP, fill=X)

	objListview = ttk.Treeview(frame1, show='headings')
	objScroll = Scrollbar(frame1)
	objListview.pack(side=LEFT, expand=YES, fill=BOTH)
	objScroll.pack(side=RIGHT, fill=Y)
	objListview['yscrollcommand'] = objScroll.set
	objScroll['command'] = objListview.yview

	mainloop()
