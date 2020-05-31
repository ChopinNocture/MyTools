using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System;

public class ServerInterface : MonoBehaviour {
    public const string HTTP_Prefix = "http://";

    /// <summary>
    /// 可配置服务器地址
    /// </summary>
    public string serverIP = "122.152.207.155";
    public string port = "7000";

    public delegate void onDataRecieved<T>(T data) where T : HttpData;

    // Use this for initialization
    void Start () {
        // ------todo: get serverip from config file, maybe...  serverIP = getxxxxx
        StartCoroutine(GetFromServ<HttpData>(ondataget));

        Debug.Log("---------------");

	}

    void ondataget(HttpData data)
    {
        Debug.Log("-7-8-8-9-9");
    }

	// Update is called once per frame
	void Update () {
		
	}

    protected string getURL(HttpData data)
    {
        return HTTP_Prefix + serverIP + ":" + port + "/" + data.URL; // http://www.my-server.com
    }

    protected string getParamString(object[] postParam)
    {

    }

    public IEnumerator GetFromServ<T>(onDataRecieved<T> callback, params object[] postParam) where T : HttpData, new()
    {
        Debug.Log("1");
        T data = new T();
        if (data.postParamType.Length != postParam.Length)
        {
            Debug.LogError("Data Type:"+ T.GetType() +" need " + data.postParamType.Length.ToString() +" param!");
        }


        using (UnityWebRequest www = UnityWebRequest.Get(getURL(data)))
        {
            yield return www.SendWebRequest();
            
            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log("2" + www.error);
                
                callback(data);
            }
            else
            {
                // Show results as text
                Debug.Log("3" + www.downloadHandler.text);

                // Or retrieve results as binary data
                byte[] results = www.downloadHandler.data;

                
                callback(data);
            }
        }

        yield return null;
    }

    public SendResult SendToServ<T>(T data) where T : HttpData
    {
        SendResult res = new SendResult();
        return res;
    }
//===================================================
// 纯粹的数据data

}

public struct SendResult
{

}

public class HttpData
{
    [NonSerialized]
    public object[] postParamType;
    //[NonSerialized]
    public virtual string URL { get { return ""; } }
    //[NonSerialized]
    public virtual bool isPost { get { return false; } }
}

public class TestData : HttpData
{
    public override string URL { get { return "http://122.152.207.155:7000/course/listOneContentByContentInfo/"; } }
    //public virtual bool isPost { get { return true; } }
}