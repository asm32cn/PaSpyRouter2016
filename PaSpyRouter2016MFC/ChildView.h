// ChildView.h : interface of the CChildView class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_CHILDVIEW_H__5110FF9A_3AA1_4B6D_AA94_5ADB7387BAEE__INCLUDED_)
#define AFX_CHILDVIEW_H__5110FF9A_3AA1_4B6D_AA94_5ADB7387BAEE__INCLUDED_

#include <afxtempl.h>

#include "DevStatus.h"	// Added by ClassView
#include "MemoMAC.h"	// Added by ClassView
#include "WLanHost.h"	// Added by ClassView
#include "LanStation.h"	// Added by ClassView
#include "PaSocket2016.h"	// Added by ClassView
#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CChildView window

typedef struct
{
	COLORREF colText;
	COLORREF colTextBk;
}TEXT_BK;

class CChildView : public CListView/*CWnd*/
{
// Construction
public:
	void SetItemColor(DWORD iItem, COLORREF TextColor, COLORREF TextBkColor);	//设置某一行的前景色和背景色
	void ClearColor();															//清除颜色映射表
	CChildView();
	DECLARE_DYNCREATE(CChildView)

// Attributes
public:
	CMap<DWORD, DWORD&, TEXT_BK, TEXT_BK&> MapItemColor;

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CChildView)
	protected:
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
	//}}AFX_VIRTUAL

// Implementation
public:
	CString MatchMemo(CString strMacAddress);
	CMemoMAC A_objMemo[10];
	CPaSocket2016 cps;
	BOOL PA_DoDownloadData(CString strFile, char * lpszReadBuffer, INT nBufferSize);
	void PA_DoViewInitialize();
	virtual ~CChildView();

	// Generated message map functions
protected:
	void PA_DoDisplayDevInfo_AddRow(CListCtrl& list, CString strKey, INT nSection, INT nSub, INT& nRow);
	void PA_DoDisplayDevInfo();
	void PA_DoDisplaySysLog();
	void PA_DoDisplayStations();
	void PA_DoDisplayHosts();
	void PA_DoDisplayReport();

	void PA_DoFetchDevStatus(BYTE *lpData, DWORD dwDataLen);
	void PA_DoFetchSysLog(BYTE *lpData, DWORD dwDataLen);
	INT PA_DoFetchClientCount(BYTE* lpData, DWORD dwDataLen);
	INT PA_DoFetchWLanStationsCount(BYTE *lpData, DWORD dwDataLen);
	void PA_DoFetchClientDetails(BYTE *lpData, DWORD dwDataLen);
	void PA_DoFetchWLanStations(BYTE *lpData, DWORD dwDataLen);

	void PA_DoReloadHostsData();
	void PA_DoReloadWLanHosts();

	BOOL isConnFail;
	CDevStatus devStatus;
	CStringArray csa;
	TEXT_BK tb;

	int m_nBufferSize;
	char m_szWebBuffer[20480];

	CLanStation A_objClient[100];
	CWLanHost A_objHost[100];

	INT m_nMemoCount;
	INT m_nClientCount;
	INT m_nWLanStationsCount;
	CString m_strRequestHeader;
	//{{AFX_MSG(CChildView)
	afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
	afx_msg void OnReloadHosts();
	afx_msg void OnReloadReport();
	afx_msg void OnReloadStations();
	afx_msg void OnReloadLogs();
	afx_msg void OnRouterReboot();
	afx_msg void OnClearLog();
	afx_msg void OnDevInfo();
	//}}AFX_MSG
	void OnNMCustomdraw(NMHDR *pNMHDR, LRESULT *pResult);
	DECLARE_MESSAGE_MAP()
};

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_CHILDVIEW_H__5110FF9A_3AA1_4B6D_AA94_5ADB7387BAEE__INCLUDED_)
