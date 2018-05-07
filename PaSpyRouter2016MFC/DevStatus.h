// DevStatus.h: interface for the CDevStatus class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_DEVSTATUS_H__C1135996_C999_494C_807B_5C3D91740B64__INCLUDED_)
#define AFX_DEVSTATUS_H__C1135996_C999_494C_807B_5C3D91740B64__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

class CDevStatus  
{
public:
	CString GetAt(INT nSection, INT nIndex);
	BOOL AppendString(INT nSection, CString s);
	BOOL SetAt(INT nSection, INT nIndex, CString s);
	void RemoveAll();
	CDevStatus();
	virtual ~CDevStatus();
private:
	CStringArray A_cacheStatus[5];
protected:
};

#endif // !defined(AFX_DEVSTATUS_H__C1135996_C999_494C_807B_5C3D91740B64__INCLUDED_)
