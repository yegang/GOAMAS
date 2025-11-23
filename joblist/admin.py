from django.contrib import admin, messages
from .job_utils import refresh_job_logic, run_job_once_now
from .scheduler_action import JobAction
#-----------------
#说明：
# program update 1
#-----------------
# Register your models here.
from .resource import joblistResource

from .models import joblist

from .mixins import CustomImportExportMixin
from .forms import JobListForm
import logging
import os






from django.utils.html import format_html
from django.contrib import admin
from django_apscheduler.models import DjangoJob, DjangoJobExecution

# 🔥 先取消已有的注册
try:
    admin.site.unregister(DjangoJob)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(DjangoJobExecution)
except admin.sites.NotRegistered:
    pass

# ✅ 自己重新注册
@admin.register(DjangoJob)
class DjangoJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'next_run_time')

'''
    SENT = "Started execution"
    SUCCESS = "Executed"
    MISSED = "Missed!"
    MAX_INSTANCES = "Max instances!"
    ERROR = "Error!"
'''
@admin.register(DjangoJobExecution)
class DjangoJobExecutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'colored_status', 'run_time', 'duration', 'exception_message')
    list_filter = ('status',)
    readonly_fields = ('job', 'status', 'run_time', 'duration', 'exception_message', 'traceback')
    ordering = ('-run_time',)
    # 自定义列：带颜色显示任务状态
    def colored_status(self, obj):
        # 对应状态的判断
        if obj.status == 'Executed':
            return format_html('<span style="color: green; font-weight: bold;">成功 ({})</span>', obj.status)  # 成功的任务
        elif obj.status == 'Started execution':
            return format_html('<span style="color: orange;">开始执行 ({})</span>', obj.status)  # 已执行的任务
        elif obj.status == 'Missed!':
            return format_html('<span style="color: blue;">错过时间 ({})</span>', obj.status)  # 任务等待执行
        elif obj.status == 'Max instances!':
            return format_html('<span style="color: purple;">最大实例 ({})</span>', obj.status)  # 任务正在执行
        elif obj.status == 'Error!':
            #return format_html('<span style="color: red;">失败</span>')  # 执行失败的任务
            return format_html('<span style="color: red;">失败 ({})</span>', obj.status)
        else:
            #return format_html('<span style="color: gray;">未知</span>')  # 其他状态或未知状态
            return format_html('<span style="color: gray;">未知 ({})</span>', obj.status)

    # def colored_status(self, obj):
    #     # 根据 obj.status 的不同值来判断显示内容
    #     if obj.status == 'success':
    #         return format_html('<span style="color: green; font-weight: bold;">成功</span>')
    #     elif obj.status == 'Executed':  # 如果状态是执行完成
    #         return format_html('<span style="color: orange;">已执行</span>')
    #     else:
    #         return format_html('<span style="color: red;">失败 ({})</span>', obj.status)

    # # 自定义列：带颜色显示任务状态
    # def colored_status(self, obj):
    #     if obj.status == 'success':
    #         return format_html('<span style="color: green;">成功</span>')
    #     else:
    #         #return format_html('<span style="color: red;">失败</span>')
    #         return format_html('<span style="color: red;">失败 ({})</span>', obj.status)

    colored_status.short_description = '执行状态'  # 设置列名

    def duration(self, obj):
        if obj.run_duration:
            return f"{obj.run_duration:.2f} 秒"
        return "无"

    def exception_message(self, obj):
        if obj.exception:
            return str(obj.exception)
        return "无异常"

    duration.short_description = "运行时长"
    exception_message.short_description = "异常信息"


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






@admin.register(joblist)
class joblistAdmin(admin.ModelAdmin):
    form = JobListForm
    list_display = ('id', 'func_name','args_list','job_name', 'decpet', 'trigger_name', 'job_state', 'action_type', 'job_rate')
    list_display_links = ('id', 'job_name')
    list_filter = ('job_state',)
    list_editable = ('action_type', 'job_rate','func_name','args_list', 'decpet')
    list_per_page = 20
    list_max_show_all = 7
    ordering = ('-job_state', 'id',)

    # class Media:
    #     css = {
    #         'all': ('css/custom_admin.css',)
    #     }

    # -----------------------------------------------------------------
    #   自定义按钮
    # -----------------------------------------------------------------

    actions = [ 'start_job','stop_job','button_exeScript', 'refresh_job','run_once_now']

    def run_once_now(self, request, queryset):
        for item in queryset:
            success = run_job_once_now(item)
            if success:
                messages.success(request, f"[成功] {item.job_name} 已被手动触发，立即执行")
            else:
                messages.error(request, f"[失败] {item.job_name} 手动触发，执行异常，请查看日志")

    def refresh_job(self, request, queryset):
        for item in queryset:
            try:
                refresh_job_logic(item)
                messages.success(request, f"[刷新成功] {item.job_name}")
                logger.info(f"[刷新成功] {item.job_name}")
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                messages.error(request, f"[刷新失败] {item.job_name}：{e}\n{tb}")
                logger.info(f"[刷新失败] {item.job_name}：{e}\n{tb}")

    def start_job(self, request, queryset):
        # 这里省略一部分循环选择的页面数据的部分，根据下面代码可以还原出来
        # 就是将选中的任务循环添加到任务池中，并修改状态；若有错，返回错误信息
        for item in queryset:

            job_id = item.id

            job_name = item.job_name

            decpet = item.decpet

            trigger_name = item.trigger_name

            job_state = item.job_state

            job_type = item.action_type

            job_rate = item.job_rate
            func_name_job = item.func_name
            args_list = item.args_list
            # 在这里添加调试信息，输出 args_list，确保它是有效的 JSON 字符串
            messages.add_message(request, messages.INFO, f"args_list: {args_list}")
            logger.info(f"args_list: {args_list}")


            #messages.add_message(request, messages.INFO, str(job_id) +job_name + decpet +
            #                     trigger_name + str(job_state) + job_type + job_rate+func_name_job + args_list)

            if hasattr(JobAction(), 'start_%s_job' % job_type):

                instance = JobAction()
                func_name = 'start_%s_job' % job_type
                func = getattr(instance, func_name)
                messages.add_message(request, messages.INFO, 'JobAction class中找'
                                     + '[ %s ]' % func_name
                                     + '[ %s ]' % type(func)
                                     )
                logger.info('JobAction class中找'
                                     + '[ %s ]' % func_name
                                     + '[ %s ]' % type(func))
                #func(trigger_name, job_rate, str(job_id),func_name_job,args_list)
                try:
                    # 如果 args_list 是有效的 JSON 字符串，则传递给 start_job 方法
                    func(trigger_name, job_rate, str(job_id), func_name_job, args_list)
                    queryset.update(job_state=1)  # 更新任务状态为已启动
                except Exception as e:
                    # 记录异常信息
                    messages.error(request, f"启动任务失败: {e}")
                    logger.info(f"启动任务失败: {e}")

                #queryset.update(job_state=1)
            else:
                logger.info('【启动错误】 ' + job_name + ' 任务不存在!')
                return messages.error(request, '【启动错误】 ' + job_name + ' 任务不存在!')


        # if hasattr(JobAction(), 'start_%s_job' % job_type):
        #     func = getattr(JobAction(), 'start_%s_job' % job_type)
        #     func(trigger_name, job_rate, str(job_id))
        #     queryset.update(job_state=1)
        #
        #
        #     '''
        #     func must be a callable or a textual reference to one
        #     '''
        # else:
        #     return messages.error(request, '【启动错误】 ' + job_name + ' 任务不存在!')

    # 显示的文本，与django admin一致
    start_job.short_description = '启动'
    # icon，参考element-ui icon与https://fontawesome.com
    start_job.icon = 'el-icon-video-play'

    start_job.confirm = '你是否确定要启动？'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    start_job.type = 'danger'

    # 给按钮追加自定义的颜色
    start_job.style = 'color:black;'




    # 这里也省略一部分循环选择的页面数据的部分，根据下面代码可以还原出来
    # 就是根据选中的任务，从任务池中删除
    def stop_job(self, request, queryset):

        for item in queryset:

            job_id = item.id

            job_name = item.job_name

            decpet = item.decpet

            trigger_name = item.trigger_name

            job_state = item.job_state

            job_type = item.action_type

            job_rate = item.job_rate

            JobAction.stop_job(trigger_name + '-' + str(job_id))
            queryset.update(job_state=0)

    # 显示的文本，与django admin一致
    stop_job.short_description = '停止'
    # icon，参考element-ui icon与https://fontawesome.com
    stop_job.icon = 'el-icon-video-pause'

    stop_job.confirm = '你是否确定要停止？'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    stop_job.type = 'warning'

    # 给按钮追加自定义的颜色
    stop_job.style = 'color:black;'

    # 我们的项目中在点击保存按钮之后对数据就行了一定的处理，重写了save_model函数
    # 这里是在保存数据的时候，先判断任务状态是否是运行状态
    # 是的话，以任务触发器+‘_’+任务ID 为key，任务类型和新的策略存储在redis中；反之不进行操作。最后将修改后的数据存入数据库；
    def save_model(self, request, obj, form, change):
        from django.core.cache import cache
        if obj.job_state == 1:
            cache.set(obj.trigger_name + '-' + str(obj.id), (obj.action_type, obj.job_rate))
        obj.save()

    #----------演示用----
    def button_exeScript(self, request, queryset):
        pass

    button_exeScript.layer = {

        # 弹出层中的输入框配置

        # 这里指定对话框的标题

        'title': '弹出层输入框',

        # 提示信息

        'tips': '这个弹出对话框是需要在admin中进行定义，数据新增编辑等功能，需要自己来实现。',

        # 确认按钮显示文本

        'confirm_button': '确认提交',

        # 取消按钮显示文本

        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%

        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px

        'labelWidth': "80px",

        'params': [{

            # 这里的type 对应el-input的原生input属性，默认为input

            'type': 'input',

            # key 对应post参数中的key

            'key': 'name',

            # 显示的文本

            'label': '名称',

            # 为空校验，默认为False

            'require': True

        }, {

            'type': 'select',

            'key': 'type',

            'label': '类型',

            'width': '200px',

            # size对应elementui的size，取值为：medium  small  mini

            'size': 'small',

            # value字段可以指定默认值

            'value': '0',

            'options': [{

                'key': '0',

                'label': '收入'

            }, {

                'key': '1',

                'label': '支出'

            }]

        }, {

            'type': 'number',

            'key': 'money',

            'label': '金额',

            # 设置默认值

            'value': 1000

        }, {

            'type': 'date',

            'key': 'date',

            'label': '日期',

        }, {

            'type': 'datetime',

            'key': 'datetime',

            'label': '时间',

        }, {

            'type': 'rate',

            'key': 'star',

            'label': '评价等级'

        }, {

            'type': 'color',

            'key': 'color',

            'label': '颜色'

        }, {

            'type': 'slider',

            'key': 'slider',

            'label': '滑块'

        }, {

            'type': 'switch',

            'key': 'switch',

            'label': 'switch开关'

        }, {

            'type': 'input_number',

            'key': 'input_number',

            'label': 'input number'

        }, {

            'type': 'checkbox',

            'key': 'checkbox',

            # 必须指定默认值

            'value': [],

            'label': '复选框',

            'options': [{

                'key': '0',

                'label': '收入'

            }, {

                'key': '1',

                'label': '支出'

            }, {

                'key': '2',

                'label': '收益'

            }]

        }, {

            'type': 'radio',

            'key': 'radio',

            'label': '单选框',

            'options': [{

                'key': '0',

                'label': '收入'

            }, {

                'key': '1',

                'label': '支出'

            }, {

                'key': '2',

                'label': '收益'

            }]

        }]

    }

