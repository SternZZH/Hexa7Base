from waapi import WaapiClient,CannotConnectToWaapiException #用于Wwapi核心和异常抛出
import tkinter as tk #用于搭建UI框架
from pprint import pprint

# 后端文件
from findOBJinPE import find_Obj_inPE
from findOBJinPE import bringWwise_frount
from File_import import SelectFile,waapi_import_file
from Get_selected import Waapi_getSellectedOBJ
from File_rename import waapi_rename
import Get_Profiler
import Obj_check
import Log_change

#小工具主界面UI
class MenuUI:
    def __init__(self,_Tkroot):
        self._Tkroot = _Tkroot
        self._Tkroot.title("乳鸽的Wwise小工具")
        self._Tkroot.geometry("500x380")

        self.mainframe1 = tk.Frame(Tkroot)
        self.mainframe1.pack(pady = 10)

        self.mainframe2 = tk.Frame(Tkroot)
        self.mainframe2.pack()

        self.mainframe = tk.Frame(Tkroot)
        self.mainframe.pack()

        

        global img_gif
        global img_Touxiang
        img_gif = tk.PhotoImage(file="image/MIHOYO_LOGO02.gif")
        img_Touxiang = tk.PhotoImage(file = "image/Spiker.gif")
        touxinag_img = tk.Label(self.mainframe1,image=img_Touxiang)
        touxinag_img.grid(row=0,column=1,padx=10)

        self.UIComponemt01_name = tk.Label(self.mainframe2,text="欢迎使用乳鸽的Wwise小工具 ; )")
        self.UIComponemt01_name.grid(row=1,column=1,pady=20)

        self.AudioInport_Button = tk.Button(self.mainframe,text="     进行音频文件快速导入     ",command=self.OpenAudioImportPanel)
        self.AudioInport_Button.grid(row=2,column=0,pady=10,padx=37)
        self.AudioInport_Button.config(bg = "#58e9e6")
        
        self.Rename_Button = tk.Button(self.mainframe,text="        进行批量对象改名        ",command=self.OpenRenamePanel)
        self.Rename_Button.grid(row=2,column=1,pady=10,padx=20)
        self.Rename_Button.config(bg = "#3f92d6",fg="white")
                                                                                        
        self.GetInformation_Button = tk.Button(self.mainframe,text="        进行对象快速查询        ",command=self.OpenInformationPanel)
        self.GetInformation_Button.grid(row=3,column=0,pady=10)
        self.GetInformation_Button.config(bg = "#58e9e6")

        self.UIquickSelectOBJ_button = tk.Button(self.mainframe,text="  通过id快速定位在Wwise中  ",command=Openquick_locatePanel)
        self.UIquickSelectOBJ_button.grid(row=3,column=1,pady=10)
        self.UIquickSelectOBJ_button.config(bg = "#3f92d6",fg="white")

        self.UIComponemtX_Button = tk.Button(self.mainframe,text="        获取CPU用时占比        ",command=self.OpenGetCpuPanel)
        self.UIComponemtX_Button.grid(row=4,column=0,pady=10)
        self.UIComponemtX_Button.config(bg = "#58e9e6")

        self.UIComponemtY_Button = tk.Button(self.mainframe,text="         CPU超值警告Log        ",command=OpenLogPanel)
        self.UIComponemtY_Button.grid(row=4,column=1,pady=10)
        self.UIComponemtY_Button.config(bg = "#3f92d6",fg="white")

    #打开导入界面
    def OpenAudioImportPanel(self):

        Tkroot_Import = tk.Tk()
        importui = ImportUI(Tkroot_Import)
        Tkroot_Import.mainloop()

    #打开重命名界面
    def OpenRenamePanel(self):

        Tkroot_Rename = tk.Tk()
        renameui = RenameUI(Tkroot_Rename)
        Tkroot_Rename.mainloop()

    #打开查询信息界面
    def OpenInformationPanel(sefl):

        Tkroot_Imformation = tk.Tk()
        informationui = InformationUI(Tkroot_Imformation)
        Tkroot_Imformation.mainloop()

    #打开PCU信息查询界面
    def OpenGetCpuPanel(self):
        Tkroot_getCPU = tk.Tk()
        CPuInfromui = GetCpuProfilerUI(Tkroot_getCPU)
        Tkroot_getCPU.mainloop()

    #打开快速定界面
    global Openquick_locatePanel
    def Openquick_locatePanel():
        Tkroot_Quick_locate = tk.Tk()
        QuickLocateui = QuickCheckUI(Tkroot_Quick_locate)
        Tkroot_Quick_locate.mainloop()

    #打开log面板
    global OpenLogPanel
    def OpenLogPanel():
        Tkroot_OpenLog = tk.Tk()
        Logui = OpenLogUI(Tkroot_OpenLog)
        Tkroot_OpenLog.mainloop()
    

#导入UI界面
class ImportUI:
    def __init__(self,_Tkroot):
        self._Tkroot = _Tkroot
        self._Tkroot.title("快速导入音频")
        self._Tkroot.geometry("400x370")

        self.ImportFrame = tk.Frame(_Tkroot) #参数中填窗口tk
        self.ImportFrame.pack(pady = 20)

        self.Import_Unit_label = tk.Label(self.ImportFrame,text="Work Unit名称:")
        self.Import_Unit_label.grid(row=0,column=0,padx=5,pady=5)
        self.Import_Unit_label_entry = tk.Entry(self.ImportFrame)
        self.Import_Unit_label_entry.insert(0,"Default Work Unit")
        self.Import_Unit_label_entry.config(fg="grey")
        self.Import_Unit_label_entry.grid(row=0,column=1,padx=5,pady=10)

        self.Import_Actor_mixer = tk.Label(self.ImportFrame,text="Actor-Mixer名称:")
        self.Import_Actor_mixer.grid(row=1,column=0,padx=5,pady=5)
        self.Import_Actor_mixer = tk.Entry(self.ImportFrame)
        self.Import_Actor_mixer.insert(0,"New Actor-Mixer")
        self.Import_Actor_mixer.config(fg="grey")
        self.Import_Actor_mixer.grid(row=1,column=1,padx=5,pady=10)

        self.Import_Container_type_var = tk.StringVar(_Tkroot)
        self.Import_Container_type_var.set("   选择容器类型   ")
        self.Import_Container_type_label = tk.Label(self.ImportFrame,text="容器类型:")
        self.Import_Container_type_label.grid(row=2,column=0,padx=5,pady=10)
        self.Import_Container_type_selectmenu = tk.OptionMenu(self.ImportFrame,self.Import_Container_type_var,"随机容器","序列容器","切换容器","混合容器")
        self.Import_Container_type_selectmenu.grid(row=2,column=1,padx=5,pady=10)
        self.Import_Container_type_selectmenu.config(bg = "#58e9e6")

        self.Import_Sounds_Container_name = tk.Label(self.ImportFrame,text="Container名称:")
        self.Import_Sounds_Container_name.grid(row=3,column=0,padx=5,pady=10)
        self.Import_Sounds_Container_name_entry = tk.Entry(self.ImportFrame)
        self.Import_Sounds_Container_name_entry.insert(0,"New Container")
        self.Import_Sounds_Container_name_entry.config(fg="grey")
        self.Import_Sounds_Container_name_entry.grid(row=3,column=1,padx=5,pady=10)

        self.Import_Sounds_type_var = tk.StringVar(_Tkroot)
        self.Import_Sounds_type_var.set("SFX")
        self.Import_Sounds_type_label = tk.Label(self.ImportFrame,text = "声音类型:")
        self.Import_Sounds_type_label.grid(row=4,column=0,padx=5,pady=10)
        self.Import_Sounds_type_selectmenu = tk.OptionMenu(self.ImportFrame,self.Import_Sounds_type_var,"SFX","Voice")
        self.Import_Sounds_type_selectmenu.grid(row=4,column=1,padx=5,pady=10)
        self.Import_Sounds_type_selectmenu.config(bg = "#58e9e6")

        self.Import_Sounds_Source_label = tk.Label(self.ImportFrame,text = "选择音频文件：")
        self.Import_Sounds_Source_label.grid(row=5,column=0,padx=5,pady=10)

        self.Import_Sounds_Button = tk.Button(self.ImportFrame,text="点击选择文件：",command=SelectFile)
        self.Import_Sounds_Button.grid(row=5,column=1)
        self.Import_Sounds_Button.config(bg = "#58e9e6")
        
        self.Import_Sounds_Button_finish = tk.Button(self.ImportFrame,text = "   选择完毕   ",command=self.import_audio)
        self.Import_Sounds_Button_finish.grid(row=6,column=1,pady=25)
        self.Import_Sounds_Button_finish.config(bg = "#3f92d6",fg="white")

    #导入SFX行为函数
    def import_audio(self):
        work_unit_name = self.Import_Unit_label_entry.get()
        Import_Actor_mixer = self.Import_Actor_mixer.get()
        container_type = self.Import_Container_type_var.get()
        sound_type = self.Import_Sounds_type_var.get()

        container_name = self.Import_Sounds_Container_name_entry.get()

        container_type_mapping = {
            "   选择容器类型   ":"RandomSequenceContainer",
            "随机容器":"RandomSequenceContainer",
            "序列容器":"Sequence Container",
            "切换容器":"SwitchContainer",
            "混合容器":"BlendContainer",
        }
        container_type = container_type_mapping.get(container_type)

        # 进行文件导入后端操作
        with WaapiClient() as Client:
            waapi_import_file(Client,work_unit_name,Import_Actor_mixer,container_type,container_name,sound_type)
        
#重命名UI界面
class RenameUI:
    def __init__(self,_Tkroot):
        self._Tkroot = _Tkroot
        self._Tkroot.title("快速重命名")
        self._Tkroot.geometry("500x400")

        self.Renameframe = tk.Frame(_Tkroot)#参数为框架的父对象
        self.Renameframe.pack(pady = 10)

        self.Rename_tips01 = tk.Label(self.Renameframe,text="请在Wwise中选中要修改的对象")
        self.Rename_tips01.grid(row=0,column=0,padx=5,pady=20)

        global Check_selected_Button
        global check_button_text
        check_button_text = "   选择好后点击继续   "
        Check_selected_Button = tk.Button(self.Renameframe,text=check_button_text,command=self.getSellected)
        Check_selected_Button.grid(row=1,column=0,pady=20)
        Check_selected_Button.config(bg = "#3f92d6",fg="white")


        
        #rename list用于存储用户输入的修改名组
        global rename_list
        rename_list = []

    #获取所选物体
    def getSellected(self):
        with WaapiClient() as client:
            # waapi选取选中的对象，放回一个列表
            result  = Waapi_getSellectedOBJ(client)

        self.text = tk.Text(self.Renameframe,width=30,height=8)

        SelectedName = []
        #选中物体的id
        global SelectedID
        SelectedID = [] 
        #遍历获取信息：
        num  = 0
        for i in result['objects']:
            num = num+1
            SelectedID.append(i['id']) #塞 ID 进 SelectID 
            SelectedName.append(i['name']) #塞 Name 进 SelectID
        num = len(SelectedName)
        if num == 0:
            self.text.insert('0.0',"你还没选中对象呢"+'\n'+"别心急,先在Wwise中选择对象 ; )"+'\n'+"然后再点击上面的按钮刷新一下再继续吧")
        while num>0:
            self.text.insert('0.0',SelectedName[num-1]+'\n')
            num = num-1

        
        self.text.grid(row=1,column=1)
        check_button_text = "点击刷新选择物体状态"
        Check_selected_Button.config(text=check_button_text,bg = "#58e9e6",fg="black")
        Check_selected_Button.grid(row=0,column=1,pady=20)

        self.rename_old_name = tk.Label(self.Renameframe,text="物体的老名字为：")
        self.rename_old_name.grid(row = 1,column=0,padx=5,pady=20)
        self.Rename_Input = tk.Label(self.Renameframe,text="请输入要修改的新名字：(回车换行分割)")
        self.Rename_Input.grid(row = 2,column=0,padx=5,pady=20)

        global Rename_Input_text
        Rename_Input_text = tk.Text(self.Renameframe,width=30,height=8)
        Rename_Input_text.grid(row = 2,column=1,padx=5,pady=10)

        self.Rename_Input_button = tk.Button(self.Renameframe,text="开始重命名",command=self.StartRename)
        self.Rename_Input_button.grid(row=3,column=1)
        self.Rename_Input_button.config(bg = "#3f92d6",fg="white")

    #开始重命名
    def StartRename(self):

        #读取逐行输入
        rename_list = (Rename_Input_text.get("0.0","end")).split("\n")
        rename_list.pop()#列表最后一个元素是空删除它
        
        try:
            with WaapiClient() as Client:
                num = 0
                bringWwise_frount(Client)
                while(num<len(SelectedID)):
                    #调用waapi重命名
                    waapi_rename(Client,SelectedID[num],rename_list[num])
                    num = num+1
            
        except CannotConnectToWaapiException:
            print("连接失败")

#查询信息UI界面
class InformationUI:
    def __init__(self,_Tkroot):

        self._Tkroot = _Tkroot
        self._Tkroot.title("快速查询信息")
        self._Tkroot.geometry("400x610")

        self.imformationFram = tk.Frame(_Tkroot)
        self.imformationFram.pack(pady=20)

        self.imformationFram1 = tk.Frame(_Tkroot)
        self.imformationFram1.pack()

        self.imformationFram2 = tk.Frame(_Tkroot,bg = "#3f92d6")
        self.imformationFram2.pack(pady=5)

        self.imformationFram3 = tk.Frame(_Tkroot)
        self.imformationFram3.pack()

        self.imformationFram4 = tk.Frame(_Tkroot)
        self.imformationFram4.pack()

        self.imformationFram5 = tk.Frame(_Tkroot)
        self.imformationFram5.pack()

        self.imformationFram6 = tk.Frame(_Tkroot)
        self.imformationFram6.pack()

        self.imformationLabel = tk.Label(self.imformationFram,text="请选择要搜索的对象类型：")
        self.imformationLabel.grid(row=0,column=0,padx=5,pady=10)
        
        global imformation_Obj_Var
        imformation_Obj_Var = tk.StringVar(_Tkroot)
        imformation_Obj_Var.set("全部对象")
        self.imformation_Obj_type = tk.OptionMenu(self.imformationFram,imformation_Obj_Var,"全部对象","WorkUnit","ActorMixer","RandomSequenceContainer","SwitchContainer","BlendContainer","Sound","SoundBank")
        self.imformation_Obj_type.grid(row=0,column=1,padx=5,pady=10)
        self.imformation_Obj_type.config(bg = "#58e9e6")

        self.imformation_Obj_name_Label = tk.Label(self.imformationFram,text="请输入查找对象包含的关键字：")
        self.imformation_Obj_name_Label.grid(row=1,column=0,padx=5,pady=10)

        global imformation_Obj_name_entry
        imformation_Obj_name_entry = tk.Entry(self.imformationFram)
        imformation_Obj_name_entry.grid(row=1,column=1,padx=5,pady=10)

        self.imformation_return_option_label = tk.Label(self.imformationFram1,text="请选择想要查询的内容：")
        self.imformation_return_option_label.grid(row=0,column=0)

        #勾选想要返回的属性
        global imformation_return_option_var01,imformation_return_option_var02,imformation_return_option_var03,imformation_return_option_var04

        imformation_return_option_var01 = tk.StringVar(_Tkroot)
        imformation_return_option_var01.set("name")
        imformation_return_option01 = tk.Checkbutton(self.imformationFram2,text = "name",variable=imformation_return_option_var01,onvalue="name",offvalue="")
        imformation_return_option01.grid(row=1,column=0,padx=5,pady=10)
        
        imformation_return_option_var02 = tk.StringVar(_Tkroot)
        imformation_return_option_var02.set("id")
        imformation_return_option02 = tk.Checkbutton(self.imformationFram2,text = "id",variable=imformation_return_option_var02,onvalue="id",offvalue="")
        imformation_return_option02.grid(row=1,column=1,padx=5,pady=10)

        imformation_return_option_var03 = tk.StringVar(_Tkroot)
        imformation_return_option_var03.set("path")
        imformation_return_option03 = tk.Checkbutton(self.imformationFram2,text = "path",variable=imformation_return_option_var03,onvalue="path",offvalue="")
        imformation_return_option03.grid(row=1,column=2,padx=5,pady=10)

        imformation_return_option_var04 = tk.StringVar(_Tkroot)
        imformation_return_option_var04.set("type")
        imformation_return_option04 = tk.Checkbutton(self.imformationFram2,text = "type",variable=imformation_return_option_var04,onvalue="type",offvalue="")
        imformation_return_option04.grid(row=1,column=3,padx=5,pady=10)


        #找自己还是父子级别
        self.imformation_Obj_name_relation_label=tk.Label(self.imformationFram3,text="你想找的是这个对象的：")
        self.imformation_Obj_name_relation_label.grid(row=0,column=0)

        global imformation_Obj_name_relation_var
        imformation_Obj_name_relation_var = tk.StringVar(_Tkroot)
        imformation_Obj_name_relation_var.set("它自己")
        self.imformation_Obj_name_relation_option = tk.OptionMenu(self.imformationFram3,imformation_Obj_name_relation_var,"它自己","上一级父级","子集")
        self.imformation_Obj_name_relation_option.grid(row=0,column=1,padx=5,pady=10)
        self.imformation_Obj_name_relation_option.config(bg = "#58e9e6")

        self.imformation_Obj_imformations_button = tk.Button(self.imformationFram4,text="    开始查找    ",command=self.showmessages)
        self.imformation_Obj_imformations_button.grid(row=0,column=0,padx=5,pady=30)
        self.imformation_Obj_imformations_button.config(bg="#3f92d6",fg="white")

        global imformation_Obj_imformations_text
        imformation_Obj_imformations_text = tk.Text(self.imformationFram4,width=50,height=15)
        imformation_Obj_imformations_text.grid(row=1,column=0)


    global Selected_return
    Selected_return = []

    global selected_type_return
    selected_type_return = []
    global selected_type_map
    selected_type_map = {
        "它自己":"",
        "上一级父级":"parent",
        "子集":"children"
    }

    def showmessages(self):
        if(imformation_return_option_var01.get()!=""):
            Selected_return.append(imformation_return_option_var01.get())
        if(imformation_return_option_var02.get()!=""):
            Selected_return.append(imformation_return_option_var02.get())
        if(imformation_return_option_var03.get()!=""):
            Selected_return.append(imformation_return_option_var03.get())
        if(imformation_return_option_var04.get()!=""):
            Selected_return.append(imformation_return_option_var04.get())

        selected_type_return.clear()
        if(imformation_Obj_name_relation_var.get()!=""):
            selected_type_return.append(selected_type_map.get(imformation_Obj_name_relation_var.get()))
        
        with WaapiClient() as Client:

            if(imformation_Obj_Var.get()=="全部对象"):

                # 选择了全部对象返回子级或者父级:
                if(selected_type_return[0]!=''):
                    result = Obj_check.waapi_check_AllOBJ(Client,[imformation_Obj_name_entry.get()],Selected_return,selected_type_return)
                
                # 选择了全部对象返回自己：
                elif(selected_type_return[0] ==''):
                    result = Obj_check.waapi_check_AllOBJ(Client,[imformation_Obj_name_entry.get()],Selected_return)
            
            else:
                # 选择了使用类型放回子级或者父级
                if(selected_type_return[0]!=''):
                    result = Obj_check.waapi_check_ofTypeClient(Client,[imformation_Obj_Var.get()],imformation_Obj_name_entry.get(),Selected_return,selected_type_return)
                
                # 选择了使用类型返回自己
                elif(selected_type_return[0] ==''):
                    result = Obj_check.waapi_check_ofTypeClient(Client,[imformation_Obj_Var.get()],imformation_Obj_name_entry.get(),Selected_return)

            imformation_Obj_imformations_text.tag_add("type","0.0")
            imformation_Obj_imformations_text.tag_config("type",foreground ="#3f92d6")

            imformation_Obj_imformations_text.tag_add("type1","0.0")
            imformation_Obj_imformations_text.tag_config("type1",foreground ="#0004b5")


            if(len(result) == 1):
                imformation_Obj_imformations_text.insert('0.0',"没有找到符合对象\n确定所搜索关键字和父子级关系\n以及对象类型是否包括在头部选项中\n\n","type1")

            for _result_type in result.values():
                num =len(_result_type)
                for _tiems in _result_type:
                    imformation_Obj_imformations_text.insert('0.0',"\n\n")
                    
                    for _key in _tiems.keys():
                        imformation_Obj_imformations_text.insert('0.0',_tiems[_key])
                        imformation_Obj_imformations_text.insert('0.0',_key+":","type")
                        imformation_Obj_imformations_text.insert('0.0',"\n")

                    imformation_Obj_imformations_text.insert('0.0',"第"+str(num)+"个对象：","type1")
                    num=num-1

            Selected_return.clear()
            self.imformation_Obj_clear_button = tk.Button(self.imformationFram5,text="   清空text   ",command=self.cleartext)
            self.imformation_Obj_clear_button.grid(row=0,column=0,pady=10) 
            self.imformation_Obj_clear_button.config(bg = "#58e9e6")

            self.quickSelectOBJ_button = tk.Button(self.imformationFram5,text="   通过id快速定位在Wwise中   ",command=Openquick_locatePanel)
            self.quickSelectOBJ_button.grid(row=0,column=1,pady=10,padx=20)
            self.quickSelectOBJ_button.config(bg = "#3f92d6",fg="white")
            
    def cleartext(self):
        imformation_Obj_imformations_text.delete("1.0","end")
        Selected_return.clear()
        selected_type_return.clear()

#快速定位界面
class QuickCheckUI:
    def __init__(self,_Tkroot):

        self._Tkroot = _Tkroot
        self._Tkroot.title("快速查询信息")
        self._Tkroot.geometry("400x350")

        self.QuickCheckFrame = tk.Frame(_Tkroot)
        self.QuickCheckFrame.pack(pady=20)

        self.QuickCheckFrame2 = tk.Frame(_Tkroot)
        self.QuickCheckFrame2.pack(pady=20)

        self.QuickCheckLabel = tk.Label(self.QuickCheckFrame,text=" 请输入要定位对象的id:"+"\n"+"(回车键换行分割)")
        self.QuickCheckLabel.grid(row=0,column=0,padx=5,pady=10)
        
        global QuickCheckText
        QuickCheckText = tk.Text(self.QuickCheckFrame,width=30,height=15)
        QuickCheckText.grid(row = 0,column=1,padx=5,pady=10)

        self.StartLocateButton = tk.Button(self.QuickCheckFrame2,text="    定位到 Wwise Project Explorer    ",command=startLocate)
        self.StartLocateButton.grid(row=0,column=0,pady=12)
        self.StartLocateButton.config(bg="#3f92d6",fg="white")

    global startLocate
    def startLocate():
        global locateList
        locateList = []

        locateList = (QuickCheckText.get("0.0","end")).split("\n")
        locateList.pop()#列表最后一个元素是空删除它

        # print(locateList)
        with WaapiClient() as Client:
            find_Obj_inPE(Client,locateList)
        
#获取CPU信息页面
class GetCpuProfilerUI:
    global timePoint_scale
    # cpu提醒限值
    global warningLimit
    global cpu_warning_limit_entry

    def __init__(self,_Tkroot):
        self._Tkroot = _Tkroot
        self._Tkroot.title("获取Cpu消耗信息")
        self._Tkroot.geometry("500x800")

        self.GetCPUFrame01 = tk.Frame(_Tkroot)
        self.GetCPUFrame01.pack(pady=5,padx=5)

        global GetCPUFrame02
        GetCPUFrame02 = tk.Frame(_Tkroot)
        GetCPUFrame02.pack(pady=5)
        GetCPUFrame02.config(bg = "#3f92d6")

        global GetCPUFrame03
        GetCPUFrame03 = tk.Frame(_Tkroot)
        GetCPUFrame03.pack(pady=5)

        global GetCPUFrame04
        GetCPUFrame04 = tk.Frame(_Tkroot)
        GetCPUFrame04.pack(pady=5)

        global GetCPUFrame05
        GetCPUFrame05 = tk.Frame(_Tkroot)
        GetCPUFrame05.pack(pady=5)

        global GetCPUFrame06
        GetCPUFrame06 = tk.Frame(_Tkroot)
        GetCPUFrame06.pack(pady=5)

        self.GetCPUFrame03 = tk.Frame(_Tkroot)
        self.GetCPUFrame03.pack(pady=20)

        self.start_capture_button = tk.Button(self.GetCPUFrame01,text="      开始捕捉      ",command=StartCapture)
        self.start_capture_button.grid(row=0,column=0,padx=40,pady=10)
        self.start_capture_button.config(bg = "#58e9e6")
        
        self.stop_capture_button = tk.Button(self.GetCPUFrame01,text="      停止捕捉      ",command=StopCapture)
        self.stop_capture_button.grid(row=0,column=1,padx=20,pady=10)
        self.stop_capture_button.config(bg = "#3f92d6",fg="white")

    # 使用按钮增加时间戳
    global add_current
    def add_current():
        timePoint_scale.set(int(timePoint_scale.get())+1)

    # 使用按钮减少时间戳
    global red_current
    def red_current():
        timePoint_scale.set(int(timePoint_scale.get())-1)

    global setScalevalue
    # 修改拖动条的数值
    def setScalevalue(event):
        #print("通过输入修改了数值")
        timePoint_scale.set(int(time_current_entry.get()))

    global show_scale
    def show_scale():
        global timePoint_scale

        timePoint_scale_start_label = tk.Label(GetCPUFrame02,text=Capture_time_start)
        timePoint_scale_start_label.grid(row=0,column=0,padx=10,pady=5)

        global timePoint_scale
        timePoint_scale = tk.Scale(GetCPUFrame02, label="选择要查询的时间戳位置",orient = tk.HORIZONTAL,
                                   from_ = Capture_time_start, to =Capture_time_end,
                                   resolution=1,command = showCPU)
        
        timePoint_scale.config(length=200)
        timePoint_scale.grid(row=0,column=1,padx=40,pady=10)

        timePoint_scale_end_label = tk.Label(GetCPUFrame02,text=Capture_time_end)
        timePoint_scale_end_label.grid(row=0,column=2,padx=10,pady=5)

        #输入精确时间戳：
        global Capture_time_Current
        Capture_time_Current = 0

        time_current_label = tk.Label(GetCPUFrame02,text="输入时间戳")
        time_current_label.grid(row=1,column=1,padx=10,pady=5)

        global time_current_entry
        time_current_entry = tk.Entry(GetCPUFrame02)
        time_current_entry.grid(row=2,column=1,padx=10,pady=5)

        time_current_red = tk.Button(GetCPUFrame02,text="  << ",command=red_current)
        time_current_red.grid(row=2,column=0,padx=10,pady=5)

        time_current_add = tk.Button(GetCPUFrame02,text=" >>  ",command=add_current)
        time_current_add.grid(row=2,column=2,padx=10,pady=5)


        cpu_consume_text_clear_button = tk.Button(GetCPUFrame05,text="      清空text      ",command=cpu_consume_cleartext)
        cpu_consume_text_clear_button.grid(row=2,column=1,pady=5)
        cpu_consume_text_clear_button.config(bg = "#3f92d6",fg="white")
        
        cpu_consume_Warning_button = tk.Button(GetCPUFrame06,text="  显示 warning 日志  ",command=OpenLogPanel)
        cpu_consume_Warning_button.grid(row=0,column=1,pady=5)
        cpu_consume_Warning_button.config(bg = "#3f92d6",fg="white")

        #cpu_consume_warning_limit_entry = tk.Entry()
        # 绑定时间到键盘离开时调用
        time_current_entry.bind("<KeyRelease>",setScalevalue)



    #显示CPU消耗情况
    global showCPU
    def showCPU(value):
        #global warningLimit
        #print("测试："+warningLimit)
        with WaapiClient() as Client:

            # 获取时间戳
            x = int(timePoint_scale.get())
            result = Get_Profiler.getCPUInf(Client,x)

            # 获取警告限值
            y = float(cpu_warning_limit_scale.get())

            if(len(result)!=0):
                cpu_consume_cleartext()
            num = len(result)
            max_cpu_eater = "None"
            max_cpu_comsume = 0
            max_cpu_num = 0


            cpu_consume_text.tag_add("type","0.0")
            cpu_consume_text.tag_config("type",foreground ="#3f92d6")

            cpu_consume_text.tag_add("type1","0.0")
            cpu_consume_text.tag_config("type1",foreground ="#0004b5")
            for _items in result:
                # print("\n第"+str(num)+"个元素：")
                cpu_consume_text.insert('0.0',str(_items["percentInclusive"])+"\n\n")
                cpu_consume_text.insert('0.0',"cpu处理时间/音频帧长度的比值为: \n","type")
                cpu_consume_text.insert('0.0',_items["elementName"]+"\n")
                cpu_consume_text.insert("0.0","\n第"+str(num)+"个元素：\n","type1")

                
                # print(_items["elementName"])
                if(_items["percentInclusive"]>max_cpu_comsume):
                    max_cpu_comsume = _items["percentInclusive"]
                    max_cpu_eater = _items["elementName"]
                    max_cpu_num = num
                current_str = ""
                if(_items["percentInclusive"]>float(y)):
                    # 加入log日志
                    if(current_str!=max_cpu_eater):

                        Log_change.write_to_log("超值警告："+"\n物体 :\n"+str(max_cpu_eater)+
                                                "\n在  "+ str(x) +" （毫秒） 处CPU处理时间/音频帧长比值为 :\n"+
                                                str(max_cpu_comsume)+"\n超出了限值 "+str(y)+
                                                "\n超出部分为 :"+str(max_cpu_comsume-y)+"\n\n\n")
                        # print("物体"+str(max_cpu_eater)+" 在 "+ str(x) +"处占用比例为"+str(max_cpu_comsume))
                        # print("\n超过了占用预警"+str(y)+"值"+str(max_cpu_comsume-y)+"\n\n")
                        current_str = max_cpu_eater

                # print(_items["percentInclusive"])
                num=num-1
            if(len(result)!=0):

                cpu_consumeMax_text.tag_add("type1","0.0")
                cpu_consumeMax_text.tag_config("type1",foreground ="#0004b5")
                cpu_consumeMax_text.tag_add("type","0.0")
                cpu_consumeMax_text.tag_config("type",foreground ="#3f92d6")
                cpu_consumeMax_text.tag_add("type2","0.0")
                cpu_consumeMax_text.tag_config("type2",foreground ="#fa4793")
                cpu_consumeMax_text.tag_add("type2","0.0")

                cpu_consumeMax_text.insert("0.0",str(max_cpu_comsume))
                cpu_consumeMax_text.insert("0.0","CPU处理时间/音频帧长度的比值为\n","type")
                cpu_consumeMax_text.insert('0.0',str(max_cpu_num)+"号元素："+str(max_cpu_eater)+"\n")
                cpu_consumeMax_text.insert('0.0',"cpu消耗比值最高的元素是:\n","type1")
                if(float(max_cpu_comsume)>float(y)):
                    # 加入log日志
                    cpu_consumeMax_text.insert('0.0',"该元素超出了限值！\n","type2")
                


    # 开始捕捉action
    global StartCapture
    def StartCapture():
        print("开始捕捉")
        
        with WaapiClient() as Client:
            try:
                bringWwise_frount(Client)
                global Capture_time_start
                Get_Profiler.startCapture(Client)
                Capture_time_start = Get_Profiler.getCursorTime(Client)
                print(Capture_time_start)
            except:
                print("开始捕捉失败")

    # 停止捕捉action
    global StopCapture

    global addWarn
    def addWarn():
        cpu_warning_limit_scale.set(cpu_warning_limit_scale.get()+float(0.01))

    global redWarn
    def redWarn():
        cpu_warning_limit_scale.set(cpu_warning_limit_scale.get()-float(0.01))

    def StopCapture():
        print("停止捕捉")

        # 输入占用提醒限值
        global cpu_warning_limit_scale
        cpu_warning_limit_scale = tk.Scale(GetCPUFrame03, label="cpu处理时间/音频帧长度警告限值",orient = tk.HORIZONTAL,
                                   from_ = 0, to =100,
                                   resolution=0.01,command = showCPU)
        cpu_warning_limit_scale.config(length=400)
        cpu_warning_limit_scale.grid(row=1,column=1)
        cpu_warning_limit_scale.set(float(100))

        cpu_warning_limit_scale_label =tk.Label(GetCPUFrame04,text=" 输入警告限值 ")
        cpu_warning_limit_scale_label.grid(row=2,column=1)
        global cpu_warning_limit_scale_entry
        cpu_warning_limit_scale_entry = tk.Entry(GetCPUFrame04)
        cpu_warning_limit_scale_entry.grid(row=3,column=1)
        cpu_warning_limit_scale_entry.bind("<KeyRelease>",setWarnScalevalue)

        cpu_warning_limit_scale_buttonAdd = tk.Button(GetCPUFrame04,text=">>",command=addWarn)
        cpu_warning_limit_scale_buttonAdd.grid(row=3,column=2)

        cpu_warning_limit_scale_buttonRed = tk.Button(GetCPUFrame04,text="<<",command=redWarn)
        cpu_warning_limit_scale_buttonRed.grid(row=3,column=0)
        
        
        #print("test:"+warningLimit)

        # 显示CPU消耗情况的text
        global cpu_consume_text
        global timePoint_scale
        #print(timePoint_scale.get())
        cpu_consume_text =tk.Text(GetCPUFrame05,width=67,height=17)
        cpu_consume_text.grid(row=0,column=1,pady=10)

        global cpu_consumeMax_text
        cpu_consumeMax_text =tk.Text(GetCPUFrame05,width=50,height=5)
        cpu_consumeMax_text.grid(row=1,column=1,pady=10)

        with WaapiClient() as Client:
            try:
                bringWwise_frount(Client)
                global Capture_time_end
                Get_Profiler.stopCapture(Client)
                Capture_time_end = Get_Profiler.getCursorTime(Client)
                # print(Capture_time_end)
                result = Get_Profiler.getCPUInf(Client)
                # pprint(result)
            except:
                pprint("结束捕捉失败")

            #进行分析
            cpu_consume_cleartext()
            num = len(result)
            max_cpu_eater = "x"
            max_cpu_comsume = 0
            max_cpu_num = 0

            cpu_consume_text.tag_add("type","0.0")
            cpu_consume_text.tag_config("type",foreground ="#3f92d6")

            cpu_consume_text.tag_add("type1","0.0")
            cpu_consume_text.tag_config("type1",foreground ="#0004b5")
            for _items in result:
                # print("\n第"+str(num)+"个元素：")
                cpu_consume_text.insert('0.0',str(_items["percentInclusive"])+"\n\n")
                cpu_consume_text.insert('0.0',"cpu处理时间/音频帧长度的比值为: \n","type")
                cpu_consume_text.insert('0.0',_items["elementName"]+"\n")
                cpu_consume_text.insert("0.0","\n第"+str(num)+"个元素：\n","type1")
                # print(_items["elementName"])
                if(_items["percentInclusive"]>max_cpu_comsume):
                    max_cpu_comsume = _items["percentInclusive"]
                    max_cpu_eater = _items["elementName"]
                    max_cpu_num = num


                # print(_items["percentInclusive"])
                num=num-1
            
            cpu_consumeMax_text.tag_add("type1","0.0")
            cpu_consumeMax_text.tag_config("type1",foreground ="#0004b5")
            cpu_consumeMax_text.tag_add("type","0.0")
            cpu_consumeMax_text.tag_config("type",foreground ="#3f92d6")

            cpu_consumeMax_text.insert("0.0",str(max_cpu_comsume))
            cpu_consumeMax_text.insert("0.0","CPU处理时间/音频帧长度的比值为\n","type")
            cpu_consumeMax_text.insert('0.0',str(max_cpu_num)+"号元素："+str(max_cpu_eater)+"\n")
            cpu_consumeMax_text.insert('0.0',"cpu消耗比值最高的元素是:\n","type1")
            # print("cpu消耗比值最高的元素是:"+str(max_cpu_num)+"号元素："+str(max_cpu_eater)+"\n")
            # print("\nCPU处理时间/音频帧长度的比值为:"+str(max_cpu_comsume))

        show_scale()
    
    global setWarnScalevalue
    def setWarnScalevalue(event):
        #print("通过输入修改了数值")
        cpu_warning_limit_scale.set(float(cpu_warning_limit_scale_entry.get()))
    #清空text
    global cpu_consume_cleartext
    def cpu_consume_cleartext():
        cpu_consume_text.delete("1.0","end")
        cpu_consumeMax_text.delete("1.0","end")

#log面板页面
class OpenLogUI:
    def __init__(self,_Tkroot):

        self._Tkroot = _Tkroot
        self._Tkroot.title("CPU警告LOG  ( 内容存放在Log_File中 )")
        self._Tkroot.geometry("520x520")

        self.LogUI_frame = tk.Frame(_Tkroot)
        self.LogUI_frame.pack(pady=5)

        self.LogUI_frame2 = tk.Frame(_Tkroot)
        self.LogUI_frame2.pack(pady=5)

        self.LogUI_Label = tk.Label(self.LogUI_frame,text=" CPU超值警告log如下:"+"\n"+"建议到快速查询中找到id进行定位并查找原因")
        self.LogUI_Label.config(fg="#c60653")
        self.LogUI_Label.grid(row=0,column=0,padx=5)
        
        global LogUIText
        LogUIText = tk.Text(self.LogUI_frame2,width=70,height=30)
        LogUIText.grid(row = 0,column=0,padx=5)
        readLogText()

        self.clearLogTextButton = tk.Button(self.LogUI_frame2,text="    清空Log_Text    ",command=clearLogText)
        self.clearLogTextButton.grid(row=1,column=0,pady=10)
        self.clearLogTextButton.config(bg="#3f92d6",fg="white")


    global readLogText
    def readLogText():
        result = Log_change.read_log()
        for line in result:
            LogUIText.insert("end",str(line)+"\n")

    global clearLogText
    def clearLogText():
        #清空log
        LogUIText.delete("0.0","end")
        Log_change.clear_log()

if __name__=="__main__":
    Tkroot = tk.Tk()
    UITry = MenuUI(Tkroot)
    Tkroot.mainloop()

    