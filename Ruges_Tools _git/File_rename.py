from waapi import WaapiClient
# 重命名工具后端
def waapi_rename(client:WaapiClient,_object:str,_newName:str):
    arg = {
            "object":_object,
            "value":_newName
        }
    client.call("ak.wwise.core.object.setName",arg)