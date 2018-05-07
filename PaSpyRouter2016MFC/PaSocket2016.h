// PaSocket2016.h: interface for the CPaSocket2016 class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_PASOCKET2016_H__66A7AE14_19F8_47DF_BBA9_FDA273863C61__INCLUDED_)
#define AFX_PASOCKET2016_H__66A7AE14_19F8_47DF_BBA9_FDA273863C61__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

class CPaSocket2016  
{
public:
	CPaSocket2016();
	virtual ~CPaSocket2016();
	void GetWsaLastErrorInfo(INT nCode){
		INT m_nCode = nCode;
		if(m_nCode==0) m_nCode = WSAGetLastError();
		CString m_strMessage;
		switch(m_nCode){
		case WSANOTINITIALISED:
			m_strMessage = "WSANOTINITIALISED: A successful WSAStartup must occur before using this function.";
			break;
		case WSAENETDOWN:
			m_strMessage = "WSAENETDOWN: The network subsystem has failed. ";
			break;
		case WSAEFAULT:
			m_strMessage = "WSAEFAULT: The buf parameter is not completely contained in a valid part of the user address space. ";
			break;
		case WSAENOTCONN:
			m_strMessage = "WSAENOTCONN: The socket is not connected. ";
			break;
		case WSAEINTR:
			m_strMessage = "WSAEINTR: The (blocking) call was canceled through WSACancelBlockingCall. ";
			break;
		case WSAEINPROGRESS:
			m_strMessage = "WSAEINPROGRESS: A blocking Windows Sockets 1.1 call is in progress, or the service provider is still processing a callback function. ";
			break;
		case WSAENETRESET:
			m_strMessage = "WSAENETRESET: The connection has been broken due to the keep-alive activity detecting a failure while the operation was in progress. ";
			break;
		case WSAENOTSOCK:
			m_strMessage = "WSAENOTSOCK: The descriptor is not a socket. ";
			break;
		case WSAEOPNOTSUPP:
			m_strMessage = "WSAEOPNOTSUPP: MSG_OOB was specified, but the socket is not stream-style such as type SOCK_STREAM, out-of-band data is not supported in the communication domain associated with this socket, or the socket is unidirectional and supports only send operations. ";
			break;
		case WSAESHUTDOWN:
			m_strMessage = "WSAESHUTDOWN: The socket has been shut down; it is not possible to recv on a socket after shutdown has been invoked with how set to SD_RECEIVE or SD_BOTH. ";
			break;
		case WSAEWOULDBLOCK:
			m_strMessage = "WSAEWOULDBLOCK: The socket is marked as nonblocking and the receive operation would block. ";
			break;
		case WSAEMSGSIZE:
			m_strMessage = "WSAEMSGSIZE: The message was too large to fit into the specified buffer and was truncated. ";
			break;
		case WSAEINVAL:
			m_strMessage = "WSAEINVAL: The socket has not been bound with bind, or an unknown flag was specified, or MSG_OOB was specified for a socket with SO_OOBINLINE enabled or (for byte stream sockets only) len was zero or negative. ";
			break;
		case WSAECONNABORTED:
			m_strMessage = "WSAECONNABORTED: The virtual circuit was terminated due to a time-out or other failure. The application should close the socket as it is no longer usable. ";
			break;
		case WSAETIMEDOUT:
			m_strMessage = "WSAETIMEDOUT: The connection has been dropped because of a network failure or because the peer system failed to respond. ";
			break;
		case WSAECONNRESET:
			m_strMessage = "WSAECONNRESET: The virtual circuit was reset by the remote side executing a \"hard\" or \"abortive\" close. The application should close the socket as it is no longer usable. On a UDP datagram socket this error would indicate that a previous send operation resulted in an ICMP \"Port Unreachable\" message. ";
			break;
		default:
			m_strMessage = "...";
		}
		AfxMessageBox(m_strMessage);
	}

};

#endif // !defined(AFX_PASOCKET2016_H__66A7AE14_19F8_47DF_BBA9_FDA273863C61__INCLUDED_)
