// ChildView.cpp : implementation of the CChildView class
//

#include "stdafx.h"
#include "PaSpyRouter2016MFC.h"
#include "ChildView.h"
#include <exception>

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CChildView

CChildView::CChildView()
{
}

CChildView::~CChildView()
{
}

IMPLEMENT_DYNCREATE(CChildView, CListView)

BEGIN_MESSAGE_MAP(CChildView,CWnd )
	//{{AFX_MSG_MAP(CChildView)
	ON_WM_CREATE()
	ON_COMMAND(IDC_RELOAD_HOSTS, OnReloadHosts)
	ON_COMMAND(IDC_RELOAD_REPORT, OnReloadReport)
	ON_COMMAND(IDC_RELOAD_STATIONS, OnReloadStations)
	ON_COMMAND(IDC_RELOAD_LOGS, OnReloadLogs)
	ON_COMMAND(IDC_ROUTER_REBOOT, OnRouterReboot)
	ON_COMMAND(IDC_CLEAR_LOG, OnClearLog)
	ON_COMMAND(IDC_DEV_INFO, OnDevInfo)
	//}}AFX_MSG_MAP
	ON_NOTIFY_REFLECT(NM_CUSTOMDRAW, OnNMCustomdraw)
END_MESSAGE_MAP()


/////////////////////////////////////////////////////////////////////////////
// CChildView message handlers

BOOL CChildView::PreCreateWindow(CREATESTRUCT& cs) 
{
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	return CListView::PreCreateWindow(cs);
	/*
	if (!CWnd::PreCreateWindow(cs))
		return FALSE;

	cs.dwExStyle |= WS_EX_CLIENTEDGE;
	cs.style &= ~WS_BORDER;
	cs.lpszClass = AfxRegisterWndClass(CS_HREDRAW|CS_VREDRAW|CS_DBLCLKS, 
		::LoadCursor(NULL, IDC_ARROW), HBRUSH(COLOR_WINDOW+1), NULL);

	return TRUE;
	*/
}

/////////////////////////////////////////////////////////////////////////////
// CPaTestCView2016AView message handlers

int CChildView::OnCreate(LPCREATESTRUCT lpCreateStruct) 
{
	if (CWnd ::OnCreate(lpCreateStruct) == -1)
		return -1;

	// TODO: Add your specialized creation code here
	PA_DoViewInitialize();
	return 0;
}

void CChildView::PA_DoViewInitialize()
{
	m_nClientCount = 0;

	isConnFail = FALSE;

	m_nBufferSize = sizeof(m_szWebBuffer);

	m_strRequestHeader.LoadString(IDS_REQUEST_HEADER);

	m_nMemoCount = 8;
	A_objMemo[0].Init(1, "DC-6D-CD-75-B9-79", "理发店");
	A_objMemo[1].Init(2, "F6-D0-10-96-DC-E2", "酷派.我");
	A_objMemo[2].Init(3, "9C-A9-E4-A5-8D-B8", "中兴.我");
	A_objMemo[3].Init(4, "A0-93-47-96-B7-70", "OPPO.蒋");
	A_objMemo[4].Init(5, "F4-29-81-92-4B-D0", "玉米.女");
	A_objMemo[5].Init(6, "24-09-95-63-7F-64", "鸡柳.女");
	A_objMemo[6].Init(7, "F4-29-81-C7-DD-A7", "叶刚.vo");
	A_objMemo[7].Init(8, "E8-BB-A8-A8-42-26", "奶茶.邻");

	// Init ListView Header
	CListCtrl& m_listDisplay = GetListCtrl();
	m_listDisplay.SetExtendedStyle(LVS_EX_FULLROWSELECT|LVS_EX_GRIDLINES);
	m_listDisplay.ModifyStyle(LVS_TYPEMASK, LVS_REPORT);

	OnReloadReport();

}

void CChildView::PA_DoReloadHostsData()
{
	PA_DoDownloadData("AssignedIpAddrListRpm.htm", m_szWebBuffer, m_nBufferSize);
	m_nClientCount = PA_DoFetchClientCount((BYTE *)m_szWebBuffer, m_nBufferSize);
	PA_DoFetchClientDetails((BYTE *)m_szWebBuffer, m_nBufferSize);

	//AfxMessageBox(s);
	//AfxMessageBox(m_szWebBuffer);
	/*
	CHAR szType[] = "TEXT";
	UINT nResourceID = IDR_TEXT1;
	HINSTANCE hModule = AfxGetApp()->m_hInstance;
	HRSRC hr;
	HGLOBAL lpData;
	if( hr = FindResource(hModule, MAKEINTRESOURCE(nResourceID), szType) ){
		if(lpData = LoadResource(hModule,  hr)){
			DWORD dwSize = SizeofResource(hModule, hr);
			BYTE * lpbData = (BYTE *)lpData;
			m_nClientCount = PA_DoFetchClientCount(lpbData, dwSize);
			PA_DoFetchClientDetails(lpbData, dwSize);
		}
	}
	*/

	//m_nClientCount = 4;
	// Init Demo Data
	//A_objClient[0].Init(1, "MIPAD-Asm32", "98-FA-E3-44-F2-DB", "192.168.1.88", "Permanent");
	//A_objClient[1].Init(2, "Asm32-PC", "00-1E-4F-57-25-BA", "192.168.1.66", "Permanent");
	//A_objClient[2].Init(3, "android-d4a89eb1e295ab93", "58-7F-66-81-9F-2B", "192.168.1.100", "00:03:06");
	//A_objClient[3].Init(4, "PASCAL", "DC-0E-A1-5E-1D-65", "192.168.1.32", "Permanent");
	//

}
INT CChildView::PA_DoFetchClientCount(BYTE *lpData, DWORD dwDataLen)
{
	BYTE A_bStartMark[] = "var DHCPDynPara=new Array(";
	BYTE szBuffer[4]={0};//假设数量不超过3位数，实际上不可能达到3位数，再者本例程不打算处理不了那么多位数的数据
	INT m_nMarkLen = strlen((CHAR *)A_bStartMark);
	BOOL m_bFound = FALSE;
	INT m_dwMatchCount=0;
	INT m_nCountLen=0;
	INT m_nCount=0;
	for(DWORD i=0; i<dwDataLen; i++){
		if(lpData[i]==A_bStartMark[m_dwMatchCount]){
			m_dwMatchCount++;
			if(m_dwMatchCount==m_nMarkLen){
				do{
					i++;
				}while(lpData[i]==0x0d || lpData[i]==0x0a);
				do{
					szBuffer[m_nCountLen++]=lpData[i];
					i++;
				}while(lpData[i]!=','&&m_nCountLen<4);
				m_nCount = atoi((CHAR *)szBuffer);
				m_bFound = TRUE;
				break;
			}
		}else{
			m_dwMatchCount=0;
		}
	}
	return m_nCount;
}

void CChildView::PA_DoFetchClientDetails(BYTE *lpData, DWORD dwDataLen)
{
	if(m_nClientCount<=0) return;

	BYTE A_bStartMark[] = "var DHCPDynList=new Array(";
	BYTE szBuffer[256];
	INT m_nMarkLen = strlen((CHAR *)A_bStartMark);
	BOOL m_bFound = FALSE;
	INT m_dwMatchCount=0;
	INT m_nCountLen=0;
	INT m_nCount=0;
	for(DWORD i=0; i<dwDataLen; i++){
		if(lpData[i]==A_bStartMark[m_dwMatchCount]){
			m_dwMatchCount++;
			if(m_dwMatchCount==m_nMarkLen){
				for(int n=0; n<m_nClientCount; n++){
					CString m_strClientName;
					CString m_strMAC;
					CString m_strIP;
					CString m_strValidTime;
					for(int m=0; m<4; m++){
						ZeroMemory(szBuffer, 256);
						m_nCountLen = 0;
						do{
							i++;
						}while(lpData[i]==0x0d || lpData[i]==0x0a || lpData[i]==',');
						if(lpData[i]=='"'){
							i++;
							do{
								szBuffer[m_nCountLen++]=lpData[i];
								i++;
							}while(lpData[i]!='"'&&m_nCountLen<256);
							i++;
							switch(m){
							case 0:
								m_strClientName=szBuffer;break;
							case 1:
								m_strMAC=szBuffer;break;
							case 2:
								m_strIP=szBuffer;break;
							case 3:
								m_strValidTime=szBuffer;break;
							}
						}else{
							m_nClientCount=n;
							return;//数据异常,中止接收,重新设定数量
						}
					}
					A_objClient[n].Init(n+1, m_strClientName, m_strMAC, m_strIP, m_strValidTime);
				}
				m_bFound = TRUE;
				break;
			}
		}else{
			m_dwMatchCount=0;
		}
	}
}

BOOL CChildView::PA_DoDownloadData(CString strFile, char * lpszReadBuffer, INT nBufferSize)
{
	if(isConnFail) return FALSE;
	try{
		WSADATA wsaData;
		WORD socketVersion = MAKEWORD(2, 2); // BYTE minorVer = 2, BYTE majorVer = 2
		if(::WSAStartup(socketVersion, &wsaData) != 0){
			AfxMessageBox("Init Socket fail.");
			isConnFail = TRUE;
			return FALSE;
		}

		SOCKET s = ::socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
		if(s==INVALID_SOCKET){
			AfxMessageBox("Failed socket()");
			isConnFail = TRUE;
			return FALSE;
		}
		char * szIpAddress = "192.168.1.1";

		sockaddr_in servAddr;
		servAddr.sin_family = AF_INET;
		servAddr.sin_port = htons(80);
		servAddr.sin_addr.S_un.S_addr = inet_addr(szIpAddress);
		if(::connect(s, (sockaddr *)&servAddr, sizeof(servAddr))==-1){
			AfxMessageBox("Failed connect()");
			isConnFail = TRUE;
			return FALSE;
		}
		ZeroMemory(lpszReadBuffer, nBufferSize);

		char szRequestHeader[1024] = {0};
		strcpy(szRequestHeader, "GET /userRpm/");
		strcat(szRequestHeader, strFile);
		strcat(szRequestHeader, "  HTTP/1.1\r\n");
		strcat(szRequestHeader, m_strRequestHeader);
		::send(s, szRequestHeader, strlen(szRequestHeader), 0);
		int bytesRecv = SOCKET_ERROR;
		char * m_lpszReadBuffer = lpszReadBuffer;
		INT m_nBytesRead = 0;
		do{
			bytesRecv = ::recv(s, m_lpszReadBuffer, 1024, 0 );
			if ( bytesRecv == 0 || bytesRecv == WSAECONNRESET ) {
				//AfxMessageBox("Connection Closed.");
				break;
			}
			m_nBytesRead += bytesRecv;
			m_lpszReadBuffer += bytesRecv;
		}while(/*bytesRecv>0 && */m_nBytesRead<10240-1024);

		::closesocket(s);
		WSACleanup();
	}catch(exception &e){
		isConnFail = TRUE;
		AfxMessageBox(e.what());
	}
	return TRUE;
}


void CChildView::PA_DoFetchDevStatus(BYTE *lpData, DWORD dwDataLen)
{
	char* A_szMarkStart[] = {
		"var statusPara=new Array(\n",
		"var lanPara=new Array(\n",
		"var wlanPara=new Array(\n",
		"var wanPara=new Array(\n",
		"var statistList=new Array(\n"};
	INT A_nMarkStartLen[] = {
		strlen(A_szMarkStart[0]),
		strlen(A_szMarkStart[1]),
		strlen(A_szMarkStart[2]),
		strlen(A_szMarkStart[3]),
		strlen(A_szMarkStart[4])};
	char* A_szMarkEnd = "0,0 );";
	INT m_nMarkEndLen = strlen(A_szMarkEnd);
	char szBuffer[2560];
	char szLine[256];
	devStatus.RemoveAll();

	DWORD nStart = 0;

	for(int n=0; n<5; n++){
		BOOL m_bFound = FALSE;
		INT m_nMatchCount=0;
		INT m_nCountLen = 0;
		INT m_nCount=0;
		INT m_nPosStart= 0;
		INT m_nPosEnd= 0;
		char* pszMarkStart = A_szMarkStart[n];
		INT m_nMarkStartLen = A_nMarkStartLen[n];

		CString s;


		// Get m_nPosStart
		m_nMatchCount = 0;
		for(DWORD i=nStart; i<dwDataLen; i++){
			if(lpData[i]==pszMarkStart[m_nMatchCount]){
				m_nMatchCount++;
				if(m_nMatchCount==m_nMarkStartLen){
					m_nPosStart = i + 1;// + m_nMarkStartLen;
					nStart = m_nPosStart;
					m_bFound = TRUE;
					break;
				}
			}
		}

		// Get m_nPosEnd
		m_nMatchCount = 0;
		for(i=m_nPosStart ; i<dwDataLen; i++){
			if(lpData[i]==A_szMarkEnd[m_nMatchCount]){
				m_nMatchCount++;
				if(m_nMatchCount==m_nMarkEndLen){
					m_nPosEnd = i - m_nMarkEndLen;
					nStart = m_nPosEnd;
					m_bFound = TRUE;
					break;
				}
			}
		}

		memset(szBuffer, 0, sizeof(szBuffer));
		strncpy(szBuffer, (CHAR *)(lpData+m_nPosStart), m_nPosEnd-m_nPosStart);

		INT nBufferLen = strlen(szBuffer);
		for(i=0; i<(DWORD)nBufferLen; i++){
			while(szBuffer[i]==0x0d || szBuffer[i]==0x0a || szBuffer[i]==','){
				i++;
			}
			if(szBuffer[i]=='"'){
				i++; // 如果是本组数据第一行 跳过 双引号
			}
			ZeroMemory(szLine, sizeof(szLine));
			m_nCountLen = 0;
			do{
				szLine[m_nCountLen++]=szBuffer[i];
				i++;
			}while(szBuffer[i]!='"'&&!(szBuffer[i]==','&&szBuffer[i+1]=='\n')&&m_nCountLen<256);
			if(szLine){
				devStatus.AppendString(n, szLine);
			}
		}
	}
}

INT CChildView::PA_DoFetchWLanStationsCount(BYTE *lpData, DWORD dwDataLen)
{
	BYTE A_bStartMark[] = "var wlanHostPara=new Array(";
	BYTE szBuffer[4]={0};//假设数量不超过3位数，实际上不可能达到3位数，再者本例程不打算处理不了那么多位数的数据
	INT m_nMarkLen = strlen((CHAR *)A_bStartMark);
	BOOL m_bFound = FALSE;
	INT m_dwMatchCount=0;
	INT m_nCountLen=0;
	INT m_nCount=0;
	for(DWORD i=0; i<dwDataLen; i++){
		if(lpData[i]==A_bStartMark[m_dwMatchCount]){
			m_dwMatchCount++;
			if(m_dwMatchCount==m_nMarkLen){
				do{
					i++;
				}while(lpData[i]==0x0d || lpData[i]==0x0a);
				do{
					szBuffer[m_nCountLen++]=lpData[i];
					i++;
				}while(lpData[i]!=','&&m_nCountLen<4);
				m_nCount = atoi((CHAR *)szBuffer);
				m_bFound = TRUE;
				break;
			}
		}else{
			m_dwMatchCount=0;
		}
	}
	return m_nCount;
}

void CChildView::PA_DoFetchWLanStations(BYTE *lpData, DWORD dwDataLen)
{
	if(m_nWLanStationsCount<=0) return;

	BYTE A_bStartMark[] = "var hostList=new Array(";
	BYTE szBuffer[256];
	INT m_nMarkLen = strlen((CHAR *)A_bStartMark);
	BOOL m_bFound = FALSE;
	INT m_dwMatchCount=0;
	INT m_nCountLen=0;
	INT m_nCount=0;
	for(DWORD i=0; i<dwDataLen; i++){
		if(lpData[i]==A_bStartMark[m_dwMatchCount]){
			m_dwMatchCount++;
			if(m_dwMatchCount==m_nMarkLen){
				for(int n=0; n<m_nWLanStationsCount; n++){
					CString m_strMAC;
					CString m_strStatus;
					CString m_strReceive;
					CString m_strSend;
					for(int m=0; m<7; m++){ // 7行一组数据
						ZeroMemory(szBuffer, 256);
						m_nCountLen = 0;
						do{
							i++;
						}while(lpData[i]==0x0d || lpData[i]==0x0a || lpData[i]==',');
						if(m==0){
							if(lpData[i]=='"'){
								i++; // 如果是本组数据第一行 跳过 双引号
							}else{
								m_nWLanStationsCount=n;
								return;//数据异常,中止接收,重新设定数量
							}
						}
						do{
							szBuffer[m_nCountLen++]=lpData[i];
							i++;
						}while(!(lpData[i]=='"'||lpData[i]==',')&&m_nCountLen<256);
						switch(m){
						case 0:
							m_strMAC=szBuffer;break;
						case 1:
							m_strStatus=szBuffer;break;
						case 5:
							m_strReceive=szBuffer;break;
						case 6:
							m_strSend=szBuffer;break;
						}
					}
					A_objHost[n].Init(n+1, m_strMAC, m_strStatus, m_strReceive, m_strSend);
				}
				m_bFound = TRUE;
				break;
			}
		}else{
			m_dwMatchCount=0;
		}
	}
}


void CChildView::PA_DoFetchSysLog(BYTE *lpData, DWORD dwDataLen)
{
	BYTE A_bStartMark[] = "var logList=new Array(";
	BYTE szBuffer[256];
	INT m_nMarkLen = strlen((CHAR *)A_bStartMark);
	BOOL m_bFound = FALSE;
	INT m_dwMatchCount=0;
	INT m_nCountLen=0;
	INT m_nCount=0;
	INT m_nPosStart= 0;
	csa.RemoveAll();
	CString s;
	for(DWORD i=0; i<dwDataLen; i++){
		if(lpData[i]==A_bStartMark[m_dwMatchCount]){
			m_dwMatchCount++;
			if(m_dwMatchCount==m_nMarkLen){
				m_nPosStart = i;
				m_bFound = TRUE;
				break;
			}
		}
	}
	for(; i<dwDataLen; i++){
		do{
			i++;
		}while(lpData[i]==0x0d || lpData[i]==0x0a || lpData[i]==',');
		if(lpData[i]=='"'){
			i++; // 如果是本组数据第一行 跳过 双引号
		}else if(lpData[i]=='0'){
			//AfxMessageBox("break");
			break;
		}
		ZeroMemory(szBuffer, 256);
		m_nCountLen = 0;
		do{
			szBuffer[m_nCountLen++]=lpData[i];
			i++;
		}while(lpData[i]!='"'&&m_nCountLen<256);
		INT noneSpace = 0;
		while(szBuffer[noneSpace]==' ') noneSpace++;
		csa.Add(szBuffer + noneSpace);
	}
	//s.Format("%d", csa.GetSize());
	//AfxMessageBox(s);
}

void CChildView::PA_DoReloadWLanHosts()
{
	PA_DoDownloadData("WlanStationRpm.htm", m_szWebBuffer, m_nBufferSize);
	m_nWLanStationsCount = PA_DoFetchWLanStationsCount((BYTE *)m_szWebBuffer, m_nBufferSize);
	PA_DoFetchWLanStations((BYTE *)m_szWebBuffer, m_nBufferSize);
}

CString CChildView::MatchMemo(CString strMacAddress)
{
	for(INT i=0; i<m_nMemoCount; i++){
		if(A_objMemo[i].m_strMacAddress == strMacAddress){
			return A_objMemo[i].m_strMemo;
		}
	}
	return "";
}

void CChildView::PA_DoDisplayDevInfo_AddRow(CListCtrl& list, CString strKey, INT nSection, INT nSub, INT& nRow){
	if(nRow = list.InsertItem(nRow, "")){
		list.SetItemText(nRow, 1, strKey);
		list.SetItemText(nRow, 2, devStatus.GetAt(nSection, nSub));
		nRow++;
	}
}

void CChildView::PA_DoDisplayDevInfo()
{
	CListCtrl& m_listDisplay = GetListCtrl();

	m_listDisplay.DeleteAllItems();
	ClearColor();
	while(m_listDisplay.DeleteColumn(0));

	m_listDisplay.InsertColumn(0, "", LVCFMT_LEFT, 90);
	m_listDisplay.InsertColumn(1, "", LVCFMT_LEFT, 110);
	m_listDisplay.InsertColumn(2, "", LVCFMT_LEFT, 352);

	//PA_DoReloadDevStatus();
	PA_DoDownloadData("StatusRpm.htm", m_szWebBuffer, m_nBufferSize);
	PA_DoFetchDevStatus((BYTE *)m_szWebBuffer, m_nBufferSize);

	INT nRow = 0;

	m_listDisplay.InsertItem(nRow, "版本信息");
	SetItemColor(nRow, RGB(255, 255, 255), RGB(0, 102, 153));
	nRow++;
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "当前软件版本：", 0, 5, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "当前硬件版本：", 0, 6, nRow);

	m_listDisplay.InsertItem(nRow, "LAN口状态");
	SetItemColor(nRow, RGB(255, 255, 255), RGB(0, 102, 153));
	nRow++;
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "MAC地址：", 1, 0, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "IP地址：", 1, 1, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "子网掩码：", 1, 2, nRow);

	m_listDisplay.InsertItem(nRow, "无线状态");
	SetItemColor(nRow, RGB(255, 255, 255), RGB(0, 102, 153));
	nRow++;
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "无线功能：", 2, 0, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "SSID号：", 2, 1, nRow);
	//PA_DoDisplayDevInfo_AddRow(m_listDisplay, "信 道：", 2, 2, nRow);
	//PA_DoDisplayDevInfo_AddRow(m_listDisplay, "模 式：", 2, 3, nRow);
	//PA_DoDisplayDevInfo_AddRow(m_listDisplay, "频段带宽：", 2, ?, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "MAC地址：", 2, 4, nRow);
	//PA_DoDisplayDevInfo_AddRow(m_listDisplay, "WDS状态：", 2, ?, nRow);

	m_listDisplay.InsertItem(nRow, "WAN口状态");
	SetItemColor(nRow, RGB(255, 255, 255), RGB(0, 102, 153));
	nRow++;
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "MAC地址：", 3, 1, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "IP地址：", 3, 2, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "子网掩码：", 3, 4, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "网关：", 3, 7, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "DNS服务器：", 3, 11, nRow);
	PA_DoDisplayDevInfo_AddRow(m_listDisplay, "上网时间：", 3, 12, nRow);

	m_listDisplay.InsertItem(nRow, "WAN口流量统计");
	SetItemColor(nRow, RGB(255, 255, 255), RGB(0, 102, 153));
	nRow++;
	if(nRow = m_listDisplay.InsertItem(nRow, "")){
		m_listDisplay.SetItemText(nRow, 1, "字节数：");
		m_listDisplay.SetItemText(nRow, 2, "接收 " + devStatus.GetAt(4, 0) + ",  发送" + devStatus.GetAt(4, 1));
		nRow++;
	}
	if(nRow = m_listDisplay.InsertItem(nRow, "")){
		m_listDisplay.SetItemText(nRow, 1, "数据包数：");
		m_listDisplay.SetItemText(nRow, 2, "接收 " + devStatus.GetAt(4, 2) + ",  发送" + devStatus.GetAt(4, 3));
		nRow++;
	}

	nRow = m_listDisplay.InsertItem(nRow, "");
	SetItemColor(nRow, RGB(255, 255, 255), RGB(0, 102, 153));
	nRow++;
	if(nRow = m_listDisplay.InsertItem(nRow, "")){
		m_listDisplay.SetItemText(nRow, 1, "运行时间：");
		INT nSeconds = atoi(devStatus.GetAt(0, 4));
		CString s;
		s.Format("%d 天 %02d:%02d:%02d", nSeconds/86400, nSeconds%86400/3600, nSeconds%3600/60, nSeconds%60);
		m_listDisplay.SetItemText(nRow, 2, s);
		nRow++;
	}

	devStatus.RemoveAll();
}

void CChildView::PA_DoDisplayReport()
{
	CListCtrl& m_listDisplay = GetListCtrl();

	m_listDisplay.DeleteAllItems();
	ClearColor();
	while(m_listDisplay.DeleteColumn(0));

	m_listDisplay.InsertColumn(0, "@", LVCFMT_RIGHT, 25);
	m_listDisplay.InsertColumn(1, "ID", LVCFMT_RIGHT, 25);
	m_listDisplay.InsertColumn(2, "客户端名", LVCFMT_LEFT, 165);
	m_listDisplay.InsertColumn(3, "MAC地址", LVCFMT_LEFT, 115);
	m_listDisplay.InsertColumn(4, "IP地址", LVCFMT_LEFT, 105);
	m_listDisplay.InsertColumn(5, "有效时间", LVCFMT_CENTER, 65);
	m_listDisplay.InsertColumn(6, "备注", LVCFMT_LEFT, 65);
	m_listDisplay.InsertColumn(7, "接收", LVCFMT_RIGHT, 65);
	m_listDisplay.InsertColumn(8, "发送", LVCFMT_RIGHT, 65);

	PA_DoReloadHostsData();
	PA_DoReloadWLanHosts();

	INT m_nItemID = 0;
	CString m_strItemID;
	for(INT i=0; i<m_nClientCount; i++){
		m_strItemID.Format("%d", m_nItemID);
		m_nItemID = m_listDisplay.InsertItem(m_nItemID, m_strItemID);
		if(m_nItemID>=0){
			m_listDisplay.SetItemText(m_nItemID, 1, A_objClient[i].m_strID);
			m_listDisplay.SetItemText(m_nItemID, 2, A_objClient[i].m_strClientName);
			m_listDisplay.SetItemText(m_nItemID, 3, A_objClient[i].m_strMAC);
			m_listDisplay.SetItemText(m_nItemID, 4, A_objClient[i].m_strIP);
			m_listDisplay.SetItemText(m_nItemID, 5, A_objClient[i].m_strValidTime);
			m_listDisplay.SetItemText(m_nItemID, 6, MatchMemo(A_objClient[i].m_strMAC));
			/**/
			for(int n=0; n<m_nWLanStationsCount; n++){
				if(A_objHost[n].nFlag==0 && A_objHost[n].m_strMacAddress == A_objClient[i].m_strMAC){
					m_listDisplay.SetItemText(m_nItemID, 7, A_objHost[n].m_strReceive);
					m_listDisplay.SetItemText(m_nItemID, 8, A_objHost[n].m_strSend);
					A_objHost[n].nFlag = 1;
					break;
				}
			}
			m_nItemID++;
		}
	}
	/**/
	for(i=0; i<m_nWLanStationsCount; i++){
		if(A_objHost[i].nFlag==0){
			m_strItemID.Format("%d", m_nItemID);
			m_nItemID = m_listDisplay.InsertItem(m_nItemID, m_strItemID);
			if(m_nItemID>=0){
				m_strItemID.Format("@%d", A_objHost[i].m_nID);
				m_listDisplay.SetItemText(m_nItemID, 1, m_strItemID);
				m_listDisplay.SetItemText(m_nItemID, 3, A_objHost[i].m_strMacAddress);
				m_listDisplay.SetItemText(m_nItemID, 6, MatchMemo(A_objHost[i].m_strMacAddress));
				m_listDisplay.SetItemText(m_nItemID, 7, A_objHost[i].m_strReceive);
				m_listDisplay.SetItemText(m_nItemID, 8, A_objHost[i].m_strSend);
				A_objHost[i].nFlag = 1;
				m_nItemID++;
			}
		}
	}
}


void CChildView::PA_DoDisplayHosts()
{
	CListCtrl& m_listDisplay = GetListCtrl();

	m_listDisplay.DeleteAllItems();
	ClearColor();
	while(m_listDisplay.DeleteColumn(0));

	m_listDisplay.InsertColumn(0, "@", LVCFMT_RIGHT, 25);
	m_listDisplay.InsertColumn(1, "ID", LVCFMT_RIGHT, 25);
	m_listDisplay.InsertColumn(2, "客户端名", LVCFMT_LEFT, 165);
	m_listDisplay.InsertColumn(3, "MAC地址", LVCFMT_LEFT, 115);
	m_listDisplay.InsertColumn(4, "IP地址", LVCFMT_LEFT, 105);
	m_listDisplay.InsertColumn(5, "有效时间", LVCFMT_CENTER, 65);
	m_listDisplay.InsertColumn(6, "备注", LVCFMT_LEFT, 65);

	PA_DoReloadHostsData();

	INT m_nItemID = 0;
	CString m_strItemID;
	for(INT i=0; i<m_nClientCount; i++){
		m_strItemID.Format("%d", m_nItemID);
		m_nItemID = m_listDisplay.InsertItem(m_nItemID, m_strItemID);
		if(m_nItemID>=0){
			m_listDisplay.SetItemText(m_nItemID, 1, A_objClient[i].m_strID);
			m_listDisplay.SetItemText(m_nItemID, 2, A_objClient[i].m_strClientName);
			m_listDisplay.SetItemText(m_nItemID, 3, A_objClient[i].m_strMAC);
			m_listDisplay.SetItemText(m_nItemID, 4, A_objClient[i].m_strIP);
			m_listDisplay.SetItemText(m_nItemID, 5, A_objClient[i].m_strValidTime);
			m_listDisplay.SetItemText(m_nItemID, 6, MatchMemo(A_objClient[i].m_strMAC));
			m_nItemID++;
		}
	}
}

void CChildView::PA_DoDisplayStations()
{
	CListCtrl& m_listDisplay = GetListCtrl();

	m_listDisplay.DeleteAllItems();
	ClearColor();
	while(m_listDisplay.DeleteColumn(0));

	m_listDisplay.InsertColumn(0, "@", LVCFMT_RIGHT, 25);
	m_listDisplay.InsertColumn(1, "ID", LVCFMT_RIGHT, 25);
	m_listDisplay.InsertColumn(2, "MAC地址", LVCFMT_LEFT, 115);
	m_listDisplay.InsertColumn(3, "状态", LVCFMT_CENTER, 40);
	m_listDisplay.InsertColumn(4, "接收", LVCFMT_RIGHT, 65);
	m_listDisplay.InsertColumn(5, "发送", LVCFMT_RIGHT, 65);
	m_listDisplay.InsertColumn(6, "IP地址", LVCFMT_LEFT, 105);
	m_listDisplay.InsertColumn(7, "客户端名", LVCFMT_LEFT, 165);
	m_listDisplay.InsertColumn(8, "备注", LVCFMT_LEFT, 65);

	PA_DoReloadHostsData();
	PA_DoReloadWLanHosts();

	INT m_nItemID = 0;
	CString m_strItemID;
	for(INT i=0; i<m_nWLanStationsCount; i++){
		m_strItemID.Format("%d", m_nItemID);
		m_nItemID = m_listDisplay.InsertItem(m_nItemID, m_strItemID);
		if(m_nItemID>=0){
			m_listDisplay.SetItemText(m_nItemID, 1, A_objHost[i].m_strID);
			m_listDisplay.SetItemText(m_nItemID, 2, A_objHost[i].m_strMacAddress);
			m_listDisplay.SetItemText(m_nItemID, 3, A_objHost[i].m_strStatus);
			m_listDisplay.SetItemText(m_nItemID, 4, A_objHost[i].m_strReceive);
			m_listDisplay.SetItemText(m_nItemID, 5, A_objHost[i].m_strSend);
			m_listDisplay.SetItemText(m_nItemID, 8, MatchMemo(A_objHost[i].m_strMacAddress));

			for(int n=0; n<m_nClientCount; n++){
				if(A_objHost[i].m_strMacAddress == A_objClient[n].m_strMAC){
					m_listDisplay.SetItemText(m_nItemID, 6, A_objClient[n].m_strIP);
					m_listDisplay.SetItemText(m_nItemID, 7, A_objClient[n].m_strClientName);
					break;
				}
			}
			m_nItemID++;
		}
	}
}

void CChildView::PA_DoDisplaySysLog()
{
	CListCtrl& m_listDisplay = GetListCtrl();

	m_listDisplay.DeleteAllItems();
	ClearColor();
	while(m_listDisplay.DeleteColumn(0));

	m_listDisplay.InsertColumn(0, "@", LVCFMT_RIGHT, 35);
	m_listDisplay.InsertColumn(1, "日志", LVCFMT_LEFT, 620);

	//PA_DoReloadSysLog();
	PA_DoDownloadData("SystemLogRpm.htm", m_szWebBuffer, m_nBufferSize);
	PA_DoFetchSysLog((BYTE *)m_szWebBuffer, m_nBufferSize);

	INT m_nCount = csa.GetSize();
	INT m_nItemID = 0;
	CString m_strItemID;
	for(INT i=0; i<m_nCount; i++){
		INT n = m_nCount-i-1;
		m_strItemID.Format("%d", n);
		m_nItemID = m_listDisplay.InsertItem(i, m_strItemID);
		if(m_nItemID>=0){
			m_listDisplay.SetItemText(m_nItemID, 1, csa.GetAt(n));
		}
	}
	csa.RemoveAll();
}

void CChildView::OnReloadReport() 
{
	// TODO: Add your command handler code here
	PA_DoDisplayReport();
}


void CChildView::OnReloadHosts() 
{
	// TODO: Add your command handler code here
	PA_DoDisplayHosts();
	
}

void CChildView::OnReloadStations() 
{
	// TODO: Add your command handler code here
	PA_DoDisplayStations();
}

void CChildView::OnReloadLogs() 
{
	// TODO: Add your command handler code here
	PA_DoDisplaySysLog();
}

void CChildView::OnRouterReboot() 
{
	// TODO: Add your command handler code here
	if(IDYES==AfxMessageBox("重启设备么?", MB_YESNO | MB_DEFBUTTON2 | MB_ICONQUESTION)){
		PA_DoDownloadData("SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7", m_szWebBuffer, m_nBufferSize);
		AfxMessageBox("正在重启，请等待15秒。");
	}
}

void CChildView::OnClearLog() 
{
	// TODO: Add your command handler code here
	if(IDYES==AfxMessageBox("清空日志么?", MB_YESNO | MB_DEFBUTTON2 | MB_ICONQUESTION)){
		PA_DoDownloadData("SystemLogRpm.htm?ClearLog=%C7%E5%B3%FD%CB%F9%D3%D0%C8%D5%D6%BE", m_szWebBuffer, m_nBufferSize);
		PA_DoDisplaySysLog();
		//AfxMessageBox("clear log");
	}
}

void CChildView::OnDevInfo() 
{
	// TODO: Add your command handler code here
	PA_DoDisplayDevInfo();
}

void CChildView::OnNMCustomdraw(NMHDR *pNMHDR, LRESULT *pResult)
{
	// TODO: Add your control notification handler code here
	*pResult = CDRF_DODEFAULT;
	NMLVCUSTOMDRAW * lplvdr=(NMLVCUSTOMDRAW*)pNMHDR;
	NMCUSTOMDRAW &nmcd = lplvdr->nmcd;
	switch(lplvdr->nmcd.dwDrawStage)//判断状态
	{
		case CDDS_PREPAINT:
		{
			*pResult = CDRF_NOTIFYITEMDRAW;
			break;
		}
		case CDDS_ITEMPREPAINT://如果为画ITEM之前就要进行颜色的改变
		{
			TEXT_BK tb;

			if(MapItemColor.Lookup(nmcd.dwItemSpec, tb))
			// 根据在 SetItemColor(DWORD iItem, COLORREF color) 设置的
			// ITEM号和COLORREF 在摸板中查找，然后进行颜色赋值。
			{
				lplvdr->clrText = tb.colText;
				lplvdr->clrTextBk = tb.colTextBk;
				*pResult = CDRF_DODEFAULT;
			}
		}
		break;
	}
}

void CChildView::SetItemColor(DWORD iItem, COLORREF TextColor, COLORREF TextBkColor)
{
	TEXT_BK tb;
	tb.colText = TextColor;
	tb.colTextBk = TextBkColor;

	MapItemColor.SetAt(iItem, tb);//设置某行的颜色。
	//this->RedrawItems(iItem, iItem);//重新染色

	//this->SetCheck(iItem,1);
	this->SetFocus();    //设置焦点
	UpdateWindow();
}

void CChildView::ClearColor()
{
	MapItemColor.RemoveAll();
}