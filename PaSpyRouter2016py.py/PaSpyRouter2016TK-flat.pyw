#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 2.7
# PaSpyRouter2016TK-flat.pyw

from Tkinter import *
import urllib2, tkMessageBox as mb

conf__strCookies = 'Authorization=Basic%20YWRtaW46cGFzc3dk; ChgPwdSubTag='
conf__strCaptain = 'PaSpyRouter2016TK.pyw'
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
A_strKeys3 = ('id', 'strBrief')

strKey1 = A_strKeys1[2] # strMacAddress
strKey2 = A_strKeys1[1] # strClientName
strKey3 = A_strKeys1[3] # strIpAddress
strKey4 = A_strKeys2[3] # nReceive
strKey5 = A_strKeys2[4] # nSend

'''
conf__strUserAgent = 'Mozilla/5.0 (Windows NT 5.2; rv:43.0) Gecko/20100101 Firefox/43.0'
conf__requestHeaders = {
	'Host': '192.168.1.1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 5.2; rv:43.0) Gecko/20100101 Firefox/43.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'Referer': 'MenuRpm.htm',
	'Cookie': 'Authorization=Basic%20YWRtaW46cGFzc3dk; ChgPwdSubTag=',
	'Connection': 'keep-alive'
}
req1 = urllib2.Request('AssignedIpAddrListRpm.htm', headers=conf__requestHeaders)
req1.add_header('User-Agent', conf__strUserAgent)
req1.add_header('Connection', 'keep-alive')
req1.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
req1.add_header('Accept-Language', 'en-US,en;q=0.5')
req1.add_header('Accept-Encoding', 'gzip, deflate')
'''


def strLen(s):
	n = 0
	for ch in s:
		n += 1 if ord(ch)<127 else 2
	return n

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
	len_keys = len(A_strKeys)
	s = ''
	for i in xrange(len_keys):
		s+= A_strKeys[i].ljust(oData['width'][i]) + ' '
	objList.insert(END, s.rstrip())
	objList.insert(END, '=' * (sum(oData['width']) + len_keys))
	for i in oData['items']:
		s = ''
		for n in xrange(len_keys):
			sData = i[A_strKeys[n]]
			if A_strKeys[n] in ('@', 'id', strKey4, strKey5):
				s += ' ' * (oData['width'][n]-strLen(sData)) + sData + ' ' # align right
			else:
				s += sData + ' ' * (oData['width'][n]-strLen(sData) + 1)   # align left
		objList.insert(END, s.rstrip())

def PA_DoFetchClientData():
	global data1
	data1 = {'items':[], 'width':[len(A_strKeys1[i]) for i in xrange(len(A_strKeys1))]}

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
			A_strKeys1[0]:str(i+1),
			A_strKeys1[1]:A_strLines[n],
			A_strKeys1[2]:A_strLines[n+1],
			A_strKeys1[3]:A_strLines[n+2],
			A_strKeys1[4]:A_strLines[n+3],
			A_strKeys1[5]:''}

		# strMemo
		for strKey in conf_dictMemo:
			if strKey == oItem[strKey1]:
				oItem['strMemo'] = conf_dictMemo[strKey]
				break

		data1['items'].append(oItem)

		# 修正列最大宽度
		for ii in xrange(len(A_strKeys1)):
			l = strLen(oItem[A_strKeys1[ii]])
			if l>data1['width'][ii]:
				data1['width'][ii] = l

def PA_DoFetchWLanStations():
	global data2
	data2 = {'items':[], 'width':[len(A_strKeys2[i]) for i in xrange(len(A_strKeys2))]}

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
			A_strKeys2[0]:str(i+1),
			A_strKeys2[1]:A_strLines[n],
			A_strKeys2[2]:A_strLines[n+1],
			A_strKeys2[3]:A_strLines[n+5],
			A_strKeys2[4]:A_strLines[n+6],
			A_strKeys2[5]:'',
			A_strKeys2[6]:'',
			A_strKeys2[7]:''}

		# strClientName, strIpAddress
		for o in data1['items']:
			if oItem[strKey1] == o[strKey1]:
				oItem[strKey2] = o[strKey2] # strClientName
				oItem[strKey3] = o[strKey3] # strIpAddress
				break

		# strMemo
		for strKey in conf_dictMemo:
			if strKey == oItem[strKey1]:
				oItem['strMemo'] = conf_dictMemo[strKey]
				break

		data2['items'].append(oItem)

		# 修正列最大宽度
		for ii in xrange(len(A_strKeys2)):
			l = strLen(oItem[A_strKeys2[ii]])
			if l>data2['width'][ii]:
				data2['width'][ii] = l

def PA_DoDisplayDevInfo():
	objList.delete(0, END)

	def addSection(s):
		objList.insert(END, '- ' + s + ' ' + '-' * (90 - 3 - strLen(s)) )
	
	def addRow(strKey, s):
		objList.insert(END, ' ' * 12 + strKey + ' ' * (15 - strLen(strKey) ) + s)

	n = 0
	nSeconds = -1
	strData = Do_DownloadData('StatusRpm.htm')
	A_strLines = GetConfigList(strData, "var statusPara=new Array(\n", strDataSufix)
	if A_strLines!=None:
		addSection(u'版本信息')
		addRow(u'当前软件版本：', A_strLines[5])
		addRow(u'当前硬件版本：', A_strLines[6])
		nSeconds = int(A_strLines[4])
	A_strLines = GetConfigList(strData, "var lanPara=new Array(\n", strDataSufix)
	if A_strLines!=None:
		addSection(u'LAN口状态')
		addRow(u'MAC地址：', A_strLines[0])
		addRow(u'IP地址：', A_strLines[1])
		addRow(u'子网掩码：', A_strLines[2])
	A_strLines = GetConfigList(strData, "var wlanPara=new Array(\n", strDataSufix)
	if A_strLines!=None:
		addSection(u'无线状态')
		addRow(u'无线功能：', A_strLines[0])
		addRow(u'SSID号：', A_strLines[1])
		addRow(u'MAC地址：', A_strLines[4])
	A_strLines = GetConfigList(strData, "var wanPara=new Array(\n", strDataSufix)
	if A_strLines!=None:
		addSection(u'WAN口状态')
		addRow(u'MAC地址：', A_strLines[1])
		addRow(u'IP地址：', A_strLines[2])
		addRow(u'子网掩码：', A_strLines[4])
		addRow(u'网关：', A_strLines[7])
		addRow(u'DNS服务器：', A_strLines[11])
		addRow(u'上网时间：', A_strLines[12])
	A_strLines = GetConfigList(strData, "var statistList=new Array(\n", strDataSufix)
	if A_strLines!=None:
		addSection(u'WAN口流量统计')
		addRow(u'字节数：', u'接收 %s, 发送 %s' % (A_strLines[0], A_strLines[1]) )
		addRow(u'数据包数：', u'接收 %s, 发送 %s' % (A_strLines[2], A_strLines[3]) )
	if nSeconds>=0:
		s = u'%s 天 %02d:%02d:%02d' % (nSeconds/86400, nSeconds%86400/3600, nSeconds%3600/60, nSeconds%60)
		objList.insert(END, '-' * 90)
		addRow(u'运行时间：', s)


def PA_DoFetchSysLog():
	data3 = {'items':[], 'width':[len(A_strKeys3[i]) for i in xrange(len(A_strKeys3))]}

	strData = Do_DownloadData('SystemLogRpm.htm')
	A_strLines = GetConfigList(strData, 'var logList=new Array(\n', strDataSufix)
	if A_strLines==None:
		print 'PA_DoFetchSysLog() fail.'
		return data3

	nCount = len(A_strLines)

	len_width = len(data3['width'])
	for i in xrange(nCount):
		oItem = {
			A_strKeys3[0]:str(i),
			A_strKeys3[1]:A_strLines[i]}

		data3['items'].insert(0, oItem)

		# 修正列最大宽度
		for ii in xrange(len(A_strKeys3)):
			l = strLen(oItem[A_strKeys3[ii]])
			if l>data3['width'][ii]:
				data3['width'][ii] = l

	return data3


def PA_DoDisplayReport():
	objList.delete(0, END)
	PA_DoFetchClientData()
	PA_DoFetchWLanStations()
	A_strKeys = ('@', 'id', 'strClientName', 'strMacAddress', 'strIpAddress', 'strTimeout', 'nReceive', 'nSend', 'strMemo')
	data3 = {'items':[], 'width':[len(A_strKeys[i]) for i in xrange(len(A_strKeys))]}
	n = 0
	catchedId = []
	for o in data1['items']:
		oItem = {
			A_strKeys[0]:str(n),
			A_strKeys[1]:o[A_strKeys[1]],
			A_strKeys[2]:o[A_strKeys[2]],
			A_strKeys[3]:o[A_strKeys[3]],
			A_strKeys[4]:o[A_strKeys[4]],
			A_strKeys[5]:o[A_strKeys[5]],
			strKey4:'',
			strKey5:'',
			A_strKeys[8]:o[A_strKeys[8]]}

		for oo in data2['items']:
			if oo[strKey1]==o[strKey1]:
				oItem[strKey4] = oo[strKey4]
				oItem[strKey5] = oo[strKey5]
				catchedId.append(oo['id'])

		data3['items'].append(oItem)

		# 修正列最大宽度
		for i in xrange(len(A_strKeys)):
			l = strLen(oItem[A_strKeys[i]])
			if l>data3['width'][i]:
				data3['width'][i] = l

		n += 1

	for o in data2['items']:
		if o['id'] not in catchedId:
			oItem = {
				A_strKeys[0]:str(n),
				A_strKeys[1]:'@' + o[A_strKeys[1]],
				A_strKeys[2]:'',
				A_strKeys[3]:o[A_strKeys[3]],
				A_strKeys[4]:'',
				A_strKeys[5]:'',
				strKey4:o[strKey4],
				strKey5:o[strKey5],
				A_strKeys[8]:''}

			data3['items'].append(oItem)

			# 修正列最大宽度
			for i in xrange(len(A_strKeys)):
				l = strLen(oItem[A_strKeys[i]])
				if l>data3['width'][i]:
					data3['width'][i] = l

			n += 1

	PA_DoReport(A_strKeys, data3)

def PA_DoDisplayHosts():
	objList.delete(0, END)
	PA_DoFetchClientData()
	PA_DoReport(A_strKeys1, data1)

def PA_DoDisplayStations():
	objList.delete(0, END)
	PA_DoFetchClientData()
	PA_DoFetchWLanStations()
	PA_DoReport(A_strKeys2, data2)

def PA_DoDisplaySysLog():
	objList.delete(0, END)
	PA_DoReport(A_strKeys3, PA_DoFetchSysLog())


def PA_DoClearSysLog():
	if mb.askyesno(conf__strCaptain, u'清空设备日志么 ?', default=mb.NO):
		Do_DownloadData('SystemLogRpm.htm?ClearLog=%C7%E5%B3%FD%CB%F9%D3%D0%C8%D5%D6%BE')
		PA_DoDisplaySysLog()


def PA_DoRebootDevice():
	if mb.askyesno(conf__strCaptain, u'确定要重启设备么 ?', default=mb.NO):
		Do_DownloadData('SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7')
		objList.delete(0, END)
		objList.insert(END, 'Reboot.')
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
	frame1.geometry('+%s+%s' % (frame1.winfo_screenwidth()/2-364, frame1.winfo_screenheight()/2-187))
	frame1.title(conf__strCaptain)

	frame1.tk.call('wm', 'iconphoto', frame1._w, PhotoImage(data=strFrameIcon))

	A_objIcons = []
	objToolbar = Frame(frame1)
	for i in xrange(len(A_strIconData)):
		A_objIcons.append(PhotoImage(data = A_strIconData[i]))
		Button(objToolbar, image=A_objIcons[i], width=16, bd=0,
			command=lambda n=i:buttonClick(n) ).pack(side=LEFT, padx=2, pady=2)

	objToolbar.pack(side=TOP, fill=X)
	objList = Listbox(frame1, width=100, height=23, font=('宋体', 10))
	objList.pack(expand=YES, fill=BOTH, side=LEFT)
	objScroll = Scrollbar(frame1)
	objScroll.pack(side=RIGHT, fill=Y)
	objList['yscrollcommand'] = objScroll.set
	objScroll['command'] = objList.yview

	mainloop()
