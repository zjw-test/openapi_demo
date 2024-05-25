import re

# 填写以下内容
vm_name = "NJ"
api_name = "nj_search"
describe = "通过查询参数获取相关的脑筋急转弯"
port = "GET"
ur = "riddle/brain/search"

# 请求参数
par = """
question	[string]		问题中包含查询参数的相关搞笑谜语
answer	[string]		答案中包含查询参数的相关搞笑谜语
search_type	[string]	是	需要查询的字段（question或者answer）
page	[string]		当前的页码符号
page_size	[string]		一页显示多少条数据(默认返回5条，最大显示20条)
"""


def to_snake_case(name):
    snake = ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')
    return snake


filters_name_a = "nodeType"
filters_name_b = "shareType"

# 将字符串转换为行的列表
lines = par.strip().split('\n')

# 将每一行分割为单词，并转换为小驼峰命名
output_dict = {}
for line in lines:
    # 提取每行的第一个单词
    word = line.split()[0]
    snake_case_word = to_snake_case(word)
    # 将原始单词和转换后的单词作为键值对添加到字典中
    output_dict[word] = snake_case_word

# 输出结果
# print("{")
# for k, v in output_dict.items():
#     print(f'  "{k}": {v},')
# print("}")
result = "{\n     "
for k, v in output_dict.items():
    result += f' "{k}": {v},\n     '
result += "}"

# print(result)
values = list(output_dict.values())
parameter = ', '.join(str(value) for value in values)
# print(parameter)

# 命名转小写下划线分隔

file_name = '_'.join([word.lower() for word in re.findall('[a-zA-Z][^A-Z]*', vm_name)])
vm = file_name + "_" + "manager"

variable_name = '_'.join([word.lower() for word in re.findall('[a-zA-Z][^A-Z]*', api_name)])
# print(variable_name)

post_api = f"""
def {variable_name}(self, data):
    \"\"\"{describe}\"\"\"
    logging.info("starting to {variable_name}")
    uri = "/{{0}}/regions/{{1}}/{ur}".format(self.apiversion, self.regionId)
    ret_code, ret_data = self.http_request(uri, "{port}", data)
    if ret_code == 200:
        return ret_code, ret_data
    logging.warning("{variable_name} failed! ret_code:{{0}}, ret_data:{{1}}".format(ret_code, ret_data))
    return ret_code, ret_data
"""
post_req = f"""
@pytest.mark.smoke
@pytest.mark.parametrize("{parameter}",
                             read_json("{file_name}.json", "{variable_name}"),
                             ids=read_json_title("{file_name}.json", "{variable_name}"))
def test_{variable_name}(self, {vm}, {parameter}):
    \"\"\"{describe}\"\"\"
    logging.info("starting test case test_{variable_name}")
    output_dict = {result}
    ret_code, ret_data = {vm}.{variable_name}(output_dict)
    assert ret_code == 200
    assert ret_data["result"]["commandTypeEnum"] == "CUSTOM"
    assert ret_data["result"]["schemaNames"]
    logging.info("test case test_{variable_name} success")
"""

get_api = f"""
def {variable_name}(self, params):
    \"\"\"{describe}\"\"\"
    logging.info("starting to {variable_name}")
    uri = "/{{0}}/regions/{{1}}/{ur}".format(self.apiversion, self.regionId)
    data = json.dumps(data)
    new_params = {{k: v for k, v in params.items() if v is not None}}
    query_string = urllib.parse.urlencode(new_params)
    new_uri = uri + "?" + query_string
    ret_code, ret_data = self.http_request(new_uri, "GET")
    if ret_code == 200:
        return ret_code, ret_data
    logging.warning("{variable_name} failed! ret_code:{{0}}, ret_data:{{1}}".format(ret_code, ret_data))
    return ret_code, ret_data

"""
get_req = f"""
@pytest.mark.smoke
@pytest.mark.parametrize("{parameter}",
                             read_json("{file_name}.json", "{variable_name}"),
                             ids=read_json_title("{file_name}.json", "{variable_name}"))
def test_{variable_name}(self, {vm}, {parameter}):
    \"\"\"{describe}\"\"\"
    logging.info("starting test case test_{variable_name}")
    params = {result}
    ret_code, ret_data = {vm}.{variable_name}(params)
    assert ret_code == 200
    assert ret_data["result"]["isMaster"]
    assert ret_data["result"]["username"]
    assert ret_data["result"]["pin"]
    logging.info("test case test_{variable_name} success")
"""

if port == "POST":
    print("已生成测试代码 post api、request")
    print(post_api)
    print(post_req)
else:
    print("已生成测试代码 get api、request")
    print(get_api)
    print(get_req)
