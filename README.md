# TaskForge - 任务调度与自动打卡系统

## 项目简介

这是一个基于Python的任务调度与自动打卡通知系统，支持多用户并发打卡（打卡类型仅支持署名输入框+位置信息，若需其他的打卡类型请自行定制），通过邮件发送授权二维码和打卡结果通知。系统采用任务管理器架构，支持动态加载和卸载任务模块。

### 主要功能

- ✅ 自动定时打卡
- ✅ 多用户并发支持
- ✅ Token自动刷新机制
- ✅ 邮件通知（授权、成功、失败）
- ✅ 动态任务管理
- ✅ 线程安全的配置文件读写
- ✅ 失败重试机制

## 项目结构

```
TaskForge/
├── Main.py                 # 程序入口
├── config.json             # 任务配置文件
├── Task.py                 # 任务基类
├── Task1.py                # 打卡任务实现
├── TaskManager.py          # 任务管理器
└── 自动打卡/
    ├── __init__.py
    ├── MainRun.py          # 多用户打卡主流程
    ├── PunchCard.py        # 打卡核心逻辑
    ├── Sendmail.py         # 邮件发送模块
    ├── WechatTokenWorkflow.py  # 微信授权流程
    └── Tokens/             # 用户配置文件目录
        └── [用户名].json   # 用户配置文件
```

## 环境要求

- Python 3.7+
- 依赖库：
  - requests
  - smtplib (Python标准库)
  - json (Python标准库)
  - threading (Python标准库)

## 安装步骤

### 1. 克隆或下载项目

```bash
git clone https://github.com/CHN-HelloWorld/TaskForge.git
cd TaskForge
```

### 2. 安装依赖

```bash
pip install requests
```

### 3. 配置邮件服务

编辑 `自动打卡/Sendmail.py` 文件，修改邮件发送配置：

```python
class Sendmail:
    def __init__(self):
        self.sender = "your_email@qq.com"      # 发件人邮箱
        self.password = "your_auth_code"       # QQ邮箱授权码
```

**获取QQ邮箱授权码：**
1. 登录QQ邮箱
2. 设置 → 账户
3. 开启POP3/SMTP服务
4. 生成授权码

### 4. 配置用户信息

在 `自动打卡/Tokens/` 目录下创建用户配置文件，格式为：`[打卡名单中要打卡的用户名].json`

**配置文件示例：**

```json
{
    "Email": "user@example.com",
    "Token": "",
    "ThreadId": 123456789,
    "Location": {
        "coordinates": "{\"latitude\":45.98765432109876,\"longitude\":120.9865432109876}",
        "text": "xxx省•xx市•xx县(区)•xxx"
    }
}
```

**字段说明：**
- `Email`: 用户邮箱，用于接收通知
- `Token`: 微信授权Token（首次为空，系统自动获取）
- `ThreadId`: 打卡接龙ID(需自行抓包)
- `Location`: 打卡地理位置信息
  - `coordinates`: 经纬度坐标（JSON字符串格式,纬度在前，经度在后）
  - `text`: 地理位置描述(最终显示的地理位置仅取决于此字段,和经纬度坐标无关)

### 5. 配置任务

编辑 `config.json` 文件，添加需要运行的任务：

```json
["Task1"]
```

可选任务模块名称，多个任务用逗号分隔。

## 使用说明

### 启动程序

```bash
python Main.py
```

程序将以守护进程模式运行，每分钟检查一次任务执行条件。

### 查看日志

程序运行时会在控制台输出详细日志，包括：
- 任务加载信息
- 打卡执行状态
- Token刷新状态
- 邮件发送状态
- 错误信息

### 日志格式示例

```
[2025-10-31  21:30:00] xxx: 开始执行打卡操作
[2025-10-31  21:30:01] xxx: 打卡操作完成
[2025-10-31  21:30:02] xxx: 打卡成功
```

## 二次开发指南

### 1. 创建自定义任务

继承 `Task` 基类创建新任务：

```python
import Task

class Task5(Task.Task):
    def __init__(self):
        # 参数: 类名, 任务名称, 频率(天), 小时, 分钟, 是否一次性
        super().__init__(
            __class__.__name__,  # 类名，固定格式
            "我的任务",           # 任务名称
            1,                   # 任务频率，几天执行一次，这里为1天1次
            14,                  # 14点
            30,                  # 30分
            False                # 非一次性任务
        )
    
    def run(self):
        """实现任务逻辑"""
        print("执行我的自定义任务")
        # 在这里编写你的业务逻辑
```

**注意事项：**
- 文件名必须与类名一致（如 `Task5.py` 对应 `Task5` 类）
- 必须继承 `Task.Task` 基类
- 必须实现 `run()` 方法
- 保存在项目根目录

### 2. 注册任务

在 `config.json` 中添加任务模块名：

```json
["Task4", "Task5"]
```

### 3. 任务参数说明

```python
def __init__(self, Name, name, frequency, hour, minute, IsDisposable=False):
```

| 参数 | 类型 | 说明 |
|------|------|------|
| Name | str | 任务类名（模块名） |
| name | str | 任务显示名称 |
| frequency | int | 执行频率（天数） |
| hour | int | 执行小时（0-23） |
| minute | int | 执行分钟（0-59） |
| IsDisposable | bool | 是否一次性任务 |

### 4. 任务生命周期

```
TaskManager.Run()
    ↓
加载 config.json
    ↓
动态导入任务模块
    ↓
实例化任务对象（调用 __init__）
    ↓
每分钟调用 interceptor()
    ↓
检查执行时间
    ↓
调用 Run() → run()
    ↓
更新下次执行时间
```

### 5. 核心类说明

#### TaskManager（任务管理器）

**主要属性：**
```python
task_group = []              # 任务对象队列
module_names = []            # 任务模块名队列
loaded_task_group = []       # 已加载的任务类队列
remove_task_group = []       # 待删除的任务对象队列
```

**主要方法：**
- `Run()`: 主循环，负责任务调度
- `Remove()`: 清理已删除的任务

#### Task（任务基类）

**主要方法：**
- `__init__()`: 初始化任务参数
- `interceptor()`: 拦截器，判断是否执行任务
- `run()`: 任务逻辑（需子类实现）
- `Run()`: 执行封装，包含日志输出
- `updata_next_run_time()`: 更新下次执行时间

#### PunchCard（打卡核心）

**主要方法：**
- `BuildRequest()`: 构建打卡请求
- `RTS()`: 发送打卡请求
- `DuplicateToken()`: Token刷新机制
- `Main()`: 打卡主流程

### 6. 微信授权流程

```
获取二维码 UUID (GetQRCode)
    ↓
发送授权邮件 (Sendmail)
    ↓
轮询等待用户扫码 (GetWx_code)
    ↓
获取 wx_code
    ↓
换取 Token (GetAuthorization)
    ↓
保存到配置文件
```

### 7. 扩展打卡接口

修改 `PunchCard.py` 中的 `BuildRequest()` 方法：

```python
def BuildRequest(self):
    self.UpdataToken()
    self.url = "https://your-api-endpoint.com/api/punch"
    self.payload = json.dumps({
        # 自定义请求参数
        "user_id": self.Name,
        "location": self.Location
    })
    self.headers = {
        "Authorization": f"Bearer {self.Token}",
        "Content-Type": "application/json"
    }
```

### 8. 自定义邮件模板

修改 `Sendmail.py` 中的方法：

```python
def sendCustomMail(self, receiver, log_prefix):
    """发送自定义邮件"""
    html_content = f"""
    <html>
      <body>
        <h1>自定义标题</h1>
        <p>自定义内容</p>
      </body>
    </html>
    """
    self.send_email(
        "自定义邮件", 
        html_content, 
        "邮件主题", 
        receiver, 
        log_prefix
    )
```

### 9. 多用户配置

支持自动扫描 `自动打卡/Tokens/` 目录下的所有JSON配置文件，每个用户独立线程执行打卡任务。

**添加新用户：**
1. 在 `Tokens/` 目录创建 `[用户名].json`
2. 填写用户信息（Email、ThreadId、Location）
3. Token留空，系统自动获取
4. 重启程序或等待下一次任务执行

### 10. 错误处理

系统包含完善的异常处理机制：

- **Token失效**: 自动发送授权邮件，等待用户扫码
- **打卡失败**: 尝试刷新Token后重试
- **多次失败**: 发送终止服务邮件并删除配置文件
- **配置文件错误**: 跳过该用户并记录日志

### 11. 线程安全

配置文件读写使用线程锁保护：

```python
import threading
lock = threading.Lock()

def RJson(self):
    lock.acquire()
    try:
        # 读取操作
    finally:
        lock.release()
```

### 12. 开发建议

1. **日志规范**: 使用统一的日志格式 `[时间] 用户名: 操作信息`
2. **异常处理**: 所有外部调用都应包裹在 try-except 中
3. **配置验证**: 读取配置文件后验证必需字段是否存在
4. **测试隔离**: 开发时使用单独的测试配置文件
5. **代码复用**: 提取公共逻辑到独立函数或类

## 注意事项

⚠️ **重要提示：**

1. **隐私保护**: 不要将包含Token的配置文件上传到公开仓库
2. **邮箱安全**: 妥善保管QQ邮箱授权码
3. **合规使用**: 确保使用场景符合相关规定
4. **稳定性**: 建议在稳定的服务器上运行
5. **备份**: 定期备份配置文件
6. **更新**: 关注接龙平台接口变更

## 技术栈

- **语言**: Python 3.x
- **网络请求**: requests
- **邮件服务**: smtplib (SMTP_SSL)
- **并发处理**: threading
- **数据格式**: JSON
- **动态加载**: importlib

## 更新日志

### v2.3
- ✅ 支持多用户并发打卡
- ✅ 添加线程安全机制
- ✅ 优化日志输出格式
- ✅ 改进Token刷新策略
- ✅ 完善异常处理机制

## 贡献指南

欢迎提交Issue和Pull Request！

**开发流程：**
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 许可证： [MIT License (修改版)](LICENSE)

---

**感谢使用本项目！** 🎉

⚠️ **再次提醒：本项目仅供学习交流，请勿用于违反规章制度的用途，使用后果自负！**
