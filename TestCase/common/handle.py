import requests
import re
import json
import demjson
from TestCase.common import data_read


class Handle:
    # 将初始值以及接口返回中后续接口会用到的字段值添加到全局变量中
    def set_global(self, data):
        yaml_data = data_read.get_yaml()
        if yaml_data is None:
            yaml_data = data
        else:
            yaml_data.update(data)
        data_read.set_yaml(yaml_data)

    # 处理前置setup
    def handle_setup(self):
        pass

    # 处理后置teardown，从接口返回中获取参数值，并保存参数到全局变量中
    def handle_teardown(self, teardown, res_content):
        # json.loads将str类型转化为dict类型
        self.teardown = json.loads(teardown)
        # print("teardown值： %s && type: %s" % (self.teardown, type(self.teardown)))
        self.response = json.loads(res_content)
        teardown_dict = {}
        # 判断返回值类型是list还是dict
        if isinstance(self.response, list):
            for i in self.teardown.keys():
                res_value = self.response[int(i)]
                t_value = self.teardown[i]
                for keys in t_value.keys():
                    teardown_dict[t_value[keys]] = res_value[keys]
        else:
            for i in self.teardown.keys():
                value = self.response[i]
                if isinstance(self.teardown[i], dict):
                    # 这里考虑teardown[i]的值仍是字典的情况，类似{"Entities":{"0":{"Id":"PatientId"}}}
                    for a in self.teardown[i].keys():
                        # 这里考虑value是个列表的情况，类似如下
                        # {"Entities": [{"Id": "11", "LoginAccount": "22"}, {"Id": "33", "LoginAccount": "44"}]}
                        if isinstance(value, list):
                            value2 = value[int(a)]
                            aa = self.teardown[i][a]
                            for aaa in aa.keys():
                                b = aa[aaa]
                                teardown_dict[b] = value2[aaa]
                        elif isinstance(value, dict):
                            value2 = value[a]
                            key = self.teardown[i][a]
                            teardown_dict[key] = value2
                else:
                    key = self.teardown[i]
                    teardown_dict[key] = value
        self.set_global(teardown_dict)

    # 提交接口请求
    def handle_request(self, method, url, param, header=None):
        res = ""
        if method == "post":
            if header == "":
                res = requests.post(url, data=param)
            else:
                res = requests.post(url, json=param, headers=header)
        elif method == "get":
            res = requests.get(url, headers=header)
        elif method == "put":
            res = requests.put(url, json=param, headers=header)

        return res.status_code, res.content, res.headers

    # 处理result中参数
    def handle_result(self, data):
        if "{" in data:
            result = re.findall('{(.*?)}', data)
            for i in result:
                yamldata = data_read.get_yaml()
                h = data.replace("{" + i + "}", '"' + yamldata[i] + '"')
                data = h
            return demjson.decode(data)

    # 处理param中参数
    def handle_param(self, data):
        if "{" in data:
            param = re.findall('{(.*?)}', data)  # 正则匹配出参数，结果为list类型

            for i in param:
                # 将data中各个参数替换成yaml中对应的值
                yamldata = data_read.get_yaml()
                b = data.replace("{"+i+"}", '"'+yamldata[i]+'"')
                data = b
        # print("handle_param_data: %s && type(data):%s" % (data, type(data)))
        return demjson.decode(data)

    # 处理url中参数
    def handle_url(self, data):
        if "{" in data:
            param = re.findall('{(.*?)}', data)  # 正则匹配出参数
            for i in param:
                yamldata = data_read.get_yaml()
                u = data.replace("{"+i+"}", yamldata[i])
                data = u
        return data

    # 处理前置header
    def handle_header(self, header):
        self.handle_head_name = header
        if self.handle_head_name == "admin_header":
            self.header = self.get_header("admin_token")
        elif self.handle_head_name == "user_header":
            self.header = self.get_header("user_token")
        elif self.handle_head_name == "doctor_header":
            self.header = self.get_header("doctor_token")
        elif self.handle_head_name == "check_header":
            self.header = self.get_header("check_token")

        return self.header

    # 组合header，返回header
    def get_header(self, key):
        yamldata = data_read.get_yaml()
        token = yamldata[key]
        header = "{'token': '%s'}" % token
        return demjson.decode(header)


