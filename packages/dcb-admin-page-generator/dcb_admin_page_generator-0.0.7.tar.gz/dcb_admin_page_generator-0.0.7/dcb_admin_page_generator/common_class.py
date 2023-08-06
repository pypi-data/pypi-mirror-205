from .funcs import *
import json
from .config import template_data
import re


def deal_path(path):
    print(path["path"])
    return convert(f'api{path["path"]}', '/')


def label_format(label, prop):
    label_arr = label.split(' ')
    label_arr = label_arr[0]
    label_arr = label_arr.split('：')
    return label_arr[0]


def type_format(p_type, ele_type, desc, prop):
    # print('desc',desc)
    img_arr = ['图']
    type_arr = ['状态', '类型']
    type_arr_en = ['Status', 'status', 'Type', 'type']
    fitter_type_arr = ['名称']
    if p_type == 'edit':
        type_dict = {'string': 'input', 'number': 'price', 'integer': 'num'}
        if any(x in desc for x in img_arr):
            return 'img'
        elif any(x in desc for x in type_arr) or any(x in prop for x in type_arr_en) and not any(x in desc for x in fitter_type_arr):
            return 'select'
        else:
            return type_dict[ele_type] if ele_type in type_dict else ele_type
    elif p_type == 'show':
        type_dict = {'string': 'str', 'number': 'str', 'integer': 'str'}
        if any(x in desc for x in img_arr):
            return 'img_s'
        elif any(x in desc for x in type_arr) or any(x in prop for x in type_arr_en) and not any(x in desc for x in fitter_type_arr):
            return 'dict'
        else:
            return type_dict[ele_type] if ele_type in type_dict else ele_type


def deal_type_str(s, default_label):
    s = s.replace('=', '')
    print('s',s)
    number = re.findall('(-?\d+)-?', s)
    print('number',number)
    s = s.split(number[0], 1)
    # print('s',s)

    if s[0] != '':
        # print('step1', s[0])
        label = s[0].replace(':', '').replace('：', '').replace('-', '')
    else:
        # print('step2', s[0])
        label = default_label
    res = []
    res_dict = {}
    # print('number', number)
    for index in range(1, len(number)):
        # print('s1', s[1])
        # print('number[index]', number[index])
        s = s[1].split(number[index])
        res.append({'key': number[index-1], 'value': s[0].replace('，', '').replace('-', '').replace('、', '')})
        res_dict[number[index-1]] = s[0].replace('-', '').replace('、', '')
        if index == len(number) - 1:
            res.append({'key': number[index], 'value': s[1].replace('，', '').replace('-', '').replace('、', '')})
            res_dict[number[index]] = s[1].replace('-', '').replace('、', '')

    return label, res, res_dict


def deal_with_parameter(data, p_type, need_req=False):
    resp = []
    for ele in data:
        if data[ele]['type'] != 'object' and data[ele]['type'] != 'array' and ele != 'pageIndex' and ele != 'pageSize':
            temp_dict = []
            res_dict = {}
            print('ele',data[ele])
            temp_type = type_format(p_type, data[ele]['type'], data[ele]['description'],ele)
            #  判断特殊类型
            if temp_type == 'dict' or temp_type == 'select':
                print("(data[ele]['description']", (data[ele]['description']))
                try:
                    temp_label, temp_dict, res_dict = deal_type_str(data[ele]['description'],ele)
                except:
                    temp_label = label_format(data[ele]['description'], ele)
                    temp_type = 'str' if p_type == 'show' else 'input'
            else:
                temp_label = label_format(data[ele]['description'], ele)
            #  生成template
            if p_type == 'edit':
                if need_req:
                    resp.append({'prop': ele, 'type': temp_type, 'label': temp_label, 'value': '',
                                 'data': temp_dict, 'options': {}, 'verification': 'req'})
                else:
                    resp.append({'prop': ele, 'type': temp_type, 'label': temp_label, 'value': '',
                                 'data': temp_dict, 'options': {}})
            else:
                if len(temp_dict):
                    resp.append({'prop': ele, 'type': temp_type, 'label': temp_label, 'value': '',
                                 'data': [], 'options': {'dict': res_dict}})
                else:
                    resp.append({'prop': ele, 'type': temp_type, 'label': temp_label, 'value': '',
                                 'data': [], 'options': {}})
    return resp


class ZYapi(object):
    def __init__(self, url, yapi_type):
        self.GenerateConfig = None
        self.url = url
        self.type = yapi_type
        self.token = None
        self.id = None

    def get_id(self, string, config):
        split_arr = string.split('/')
        if len(split_arr) > 4:
            api_id = split_arr[-1]
            project_id = int(split_arr[4])
            if project_id in config['projects']['token']:
                self.id = api_id
                self.token = config['projects']['token'][project_id]
                return {"id": api_id, "token": config['projects']['token'][project_id]}
            else:
                token = input('请输入token')
                self.id = api_id
                self.token = token
                return {"id": api_id, "token": token}
        else:
            return False

    def get_yapi_config(self, configuration):
        # print('file_path', file_path)
        # yapi_url = get_user_input('请输入获取数据的YapiURL(默认配置直接敲回车)')
        if 'http' in self.url:
            id_dict = self.get_id(self.url, configuration)
            resp = requests.get(f'{configuration["serverUrl"]}{configuration["getInfoPath"]}', params=id_dict)
            resp_text = json.loads(resp.text)
        else:
            resp_text = template_data[self.type]
        resp_query_path = deal_path(resp_text["data"]["query_path"])
        resp_body_other = json.loads(resp_text["data"]["req_body_other"])['properties']
        resp_body = []
        if self.type == 'list':
            resp_body = json.loads(resp_text["data"]["res_body"])['properties']
            resp_body = resp_body['data']['properties']['list']['items']['properties']
            # print('res_body',resp_body)
            # for key in resp_body:
            #     if key in resp_body_other:
            #         resp_body[]
        diff_arr = list(set([key for key in resp_body_other]) & set([key for key in resp_body]))
        for key in diff_arr:
            if len(resp_body_other[key]['description']) > len(resp_body[key]['description']):
                resp_body[key]['description'] = resp_body_other[key]['description']
            else:
                resp_body_other[key]['description'] = resp_body[key]['description']

        resp_body = sort_p(deal_with_parameter(resp_body, 'show'))
        resp_body_other = sort_p(deal_with_parameter(resp_body_other, 'edit'))

        generate_config = {
            'resp_query_path': resp_query_path,
            'resp_body_other': resp_body_other,
            'resp_body': resp_body,
        }
        self.GenerateConfig = generate_config
        return generate_config
