# 详细说明安装相关事宜
## pip包安装 django pymysql
(.venv) PS D:\workspace\GOAMAS> pip freeze
(.venv) PS D:\workspace\GOAMAS>
(.venv) PS D:\workspace\GOAMAS> pip install django
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting django
  Using cached https://mirrors.aliyun.com/pypi/packages/9d/6e/98a1d23648e0085bb5825326af17612ecd8fc76be0ce96ea4dc35e17b926/django-5.2.5-py3-none-any.whl (8.3 MB)
Collecting asgiref>=3.8.1 (from django)
  Using cached https://mirrors.aliyun.com/pypi/packages/7c/3c/0464dcada90d5da0e71018c04a140ad6349558afb30b3051b4264cc5b965/asgiref-3.9.1-py3-none-any.whl (23 kB)
Collecting sqlparse>=0.3.1 (from django)
  Downloading https://mirrors.aliyun.com/pypi/packages/a9/5c/bfd6bd0bf979426d405cc6e71eceb8701b148b16c21d2dc3c261efc61c7b/sqlparse-0.5.3-py3-none-any.whl (44 kB)
Collecting tzdata (from django)
  Downloading https://mirrors.aliyun.com/pypi/packages/5c/23/c7abc0ca0a1526a0774eca151daeb8de62ec457e77262b66b359c3c7679e/tzdata-2025.2-py2.py3-none-any.whl (347 kB)
Installing collected packages: tzdata, sqlparse, asgiref, django
Successfully installed asgiref-3.9.1 django-5.2.5 sqlparse-0.5.3 tzdata-2025.2

[notice] A new release of pip is available: 25.1.1 -> 25.2
[notice] To update, run: python.exe -m pip install --upgrade pip
(.venv) PS D:\workspace\GOAMAS> pip freeze ^C
(.venv) PS D:\workspace\GOAMAS> python.exe -m pip install --upgrade pip
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Requirement already satisfied: pip in d:\workspace\goamas\.venv\lib\site-packages (25.1.1)
Collecting pip
  Using cached https://mirrors.aliyun.com/pypi/packages/b7/3f/945ef7ab14dc4f9d7f40288d2df998d1837ee0888ec3659c813487572faa/pip-25.2-py3-none-any.whl (1.8 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 25.1.1
    Uninstalling pip-25.1.1:
      Successfully uninstalled pip-25.1.1
Successfully installed pip-25.2

(.venv) PS D:\workspace\GOAMAS> pip install pymysql
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting pymysql
  Downloading https://mirrors.aliyun.com/pypi/packages/7c/4c/ad33b92b9864cbde84f259d5df035a6447f91891f5be77788e2a3892bce3/pymysql-1.1.2-py3-none-any.whl (45 kB)
Installing collected packages: pymysql

## 在settings.py里配置好mysql数据库配置
1、goamas/__init__.py
import pymysql
pymysql.install_as_MySQLdb()
2、.gitignore
.env
3、在settings.py同目录创建.env文件,内容例如：
DB_NAME=GOAMAS
DB_USER=test1
DB_PASSWORD=test1
DB_HOST=2.2.2.2
DB_PORT=3306
3、pip install  python-decouple
(.venv) PS D:\workspace\GOAMAS\goamas> pip install python-decouple
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting python-decouple
  Downloading https://mirrors.aliyun.com/pypi/packages/a2/d4/9193206c4563ec771faf2ccf54815ca7918529fe81f6adb22ee6d0e06622/python_decouple-3.8-py3-none-any.whl (9.9 kB)
Installing collected packages: python-decouple
Successfully installed python-decouple-3.8

4、settings.py

from decouple import config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Django 用 mysql 引擎
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
## 创建 project
django-admin createproject goamas
#配置好settings.py
(.venv) PS D:\workspace\GOAMAS\goamas> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
(.venv) PS D:\workspace\GOAMAS\goamas>

## 创建超级用户
(.venv) PS D:\workspace\GOAMAS\goamas> python manage.py createsuperuser
用户名 (leave blank to use 'ye'): admin
电子邮件地址:
Password:
Password (again):
Superuser created successfully

# django连接测试

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
September 01, 2025 - 16:40:53
Django version 5.2.5, using settings 'goamas.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/5.2/howto/deployment/

# 安装基础包 1 simplepro
(.venv) PS D:\workspace\GOAMAS\goamas> pip install simplepro
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting simplepro
  Downloading https://mirrors.aliyun.com/pypi/packages/b2/aa/50eeb82453e6f7ae633e9719b21e9ee36248e2b9d7d680a6864031e57ef7/simplepro-7.20.tar.gz (18.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 18.0/18.0 MB 12.3 MB/s  0:00:01                                                                                                                                                       
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Requirement already satisfied: django>=2.1 in d:\workspace\goamas\.venv\lib\site-packages (from simplepro) (5.2.5)
Collecting django-simpleui>=2025.05.16 (from simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/97/d7/57ac337258399c33c28b5d960407e2c640f22a2edabf2e894d1b51e25fee/django-simpleui-2025.6.24.tar.gz (6.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.5/6.5 MB 12.0 MB/s  0:00:00                                                                                                                                                         
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting django-import-export (from simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/33/20/8502f3985b91befb3e771c258b7e2a3fa916bdb834e960da307ecc359d66/django_import_export-4.3.9-py3-none-any.whl (148 kB)
Collecting requests (from simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/1e/db/4254e3eabe8020b458f1a747140d32277ec7a271daf1d235b70dc0b4e6e3/requests-2.32.5-py3-none-any.whl (64 kB)
Collecting rsa (from simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/64/8d/0133e4eb4beed9e425d9a98ed6e081a55d195481b7632472be1af08d2f6b/rsa-4.9.1-py3-none-any.whl (34 kB)
Collecting psutil (from simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/50/1b/6921afe68c74868b4c9fa424dad3be35b095e16687989ebbb50ce4fceb7c/psutil-7.0.0-cp37-abi3-win_amd64.whl (244 kB)
Collecting pillow (from simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/23/85/397c73524e0cd212067e0c969aa245b01d50183439550d24d9f55781b776/pillow-11.3.0-cp313-cp313-win_amd64.whl (7.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.0/7.0 MB 11.8 MB/s  0:00:00                                                                                                                                                         
Requirement already satisfied: asgiref>=3.8.1 in d:\workspace\goamas\.venv\lib\site-packages (from django>=2.1->simplepro) (3.9.1)
Requirement already satisfied: sqlparse>=0.3.1 in d:\workspace\goamas\.venv\lib\site-packages (from django>=2.1->simplepro) (0.5.3)
Requirement already satisfied: tzdata in d:\workspace\goamas\.venv\lib\site-packages (from django>=2.1->simplepro) (2025.2)
Collecting diff-match-patch==20241021 (from django-import-export->simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/f7/bb/2aa9b46a01197398b901e458974c20ed107935c26e44e37ad5b0e5511e44/diff_match_patch-20241021-py3-none-any.whl (43 kB)
Collecting tablib>=3.7.0 (from django-import-export->simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/5c/95/6542f54ebd90539b12ed6189cb54a6550a28407b1c503c2e55190c29a4c9/tablib-3.8.0-py3-none-any.whl (47 kB)
Collecting charset_normalizer<4,>=2 (from requests->simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/9a/8f/ae790790c7b64f925e5c953b924aaa42a243fb778fed9e41f147b2a5715a/charset_normalizer-3.4.3-cp313-cp313-win_amd64.whl (107 kB)
Collecting idna<4,>=2.5 (from requests->simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/76/c6/c88e154df9c4e1a2a66ccf0005a88dfb2650c1dffb6f5ce603dfbd452ce3/idna-3.10-py3-none-any.whl (70 kB)
Collecting urllib3<3,>=1.21.1 (from requests->simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/a7/c2/fe1e52489ae3122415c51f387e221dd0773709bad6c6cdaa599e8a2c5185/urllib3-2.5.0-py3-none-any.whl (129 kB)
Collecting certifi>=2017.4.17 (from requests->simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/e5/48/1549795ba7742c948d2ad169c1c8cdbae65bc450d6cd753d124b17c8cd32/certifi-2025.8.3-py3-none-any.whl (161 kB)
Collecting pyasn1>=0.1.3 (from rsa->simplepro)
  Downloading https://mirrors.aliyun.com/pypi/packages/c8/f1/d6a797abb14f6283c0ddff96bbdd46937f64122b8c925cab503dd37f8214/pyasn1-0.6.1-py3-none-any.whl (83 kB)
Building wheels for collected packages: simplepro, django-simpleui
  Building wheel for simplepro (pyproject.toml) ... done
  Created wheel for simplepro: filename=simplepro-7.20-py3-none-any.whl size=18646952 sha256=84429a74db13f9139e4b5db6aed48437e77021b35a36f57b1123060b31fc9c0f
  Stored in directory: c:\users\ye\appdata\local\pip\cache\wheels\31\44\80\97d99e0fb69cffc534c9f9d2535550dcae5c5c0dac64ec6652
  Building wheel for django-simpleui (pyproject.toml) ... done
  Created wheel for django-simpleui: filename=django_simpleui-2025.6.24-py3-none-any.whl size=7793301 sha256=4bac0565b25205de859aa2cf8ae112ec1d251543167889bfd9eb6a59fbf4efab
  Stored in directory: c:\users\ye\appdata\local\pip\cache\wheels\66\6b\be\316f1d7e108975083cfc644782e742b47eae166328f3450148
Successfully built simplepro django-simpleui
Installing collected packages: urllib3, tablib, pyasn1, psutil, pillow, idna, diff-match-patch, charset_normalizer, certifi, rsa, requests, django-simpleui, django-import-export, simplepro
Successfully installed certifi-2025.8.3 charset_normalizer-3.4.3 diff-match-patch-20241021 django-import-export-4.3.9 django-simpleui-2025.6.24 idna-3.10 pillow-11.3.0 psutil-7.0.0 pyasn1-0.6.1 requests-2.32.5 rsa-4.9.1 simplepro-7.20 tablib-3.8.0 urllib3-2.5.0
(.venv) PS D:\workspace\GOAMAS\goamas

## simplepro 配置
登录https://www.noondot.com/
点用户图标，点我的许可证，点域名管理
1、在域名管理加入如192.168.1.32
2、在settings.py中加入SIMPLEPRO_SECRET_KEY = '密钥' 密钥从上面的网站获取
3、INSTALL_APPS部分的最前面加入以下配置（simplepro 是核心程序，simpleui是皮肤，import_export是用于实现导入和导出的插件）：
INSTALLED_APPS = [
    'simplepro',
    'simpleui',
    'import_export',
4、在MIDDLEWARE部分的最后面加入simplepro的中间件
MIDDLEWARE = [
...
    # 加入simplepro的中间件
    'simplepro.middlewares.SimpleMiddleware'
]
5、在urls.py中增加：
from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sp/', include('simplepro.urls')),
]

通过以上配置，以下地址会加载simplePro
http://192.168.1.32:8000/admin/login/?next=/admin/



# 一些基础修改

SIMPLEUI_HOME_PAGE = 'https://www.xueqiu.com'
### 标题
SIMPLEUI_HOME_TITLE = 'a100社区'
### 图标
SIMPLEUI_HOME_ICON = 'fa fa-user'
##### 支持element-ui和fontawesome的图标，参考https://fontawesome.com/icons Free图标
### 隐藏监控图表
SIMPLEPRO_MONIT_DISPLAY = False
### 验证码开关
SIMPLEPRO_CAPTCHA_ENABLED = False

# 用uvicorn启动
### WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
### For more information on production servers see: https://docs.djangoproject.com/en/5.2/howto/deployment/

(.venv) PS D:\workspace\GOAMAS\goamas> pip install uvicorn
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting uvicorn
  Downloading https://mirrors.aliyun.com/pypi/packages/d2/e2/dc81b1bd1dcfe91735810265e9d26bc8ec5da45b4c0f6237e286819194c3/uvicorn-0.35.0-py3-none-any.whl (66 kB)
Collecting click>=7.0 (from uvicorn)
  Downloading https://mirrors.aliyun.com/pypi/packages/85/32/10bb5764d90a8eee674e9dc6f4db6a0ab47c8c4d0d83c27f7c39ac415a4d/click-8.2.1-py3-none-any.whl (102 kB)
Collecting h11>=0.8 (from uvicorn)
  Downloading https://mirrors.aliyun.com/pypi/packages/04/4b/29cac41a4d98d144bf5f6d33995617b185d14b22401f75ca86f384e87ff1/h11-0.16.0-py3-none-any.whl (37 kB)
Collecting colorama (from click>=7.0->uvicorn)
  Downloading https://mirrors.aliyun.com/pypi/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl (25 kB)
Installing collected packages: h11, colorama, click, uvicorn
Successfully installed click-8.2.1 colorama-0.4.6 h11-0.16.0 uvicorn-0.35.0
(.venv) PS D:\workspace\GOAMAS\goamas> 

用 uvicorn 启动 Django（ASGI 模式）

可以在 lifespan 的 startup 阶段：
初始化 Redis 客户端
连接外部 API 服务
打印系统日志
写入启动标记到数据库等

也可以在 shutdown 阶段：
关闭数据库连接池
清除缓存或文件
通知外部系统服务下线

集成 Redis、SQLAlchemy、RabbitMQ 或别的组件的初始化处理器

uvicorn goamas.asgi:application --host 0.0.0.0 --port 8000

# 以上uvicorn启动，有一些static的报错，安装whitenoise
(.venv) PS D:\workspace\GOAMAS\goamas> pip install whitenoise
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting whitenoise
  Downloading https://mirrors.aliyun.com/pypi/packages/64/b2/2ce9263149fbde9701d352bda24ea1362c154e196d2fda2201f18fc585d7/whitenoise-6.9.0-py3-none-any.whl (20 kB)
Installing collected packages: whitenoise
Successfully installed whitenoise-6.9.0

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 注意要放在 Django CommonMiddleware 之前
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"



(.venv) PS D:\workspace\GOAMAS\goamas> python manage.py collectstatic

You have requested to collect static files at the destination
location as specified in your settings:

    D:\workspace\GOAMAS\goamas\staticfiles

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes
Found another file with the destination path 'admin\simpleui-x\theme\base.less'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.

1772 static files copied to 'D:\workspace\GOAMAS\goamas\staticfiles', 1652 unmodified.

uvicorn goamas.asgi:application --host 0.0.0.0 --port 8000 访问正常


#

(.venv) PS D:\workspace\GOAMAS\goamas> pip install django_apscheduler
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting django_apscheduler
  Downloading https://mirrors.aliyun.com/pypi/packages/e0/19/c3d2dea21a6afdc93689b9f769ff3694cac810e4a09c24ab423dd1613e6c/django_apscheduler-0.7.0-py3-none-any.whl (24 kB)
Requirement already satisfied: django>=4.2 in d:\workspace\goamas\.venv\lib\site-packages (from django_apscheduler) (5.2.5)
Collecting apscheduler<4.0,>=3.2 (from django_apscheduler)
  Downloading https://mirrors.aliyun.com/pypi/packages/d0/ae/9a053dd9229c0fde6b1f1f33f609ccff1ee79ddda364c756a924c6d8563b/APScheduler-3.11.0-py3-none-any.whl (64 kB)
Collecting tzlocal>=3.0 (from apscheduler<4.0,>=3.2->django_apscheduler)
  Downloading https://mirrors.aliyun.com/pypi/packages/c2/14/e2a54fabd4f08cd7af1c07030603c3356b74da07f7cc056e600436edfa17/tzlocal-5.3.1-py3-none-any.whl (18 kB)
Requirement already satisfied: asgiref>=3.8.1 in d:\workspace\goamas\.venv\lib\site-packages (from django>=4.2->django_apscheduler) (3.9.1)
Requirement already satisfied: sqlparse>=0.3.1 in d:\workspace\goamas\.venv\lib\site-packages (from django>=4.2->django_apscheduler) (0.5.3)
Requirement already satisfied: tzdata in d:\workspace\goamas\.venv\lib\site-packages (from django>=4.2->django_apscheduler) (2025.2)
Installing collected packages: tzlocal, apscheduler, django_apscheduler
Successfully installed apscheduler-3.11.0 django_apscheduler-0.7.0 tzlocal-5.3.1


INSTALLED_APPS = [
    ...
    'django_apscheduler',
]


(.venv) PS D:\workspace\GOAMAS\goamas> python manage.py makemigrations
No changes detected
(.venv) PS D:\workspace\GOAMAS\goamas> python manage.py migrate             
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, django_apscheduler, sessions
Running migrations:
  Applying django_apscheduler.0001_initial... OK
  Applying django_apscheduler.0002_auto_20180412_0758... OK
  Applying django_apscheduler.0003_auto_20200716_1632... OK
  Applying django_apscheduler.0004_auto_20200717_1043... OK
  Applying django_apscheduler.0005_migrate_name_to_id... OK
  Applying django_apscheduler.0006_remove_djangojob_name... OK
  Applying django_apscheduler.0007_auto_20200717_1404... OK
  Applying django_apscheduler.0008_remove_djangojobexecution_started... OK
  Applying django_apscheduler.0009_djangojobexecution_unique_job_executions... OK
(.venv) PS D:\workspace\GOAMAS\goamas>