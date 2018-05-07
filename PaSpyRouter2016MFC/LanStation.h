// LanStation.h: interface for the CLanStation class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_LANSTATION_H__5E71F197_DEC4_49C8_960E_61E811F727EE__INCLUDED_)
#define AFX_LANSTATION_H__5E71F197_DEC4_49C8_960E_61E811F727EE__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

class CLanStation  
{
public:
	void Init(INT id, CString strClientName, CString strMAC, CString strIP, CString strValidTime);
	INT m_nID;
	CString m_strMemo;
	CString m_strID;
	CString m_strClientName;
	CString m_strMAC;
	CString m_strIP;
	CString m_strValidTime;
	CLanStation();
	virtual ~CLanStation();

};

#endif // !defined(AFX_LANSTATION_H__5E71F197_DEC4_49C8_960E_61E811F727EE__INCLUDED_)
