from datetime import datetime
import requests
import re
import time

import 自动打卡.Sendmail


# 第一步：获取微信授权二维码的 URL
class GetQRCode:

    def __init__(self):
        # 微信授权二维码的 URL
        self.url = r"https://open.weixin.qq.com/connect/qrconnect?appid=wx4a23ae4b8f291087&scope=snsapi_login&redirect_uri=https%3A%2F%2Fi.jielong.com%2Flogin-callback&state=&login_type=jssdk&self_redirect=true&styletype=&sizetype=&bgcolor=&rst=&style=black&href=data:text/css;base64,Ci5pbXBvd2VyQm94IC5xcmNvZGUgewogIHdpZHRoOiAzMDBweDsKICBib3JkZXI6IG5vbmU7Cn0KLmltcG93ZXJCb3ggLnRpdGxlIHsKICBkaXNwbGF5OiBub25lOwp9Ci5pbXBvd2VyQm94IC5pbmZvIHsKICBkaXNwbGF5OiBub25lOwp9Ci5pbXBvd2VyQm94IC5xcmNvZGUgewogIG1hcmdpbi10b3A6IDBweCAhaW1wb3J0YW50Owp9Ci5zdGF0dXNfaWNvbiB7CiAgZGlzcGxheTogbm9uZTsKfQouanNfcXVpY2tfbG9naW4gewogIG1hcmdpbi10b3A6IDUwcHg7Cn0="
        self.payload = {}
        self.headers = {
            "pragma":
            "no-cache",
            "priority":
            "u=0, i",
            "sec-fetch-user":
            "?1",
            "upgrade-insecure-requests":
            "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
        }

    def _send_request(self, log_prefix):
        """请求微信授权二维码"""
        try:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 开始请求微信授权二维码 URL..."
            )
            response = requests.request("GET",
                                        self.url,
                                        headers=self.headers,
                                        data=self.payload)
            response.raise_for_status()
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 请求微信授权二维码 URL 成功"
            )
            return response
        except requests.RequestException as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 请求微信授权二维码 URL 时出错: {e}"
            )
            return None

    def _extract_qr_id(self, response, log_prefix):
        """提取extracted_value"""
        pattern = r'src=["\']/connect/qrcode/(\w+)["\']'
        match = re.search(pattern, response.text)
        if match:
            extracted_value = match.group(1)
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 成功获取到微信授权码的 extracted_value: {extracted_value}"
            )
            return extracted_value
        return None

    def getQRCodeEV(self, log_prefix):
        """获取微信授权码的 extracted_value"""
        # 首次请求
        response = self._send_request(log_prefix)
        if response:
            # 提取二维码 ID
            extracted_value = self._extract_qr_id(response, log_prefix)
            if extracted_value:
                return extracted_value
        # 未找到二维码 ID，进行重试
        print(
            f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 未找到微信授权码的 extracted_value 正在重新获取..."
        )
        for i in range(5):
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 第{i + 1}次重新请求 开始请求微信授权二维码 URL..."
            )
            response = self._send_request(log_prefix)
            if response:
                extracted_value = self._extract_qr_id(response, log_prefix)
                if extracted_value:
                    return extracted_value
            time.sleep(3)
            continue

        print(
            f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 已重试5次，仍未找到微信授权码的 extracted_value"
        )
        return None


# 第三步，获取 wx_code 属性值
class GetWx_code:

    def __init__(self, uuid):
        # 构建 13 位时间戳
        timestamp = int(time.time() * 1000)
        self.url = f"https://lp.open.weixin.qq.com/connect/l/qrconnect?uuid={uuid}&last=404&_={timestamp}"
        self.payload = {}
        self.headers = {
            "Host": "lp.open.weixin.qq.com",
            "Connection": "keep-alive",
            "sec-ch-ua":
            '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
            "sec-ch-ua-platform": '"Windows"',
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Dest": "script",
            "Referer":
            r"https://open.weixin.qq.com/connect/qrconnect?appid=wx4a23ae4b8f291087&scope=snsapi_login&redirect_uri=https%3A%2F%2Fi.jielong.com%2Flogin-callback&state=&login_type=jssdk&self_redirect=true&styletype=&sizetype=&bgcolor=&rst=&style=black&href=data:text/css;base64,Ci5pbXBvd2VyQm94IC5xcmNvZGUgewogIHdpZHRoOiAzMDBweDsKICBib3JkZXI6IG5vbmU7Cn0KLmltcG93ZXJCb3ggLnRpdGxlIHsKICBkaXNwbGF5OiBub25lOwp9Ci5pbXBvd2VyQm94IC5pbmZvIHsKICBkaXNwbGF5OiBub25lOwp9Ci5pbXBvd2VyQm94IC5xcmNvZGUgewogIG1hcmdpbi10b3A6IDBweCAhaW1wb3J0YW50Owp9Ci5zdGF0dXNfaWNvbiB7CiAgZGlzcGxheTogbm9uZTsKfQouanNfcXVpY2tfbG9naW4gewogIG1hcmdpbi10b3A6IDUwcHg7Cn0=",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

    # 轮询获取 token
    def getWx_code(self, receiver, log_prefix):
        start_time = time.time()
        print(
            f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 开始轮询获取 wx_code..."
        )  # 添加时间戳
        while time.time() - start_time < 300:
            try:
                response = requests.request("GET",
                                            self.url,
                                            headers=self.headers,
                                            data=self.payload)
                response.raise_for_status()  # 检查响应状态码
                if response.status_code == 200:
                    # 在响应体中获取 window.wx_code  属性值
                    if "window.wx_code" in response.text and len(
                            response.text) != len(
                                r"window.wx_errcode=408;window.wx_code='';"):
                        print(
                            f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: response.text:",
                            response.text,
                        )  # 添加时间戳
                        pattern = r"window\.wx_code='([^']*)'"
                        wx_code_match = re.search(pattern, response.text)
                        if wx_code_match:
                            wx_code = wx_code_match.group(1)
                            print(
                                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 成功获取到 wx_code: {wx_code}"
                            )  # 添加时间戳
                            return wx_code
            except requests.RequestException as e:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 请求获取 wx_code 时出错: {e}"
                )  # 添加时间戳
            time.sleep(5)
        print(
            f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 300 秒内未获取到 wx_code"
        )  # 添加时间戳
        send_mail = 自动打卡.Sendmail.Sendmail()
        send_mail.sendUnauthorizedMail(receiver, log_prefix)
        return None


# 第四步，获取 Token
class GetAuthorization:

    def __init__(self, code):
        self.url = f"https://i-api.jielong.com/api/User/OpenAuth?code={code}"
        self.payload = {}
        self.headers = {
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Accept": "*/*",
            "Host": "i-api.jielong.com",
            "Connection": "keep-alive",
        }

    def getToken(self, log_prefix):
        try:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 开始请求获取 Token..."
            )  # 添加时间戳
            response = requests.request("POST",
                                        self.url,
                                        headers=self.headers,
                                        data=self.payload)
            response.raise_for_status()  # 检查响应状态码
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 请求获取 Token 成功"
            )  # 添加时间戳

            # 解析 JSON 字符串
            data = response.json()
            # 获取 Token 字段的值
            token = data["Data"]["Token"]
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 成功获取到 Token: {token}"
            )  # 添加时间戳
            return token
        except requests.RequestException as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 请求获取 Token 时出错: {e}"
            )  # 添加时间戳
        except (KeyError, ValueError) as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {log_prefix}: 解析 Token 时出错: {e}"
            )  # 添加时间戳
            return None


def AllFlow(receiver, log_prefix):
    """获取 Token 全流程整合"""
    # 第一步：获取微信授权码的 extracted_value
    get_qr_code = GetQRCode()
    extracted_value = get_qr_code.getQRCodeEV(log_prefix)
    if extracted_value:
        # 第二步：发送邮件
        send_mail = 自动打卡.Sendmail.Sendmail()
        send_mail.sendAuthorizationMail(extracted_value, receiver, log_prefix)

        # 第三步：获取 wx_code 属性值
        get_wx_code = GetWx_code(extracted_value)
        wx_code = get_wx_code.getWx_code(receiver, log_prefix)
        if wx_code:
            # 第四步：获取并返回 Token
            get_authorization = GetAuthorization(wx_code)
            token = get_authorization.getToken(log_prefix)
            if token:
                return token
    return None
