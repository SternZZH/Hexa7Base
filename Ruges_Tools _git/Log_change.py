# Log文件修改后端
#写入_imform进入log文件
def write_to_log(_imform):
    with open("Log_File.txt","a",encoding="utf-8") as file:
        file.write(_imform)
        file.close()

#读取log文件到text中
def read_log():
    result = []
    file = open("Log_File.txt","r",encoding='UTF-8')
    for line in file:
        result.append(line)

    file.close()
    return result

#清除log文件内容
def clear_log():
    with open("Log_File.txt","w") as file:
        file.truncate(0)
        file.close()
