from waapi import WaapiClient
from tkinter import filedialog #用于选择文件选择
from findOBJinPE import find_Obj_inPE #在wwise的pe中选中对象
import os

#选择文件函数
def SelectFile():
        print("选择文件")
        global selected_audio_files
        audio_files = filedialog.askopenfilenames(filetypes=[("WAV Files","*.wav")])
        selected_audio_files = audio_files

#进行文件导入后端
def waapi_import_file(Client:WaapiClient,_work_unit_name:str,_Import_Actor_mixer:str,_container_type:str,
                _container_name:str,_sound_type:str):
        imports = []
        for i,audio_file in enumerate(selected_audio_files,start=1):
            object_path = f"\\Actor-Mixer Hierarchy\\<WorkUnit>{_work_unit_name}\\<Actor-Mixer>{_Import_Actor_mixer}\\<{_container_type}>{_container_name}\\<Sound>{_sound_type}_{_container_name}_{i:02}"
            audio_file_path = os.path.abspath(audio_file)
            import_data = {
                    'objectPath':object_path,
                    'audioFile':audio_file_path,
                    '@Volume':0,
                }
            imports.append(import_data)

        args = {
                "importOperation":"createNew",
                "default":{
                    "importLanguage": _sound_type
                },
                "imports":imports
            }

        try:
            result = Client.call("ak.wwise.core.audio.import",args)
            print("音频文件导入成功")
            global inports_obj_ids
            inports_obj_ids = []
            for _items in result["objects"]:
                #print(_items["id"])
                inports_obj_ids.append(_items["id"])
            print(inports_obj_ids)
            # 完成后Wwise中PE选中        
            find_Obj_inPE(Client,inports_obj_ids)
            inports_obj_ids.clear()
            # locate_OBJ()
        except Exception as e:
            print("导入时出现异常",e)