import os

from joblist_scheduler.scheduler import scheduler  # 引用全局唯一的 scheduler

from joblist.scheduler_action import JobAction  # 你的任务注册逻辑类
import logging


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

def run_job_once_now(job_obj):
    """
    立即执行任务一次（不进入调度器）
    job_obj: joblist 表中的一条记录
    """
    job_id = str(job_obj.id)
    func_name = job_obj.func_name
    args_list = job_obj.args_list
    trigger_id = f"manual-{job_id}"

    try:
        func = JobAction.str_to_func(func_name)
        kwargs = JobAction.build_kwargs(trigger_id, args_list)

        logger.info(f"[立即执行] 函数: {func.__name__}，参数: {kwargs}")
        result = func(**kwargs)

        logger.info(f"[立即执行] 任务 {job_obj.job_name} 执行完成，返回: {result}")
        return True
    except Exception as e:
        logger.error(f"[立即执行失败] 任务 {job_obj.job_name}：{e}", exc_info=True)
        return False

def refresh_job_logic(job_obj):
    job_id = str(job_obj.id)
    trigger_name = job_obj.trigger_name
    job_type = job_obj.action_type
    job_rate = job_obj.job_rate
    func_name_job = job_obj.func_name
    args_list = job_obj.args_list

    full_job_id = f"{trigger_name}-{job_id}"

    try:
        scheduler.remove_job(full_job_id)
        logger.info(f"[刷新任务] 已移除旧任务 {full_job_id}")
    except Exception as e:
        logger.warning(f"[刷新任务] 移除任务失败（可能未注册）: {e}")

    instance = JobAction()
    func = getattr(instance, f"start_{job_type}_job", None)
    if not func:
        raise ValueError(f"[刷新任务] 无效的 job_type: {job_type}")

    func(trigger_name, job_rate, job_id, func_name_job, args_list)
    logger.info(f"[刷新任务] 新任务 {full_job_id} 注册成功")
