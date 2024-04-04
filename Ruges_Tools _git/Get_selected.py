from waapi import WaapiClient
# 选择对象后端
def Waapi_getSellectedOBJ(client:WaapiClient):
    Checkoptions = {'return':['id','name']}

    _result  = client.call('ak.wwise.ui.getSelectedObjects',options=Checkoptions)
    return _result
