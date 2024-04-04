from waapi import WaapiClient
# 返回搜索值
# 参数：client,搜索名，选择返回的包含物，选择返回的层级关系（默认为空，即返回自己）
def waapi_check_AllOBJ(Client:WaapiClient,_aimName:list,_selected_options_to_return:list,_selected_result_to_return = None):
    
    # 父子级的重载判断：
    if _selected_result_to_return!=None:
        arg = {
                'from':{'search':_aimName},
                'transform':[
                        #选择哪些内容：parent  children  descendants  ancestors
                        {'select':_selected_result_to_return},
                        #符合哪些条件： name:contains  name:matches  type:isIn  category:isIn
                        #{'where':['name:contains',imformation_Obj_name_entry.get()]}#包含哪些字符
                    ]
                }
        
    else:
        arg = {
                    'from':{'search':_aimName},
                    'transform':[
                        #选择哪些内容：parent  children  descendants  ancestors
                        #{'select':_selected_result_to_return},
                        #符合哪些条件： name:contains  name:matches  type:isIn  category:isIn
                        #{'where':['name:contains',imformation_Obj_name_entry.get()]}#包含哪些字符
                        ]
                }
        
    Myoptions = {
                    'return':_selected_options_to_return
                }
    result = Client.call('ak.wwise.core.object.get',arg,options = Myoptions)
    return result



# 返回类型筛选值
# 参数：client,目标类型，目标名字，选择返回的包含物，选择返回的层级关系（默认为空，即返回自己）
def waapi_check_ofTypeClient(Client:WaapiClient,_aim_type:list,_aimName,_selected_options_to_return:list,_selected_result_to_return = None):
    # 父子级的重载判断：
    if _selected_result_to_return!=None:
        arg = {
                    'from':{'ofType':_aim_type},
                    'transform':[
                        #选择哪些内容：parent  children  descendants  ancestors
                        {'select':_selected_result_to_return},
                        #符合哪些条件： name:contains  name:matches  type:isIn  category:isIn
                        {'where':['name:contains',_aimName]}#包含哪些字符
                    ]
                }
        
    else:
        arg = {
                    'from':{'ofType':_aim_type},
                    'transform':[
                        #选择哪些内容：parent  children  descendants  ancestors
                        #{'select':_selected_result_to_return},
                        #符合哪些条件： name:contains  name:matches  type:isIn  category:isIn
                        {'where':['name:contains',_aimName]}#包含哪些字符
                    ]
                }
        
    Myoptions = {
                    'return':_selected_options_to_return
                }
    result = Client.call('ak.wwise.core.object.get',arg,options = Myoptions)
    return result





