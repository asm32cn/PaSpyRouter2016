// MemoMAC.cpp: implementation of the CMemoMAC class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "PaSpyRouter2016MFC.h"
#include "MemoMAC.h"

#ifdef _DEBUG
#undef THIS_FILE
static char THIS_FILE[]=__FILE__;
#define new DEBUG_NEW
#endif

//////////////////////////////////////////////////////////////////////
// Construction/Destruction
//////////////////////////////////////////////////////////////////////

CMemoMAC::CMemoMAC()
{

}

CMemoMAC::~CMemoMAC()
{

}

void CMemoMAC::Init(INT nID, CString strMacAddress, CString strMemo)
{
	m_nID = nID;
	m_strID.Format("%d", m_nID);
	m_strMacAddress = strMacAddress;
	m_strMemo = strMemo;
}
