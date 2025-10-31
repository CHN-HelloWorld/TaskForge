from datetime import datetime
import requests
import json

import 自动打卡.Sendmail
import 自动打卡.WechatTokenWorkflow
import time
import threading

# 创建一个锁对象
lock = threading.Lock()


class PunchCard:

    def __init__(self, Name):
        try:
            # 输出初始化开始的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {Name}: 开始初始化PunchCard对象"
            )
            self.Name = Name  # 在外边读取并传入
            data = self.RJson()
            self.Email = data["Email"]
            self.Token = data["Token"]
            self.ThreadId = data["ThreadId"]
            self.Location = data["Location"]
            self.url = ""
            self.payload = {}
            self.headers = {}
            # 输出初始化完成的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {Name}: PunchCard对象初始化完成"
            )
        except KeyError as e:
            # 输出配置文件中用户信息缺失的异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {Name}: 配置文件中缺少必要字段: {e}"
            )
        except Exception as e:
            # 输出初始化过程中的其他异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {Name}: 初始化PunchCard对象时出现异常: {e}"
            )

    def UpdataToken(self):
        """更新对象的Token属性，在构建请求体前自动执行"""
        try:
            # 输出更新Token开始的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 开始更新Token"
            )
            data = self.RJson()
            self.Token = data["Token"]
            self.ThreadId = data["ThreadId"]
            self.Location = data["Location"]
            # 输出更新Token完成的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: Token更新完成"
            )
        except KeyError as e:
            # 输出配置文件中用户信息缺失的异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 配置文件中缺少必要字段: {e}"
            )
        except Exception as e:
            # 输出更新Token过程中的其他异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 更新Token时出现异常: {e}"
            )

    def UpdateEmail(self):
        """更新对象的Email属性"""
        try:
            # 输出更新Email开始的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 开始更新Email"
            )
            data = self.RJson()
            self.Email = data["Email"]
            # 输出更新Email完成的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: Email更新完成"
            )
        except KeyError as e:
            # 输出配置文件中用户信息缺失的异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 配置文件中缺少必要字段: {e}"
            )
        except Exception as e:
            # 输出更新Email过程中的其他异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 更新Email时出现异常: {e}"
            )

    def BuildRequest(self):
        """构建请求体，在发送请求之前必须调用一次"""
        try:
            # 输出构建请求体开始的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 开始构建请求体"
            )
            self.UpdataToken()
            self.url = "https://h-api.jielong.co/api/CheckIn/EditRecord"
            self.payload = json.dumps({
                "Id":
                0,
                "ThreadId":
                self.ThreadId,
                "Number":
                "",
                "Signature":
                self.Name,
                "RecordValues": [{
                    "FieldId":
                    1,
                    "Values": [
                        self.Location["coordinates"]
                    ],
                    "Texts": [self.Location["text"]],
                    "Scores": [],
                    "Files": [],
                    "MatrixValues": [],
                    "CustomTableValues": [],
                    "FillInMatrixFieldValues": [],
                    "MatrixFormValues": [],
                    "HasValue":
                    True,
                }],
                "DateTarget":
                "",
                "IsNeedManualAudit":
                False,
                "MinuteTarget":
                -1,
                "IsNameNumberComfirm":
                False,
            })
            self.headers = {
                "Authorization": "Bearer %s" % self.Token,
                "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Host": "h-api.jielong.co",
                "Connection": "keep-alive",
            }
            # 输出构建请求体完成的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 请求体构建完成"
            )
        except Exception as e:
            # 输出构建请求体过程中的异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 构建请求体时出现异常: {e}"
            )

    def RJson(self):
        """读取JSON文件内的信息"""
        try:
            # 获取锁
            lock.acquire()
            # 输出读取JSON文件开始的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 开始读取配置文件"
            )
            file_path = f"自动打卡/Tokens/{self.Name}.json"
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            # 输出读取JSON文件完成的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 配置文件读取完成"
            )
            return data
        except FileNotFoundError:
            # 输出文件未找到的异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 未找到配置文件 {self.Name}.json"
            )
        except json.JSONDecodeError:
            # 输出JSON解析错误的异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 配置文件格式错误，无法解析"
            )
        except Exception as e:
            # 输出读取JSON文件过程中的其他异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 读取配置文件时出现异常: {e}"
            )
        finally:
            # 释放锁
            lock.release()
        return {}

    def WJson(self, data):
        """更新Json文件内的信息"""
        try:
            # 获取锁
            lock.acquire()
            # 输出更新JSON文件开始的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 开始更新配置文件"
            )
            file_path = f"自动打卡/Tokens/{self.Name}.json"
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            # 输出更新JSON文件完成的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 配置文件更新完成"
            )
        except FileNotFoundError:
            # 输出文件未找到的异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 未找到配置文件 {self.Name}.json"
            )
        except Exception as e:
            # 输出更新JSON文件过程中的其他异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 更新配置文件时出现异常: {e}"
            )
        finally:
            # 释放锁
            lock.release()

    def UpdataJsonToken(self, Token):
        """更新JSON文件内此对象的Token"""
        try:
            # 输出更新JSON文件中Token开始的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 开始更新配置文件中的Token"
            )
            data = self.RJson()
            data["Token"] = Token
            self.WJson(data)
            # 输出更新JSON文件中Token完成的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 配置文件中的Token更新完成"
            )
        except KeyError as e:
            # 输出配置文件中用户信息缺失的异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 配置文件中缺少必要字段: {e}"
            )
        except Exception as e:
            # 输出更新JSON文件中Token过程中的其他异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 更新配置文件中的Token时出现异常: {e}"
            )

    def RTS(self):
        """打卡，根据最新的信息重新构建请求体+发送请求"""
        try:
            # 输出打卡开始的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 开始打卡操作"
            )
            self.BuildRequest()
            response = requests.request("POST",
                                        self.url,
                                        headers=self.headers,
                                        data=self.payload)
            response.raise_for_status()
            # 输出打卡完成的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 打卡操作完成"
            )
            return response
        except requests.RequestException as e:
            # 输出请求异常的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 打卡请求时出现异常: {e}"
            )
        except Exception as e:
            # 输出打卡过程中的其他异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 打卡操作时出现异常: {e}"
            )
        return None

    def DuplicateToken(self):
        """对于获取Token失败时，重新发送授权邮件获取Token，获取成功返回True，失败返回False"""
        try:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 开始重新获取Token"
            )
            self.UpdateEmail()
            Token = 自动打卡.WechatTokenWorkflow.AllFlow(self.Email,
                                                     self.Name)  # 21:30邮件到
            attempts = 0
            while Token is None and attempts < 6:
                # 根据尝试次数动态调整等待时间
                if attempts < 2:  # 第1-2次等待25分钟
                    wait_time = 1500
                elif attempts == 2:  # 第3次等待10小时25分钟（跨天逻辑）
                    自动打卡.Sendmail.Sendmail().sendFailMail(
                        self.Email, self.Name)  # 提醒用户手动打卡
                    wait_time = 37500  # 10h25m=37500秒 [5]()
                else:  # 第4-5次等待1小时
                    wait_time = 3600

                time.sleep(wait_time)
                self.UpdateEmail()
                Token = 自动打卡.WechatTokenWorkflow.AllFlow(self.Email, self.Name)
                attempts += 1

            if Token is None:
                # 最终失败处理（对应原函数次日12:05逻辑）
                自动打卡.Sendmail.Sendmail().sendEndlMail(self.Email, self.Name)
                # 删除该用户的配置文件
                import os
                try:
                    os.remove(f"自动打卡/Tokens/{self.Name}.json")
                except Exception as e:
                    print(f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 删除配置文件失败: {e}")
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 重新获取Token失败，自动打卡服务终止"
                )
                return False

            self.UpdataJsonToken(Token)
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 重新获取Token成功"
            )
            return True
        except Exception as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 重新获取Token时出现异常: {e}"
            )
            return False

    def Main(self):
        """打卡主流程"""
        try:
            # 输出主流程开始的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 开始执行打卡主流程"
            )
            if self.Token == "":  # JSON文件内的Token如果为空则先获取Token
                isRun = (self.DuplicateToken())  # 最终还是未获取到Token，则直接退出整个程序
                if isRun == False:
                    return

            response = self.RTS()
            if (response and response.json().get("Data") == "打卡成功"
                    and response.json().get("Description") == "打卡成功"):
                # 发送打卡成功邮件
                自动打卡.Sendmail.Sendmail().sendSucceedMail(self.Email, self.Name)
            else:
                # 首先更新token，然后再次尝试打卡
                if self.DuplicateToken():
                    response = self.RTS()
                    if (response and response.json().get("Data") == "打卡成功"
                            and response.json().get("Description") == "打卡成功"):
                        # 发送打卡成功邮件
                        自动打卡.Sendmail.Sendmail().sendSucceedMail(
                            self.Email, self.Name)
                    else:
                        # 发送打卡失败邮件
                        自动打卡.Sendmail.Sendmail().sendFailMail(
                            self.Email, self.Name)
            # 输出主流程完成的日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 打卡主流程执行完成"
            )
        except ValueError:
            # 输出JSON解析错误的异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 解析响应JSON数据时出现错误"
            )
        except Exception as e:
            # 输出主流程执行过程中的其他异常日志
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {self.Name}: 执行打卡主流程时出现异常: {e}"
            )
