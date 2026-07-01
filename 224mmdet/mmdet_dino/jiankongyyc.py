import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import subprocess
import time
# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "e1029384756abc@qq.com"  # 用户名
mail_pass = "dufjgrjajmmkdeaa"  # 密码或授权码

sender = 'e1029384756abc@qq.com'  # 发送邮箱
receivers = ['2865244661@qq.com']  # 接收邮箱

# 邮件主题，邮件内容
def send_mail(title, message):
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(message, 'plain', 'utf-8')
    
    # 设置带有昵称的 'From' 字段，昵称包含中文并使用 Base64 编码
    from_name = "yyc"  # 这是中文昵称，可以自定义
    message['From'] = formataddr((str(Header(from_name, 'utf-8')), sender))
    
    # 直接使用邮箱地址作为 'To' 字段
    message['To'] = formataddr((str(Header("接收者", 'utf-8')), receivers[0]))
    
    # 设置邮件主题
    message['Subject'] = Header(title, 'utf-8')

    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()
def get_gpu_memory():
	result = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.free', '--format=csv,nounits,noheader'])
	result = result.decode('utf-8').strip()
	free_memory = [int(x) for x in result.split('\n')]
	return free_memory   


while True:
    free_mem = get_gpu_memory()
    # print(free_mem[0])
    # print(free_mem[1])
    if free_mem[1] >= 20000 and free_mem[0] >= 20000 and free_mem[2] >= 20000 and free_mem[3] >= 20000:
        time.sleep(200) # make sure
        if free_mem[1] >= 20000 and free_mem[0] >= 20000 and free_mem[2] >= 20000 and free_mem[3] >= 20000:
            # 发送邮件
            send_mail('224服务器显存监控', f'显存空余：GPU0: {free_mem[0]} Mb; GPU1: {free_mem[1]} Mb，该跑模型啦！！')
            break
    time.sleep(600) # 每10分钟查询一次
print(">>>>>>邮件已经发送，想要再次监控请重新运行此程序-_-")
