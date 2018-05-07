// LanStation.cpp: implementation of the CLanStation class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "PaSpyRouter2016MFC.h"
#include "LanStation.h"

#ifdef _DEBUG
#undef THIS_FILE
static char THIS_FILE[]=__FILE__;
#define new DEBUG_NEW
#endif

//////////////////////////////////////////////////////////////////////
// Construction/Destruction
//////////////////////////////////////////////////////////////////////

CLanStation::CLanStation()
{

}

CLanStation::~CLanStation()
{

}

void CLanStation::Init(INT id, CString strClientName, CString strMAC, CString strIP, CString strValidTime)
{
	m_nID = id;
	m_strID.Format("%d", id);
	m_strClientName = strClientName;
	m_strMAC = strMAC;
	m_strIP = strIP;
	m_strValidTime = strValidTime.Compare("Permanent") ? strValidTime : "сю╬ц";
	m_strMemo = "";
}
