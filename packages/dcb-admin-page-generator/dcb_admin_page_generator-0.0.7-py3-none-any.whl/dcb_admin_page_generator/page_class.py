import time
import requests
import re
import os
import sys
from .funcs import *
from .common_class import ZYapi

here = os.path.dirname(os.path.abspath(__file__))


def read_template(file_type):
    if file_type == 'list':
        with open(f'{here}\\template\\list.vue', encoding='utf8') as f:
            text = f.read()
        return text
    elif file_type == 'add':
        with open(f'{here}\\template\\add_or_edit.vue', encoding='utf8') as f:
            text = f.read()
        return text
    elif file_type == 'dialog_add':
        with open(f'{here}\\template\\dialog_add_or_edit.vue', encoding='utf8') as f:
            text = f.read()
        return text
    elif file_type == 'dialog_list':
        with open(f'{here}\\template\\dialog_list.vue', encoding='utf8') as f:
            text = f.read()
        return text
    else:
        return ''


class GenerateList(object):
    def __init__(self, config, generator_title, file_path, generator_type):
        self.type = generator_type
        self.title = generator_title
        self.config = config
        # self.YapiURL = {'getData': {'url': ''}}
        self.getDataYapi = ZYapi(get_user_input('请输入获取数据YapiURL(直接按回车使用默认数据)'), 'list')
        self.addYapi = False
        self.detailYapi = False
        need_add = get_user_input('请输入新增数据接口(直接按回车不需要新增,输入d使用默认数据)')
        if need_add:
            self.addYapi = ZYapi(need_add, 'add')
        need_detail = get_user_input('请输入详情数据接口(直接按回车不需要详情,输入d使用默认数据)')
        if need_detail:
            self.detailYapi = ZYapi(need_add, 'add')
        self.Operate = get_user_input('输入列表页面操作函数名以、分割(不需要请直接按回车)')

    def generate(self):
        text = read_template(self.type)
        #  处理获取数据入参

        data_config = self.getDataYapi.get_yapi_config(self.config)
        add_config = self.addYapi.get_yapi_config(self.config) if self.addYapi else False
        detail_config = self.detailYapi.get_yapi_config(self.config) if self.detailYapi else False

        text = text.replace('fitter: [],', f'fitter: {data_config["resp_body_other"]},')
        #  是否需要Operate
        if self.Operate:
            operate_list = self.Operate.split('、')
            table_operation_list = [f"tp['{func}']" for func in operate_list]
            # 查看详情: { text: '查看详情', icon: 'el-icon-edit-outline', func: this.detail, authority: '' },
            op_dict = {}
            op_name_list = []
            for index in range(len(operate_list)):
                # print(op)
                s1 = translate(operate_list[index])
                s2 = convert(s1, ' ')
                op_name_list.append(s2)
                op_dict[operate_list[index]] = {'text': operate_list[index], 'icon': 'el-icon-edit-outline',
                                                'func': f'this.{op_name_list[-1]}', 'authority': ''}
                time.sleep(0.5)
            text = text.replace('tp = {}', f'tp={op_dict};'.replace("'this", 'this').replace("', 'aut", ",'aut"))
            text = text.replace('默认: []', f'默认:{table_operation_list}'.replace("\"", ''))
            for func in op_name_list:
                text = text.replace('// 函数填充', f'{func}(row)' + "{}," + '\n' + '    // 函数填充')
            data_config['resp_body'].append(
                {'prop': 'op', 'label': '操作', 'type': 'op', 'data': [], 'options': {'tableOperationList': []}}, )
        else:
            pass
        text = text.replace('table_option: [],', f'table_option: {data_config["resp_body"]},')
        if add_config:
            text = text.replace('// Api writePlace', "import { " + data_config["resp_query_path"] + "," + add_config[
                "resp_query_path"] + " } from '@/generated_api';")
        else:
            text = text.replace('// Api writePlace', "import { " + data_config["resp_query_path"] + "} from "
                                                                                                    "'@/generated_api';")
        text = text.replace('SOMEFUNCS_LIST', f'{data_config["resp_query_path"]}')
        text = text.replace('抽奖活动管理', f'{self.title}')
        # 处理新增的
        if self.addYapi:
            text = text.replace('change_active_info: []', f'change_active_info: {add_config["resp_body_other"]}')
            text = text.replace('SOMETHING_SUBMIT', f'{add_config["resp_query_path"]}')
            text = text.replace('<!--  model_update  -->', '''
                                <z_dialog_form
                                 v-if="change_edit_visible" :visible="change_edit_visible"
                                 width="60%" v-model="change_active_info" :filed-width="'500px'" label-width="120px"
                                 @finish="changeFinish"
                                 @update:visible="(val)=>{
                                 change_edit_visible = val
                                 changeActiveInfoReset()
                                 }"/>
                                 <!--  model_update  -->
                                 ''')
        if self.detailYapi:
            text = text.replace('', '')

        return text


class GenerateAdd(object):
    def __init__(self, config, generator_title, file_path, generator_type):
        self.type = generator_type
        self.title = generator_title
        self.config = config
        self.submitDataYapi = ZYapi(get_user_input('请输入保存或创建条目的YapiURL(直接按回车使用默认数据)'), 'add')

        # self.Title = config['generator_title']
        # self.Path = deal_path(config['resp_query_path'])
        # self.InP = sort_p(deal_p(config['resp_body_other'], 'edit', need_req=True))
        # self.Type = config['object_type']
        # self.FilePath = config['file_path']
        # # print('self.InP', self.InP)

    def get_p(self):
        pass
        # print('入参', self.InP)
        # return self.InP

    def generate(self):
        # pass
        text = read_template(self.type)
        data_config = self.submitDataYapi.get_yapi_config(self.config)
        text = text.replace('change_active_info: []', f'change_active_info: {data_config["resp_body_other"]}')
        text = text.replace('// Api writePlace',
                            "import { " + data_config["resp_query_path"] + " } from '@/generated_api';")
        text = text.replace('SOMETHING_SUBMIT', f'{data_config["resp_query_path"]}')
        text = text.replace('抽奖活动管理', f'{self.title}')
        return text
