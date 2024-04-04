from waapi import WaapiClient,CannotConnectToWaapiException
# 找到对应id列表的对象，在Wwise 的pe中选中
def find_Obj_inPE(client:WaapiClient,listofOBJ:list):
    try:
        listofOBJ = listofOBJ
        args = {
                "command":"FindInProjectExplorerSyncGroup1",
                "objects":listofOBJ
            }

        client.call("ak.wwise.ui.commands.execute",args)
        client.call("ak.wwise.ui.bringToForeground")
    except:
        print("选中失败")

def bringWwise_frount(client):
    client.call("ak.wwise.ui.bringToForeground")

