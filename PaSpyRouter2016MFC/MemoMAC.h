// MemoMAC.h: interface for the CMemoMAC class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_MEMOMAC_H__598320F0_82E5_43B8_803D_E1A99D17E6DB__INCLUDED_)
#define AFX_MEMOMAC_H__598320F0_82E5_43B8_803D_E1A99D17E6DB__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

class CMemoMAC  
{
public:
	void Init(INT nID, CString strMacAddress, CString strMemo);
	INT m_nID;
	CString m_strID;
	CString m_strMacAddress;
	CString m_strMemo;
	//void Init(INT nID, CString strMacAddress, CString strMemo);
	CMemoMAC();
	virtual ~CMemoMAC();

};

#endif // !defined(AFX_MEMOMAC_H__598320F0_82E5_43B8_803D_E1A99D17E6DB__INCLUDED_)
