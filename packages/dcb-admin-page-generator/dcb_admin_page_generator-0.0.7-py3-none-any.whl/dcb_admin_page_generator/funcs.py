import requests


def get_user_input(placeholder):
    res = input(f'{placeholder}\n')
    return res


#  字符串驼峰命名
def convert(one_string, space_character):
    string_list = str(one_string).split(space_character)  # 将字符串转化为list
    first = string_list[0].lower()
    others = string_list[1:]
    others_capital = [f'{word[0].capitalize()}{word[1:]}' for word in others]  # str.capitalize():将字符串的首字母转化为大写
    others_capital[0:0] = [first]
    hump_string = ''.join(others_capital)  # 将list组合成为字符串，中间无连接符。
    return hump_string


#  list排序
def sort_p(s_arr):
    print('intP', [f'{index}、{s_arr[index]["label"]}' for index in range(len(s_arr))])
    is_sort = input('输入调整后的参数顺序以,或、分割（不需要请直接按回车）')
    if is_sort:
        # print(is_sort.split(','))
        return [s_arr[int(index)] for index in is_sort.split(',' if ',' in is_sort else '、')]
    else:
        return s_arr


# 翻译
def translate(string):
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'i': string
    }
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url, params=data)
    result = r.json()
    try:
        return result['translateResult'][0][0]['tgt']
    except:
        return False
