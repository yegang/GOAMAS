# 创建joblist应用
python .\manage.py startapp joblist

# 日志太多，为了看清日志，增加终端颜色
(.venv) PS D:\workspace\GOAMAS\goamas> pip install termcolor
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting termcolor
  Downloading https://mirrors.aliyun.com/pypi/packages/4f/bd/de8d508070629b6d84a30d01d57e4a65c69aa7f5abe7560b8fad3b50ea59/termcolor-3.1.0-py3-none-any.whl (7.7 kB)
Installing collected packages: termcolor
Successfully installed termcolor-3.1.0


(.venv) PS D:\workspace\GOAMAS> pip install django_redis
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting django_redis
  Downloading https://mirrors.aliyun.com/pypi/packages/7e/79/055dfcc508cfe9f439d9f453741188d633efa9eab90fc78a67b0ab50b137/django_redis-6.0.0-py3-none-any.whl (33 kB)
Requirement already satisfied: Django>=4.2 in d:\workspace\goamas\.venv\lib\site-packages (from django_redis) (5.2.5)
Collecting redis>=4.0.2 (from django_redis)
  Downloading https://mirrors.aliyun.com/pypi/packages/e8/02/89e2ed7e85db6c93dfa9e8f691c5087df4e3551ab39081a4d7c6d1f90e05/redis-6.4.0-py3-none-any.whl (279 kB)
Requirement already satisfied: asgiref>=3.8.1 in d:\workspace\goamas\.venv\lib\site-packages (from Django>=4.2->django_redis) (3.9.1)
Requirement already satisfied: sqlparse>=0.3.1 in d:\workspace\goamas\.venv\lib\site-packages (from Django>=4.2->django_redis) (0.5.3)
Requirement already satisfied: tzdata in d:\workspace\goamas\.venv\lib\site-packages (from Django>=4.2->django_redis) (2025.2)
Installing collected packages: redis, django_redis
Successfully installed django_redis-6.0.0 redis-6.4.0
(.venv) PS D:\workspace\GOAMAS> 


