import json
import logging
import os

from goamas.joblist_scheduler.job import tick, aps_test, count_users, update_database, pldReport01,passModify_func
from goamas.joblist_scheduler.job import passQuery_func, loanbatDataFileTransfer_func

#---------------------------------------------------
from goamas.joblist_scheduler.scheduler import scheduler
#from run_filesync.os_file_collectAclear_main_new import os_file_collectAclear_main
#---------------------------------------------------

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED
#from scheduler.job import tick

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

#---------------------日志配置-----------------------------------
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
logfilename = root_dir + "/log/" + python_filename + ".log"
print(logfilename)
file_handler = logging.FileHandler(logfilename)
file_handler.setLevel(logging.INFO) # log等级的开关
file_handler.setFormatter(formatter)
# 添加到logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
#---------------------日志配置-----------------------------------


class JobAction:
# 这是类的一个初始化函数，初始化scheduler和监听函数
    def __init__(self):
        self.scheduler = scheduler
        self.scheduler.add_listener(self.my_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_EXECUTED)

    #静态方法不能有 self 参数
    @staticmethod
    def build_kwargs(trigger_id, args_list):
        kwargs = {"jobname": trigger_id}
        if args_list:
            try:
                args_dict = json.loads(args_list)
                if not isinstance(args_dict, dict):
                    raise ValueError("参数必须是 JSON 对象")
                kwargs.update(args_dict)
            except Exception as e:
                logger.error(f"解析参数失败: {e}, 输入: {args_list}")
                raise
        return kwargs

    func_registry = {
        "tick": tick,
        "aps_test": aps_test,
        "count_users": count_users,
        "update_database": update_database,
        "pldReport01": pldReport01,
        "passModify_func": passModify_func,
        "passQuery_func": passQuery_func,
        "loanbatDataFileTransfer_func": loanbatDataFileTransfer_func
    }

    @staticmethod
    def str_to_func(func_name):
        if func_name in JobAction.func_registry:
            return JobAction.func_registry[func_name]
        else:
            raise ValueError(f"未识别的函数名：{func_name}")


    @staticmethod
    def start_date_job(trigger, job_rate, id, func_name, args_list):
        func_real = JobAction.str_to_func(func_name)
        trigger_id = f"{trigger}-{id}"
        kwargs = JobAction.build_kwargs(trigger_id, args_list)

        logger.info(f"[start_date_job] trigger_id: {trigger_id}, func: {func_real.__name__}, kwargs: {kwargs}")

        try:
            scheduler.add_job(
                id=trigger_id,
                func=func_real,
                trigger='date',
                run_date=job_rate,
                kwargs=kwargs,
                coalesce=True
            )
        except Exception as e:
            logger.error(f"添加 date 任务出错: {e}")
            raise

        logger.info(f"{trigger} 任务添加成功")
        logger.info('当前任务池：' + str(scheduler.get_jobs()))

    @staticmethod
    def start_cron_job(trigger, job_rate, id, func_name, args_list):
        func_real = JobAction.str_to_func(func_name)
        trigger_id = f"{trigger}-{id}"
        kwargs = JobAction.build_kwargs(trigger_id, args_list)

        rate = job_rate.split()
        if len(rate) != 7:
            logger.error("cron 表达式应包含 7 个字段：秒 分 时 日 月 周 年")
            raise ValueError("无效的 cron 表达式")

        logger.info(f"[start_cron_job] trigger_id: {trigger_id}, func: {func_real.__name__}, kwargs: {kwargs}")

        try:
            scheduler.add_job(
                id=trigger_id,
                func=func_real,
                trigger='cron',
                second=rate[0],
                minute=rate[1],
                hour=rate[2],
                day=rate[3],
                month=rate[4],
                day_of_week=rate[5],
                year=rate[6],
                kwargs=kwargs,
                coalesce=True
            )
        except Exception as e:
            logger.error(f"添加 cron 任务出错: {e}")
            raise

        logger.info(f"{trigger} 任务添加成功")
        logger.info('当前任务池：' + str(scheduler.get_jobs()))



    # 停止任务
    @staticmethod
    def stop_job(trigger_id):
        if scheduler.get_job(trigger_id):
            scheduler.remove_job(trigger_id)
            logger.info('已启动的任务：' + str(scheduler.get_jobs()))

    # 暂停任务
    @staticmethod
    def pause_job(trigger_id):
        logger.info(trigger_id)
        scheduler.pause_job(trigger_id)

    # 重启任务
    @staticmethod
    def resume_job(trigger_id):
        scheduler.resume_job(trigger_id)

    # 修改任务
    @staticmethod
    def modify_job(trigger_id, job_value):
        if job_value[0] == 'cron':
            rate = job_value[1].split()
            scheduler.reschedule_job(trigger_id, trigger='cron', second=rate[0], minute=rate[1],hour=rate[2], day=rate[3], month=rate[4], day_of_week=rate[5], year=rate[6])
        elif job_value[0] == 'date':
            scheduler.reschedule_job(trigger_id, trigger='date', run_date=job_value[1])
	# 这里是监听函数
    @staticmethod
    def my_listener(event):  # 添加监听器
        job = scheduler.get_job(event.job_id)
        if not event.exception:
            pass
        else:
            logger.error("jobname=%s|jobtrigger=%s|errcode=%s|exception=[%s]|traceback=[%s]|scheduled_time=%s", job.name, job.trigger, event.code, event.exception, event.traceback, event.scheduled_run_time)
        # scheduler.shutdown(wait=False)