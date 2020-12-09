import requests
import json

UE4_WEB_REMOTE_CONTROL_URL = "http://127.0.0.1:8080/"

UE4_WRC_CALL = "remote/object/call"
UE4_WRC_PROPERTY = "remote/object/property"


def testlink():
    """
    docstring
    """
    url = UE4_WEB_REMOTE_CONTROL_URL + UE4_WRC_PROPERTY
    body = {
        "objectPath": "/Game/Levels/TempMap.TempMap:PersistentLevel.LightSource",
        "access": "READ_ACCESS"
    }
    print(url, body)
    response = requests.put(url, json=body)

    print(response, response.text, response.json())
    pass


testlink()
