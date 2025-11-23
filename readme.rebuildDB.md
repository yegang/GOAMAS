# (.venv) PS D:\workspace\GOAMAS> python .\manage.py makemigrations
C:\Users\ye\log 目录存在
C:\Users\ye/log/scheduler.log
2025-09-15 20:05:20,267 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
INFO: 已添加自动清理历史任务记录的定时任务。
2025-09-15 20:05:20,267 - scheduler.py[line:173] - INFO: 已添加自动清理历史任务记录的定时任务。
C:\Users\ye\log 目录存在
C:\Users\ye/log/scheduler_action.log
C:\Users\ye\log 目录存在
C:\Users\ye/log/job_utils.log
C:\Users\ye\log 目录存在
C:\Users\ye/log/admin.log
ERROR: APScheduler启动失败: (1146, "Table 'GOAMAS.django_apscheduler_djangojob' doesn't exist")
2025-09-15 20:05:20,625 - scheduler.py[line:184] - ERROR: APScheduler启动失败: (1146, "Table 'GOAMAS.django_apscheduler_djangojob' doesn't exist")
Migrations for 'joblist':
  joblist\migrations\0001_initial.py
    + Create model joblist
# (.venv) PS D:\workspace\GOAMAS> python manage.py migrate
C:\Users\ye\log 目录存在
C:\Users\ye/log/scheduler.log
2025-09-15 20:06:27,616 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
INFO: 已添加自动清理历史任务记录的定时任务。
2025-09-15 20:06:27,617 - scheduler.py[line:173] - INFO: 已添加自动清理历史任务记录的定时任务。
C:\Users\ye\log 目录存在
C:\Users\ye/log/scheduler_action.log
C:\Users\ye\log 目录存在
C:\Users\ye/log/job_utils.log
C:\Users\ye\log 目录存在
C:\Users\ye/log/admin.log
ERROR: APScheduler启动失败: (1146, "Table 'GOAMAS.django_apscheduler_djangojob' doesn't exist")
2025-09-15 20:06:27,932 - scheduler.py[line:184] - ERROR: APScheduler启动失败: (1146, "Table 'GOAMAS.django_apscheduler_djangojob' doesn't exist")
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, django_apscheduler, joblist, sessions
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
  Applying django_apscheduler.0001_initial... OK
  Applying django_apscheduler.0002_auto_20180412_0758... OK
  Applying django_apscheduler.0003_auto_20200716_1632... OK
  Applying django_apscheduler.0004_auto_20200717_1043... OK
  Applying django_apscheduler.0005_migrate_name_to_id... OK
  Applying django_apscheduler.0006_remove_djangojob_name... OK
  Applying django_apscheduler.0007_auto_20200717_1404... OK
  Applying django_apscheduler.0008_remove_djangojobexecution_started... OK
  Applying django_apscheduler.0009_djangojobexecution_unique_job_executions... OK
  Applying joblist.0001_initial... OK
  Applying sessions.0001_initial... OK

(.venv) PS D:\workspace\GOAMAS> python manage.py createsuperuser
C:\Users\ye\log 目录存在
C:\Users\ye/log/scheduler.log
2025-09-15 20:08:10,965 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
INFO: 已添加自动清理历史任务记录的定时任务。
2025-09-15 20:08:10,965 - scheduler.py[line:173] - INFO: 已添加自动清理历史任务记录的定时任务。
C:\Users\ye\log 目录存在
C:\Users\ye/log/scheduler_action.log
C:\Users\ye\log 目录存在
C:\Users\ye/log/job_utils.log
C:\Users\ye\log 目录存在
C:\Users\ye/log/admin.log
2025-09-15 20:08:11,319 - apscheduler.scheduler - INFO - Added job "delete_old_job_executions" to job store "default"
2025-09-15 20:08:11,319 - apscheduler.scheduler - INFO - Scheduler started
INFO: APScheduler已启动。
2025-09-15 20:08:11,320 - scheduler.py[line:182] - INFO: APScheduler已启动。
用户名 (leave blank to use 'ye'): admin
电子邮件地址: yegang@foxmail.com
Password:
Password (again):
Error: Your passwords didn't match.
Password:
Password (again):
Superuser created successfully.
