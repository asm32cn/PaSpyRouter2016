// DevStatus.cpp: implementation of the CDevStatus class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "PaSpyRouter2016MFC.h"
#include "DevStatus.h"

#ifdef _DEBUG
#undef THIS_FILE
static char THIS_FILE[]=__FILE__;
#define new DEBUG_NEW
#endif

//////////////////////////////////////////////////////////////////////
// Construction/Destruction
//////////////////////////////////////////////////////////////////////

CDevStatus::CDevStatus()
{

}

CDevStatus::~CDevStatus()
{

}

void CDevStatus::RemoveAll()
{
	for(int i=0; i<5; i++){
		A_cacheStatus[i].RemoveAll();
	}
}

BOOL CDevStatus::AppendString(INT nSection, CString s)
{
	if(nSection>=0 && nSection<5){
		A_cacheStatus[nSection].Add(s);
		return TRUE;
	}else{
		return FALSE;
	}
}

CString CDevStatus::GetAt(INT nSection, INT nIndex)
{
	if(nSection>=0 && nSection<5 && nIndex>=0 && nIndex<A_cacheStatus[nSection].GetSize()){
		return A_cacheStatus[nSection].GetAt(nIndex);
	}else{
		return "";
	}
}

BOOL CDevStatus::SetAt(INT nSection, INT nIndex, CString s)
{
	if(nSection>=0 && nSection<5 && nIndex>=0 && nIndex<A_cacheStatus[nSection].GetSize()){
		A_cacheStatus[nSection].SetAt(nIndex, s);
		return TRUE;
	}else{
		return FALSE;
	}
}
