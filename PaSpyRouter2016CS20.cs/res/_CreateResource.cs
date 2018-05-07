using System;
using System.IO;
using System.Drawing;
using System.Resources;

public class _CreateResource{
	public static void Main(string[] args){
		string strCrlf = "\r\n";
		string strOutputFile = null;
		bool isReady = false;
		try{
			string m_strFile_xml = "_CreateResource.xml";
			System.Xml.XmlTextReader xtr = new System.Xml.XmlTextReader(m_strFile_xml);
			//xtr.ReadToFollowing ("item");//.net2.0+
			while(xtr.Read()){
				if(xtr.Name.Equals("strOutputFile")){
					strOutputFile = xtr.GetAttribute("strFile");
					isReady = true;
					break;
				}
			}
			if(isReady){
				ResourceWriter rw = new ResourceWriter(strOutputFile);
				Console.Write("Output: " + strOutputFile + strCrlf);
				Console.Write("------------------------------" + strCrlf);

				while(xtr.Read()){
					string strTypeName = xtr.Name;
					string strItemName = "key";
					string strResource = "value";
					if(strTypeName.Equals("Icon")){
						Icon ico = new Icon(strItemName = xtr.GetAttribute("strFile"));
						rw.AddResource(strResource = xtr.GetAttribute("strResourceName"), ico);
						Console.Write(strTypeName + ": \"" + strItemName + "\" => \"" + strResource + "\"" + strCrlf);
					}else if(strTypeName.Equals("Image")){
						Image image = Image.FromFile(strItemName = xtr.GetAttribute("strFile"));
						rw.AddResource(strResource = xtr.GetAttribute("strResourceName"), image);
						Console.Write(strTypeName + ": \"" + strItemName + "\" => \"" + strResource + "\"" + strCrlf);
					}else if(strTypeName.Equals("Data")){
						FileStream fs = new FileStream(strItemName = xtr.GetAttribute("strFile"),
							FileMode.Open, FileAccess.Read, FileShare.Read);
						int nFileLength = (int)fs.Length;
						BinaryReader br = new BinaryReader(fs);
						byte[] byteBuffer = br.ReadBytes(nFileLength);
						if(byteBuffer.Length==nFileLength){
							rw.AddResource(strResource = xtr.GetAttribute("strResourceName"), byteBuffer);
						}else{
							Console.Write("Read fail." + strCrlf);
						}
						br.Close();
						fs.Close();
						Console.Write(strTypeName + ": \"" + strItemName + "\" => \"" + strResource + "\"" + strCrlf);
					}else if(strTypeName.Equals("String")){
						rw.AddResource(strItemName = xtr.GetAttribute("strResourceName"),
							strResource = xtr.GetAttribute("strContent"));
						Console.Write(strTypeName + ": \"" + strItemName + "\" => \"" + strResource + "\"" + strCrlf);
					}
				}
				rw.Generate();
				rw.Close();
				Console.Write("------------------------------" + strCrlf);
				Console.Write("Done." + strCrlf);
			}
			xtr.Close();


		}catch(Exception ex){
			Console.Write("Exception: " + ex.Message + strCrlf);
		}

	}
}