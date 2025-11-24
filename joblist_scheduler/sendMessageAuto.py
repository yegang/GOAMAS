import os
import sys
import lib.sendMail_html as sendMail_html

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 设置 Django 的 settings 模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goamas.settings")

import django

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GOAMAS.settings")
    django.setup()


from alertcontent.models import AlertContent

from config.models import (
    NotificationConfig,
    EmailConfig,
    QQConfig,
    WeixinConfig,
    StockMonitor
)


from config.config_loader import get_config

# 获取第一个全局配置，如果没有则默认关闭
email_config = EmailConfig.objects.first()
qq_config = QQConfig.objects.first()
weixin_config = WeixinConfig.objects.first()

email_enabled = getattr(NotificationConfig, "email_enabled", False)
qq_enabled = getattr(NotificationConfig, "qq_enabled", False)
weixin_enabled = getattr(NotificationConfig, "weixin_enabled", False)

def send_email(alert):
    print(f"[EMAIL] 发送告警: {alert.title}")
    # to_list, sub, content, mail_host,mail_user,mail_pass
    sendMail_html.py_send_mail_html(
        to_list=email_config.receivers,
        sub=alert.title,
        content=alert.content,
        mail_host= email_config.host,
        mail_user= email_config.user,
        mail_pass= email_config.password,
        mail_sender = email_config.sender,
    )


def send_qq(alert):
    print(f"[QQ] 发送告警: {alert.title}")

def send_weixin(alert):
    print(f"[WEIXIN] 发送告警: {alert.title}")

def process_alerts(category,severrity,source):
    print("开始处理启用的告警内容...")
    print(f"{category} {severrity} {source}")

    alerts = AlertContent.objects.filter(status="enabled")
    for alert in alerts:
        if email_enabled:
            send_email(alert)
        if qq_enabled:
            send_qq(alert)
        if weixin_enabled:
            send_weixin(alert)

    print("告警处理完成。")

# ③ 业务逻辑
def sendMessageAuto(category,severrity,source):
    #cfg = get_config()
    #print(cfg)
    process_alerts(category,severrity,source)

if __name__ == "__main__":
    '''
    param1 = kwargs.get("category")
    param2 = kwargs.get("severrity")
    param3 = kwargs.get("source")
    '''
    category = 1
    severrity =2
    source = 'system'

    sendMessageAuto(category,severrity,source)