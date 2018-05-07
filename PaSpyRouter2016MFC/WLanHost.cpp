// WLanHost.cpp: implementation of the CWLanHost class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "PaSpyRouter2016MFC.h"
#include "WLanHost.h"

#ifdef _DEBUG
#undef THIS_FILE
static char THIS_FILE[]=__FILE__;
#define new DEBUG_NEW
#endif

//////////////////////////////////////////////////////////////////////
// Construction/Destruction
//////////////////////////////////////////////////////////////////////

CWLanHost::CWLanHost()
{

}

CWLanHost::~CWLanHost()
{

}

void CWLanHost::Init(INT nID, CString strMacAddress, CString strStatus, CString strReceive, CString strSend)
{
	m_nID = nID;
	m_strID.Format("%d", nID);
	m_strMacAddress = strMacAddress;
	m_strStatus = strStatus;
	m_strReceive = strReceive;
	m_strSend = strSend;

	m_nStatus = atoi(strStatus);
	m_nReceive = atoi(strReceive);
	m_nSend = atoi(strSend);

	nFlag = 0;
}
