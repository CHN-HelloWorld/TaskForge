from datetime import datetime
import smtplib
from email.mime.text import MIMEText


# 第二步，发送邮件
class Sendmail:
    def __init__(self):
        # 发件人
        self.sender = "your_email@qq.com"
        # 授权码（非密码）
        self.password = "your_auth_code"

    def send_email(self, Class, html_content, subject, receiver, log_prefix):
        """
        通用的邮件发送方法，减少代码重复
        :param html_content: 邮件的 HTML 内容
        :param subject: 邮件主题
        :param receiver: 收件人邮箱
        :param log_prefix: 日志前缀，用于区分不同线程的日志
        """
        # 创建邮件对象
        msg = MIMEText(html_content, "html", "utf-8")
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = receiver

        try:
            # 所有日志添加统一时间格式
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 开始连接邮件服务器..."
            )
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(self.sender, self.password)
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 成功连接并登录邮件服务器"
            )

            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 开始发送{Class}..."
            )
            server.sendmail(self.sender, [receiver], msg.as_string())
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: {Class}发送成功"
            )
        except Exception as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: {Class}发送失败: {e}"
            )
        finally:
            try:
                server.quit()
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 邮件服务器连接已关闭"
                )
            except NameError:
                pass

    def sendAuthorizationMail(self, extracted_value, receiver, log_prefix):
        """发送授权邮件"""
        # 构建 HTML 内容
        html_content = f"""
        <html>
          <body>
            <h1>您的 Token 已失效</h1>
            <h2 style="color: red;">注意，此二维码不支持微信相册扫一扫授权</h2>
            <p>请在 5 分钟内按照以下步骤重新扫描二维码授权，否则请等待 30 分钟后的邮件推送</p>
            <p>1.请通过截图保存此二维码</p>
            <p>2.将此二维码发送到其他设备上，并使用微信扫一扫授权</p>
            <img src="https://open.weixin.qq.com/connect/qrcode/{extracted_value}"   alt="二维码">
          </body>
        </html>
        """
        self.send_email(
            "授权邮件", html_content, "您的 Token 已失效", receiver, log_prefix
        )

    def sendUnauthorizedMail(self, receiver, log_prefix):
        """发送授权未成功邮件"""
        html_content = f"""
        <html>
          <body>
            <h1 style="color: red;">授权失败</h1>
            <p>您在规定的时间内未完成扫码授权，请等待下一次的邮件推送</p>
          </body>
        </html>
        """
        self.send_email(
            "授权未成功邮件", html_content, "授权失败", receiver, log_prefix
        )

    def sendSucceedMail(self, receiver, log_prefix):
        """发送打卡成功邮件"""
        html_content = f"""
        <html>
          <body>
            <h1 style="color: #90ee90;">打卡成功</h1>
            <p>您的打卡已成功，请及时查看</p>
          </body>
        </html>
        """
        self.send_email("打卡成功邮件", html_content, "打卡成功", receiver, log_prefix)

    def sendFailMail(self, receiver, log_prefix):
        """发送打卡失败邮件"""
        html_content = f"""
        <html>
          <body>
            <h1 style="color: red;">打卡失败</h1>
            <p>您的打卡失败，请自行打卡</p>
          </body>
        </html>
        """
        self.send_email("打卡失败邮件", html_content, "打卡失败", receiver, log_prefix)

    def sendEndlMail(self, receiver, log_prefix):
        """发送终止自动打卡服务邮件"""
        html_content = f"""
        <html>
          <body>
            <h1 style="color: red;">您的自动打卡服务已终止</h1>
            <p>抱歉，由于您在规定的时间内未进行授权操作，为缓解服务器压力，自动打卡服务将不在对您提供。</p>
            <p>若要重新订阅服务请联系管理员</p>
          </body>
        </html>
        """
        self.send_email(
            "终止自动打卡服务邮件",
            html_content,
            "您的自动打卡服务已终止",
            receiver,
            log_prefix,
        )
