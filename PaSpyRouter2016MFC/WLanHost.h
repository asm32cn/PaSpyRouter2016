// WLanHost.h: interface for the CWLanHost class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_WLANHOST_H__7748EE69_43BE_487B_B8D0_F339EBEE75DE__INCLUDED_)
#define AFX_WLANHOST_H__7748EE69_43BE_487B_B8D0_F339EBEE75DE__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

class CWLanHost  
{
public:
	void Init(INT nID, CString strMacAddress, CString strStatus, CString strReceive, CString strSend);
	CString m_strMemo;
	CString m_strClientName;
	CString m_strSend;
	INT m_nSend;
	CString m_strReceive;
	INT m_nReceive;
	CString m_strStatus;
	INT m_nStatus;
	CString m_strMacAddress;
	CString m_strID;
	INT m_nID;
	INT nFlag;
	CWLanHost();
	virtual ~CWLanHost();

};

#endif // !defined(AFX_WLANHOST_H__7748EE69_43BE_487B_B8D0_F339EBEE75DE__INCLUDED_)
