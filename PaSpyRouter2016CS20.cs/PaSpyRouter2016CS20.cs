using System;
using System.Net;
using System.Text;
using System.Drawing;
using System.Windows.Forms;
using System.Resources;

class PaSpyRouter2016CS20 : Form{
	private const string conf__strCaptain = "PaSpyRouter2016CS20";

	private ResourceManager rm = new ResourceManager("PaSpyRouter2016CS20",
			System.Reflection.Assembly.GetExecutingAssembly());
	private const string conf__strCookies = "Authorization=Basic%20YWRtaW46cGFzc3dk; ChgPwdSubTag=";
	private const string strSufix = "\n0,0 );\n";

	private Color colorSection = Color.FromArgb(255, 0, 102, 153);
	private Color colorSectionText = Color.FromArgb(255, 255, 255, 255);
	private int nClientsCount = 0;
	private int nStationsCount = 0;
	private CLanHost[] A_objClients = new CLanHost[100];
	private CLanStation[] A_objStations = new CLanStation[100];

	private string[,] A_strMemos = {
		{"DC-6D-CD-75-B9-79", "理发店"},
		{"F6-D0-10-96-DC-E2", "酷派.我"},
		{"A0-93-47-96-B7-70", "OPPO.蒋"},
		{"F4-29-81-92-4B-D0", "玉米.女"},
		{"24-09-95-63-7F-64", "鸡柳.女"},
		{"F4-29-81-C7-DD-A7", "叶刚.vo"},
		{"E8-BB-A8-A8-42-26", "奶茶.邻"}};

	private ListView listview1 = new ListView();
	private ToolBar toolbar1 = new ToolBar();
	private ImageList imagelist1 = new ImageList();

	protected override Size DefaultSize{
		get{
			return new Size(780, 450);
		}
	}

	public PaSpyRouter2016CS20(){
		this.Text = conf__strCaptain;
		this.StartPosition = FormStartPosition.CenterScreen;
		this.Icon = (Icon)(rm.GetObject("this.ico"));

		Do_AppInitialize();

	}

	private void Do_AppInitialize(){

		for(int i=0; i<100; i++){
			A_objClients[i] = new CLanHost();
			A_objStations[i] = new CLanStation();
		}

		imagelist1.ImageSize = new Size(16, 15);
		imagelist1.Images.Add((Image)(rm.GetObject("res-button-01.png")));
		imagelist1.Images.Add((Image)(rm.GetObject("res-button-02.png")));
		imagelist1.Images.Add((Image)(rm.GetObject("res-button-03.png")));
		imagelist1.Images.Add((Image)(rm.GetObject("res-button-04.png")));
		imagelist1.Images.Add((Image)(rm.GetObject("res-button-05.png")));
		imagelist1.Images.Add((Image)(rm.GetObject("res-button-06.png")));
		imagelist1.Images.Add((Image)(rm.GetObject("res-button-07.png")));

		string[] A_strToolTipText = {"设备状态", "报表", "DHCP", "数据包", "日志", "清空日志", "重启设备"};

		toolbar1.ImageList = imagelist1;
		toolbar1.ButtonSize = new Size(16, 15);

		int n = 0;
		ToolBarButton[] A_toolBarButtons = new ToolBarButton[10];
		for(int i = 0; i<10; i++){
			A_toolBarButtons[i] = new ToolBarButton();
			if(i==1 || i==5 || i==8){
				A_toolBarButtons[i].Style = ToolBarButtonStyle.Separator;
			}else{
				A_toolBarButtons[i].ToolTipText = A_strToolTipText[n];
				A_toolBarButtons[i].ImageIndex = n++;
			}
			toolbar1.Buttons.Add(A_toolBarButtons[i]);
		}

		toolbar1.ButtonClick += new ToolBarButtonClickEventHandler(this.toolbar1_ButtonClick);

		listview1.Dock = DockStyle.Fill;
		listview1.View = View.Details;
		listview1.GridLines = true;
		listview1.FullRowSelect = true;

		this.Controls.Add(listview1);
		this.Controls.Add(toolbar1);

		PA_DoDisplayReport();
	}

	protected void toolbar1_ButtonClick(object sender, ToolBarButtonClickEventArgs e){
		int m_nIndex = toolbar1.Buttons.IndexOf(e.Button);
		switch(m_nIndex){
			case 0:
				PA_DoDisplayDevInfo(); break;
			case 2:
				PA_DoDisplayReport(); break;
			case 3:
				PA_DoDisplayHosts(); break;
			case 4:
				PA_DoDisplayStations(); break;
			case 6:
				PA_DoDisplaySysLog(); break;
			case 7:
				PA_DoClearDeviceLog(); break;
			case 9:
				PA_DoRebootDevice(); break;
			//default:
			//	MessageBox.Show("index=" + m_nIndex); break;
		}
	}

	private string Do_DownloadData(string strParam){
		string strLinkPrefix = "http://192.168.1.1/userRpm/";
		WebClient wc = new WebClient();
		wc.Encoding = System.Text.Encoding.Default;
		wc.Headers.Add("Cookie", conf__strCookies);
		wc.Headers.Add("Referer", strLinkPrefix + "MenuRpm.htm");
		return Encoding.Default.GetString( wc.DownloadData(strLinkPrefix + strParam) );
	}

	private void PA_DoDisplayDevInfo_AddSectionRow(string strKey, int nRow){
		ListViewItem lvi = new ListViewItem(strKey, nRow);
		lvi.BackColor = colorSection;
		lvi.ForeColor = colorSectionText;
		listview1.Items.Add(lvi);
	}
	private void PA_DoDisplayDevInfo_AddRow(string strKey, string[] A_strItems, int nSub, int nRow){
		ListViewItem lvi = new ListViewItem("", nRow);
		lvi.SubItems.Add(strKey);
		lvi.SubItems.Add(A_strItems[nSub]);
		listview1.Items.Add(lvi);
	}

	private void PA_DoDisplayDevInfo(){
		listview1.Clear();
		listview1.Columns.Add("", 90, HorizontalAlignment.Left);
		listview1.Columns.Add("", 110, HorizontalAlignment.Left);
		listview1.Columns.Add("", 352, HorizontalAlignment.Left);

		string strData = Do_DownloadData("StatusRpm.htm");
		int nRow = 0;
		int nLen = 0;
		int nSeconds = -1;
		string[] A_strLines = GetConfigList(strData, "var statusPara=new Array(\n", strSufix);
		if(A_strLines!=null && (nLen = A_strLines.Length)>0){
			PA_DoDisplayDevInfo_AddSectionRow("版本信息", nRow++);
			PA_DoDisplayDevInfo_AddRow("当前软件版本：", A_strLines, 5, nRow++);
			PA_DoDisplayDevInfo_AddRow("当前硬件版本：", A_strLines, 6, nRow++);
			nSeconds = Convert.ToInt32(A_strLines[4]);
		}

		A_strLines = GetConfigList(strData, "var lanPara=new Array(\n", strSufix);
		if(A_strLines!=null && (nLen = A_strLines.Length)>0){
			PA_DoDisplayDevInfo_AddSectionRow("LAN口状态", nRow++);
			PA_DoDisplayDevInfo_AddRow("MAC地址：", A_strLines, 0, nRow++);
			PA_DoDisplayDevInfo_AddRow("IP地址：", A_strLines, 1, nRow++);
			PA_DoDisplayDevInfo_AddRow("子网掩码：", A_strLines, 2, nRow++);
		}

		A_strLines = GetConfigList(strData, "var wlanPara=new Array(\n", strSufix);
		if(A_strLines!=null && (nLen = A_strLines.Length)>0){
			PA_DoDisplayDevInfo_AddSectionRow("无线状态", nRow++);
			PA_DoDisplayDevInfo_AddRow("无线功能：", A_strLines, 0, nRow++);
			PA_DoDisplayDevInfo_AddRow("SSID号：", A_strLines, 1, nRow++);
			PA_DoDisplayDevInfo_AddRow("MAC地址：", A_strLines, 4, nRow++);
		}

		A_strLines = GetConfigList(strData, "var wanPara=new Array(\n", strSufix);
		if(A_strLines!=null && (nLen = A_strLines.Length)>0){
			PA_DoDisplayDevInfo_AddSectionRow("WAN口状态", nRow++);
			PA_DoDisplayDevInfo_AddRow("MAC地址：", A_strLines, 1, nRow++);
			PA_DoDisplayDevInfo_AddRow("IP地址：", A_strLines, 2, nRow++);
			PA_DoDisplayDevInfo_AddRow("子网掩码：", A_strLines, 4, nRow++);
			PA_DoDisplayDevInfo_AddRow("网关：", A_strLines, 7, nRow++);
			PA_DoDisplayDevInfo_AddRow("DNS服务器：", A_strLines, 11, nRow++);
			PA_DoDisplayDevInfo_AddRow("上网时间：", A_strLines, 12, nRow++);
		}

		A_strLines = GetConfigList(strData, "var statistList=new Array(\n", strSufix);
		if(A_strLines!=null && (nLen = A_strLines.Length)>0){
			PA_DoDisplayDevInfo_AddSectionRow("WAN口流量统计", nRow++);

			ListViewItem lvi = new ListViewItem("", nRow++);
			lvi.SubItems.Add("字节数：");
			lvi.SubItems.Add("接收 " + A_strLines[0] + ", 发送 " + A_strLines[1]);
			listview1.Items.Add(lvi);

			lvi = new ListViewItem("", nRow++);
			lvi.SubItems.Add("数据包数：");
			lvi.SubItems.Add("接收 " + A_strLines[2] + ", 发送 " + A_strLines[3]);
			listview1.Items.Add(lvi);
		}

		if(nSeconds>=0){
			PA_DoDisplayDevInfo_AddSectionRow("", nRow++);

			ListViewItem lvi = new ListViewItem("", nRow++);
			lvi.SubItems.Add("运行时间：");
			string s;
			s = String.Format("{0:d} 天 {1:d2}:{2:d2}:{3:d2}", nSeconds/86400, nSeconds%86400/3600, nSeconds%3600/60, nSeconds%60);
			lvi.SubItems.Add(s);
			listview1.Items.Add(lvi);
		}
	}

	private void PA_DoDisplayReport(){
		listview1.Clear();
		listview1.Columns.Add("@", 25, HorizontalAlignment.Left);
		listview1.Columns.Add("ID", 25, HorizontalAlignment.Left);
		listview1.Columns.Add("客户端名", 165, HorizontalAlignment.Left);
		listview1.Columns.Add("MAC地址", 115, HorizontalAlignment.Left);
		listview1.Columns.Add("IP地址", 105, HorizontalAlignment.Left);
		listview1.Columns.Add("有效时间", 65, HorizontalAlignment.Center);
		listview1.Columns.Add("备注", 65, HorizontalAlignment.Left);
		listview1.Columns.Add("接收", 65, HorizontalAlignment.Right);
		listview1.Columns.Add("发送", 65, HorizontalAlignment.Right);

		PA_DoFetchClientData();
		PA_DoFetchWLanStations();
		int nItemID = 0;
		for(int i=0; i<nClientsCount; i++){
			ListViewItem lvi = new ListViewItem(nItemID.ToString(), nItemID);
			lvi.SubItems.Add(A_objClients[i].m_strID);
			lvi.SubItems.Add(A_objClients[i].m_strClientName);
			lvi.SubItems.Add(A_objClients[i].m_strMacAddress);
			lvi.SubItems.Add(A_objClients[i].m_strIpAddress);
			lvi.SubItems.Add(A_objClients[i].m_strValidTime);
			lvi.SubItems.Add(A_objClients[i].m_strMemo);
			for(int n=0; n<nStationsCount; n++){
				if(A_objClients[i].m_strMacAddress == A_objStations[n].m_strMacAddress){
					lvi.SubItems.Add(A_objStations[n].m_strReceive);
					lvi.SubItems.Add(A_objStations[n].m_strSend);
					A_objStations[n].nFlag = 1;
				}
			}
			listview1.Items.Add(lvi);
			nItemID++;
		}
		for(int i=0; i<nStationsCount; i++){
			if(A_objStations[i].nFlag==0){
				ListViewItem lvi = new ListViewItem(nItemID.ToString(), nItemID);
				lvi.SubItems.Add("@" + A_objStations[i].m_strID);
				lvi.SubItems.Add("");
				lvi.SubItems.Add(A_objStations[i].m_strMacAddress);
				lvi.SubItems.Add("");
				lvi.SubItems.Add("");
				lvi.SubItems.Add(A_objStations[i].m_strMemo);
				lvi.SubItems.Add(A_objStations[i].m_strReceive);
				lvi.SubItems.Add(A_objStations[i].m_strSend);
				listview1.Items.Add(lvi);
				nItemID++;
			}
		}/**/
	}

	private void PA_DoDisplayHosts(){
		listview1.Clear();
		listview1.Columns.Add("@", 25, HorizontalAlignment.Left);
		listview1.Columns.Add("ID", 25, HorizontalAlignment.Left);
		listview1.Columns.Add("客户端名", 165, HorizontalAlignment.Left);
		listview1.Columns.Add("MAC地址", 115, HorizontalAlignment.Left);
		listview1.Columns.Add("IP地址", 105, HorizontalAlignment.Left);
		listview1.Columns.Add("有效时间", 65, HorizontalAlignment.Center);
		listview1.Columns.Add("备注", 65, HorizontalAlignment.Left);

		PA_DoFetchClientData();

		for(int i=0; i<nClientsCount; i++){
			ListViewItem lvi = new ListViewItem(i.ToString(), i);
			lvi.SubItems.Add(A_objClients[i].m_strID);
			lvi.SubItems.Add(A_objClients[i].m_strClientName);
			lvi.SubItems.Add(A_objClients[i].m_strMacAddress);
			lvi.SubItems.Add(A_objClients[i].m_strIpAddress);
			lvi.SubItems.Add(A_objClients[i].m_strValidTime);
			lvi.SubItems.Add(A_objClients[i].m_strMemo);
			listview1.Items.Add(lvi);
		}
	}

	private void PA_DoDisplayStations(){
		listview1.Clear();
		listview1.Columns.Add("@", 25, HorizontalAlignment.Left);
		listview1.Columns.Add("ID", 25, HorizontalAlignment.Left);
		listview1.Columns.Add("MAC地址", 115, HorizontalAlignment.Left);
		listview1.Columns.Add("状态", 40, HorizontalAlignment.Center);
		listview1.Columns.Add("接收", 65, HorizontalAlignment.Right);
		listview1.Columns.Add("发送", 65, HorizontalAlignment.Right);
		listview1.Columns.Add("IP地址", 105, HorizontalAlignment.Left);
		listview1.Columns.Add("客户端名", 165, HorizontalAlignment.Left);
		listview1.Columns.Add("备注", 65, HorizontalAlignment.Left);

		PA_DoFetchWLanStations();
		PA_DoFetchClientData();
		for(int i=0; i<nStationsCount; i++){
			ListViewItem lvi = new ListViewItem(i.ToString(), i);
			lvi.SubItems.Add(A_objStations[i].m_strID);
			lvi.SubItems.Add(A_objStations[i].m_strMacAddress);
			lvi.SubItems.Add(A_objStations[i].m_strStatus);
			lvi.SubItems.Add(A_objStations[i].m_strReceive);
			lvi.SubItems.Add(A_objStations[i].m_strSend);
			for(int n=0; n<nClientsCount; n++){
				if(A_objStations[i].m_strMacAddress==A_objClients[n].m_strMacAddress){
					lvi.SubItems.Add(A_objClients[n].m_strIpAddress);
					lvi.SubItems.Add(A_objClients[n].m_strClientName);
					lvi.SubItems.Add(A_objClients[n].m_strMemo);
					//lvi.SubItems.Add(A_objStations[i].m_strMemo);
				}
			}
			listview1.Items.Add(lvi);
		}
	}

	private string[] GetConfigList(string strData, string strPrefix, string strSufix){
		//string strPrefix = "var logList=new Array(\n";
		int nPosStart = strData.IndexOf(strPrefix);
		int nPosEnd = -1;
		if(nPosStart>=0){
			nPosStart += strPrefix.Length;
			nPosEnd = strData.IndexOf(strSufix, nPosStart);
			if(nPosEnd>=0){
				strData = strData.Substring(nPosStart, nPosEnd-nPosStart);
				//string[] A_strLines = strData.Split(new Char[]{'\n'});
				string[] A_strLines = strData.Split('\n');
				int nLen = A_strLines.Length;
				for(int i=0; i<nLen; i++){
					if(A_strLines[i][0]=='"'){
						A_strLines[i] = A_strLines[i].Substring(1, A_strLines[i].Length-3).Trim();
					}else{
						A_strLines[i] = A_strLines[i].Substring(0, A_strLines[i].Length-1).Trim();
					}
				}
				return A_strLines;
			}
		}
		//MessageBox.Show(nPosStart.ToString() + " " + nPosEnd.ToString() + "\n" + strData);
		return null;
	}

	private void PA_DoDisplaySysLog(){
		listview1.Clear();
		listview1.Columns.Add("@", 35, HorizontalAlignment.Left);
		listview1.Columns.Add("日志", 625, HorizontalAlignment.Left);

		string strData = Do_DownloadData("SystemLogRpm.htm");
		string[] A_strLines = GetConfigList(strData, "var logList=new Array(\n", strSufix);
		if(A_strLines!=null){
			int nLen = A_strLines.Length;
			for(int i=0; i<nLen; i++){
				int n = nLen - i - 1;
				ListViewItem lvi = new ListViewItem(n.ToString(), i);
				lvi.SubItems.Add(A_strLines[n]);
				listview1.Items.Add(lvi);
			}
			//MessageBox.Show("len=" + A_strLines.Length + "\n" + A_strLines[0]);
		}
	}

	private void PA_DoFetchClientData(){
		string strData = Do_DownloadData("AssignedIpAddrListRpm.htm");
		string[] A_strLines = GetConfigList(strData, "var DHCPDynPara=new Array(\n", strSufix);
		nClientsCount = 0;
		if(A_strLines!=null){
			nClientsCount = Convert.ToInt32(A_strLines[0]);
			if(nClientsCount>0){
				A_strLines = GetConfigList(strData, "var DHCPDynList=new Array(\n", strSufix);
				if(A_strLines!=null){
					int nLen = A_strLines.Length;
					int nCount = nLen / 4;
					nClientsCount = nCount;

					for(int i=0; i<nCount; i++){
						int n = i * 4;
						string m_strMacAddress = A_strLines[n+1];
						A_objClients[i].init(i+1, A_strLines[n], m_strMacAddress, A_strLines[n+2], A_strLines[n+3]);
						A_objClients[i].m_strMemo = GetMemo(m_strMacAddress);
					}
					//MessageBox.Show(nLen + " " + nCount);
				}
			}
		}
	}

	private void PA_DoFetchWLanStations(){
		string strData = Do_DownloadData("WlanStationRpm.htm");
		string[] A_strLines = GetConfigList(strData, "var wlanHostPara=new Array(\n", strSufix);
		nStationsCount = 0;
		if(A_strLines!=null){
			nStationsCount = Convert.ToInt32(A_strLines[0]);
			if(nStationsCount>0){
				A_strLines = GetConfigList(strData, "var hostList=new Array(\n", strSufix);
				if(A_strLines!=null){
					int nLen = A_strLines.Length;
					int nCount = nLen / 7;
					nStationsCount = nCount;

					for(int i=0; i<nCount; i++){
						int n = i * 7;
						string m_strMacAddress = A_strLines[n];
						A_objStations[i].init(i+1, m_strMacAddress, A_strLines[n+1], A_strLines[n+5], A_strLines[n+6]);
						A_objStations[i].m_strMemo = GetMemo(m_strMacAddress);
					}
					//MessageBox.Show(nLen + " " + nCount);
				}
			}
		}
	}

	private string GetMemo(string s){
		for(int i=0; i<A_strMemos.Length/2; i++){
			if(A_strMemos[i, 0]==s){
				return A_strMemos[i, 1];
			}
		}
		return null;
	}

	private void PA_DoClearDeviceLog(){
		DialogResult dr = MessageBox.Show("清除设备日志么?", conf__strCaptain,
			MessageBoxButtons.YesNo, MessageBoxIcon.Question, MessageBoxDefaultButton.Button2);
		if(dr==DialogResult.Yes){
			Do_DownloadData("SystemLogRpm.htm?ClearLog=%C7%E5%B3%FD%CB%F9%D3%D0%C8%D5%D6%BE");
			PA_DoDisplaySysLog();
		}
	}

	private void PA_DoRebootDevice(){
		DialogResult dr = MessageBox.Show("重启设备么?", conf__strCaptain,
			MessageBoxButtons.YesNo, MessageBoxIcon.Question, MessageBoxDefaultButton.Button2);
		if(dr==DialogResult.Yes){
			Do_DownloadData("SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7");
			MessageBox.Show("正在重启，请等待15秒。", conf__strCaptain,	MessageBoxButtons.OK, MessageBoxIcon.Information);
		}
	}

	public static void Main(string[] args){
		Application.Run(new PaSpyRouter2016CS20());
	}
}

class CLanHost{
	public int m_nID;
	public string m_strID;
	public string m_strClientName;
	public string m_strMacAddress;
	public string m_strIpAddress;
	public string m_strValidTime;
	public string m_strMemo;

	public void init(int id, string strClientName, string strMacAddress, string strIpAddress, string strValidTime){
		this.m_nID			 = id;
		this.m_strID		 = id.ToString();
		this.m_strClientName = strClientName;
		this.m_strMacAddress = strMacAddress;
		this.m_strIpAddress	 = strIpAddress;
		this.m_strValidTime  = (strValidTime == "Permanent" ? "永久" : strValidTime);
		this.m_strMemo		 = "";
	}
}

class CLanStation{
	public int m_nID;
	public string m_strMacAddress;
	public string m_strStatus;
	public string m_strReceive;
	public string m_strSend;
	public string m_strMemo;

	public string m_strID;
	public int m_nStatus;
	public int m_nReceive;
	public int m_nSend;

	public int nFlag = 0;

	public void init(int nID, string strMacAddress, string strStatus, string strReceive, string strSend){
		this.m_nID = nID;
		this.m_strMacAddress = strMacAddress;
		this.m_strStatus = strStatus;
		this.m_strReceive = strReceive;
		this.m_strSend = strSend;

		this.m_strID = nID.ToString();
		this.m_nStatus = Convert.ToInt32(strStatus);
		this.m_nReceive = Convert.ToInt32(strReceive);
		this.m_nSend = Convert.ToInt32(strSend);
		this.m_strMemo = "";

		this.nFlag = 0;
	}
}
