from waapi import WaapiClient
# Profiler操控工具后端
# 开始捕捉
def startCapture(Client:WaapiClient):
    Client.call("ak.wwise.core.profiler.startCapture")

# 结束捕捉
def stopCapture(Client:WaapiClient):
    Client.call("ak.wwise.core.profiler.stopCapture")

# 获取时间戳
def getCursorTime(Client:WaapiClient):
    args = {
        "cursor":"capture"
    }
    result = Client.call("ak.wwise.core.profiler.getCursorTime",args)
    return result["return"]

# 获取CPU占用
def getCPUInf(Client:WaapiClient,_time=None):
    if(_time == None):
        arg = {
            "time":"capture"
        }
    else:
        arg = {
            "time":_time
        }

    result = Client.call("ak.wwise.core.profiler.getCpuUsage",arg)
    return(result["return"])

with WaapiClient() as Client:
    #print(getCPUInf(Client,180000))
    pass
