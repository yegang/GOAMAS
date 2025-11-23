# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import encode_rfc2231
#--------------------------------------------------------------------
import logging
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
# 文件handler
#--------------------------------------------------------------------
root_dir = os.path.expanduser("~")
logdir = root_dir + "/log"
if os.path.exists(logdir):
    pass
    #print("日志目录存在")
else:
    print("日志目录" + logdir + "不存在")
    os.mkdir(logdir)

if os.path.exists(logdir):
    pass
else:
    print("创建日志目录" + logdir + "失败!")
    exit(1)
file_handler = logging.FileHandler(root_dir + "/log/" + python_filename + ".log")
print(root_dir + "/log/" + python_filename + ".log")
#--------------------------------------------------------------------
file_handler.setLevel(logging.INFO) # log等级的开关
file_handler.setFormatter(formatter)
# 添加到logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# 获取当前时间
def datetimestr():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_email_domain(mail_host: str) -> str:
    return ".".join(mail_host.split(".")[1:])




# 通用的邮件发送函数
def py_send_mail_html(to_list, sub, content, mail_host,mail_user,mail_pass,mail_sender, files=None, charset="utf-8"):
    """
    发送带附件的邮件。
    
    参数:
        to_list: 收件人列表或字符串，多个收件人用列表
        sub: 邮件主题
        content: 邮件正文
        files: 附件路径列表，可为空
        charset: 邮件内容的编码方式，默认 utf-8
    """

    mail_postfix = get_email_domain(mail_host)
    address = mail_user + "<" + mail_user + ">"

    logger.info(f"mail_host:{mail_host}")
    logger.info(f"mail_user:{mail_user}")
    logger.info(f"mail_pass:{mail_pass}")
    logger.info(f"mail_postfix:{mail_postfix}")
    logger.info(f"address:{address}")


    # 确保收件人是字符串形式
    to_str = ','.join(to_list) if isinstance(to_list, list) else to_list


    # message = MIMEText(content, 'plain', 'utf-8')
    # message['From'] = self.email_config['sender']
    # message['To'] = ",".join(self.email_config['receivers'])
    # message['Subject'] = self.email_config['title']


    
    # 构造多部分邮件
    msg = MIMEMultipart()
    msg['Subject'] = sub + ' ' + datetimestr()
    msg['From'] = address
    msg['To'] = to_str
    
    # 添加邮件正文
    body = MIMEText(content, _subtype="html", _charset=charset)
    msg.attach(body)
    
    # 添加附件
    if files:
        for file_path in files:
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)  # 编码附件
                    filename = os.path.basename(file_path)
                    part.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=encode_rfc2231(filename, charset)  # 编码中文附件名称
                    )
                    msg.attach(part)
            else:
                print(f"Warning: 文件 {file_path} 不存在，跳过该附件")

    # 发送邮件
    try:
        with smtplib.SMTP_SSL(mail_host, 465) as smtp:
            smtp.login(mail_user, mail_pass)
            smtp.sendmail(mail_sender, to_str, msg.as_string())
            print("Mail sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send mail: {e}")
        return False

######################################################
#       main
######################################################
def main():
    len_sys_argv = len(sys.argv)
    logger.info("参数个数len(sys.argv)=%d" % len_sys_argv )

    logger.info ("输出所有参数:")
    argv_num = 0
    for argv_num in range(0,len_sys_argv):
        now_argv = argv_num,sys.argv[argv_num]
        logger.info("%d sys.argv[%d]=%s" % (argv_num,argv_num,now_argv))
        argv_num = argv_num +1

    #设定参数个数
#####################
    len_sys_argv_std = 5
    len_sys_argv_practical = len_sys_argv -1
    if len_sys_argv_practical < len_sys_argv_std:
        logger.info ('参数个数必须 >= %d , 现值 = %d < %d' % (len_sys_argv_std,len_sys_argv_practical,len_sys_argv_std))
        logger.info (f"""
参数一:to_list
参数二:sub
参数三:content
参数四:attachments
参数五:字符集
python {python_filename}.py 00080@czcb.com.cn test_sub test_content a.txt,b.pdf,c.xlsx GB2312
""")
        sys.exit(1)

    # 从命令行接收输入
    email_string = sys.argv[1]  # 假设输入为 'example1@example.com, example2@example.com'
    # 按逗号分割并去除空格
    to_list = [email.strip() for email in email_string.split(',')]

    sub = sys.argv[2]
    content = sys.argv[3]

    # 从命令行接收输入
    file_string = sys.argv[4]  # 假设输入为 'example1@example.com, example2@example.com'
    # 按逗号分割并去除空格
    attachments  = [file.strip() for file in file_string.split(',')]

    charset = sys.argv[5]

    logger.info("%s %s %s %s" % (
        type(to_list),
        type(sub),
        type(content),
        type(attachments)
        )
    )
    logger.info("%s %s %s %s" % (to_list,sub,content,attachments))

#    # 调用函数示例
#    to_list = ["example1@example.com", "example2@example.com"]
#    sub = "测试邮件"
#    content = "这是邮件正文，支持 GB2312 编码"
#    files = ["test.txt", "report.pdf"]  # 附件路径列表

    py_send_mail_html(to_list, sub, content, attachments, charset)

if __name__ == '__main__':
    main()
