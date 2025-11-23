from django.db import models

# Create your models here.
class joblist(models.Model):
    decpet = models.CharField('描述decpet', max_length=255,default="")
    job_name = models.CharField('任务名称job_name', max_length=25,default="")
    trigger_name = models.CharField('触发器trigger_name', max_length=25,default="")
    type_choices = (('date', 'date'), ('cron', 'cron'))
    type_content = '''调度类型 对应 参数（执行频率）  例：<br/>
                    1、date：2025年9月20日 凌晨一点 执行任务<br/>参数值：2025-9-20 01:00:00 <br/>
                    2、cron：每天 凌晨两点 执行任务 (秒 分 时 日 月 星期 年)<br/>参数值：0 0 2 * * * *'''
    action_type = models.CharField('调度类型', choices=type_choices, max_length=25, default='cron')
    gender_choices = ((0, '停止'), (1, '启动'),)
    job_state = models.IntegerField('任务状态job_state', choices=gender_choices, default=0)
    job_rate = models.CharField(
        '执行频率job_rate',
        help_text=type_content,
        max_length=50,
        default=""
    )
    time = models.IntegerField('执行次数', default=0)
    func_name = models.CharField('程序名func_name', max_length=255,default="")
    args_list = models.CharField(
        '参数列表args_list',
        max_length=255,
        blank=False,
        default="",
        help_text='请输入 JSON 格式，例如：{"ip": "127.0.0.1", "param1": "abc"}'
    )

    def __str__(self):
        return self.decpet

    class Meta :
        verbose_name = '定时任务表'
        verbose_name_plural = verbose_name