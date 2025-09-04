# #============================================================================================================
# import os
# import sys
# import django
#
# # 添加 Django 项目的根目录到 sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
# # 设置 Django 的配置模块
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resbat02.settings')
#
# # 初始化 Django
# django.setup()
#
# #============================================================================================================
import logging
from contextlib import contextmanager

from django.conf import settings
import datetime
from datetime import timedelta
from django.contrib.auth.models import User

# from scheduler.db_query_mysql_pld_createUserAppboxLoginStatisticsExcel import db_query_mysql_pld_createUserAppboxLoginStatisticsExcel
# from related_source_code.system import passModify,passQuery
# from scheduler.loanbatDataFileTransfer import loanbatDataFileTransfer


#from django.core.cache import cache

# 获取同步 Redis 连接
from django_redis import get_redis_connection
sync_redis_connection = get_redis_connection('default')

# 获取异步 Redis 连接
import redis.asyncio as aioredis
async_redis_connection = aioredis.from_url(settings.REDIS_SERVER_URL)

#----------------------日志配置-----------------------------
logger = logging.getLogger("apscheduler")
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("apscheduler.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(console)
#============================================================================================================
# from resbat02.lock_service import LockService
#
# # 普通锁（非可重入）
# def normal_lock_example():
#     lock_key = "normal_lock_key"
#     with LockService.lock(lock_key, expire=30, reentrant=False) as acquired:
#         if acquired:
#             print("Normal lock acquired.")
#         else:
#             print("Failed to acquire normal lock.")
#
# # 可重入锁（同步）
# def reentrant_lock_example():
#     lock_key = "reentrant_lock_key"
#     with LockService.lock(lock_key, expire=30, reentrant=True) as acquired:
#         if acquired:
#             print("Reentrant lock acquired.")
#         else:
#             print("Failed to acquire reentrant lock.")
#
# # 异步锁（非可重入）
# async def async_normal_lock_example():
#     lock_key = "async_normal_lock_key"
#     async with LockService.alock(lock_key, expire=30, reentrant=False) as acquired:
#         if acquired:
#             print("Async normal lock acquired.")
#         else:
#             print("Failed to acquire async normal lock.")
#
# # 异步可重入锁
# async def async_reentrant_lock_example():
#     lock_key = "async_reentrant_lock_key"
#     async with LockService.alock(lock_key, expire=30, reentrant=True) as acquired:
#         if acquired:
#             print("Async reentrant lock acquired.")
#         else:
#             print("Failed to acquire async reentrant lock.")

# # 运行所有示例
# async def run_all():
#     normal_lock_example()
#     reentrant_lock_example()
#     await async_normal_lock_example()
#     await async_reentrant_lock_example()
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(run_all())
#============================================================================================================
@contextmanager
def redis_lock(jobname, timeout=(24 + 2) * 60 * 60):
    try:
        today_string = datetime.datetime.now().strftime("%Y-%m-%d")
        # 锁的键名
        sync_key = f"servername.lock.{jobname}.{today_string}"
        logger.info(f"<Redis Lock> {sync_key}")
        # 原子性的锁: 不存在，创建锁，返回1，相当于获取锁；存在，创建锁失败，返回0，相当于获取锁失败；过一段时间超时，避免死锁
        # nx: 不存在，key值设置为value，返回1，存在，不操作，返回0
        # ex: 设置超时

        # 使用同步 Redis 连接
        lock = sync_redis_connection.set(sync_key, value=1, nx=True, ex=timeout)
        sync_value = sync_redis_connection.get('sync_key')
        print(sync_value)

        yield lock
    finally:
        sync_redis_connection.delete(sync_key) # 释放锁

def ensure_return_value(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return "ok"  # 如果原函数没返回任何东西，自动补一个 "ok"
        return result
    return wrapper

# Define the task functions
from django_apscheduler.models import DjangoJobExecution

def delete_old_job_executions(max_records=20):
    from django.db.models import Max
    # 查询最大run_time
    latest_execution = DjangoJobExecution.objects.aggregate(latest_time=Max('run_time'))['latest_time']
    if latest_execution:
        # 只保留最近 max_records 条
        executions_to_keep = DjangoJobExecution.objects.order_by('-run_time')[:max_records]
        keep_ids = [e.id for e in executions_to_keep]
        DjangoJobExecution.objects.exclude(id__in=keep_ids).delete()
        print(f"已清理历史执行记录，只保留最近 {max_records} 条。")

def count_users():
    user_count = User.objects.count()
    print(f"Total number of users: {user_count}")

def update_database():
    # Update database logic here
    pass

def aps_test(jobname):

    with redis_lock(jobname) as lock:
        if lock:
            logger.info('aps_test : %s! The time is: %s' % (jobname,datetime.datetime.now()) )
            # 在这里执行任务
            print ('aps_test : ',jobname,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#@ensure_return_value  # 装饰器主要是为了确保有返回值，主要是用在监听的监控场景，没返回值，现在监控要报警，故此处理。
def tick(jobname, param1=None, param2=None):
    """
    处理某个任务的执行逻辑。
    :param jobname: 任务的名称
    :param param1: 第一个参数
    :param param2: 第二个参数
    """
    logger.info(f"开始执行任务 {jobname}，时间: {datetime.datetime.now()}")

    # 根据传入的参数执行不同的任务逻辑
    if param1:
        logger.info(f"任务 {jobname} 接收到参数1: {param1}")
    if param2:
        logger.info(f"任务 {jobname} 接收到参数2: {param2}")

    with redis_lock(jobname) as lock:
        if lock:
            logger.info(f"任务 {jobname} 被锁定，开始执行!")
            # 这里可以加入你具体的业务逻辑代码
            logger.info(f"标记! 时间是: {datetime.datetime.now()}")
            return None  # 如果没有其他返回值，确保返回 "ok"
        else:
            logger.error(f"任务 {jobname} 锁定失败")
            return "failed"

#@ensure_return_value  # 装饰器主要是为了确保有返回值，主要是用在监听的监控场景，没返回值，现在监控要报警，故此处理。
# def pldReport01(jobname, param1=None, param2=None, param3=None):
#     logger.info(f"开始执行任务 {jobname}，时间: {datetime.datetime.now()}")
#     logger.info(f"传入的参数: param1={param1}, param2={param2}, param3={param3}")
#
#     with redis_lock(jobname) as lock:
#         if lock:
#             logger.info(f"任务 {jobname} 被锁定，开始执行!")
#             db_query_mysql_pld_createUserAppboxLoginStatisticsExcel(param1, param2, param3)
#             # 这里可以加入你具体的业务逻辑代码
#             logger.info(f"标记! 时间是: {datetime.datetime.now()}")
#             return None  # 如果没有其他返回值，确保返回 "ok"
#         else:
#             logger.error(f"任务 {jobname} 锁定失败")
#             return "failed"

def pldReport01(jobname, **kwargs):
    logger.info(f"开始执行任务 {jobname}，时间: {datetime.datetime.now()}")
    logger.info(f"传入的参数: {kwargs}")

    with redis_lock(jobname) as lock:
        if lock:
            logger.info(f"任务 {jobname} 被锁定，开始执行!")
            # 假设你从 kwargs 中提取 param1~3
            param1 = kwargs.get("ip")
            param2 = kwargs.get("param1")
            param3 = kwargs.get("param2")
            #db_query_mysql_pld_createUserAppboxLoginStatisticsExcel(param1, param2, param3)
            logger.info(f"结束时间是: {datetime.datetime.now()}")
            return None
        else:
            logger.error(f"任务 {jobname} 锁定失败")
            return "failed"

def passModify_func(jobname, **kwargs):
    logger.info(f"开始执行任务 {jobname}，时间: {datetime.datetime.now()}")
    logger.info(f"传入的参数: {kwargs}")

    with redis_lock(jobname) as lock:
        if lock:
            logger.info(f"任务 {jobname} 被锁定，开始执行!")
            # 假设你从 kwargs 中提取 param1~3
            param1 = kwargs.get("runFlag")
            param2 = kwargs.get("runMode")
            param3 = kwargs.get("ipchoice")
            param4 = kwargs.get("samePassFlag")

            #passModify.passModify(param1, param2, param3,param4)
            logger.info(f"结束时间是: {datetime.datetime.now()}")
            return None
        else:
            logger.error(f"任务 {jobname} 锁定失败")
            return "failed"

def passQuery_func(jobname, **kwargs):
    logger.info(f"开始执行任务 {jobname}，时间: {datetime.datetime.now()}")
    logger.info(f"传入的参数: {kwargs}")

    with redis_lock(jobname) as lock:
        if lock:
            logger.info(f"任务 {jobname} 被锁定，开始执行!")
            # 假设你从 kwargs 中提取 param1~3
            param1 = kwargs.get("runFlag")
            param2 = kwargs.get("runMode")
            param3 = kwargs.get("ipchoice")
            param4 = kwargs.get("pldChoice")

            #passQuery.passQuery(param1, param2, param3,param4)
            logger.info(f"结束时间是: {datetime.datetime.now()}")
            return None
        else:
            logger.error(f"任务 {jobname} 锁定失败")
            return "failed"

def loanbatDataFileTransfer_func(jobname, **kwargs):
    logger.info(f"开始执行任务 {jobname}，时间: {datetime.datetime.now()}")
    logger.info(f"传入的参数: {kwargs}")

    with redis_lock(jobname) as lock:
        if lock:
            logger.info(f"任务 {jobname} 被锁定，开始执行!")
            # 假设你从 kwargs 中提取 param1~3
            #runFlag,runMode,ipchoice,YYYYMMDD
            param1 = kwargs.get("runFlag")
            param2 = kwargs.get("runMode")
            param3 = kwargs.get("ipchoice")
            param4 = kwargs.get("YYYYMMDD")

            #loanbatDataFileTransfer(param1, param2, param3,param4)
            logger.info(f"结束时间是: {datetime.datetime.now()}")
            return None
        else:
            logger.error(f"任务 {jobname} 锁定失败")
            return "failed"