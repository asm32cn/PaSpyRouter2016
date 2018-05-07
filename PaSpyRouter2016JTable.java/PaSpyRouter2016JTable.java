// PaSpyRouter2016JTable.java

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.table.*;
import javax.imageio.*;
//import javax.swing.JToolBar;
import java.awt.image.BufferedImage;
///
import java.io.*;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
///
import java.util.Vector;


class PaSpyRouter2016JTable extends JTable implements ActionListener{
	private final String conf__strCaptain = "PaSpyRouter2016JTable.java";
	private final int conf__nButtonCount = 7;
	private JFrame _frame = new JFrame();
	private JScrollPane _pane = new JScrollPane();
	private JToolBar jtb = new JToolBar();
	private JButton[] buttons = new JButton[conf__nButtonCount];
	private String[] icons = {"res/res-button-01.png", "res/res-button-02.png", "res/res-button-03.png",
		"res/res-button-04.png", "res/res-button-05.png", "res/res-button-06.png", "res/res-button-07.png"};
	private final String conf__strCookies = "Authorization=Basic%20YWRtaW46cGFzc3dk; ChgPwdSubTag=";
	private final String strSufix = "\n0,0 );\n";

	private Vector clients = new Vector();
	private Vector stations = new Vector();
	private int nClients = 0;
	private int nStations = 0;

	public 

	public PaSpyRouter2016JTable(){
		_frame.setTitle(conf__strCaptain);
		_frame.setSize(780, 450);
		_frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		_frame.setLocationRelativeTo(null);

		jtb.setFloatable(false);
		for(int i=0; i<conf__nButtonCount; i++){
			try{
				buttons[i] = new JButton(new ImageIcon(ImageIO.read(this.getClass().getResourceAsStream(icons[i]))));
				buttons[i].addActionListener(this);
				jtb.add(buttons[i]);
			}catch(Exception e){
				System.out.println(e);
			}
			if(i==0||i==3||i==5){
				jtb.addSeparator();
			}
		}

		_frame.getContentPane().add(jtb, BorderLayout.NORTH);
		_frame.getContentPane().add(_pane, BorderLayout.CENTER);

		_pane.setViewportView(this);
		_frame.setVisible(true);
	}


	private void doDisplayReport(){
		doFetchClientData();
		doFetchWLanStations();
		setTableContent(new String[]{"@", "ID", "¿Í»§¶ËÃû", "MACµØÖ·", "IPµØÖ·", "ÓÐÐ§Ê±¼ä", "±¸×¢", "½ÓÊÕ", "·¢ËÍ"},
			new int[]{25, 25, 165, 115, 105, 65, 65, 65, 65}, clients);
	}

	private void doDisplayHosts(){
		doFetchClientData();
		setTableContent(new String[]{"@", "ID", "¿Í»§¶ËÃû", "MACµØÖ·", "IPµØÖ·", "ÓÐÐ§Ê±¼ä", "±¸×¢"},
			new int[]{25, 25, 165, 115, 105, 65, 65}, clients);
	}

	private void doDisplayStations(){
		doFetchClientData();
		doFetchWLanStations();
		/*
		Vector data = new Vector();
		for(int i=0; i<nStations; i++){
			Vector v = new Vector();
			//Vector row = (Vector)stations.get(i);
			v.add(0, String.valueOf(i));
			Vector row = (Vector)stations.get(i);
			System.out.println("i = " + i);
			System.out.println(row);
			v.add(1, row);
			//v.add(1, ((Vector)((Vector)stations.get(i)).get(1)).toString());
			//v.add(1, stations.get(i).get(2));
			//v.add(1, stations.get(i).get(3));
			//v.add(1, stations.get(i).get(4));
			//v.add(1, stations.get(i).get(5));
			//stations
			data.add(v);
		}*/
		Vector data = stations;
		setTableContent(new String[]{"@", "ID", "MACµØÖ·", "×´Ì¬", "½ÓÊÕ", "·¢ËÍ", "IPµØÖ·", "¿Í»§¶ËÃû", "±¸×¢"},
			new int[]{25, 25, 115, 40, 65, 65, 105, 165, 65}, data);
	}

	private void doDisplaySysLog(){
		String strData = doDownloadData("SystemLogRpm.htm");
		String[] A_strLines = GetConfigList(strData, "var logList=new Array(\n", strSufix);
		Vector data = new Vector();
		if(A_strLines!=null){
			int nLen = A_strLines.length;
			for(int i=0; i<nLen; i++){
				int n = nLen - i - 1;
				Vector v = new Vector();
				v.add(0, String.valueOf(n));
				v.add(1, A_strLines[n]);
				data.add(v);
			}
		}

		setTableContent(new String[]{"@", "ÈÕÖ¾"}, new int[]{35, 720}, data);
	}

	private void doClearSysLog(){
		int answer = JOptionPane.showConfirmDialog(_frame, "Çå³ýÉè±¸ÈÕÖ¾Ã´?", conf__strCaptain,
			JOptionPane.YES_NO_OPTION, JOptionPane.INFORMATION_MESSAGE);
		if(answer==0){
			doDownloadData("SystemLogRpm.htm?ClearLog=%C7%E5%B3%FD%CB%F9%D3%D0%C8%D5%D6%BE");
			doDisplaySysLog();
		}
	}

	private void doRebootDevice(){
		int answer = JOptionPane.showConfirmDialog(_frame, "ÖØÆôÉè±¸Ã´?", conf__strCaptain,
			JOptionPane.YES_NO_OPTION, JOptionPane.INFORMATION_MESSAGE);
		if(answer==0){
			doDownloadData("SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7");
			JOptionPane.showMessageDialog(_frame, "ÕýÔÚÖØÆô£¬ÇëµÈ´ý15Ãë¡£", conf__strCaptain, JOptionPane.INFORMATION_MESSAGE);
		}
	}

	private void doFetchClientData(){
		clients = new Vector();
		String strData = doDownloadData("AssignedIpAddrListRpm.htm");
		String[] A_strLines = GetConfigList(strData, "var DHCPDynPara=new Array(\n", strSufix);
		nClients = 0;
		if(A_strLines!=null){
			nClients = toInt(A_strLines[0]);
			if(nClients>0){
				A_strLines = GetConfigList(strData, "var DHCPDynList=new Array(\n", strSufix);
				if(A_strLines!=null){
					int nLen = A_strLines.length;
					int nCount = nLen / 4;
					nClients = nCount;

					for(int i=0; i<nCount; i++){
						int n = i * 4;
						Vector v = new Vector();
						v.add(0, String.valueOf(i));
						v.add(1, String.valueOf(i + 1));
						v.add(2, A_strLines[n]);
						v.add(3, A_strLines[n+1]);
						v.add(4, A_strLines[n+2]);
						v.add(5, A_strLines[n+3]);
						clients.add(v);
					}
				}
			}
		}
	}

	private void doFetchWLanStations(){
		stations = new Vector();
		String strData = doDownloadData("WlanStationRpm.htm");
		String[] A_strLines = GetConfigList(strData, "var wlanHostPara=new Array(\n", strSufix);
		nStations = 0;
		if(A_strLines!=null){
			nStations = toInt(A_strLines[0]);
			if(nStations>0){
				A_strLines = GetConfigList(strData, "var hostList=new Array(\n", strSufix);
				if(A_strLines!=null){
					int nLen = A_strLines.length;
					int nCount = nLen / 7;
					nStations = nCount;

					for(int i=0; i<nCount; i++){
						int n = i * 7;
						Vector v = new Vector();
						v.add(0, String.valueOf(i));
						v.add(1, String.valueOf(i + 1));
						v.add(2, A_strLines[n]);
						v.add(3, A_strLines[n+1]);
						v.add(4, A_strLines[n+5]);
						v.add(5, A_strLines[n+6]);
						stations.add(v);
					}
				}
			}
		}
	}

	private void setTableContent(String[] columnsName, int[] columnsWidth, Vector data){
		setModel(getTableModel(columnsName, data));
		for(int i=0; i<columnsWidth.length; i++){
			//System.out.println(i + " " + columnsWidth[i]);
			if(columnsWidth[i]>0){
				getColumnModel().getColumn(i).setPreferredWidth(columnsWidth[i]);
			}
		}
	}

	private DefaultTableModel getTableModel(String[] columnsName, Vector data){
		DefaultTableModel tmd = new DefaultTableModel();
		Vector columns = new Vector();
		for(int i=0; i<columnsName.length; i++){
			columns.add(columnsName[i]);
		}
		tmd.setDataVector(data, columns);
		return tmd;
	}

	private String[] GetConfigList(String strData, String strPrefix, String strSufix){
		//string strPrefix = "var logList=new Array(\n";
		int nPosStart = strData.indexOf(strPrefix);
		int nPosEnd = -1;
		if(nPosStart>=0){
			nPosStart += strPrefix.length();
			nPosEnd = strData.indexOf(strSufix, nPosStart);
			if(nPosEnd>=0){
				strData = strData.substring(nPosStart, nPosEnd);
				String[] A_strLines = strData.split("\n");
				int nLen = A_strLines.length;
				for(int i=0; i<nLen; i++){
					if(A_strLines[i].charAt(0)=='"'){
						A_strLines[i] = A_strLines[i].substring(1, A_strLines[i].length()-2).trim();
					}else{
						A_strLines[i] = A_strLines[i].substring(0, A_strLines[i].length()-1).trim();
					}
				}
				return A_strLines;
			}
		}
		//MessageBox.Show(nPosStart.ToString() + " " + nPosEnd.ToString() + "\n" + strData);
		return null;
	}

	/**/
	public String doDownloadData(String strParam){
		String strLinkPrefix = "http://192.168.1.1/userRpm/";
		HttpURLConnection conn = null;
		String strHtmlData = null;
		try{
			URL url = new URL(strLinkPrefix + strParam);
			conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setDoOutput(true);
			conn.setRequestProperty("Cookie", conf__strCookies);
			conn.setRequestProperty("Referer", strLinkPrefix + "MenuRpm.htm");

			//byte[] bytes = strData.getBytes("utf-8");
			//conn.getOutputStream().write(bytes); // ÊäÈë²ÎÊý
			InputStream is = conn.getInputStream();

			ByteArrayOutputStream baos = new ByteArrayOutputStream();
			int nBytesRead = 1024;
			byte[] buffer = new byte[nBytesRead];
			while ((nBytesRead = is.read(buffer)) != -1) {
				baos.write(buffer, 0, nBytesRead);
			}
			baos.close();
			is.close();
			strHtmlData = new String(baos.toByteArray(), "gbk");
		}catch(Exception e){
			e.printStackTrace();
		}
		return strHtmlData;
	}

	//actionPerformed
	public void actionPerformed(ActionEvent e){
		int nSelected = -1;
		for(int i=0; i<conf__nButtonCount; i++){
			if(e.getSource().equals(buttons[i])){
				nSelected = i;
				break;
			}
		}
		switch(nSelected){
			case 1:
				doDisplayReport(); break;
			case 2:
				doDisplayHosts(); break;
			case 3:
				doDisplayStations(); break;
			case 4:
				doDisplaySysLog(); break;
			case 5:
				doClearSysLog(); break;
			case 6:
				doRebootDevice(); break;
			//default:
			//	System.out.println("action=" + nSelected);
			//	break;
		}
	}

	private int toInt(String s){
		int n=0;
		try{
			n = Integer.parseInt(s);
		}catch(Exception e){
			n = 0;
		}
		return n;
	}

	public static void main(String[] args){
		new PaSpyRouter2016JTable();
	}
}
