# openapi_test_demo

#### 介绍
openapi自动化测试框架

#### 软件架构
python + requests + pytest + parametrize + json / http、https + allure + mysql + log
接口自动化测试框架

#### 目录结构

    |--openapi自动化测试框架 # 主目录
       ├─ api # 封装api,用于test调用
         └─ http_base_manager.py  # http连接管理工具
         └─ xxx.py  # 接口封装
       ├─ common # 常用工具
         └─ mysql_utils.py  # mysql连接的封装
         └─ read_json.py  # 封装测试case的json文件数据读取
         └─ render_template.py  # 渲染配置文件
         └─ template.conf  # 模板文件
       ├─ config # 配置文件读取
         └─ config.ini  # 配置文件
         └─ confRead.py   # 封装读取配置文件，可修改代码中的配置文件名字
       ├─ data # 测试数据相关文件
         └─ xxx.json # test测试数据
         └─ xxx.json # test测试数据
       ├─ log # 日志
         └─ xxx.log # 日志记录
       ├─ pytest_html # pytest_html 测试报告
         └─ report.html # 报告
       ├─ report # allure测试报告目录
         └─ index.html # allure测试报告
       ├─ scripts # 测试脚本调用
         └─ conftest.py # 运行用例前置、后置配置、配置全局日志、自动生成allure测试报告
         └─ test_xxx.py # 运行的用例
         └─ zzz.py # 一键生成 api test调用脚本
       ├─ tmp # allure运行时数据、截图等
         └─ xxx.json # 运行的数据
       ├─ Dockerfile	  # dockerfile 镜像构建
       ├─ global_config.py	  # 公用log日志封装
       ├─ pytest.ini  	# pytest配置	  
       └─ README.md

#### 使用说明
根据需要,根据模版生成config配置文件,可直接修改confRead.py 中 config.ini 运行其它测试环境
```
cd cd .\common\
python render_template.py template.conf test_env.json ../config/config.ini
```

生成pytest-html测试报告
```
pytest -v -m 'nj' --html=./pytest_html/report.html --self-contained-html
```

执行只生成allure测试报告
```
pytest -v -m 'nj'
```

docker 镜像构建，修改Dockerfile FROM 地址。在项目根目录 执行 

```docker build -t openapi_base .```