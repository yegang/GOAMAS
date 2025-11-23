# scheduler/scheduler.py
import os
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from django_apscheduler.jobstores import DjangoJobStore

from django.conf import settings
from joblist_scheduler.job import delete_old_job_executions  # 你的清理函数

import logging
from termcolor import colored
from colorama import init
# 初始化 colorama，以便在 Windows 上启用颜色支持
init()

# 自定义日志格式化器
class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_message = super().format(record)
        if record.levelno == logging.INFO:
            log_message = colored(log_message, 'green')  # 绿色
        elif record.levelno == logging.WARNING:
            log_message = colored(log_message, 'yellow')  # 黄色
        elif record.levelno == logging.ERROR:
            log_message = colored(log_message, 'red')  # 红色
        return log_message

def create_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        print(f"{directory} 不存在，正在创建...")
        os.mkdir(directory)
        if not os.path.exists(directory):
            print(f"创建目录 {directory} 失败!")
            exit(1)
    print(f"{directory} 目录存在")

# 设置根目录
root_dir = os.path.expanduser("~")

# 日志目录
logdir = os.path.join(root_dir, "log")
create_dir_if_not_exists(logdir)
# ================== 日志配置 ==================
# logger = logging.getLogger("apscheduler")
# logger.setLevel(logging.INFO)
#
# handler = logging.FileHandler("apscheduler.log")
# handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# logger.addHandler(handler)
#
# console = logging.StreamHandler()
# console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# logger.addHandler(console)

# 创建logger对象
# 获取当前Python文件名（包含扩展名）
python_filename1 = os.path.basename(__file__)
# 去除扩展名，只保留文件名部分（可根据需求选择是否去除）
python_filename = os.path.splitext(python_filename1)[0]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # log等级总开关
# log输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# 控制台handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO) # log等级的开关
stream_handler.setFormatter(formatter)

# 创建控制台处理器
console_handler = logging.StreamHandler()
# 使用自定义的彩色格式化器
console_handler.setFormatter(ColorFormatter('%(levelname)s: %(message)s'))
# 添加处理器
logger.addHandler(console_handler)

logfilename = root_dir + "/log/" + python_filename + ".log"
print(logfilename)
file_handler = logging.FileHandler(logfilename)
file_handler.setLevel(logging.INFO) # log等级的开关
file_handler.setFormatter(formatter)

# 添加到logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
# ================== 调度器 ==================
scheduler = BackgroundScheduler()

# 加入 Django ORM JobStore
scheduler.add_jobstore(DjangoJobStore(), "default")



# ================== 事件监听器 ==================
from email.utils import formataddr
from django.core.mail import send_mail

def job_listener(event):
    job = scheduler.get_job(event.job_id)
    job_name = job.name if job else event.job_id

    if event.exception:
        logger.error(f"[任务失败] {job_name} 发生异常：{event.exception}")
        plain_text = f"""
任务ID: {event.job_id}
异常: {event.exception}
调度时间: {event.scheduled_run_time}
堆栈信息:
{event.traceback}
"""
        html_text = f"""
<h2>任务失败告警</h2>
<ul>
<li><strong>任务ID:</strong> {event.job_id}</li>
<li><strong>任务名:</strong> {job_name}</li>
<li><strong>异常:</strong> <span style="color:red;">{event.exception}</span></li>
<li><strong>调度时间:</strong> {event.scheduled_run_time}</li>
</ul>
<h3>堆栈信息</h3>
<pre style="background:#f4f4f4;padding:10px;border:1px solid #ccc;">{event.traceback}</pre>
"""
    elif event.retval is None:
        logger.error(f"[任务失败] {job_name} 没有返回值或发生未知失败")
        plain_text = f"""
任务ID: {event.job_id}
异常: 无返回值或未知异常
调度时间: {event.scheduled_run_time}
"""
        html_text = f"""
<h2>任务失败告警</h2>
<ul>
<li><strong>任务ID:</strong> {event.job_id}</li>
<li><strong>任务名:</strong> {job_name}</li>
<li><strong>异常:</strong> <span style="color:red;">无返回值或未知异常</span></li>
<li><strong>调度时间:</strong> {event.scheduled_run_time}</li>
</ul>
"""
    else:
        logger.info(f"[任务成功] {job_name} 正常执行完成。")
        return

    try:
        from_email = formataddr(("任务调度器告警", settings.DEFAULT_FROM_EMAIL))
        send_mail(
            subject=f"[任务失败告警] {job_name}",
            message=plain_text,
            from_email=from_email,
            recipient_list=["00080@czcb.com.cn"],
            fail_silently=False,
            html_message=html_text,  # ✨ 关键！加上HTML版本
        )
        logger.info(f"已发送任务失败邮件通知：{job_name}")
    except Exception as e:
        logger.error(f"发送任务失败邮件失败: {e}")



scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

# ================== 定时清理历史执行记录任务 ==================
def add_delete_old_jobs_task():
    scheduler.add_job(
        delete_old_job_executions,
        trigger='cron',
        day_of_week='mon-sun',  # 每天执行
        hour=3,                 # 凌晨3点执行
        id='delete_old_job_executions',
        max_instances=1,
        replace_existing=True,
    )
    logger.info("已添加自动清理历史任务记录的定时任务。")

add_delete_old_jobs_task()


# ================== 启动函数（后台线程） ==================
def start_scheduler():
    try:
        scheduler.start()
        logger.info("APScheduler已启动。")
    except Exception as e:
        logger.error(f"APScheduler启动失败: {e}")

# ================== 后台线程启动调度器 ==================
threading.Thread(target=start_scheduler, daemon=True).start()
