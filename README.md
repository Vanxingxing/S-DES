# S-DES
本项目基于 Python 语言与 Tkinter GUI 框架（Python 内置，无需额外安装），实现 S-DES 全功能加密系统。
# 项目简介
本项目实现了 S-DES 算法的完整功能，包括：  
· 字符串 / 8 位二进制数据的加解密​  
· 多线程密钥暴力破解（遍历 1024 种 10 位密钥）​  
· 直观的可视化操作界面（输入、按钮、结果日志一体化）​  
· 自动处理数据填充（确保输入长度为 8 的倍数）
# 环境要求
依赖项  | 版本要求  | 说明
------------- | ------------- | -------------
Python  | 3.6 及以上  | Tkinter 为 Python 内置库，无需额外安装
第三方库  | 无  | 纯 Python 原生实现，无需pip install任何依赖
# 快速启动
*获取代码*  
· 将用户提供的完整代码保存为 Python 文件（建议命名为sdes_tkinter.py）​  
· 确保文件编码为UTF-8（避免中文乱码）
*运行程序*  
打开终端 / 命令提示符，进入代码所在目录，执行以下命令：
`python sdes_tkinter.py`  
启动后将自动弹出 GUI 窗口，无需任何额外配置。  
# 核心功能与使用指南
*界面布局说明*  
GUI 窗口分为 5 个核心区域，操作逻辑清晰：  
区域       | 位置         | 功能                                                         
---------- | ------------ | ------------------------------------------------------------ 
明文输入区 | 顶部第一行   | 输入待加密的字符串（如 “Hello S - DES”）
密钥输入区 | 顶部第二行   | 输入至少 2 个字符（自动提取前 10 位二进制作为密钥）
密文输入区 | 顶部第三行   | 显示加密结果，或输入待解密的密文                             
功能按钮区 | 中间         | 包含 “加密”“解密”“暴力破解”“清空” 4 个操作按钮               
结果日志区 | 底部         | 显示操作过程、结果、耗时等详细信息（带滚动条）  
# 代码结构解析
`# 核心类结构
class SDES:  # 算法核心类（无GUI依赖，可独立调用）
    def __init__(self):  # 初始化：定义所有置换盒、S盒参数
        self.P10 = [3,5,2,7,4,10,1,9,8,6]  # 10位密钥置换表
        self.P8 = [6,3,7,4,8,5,10,9]       # 8位密钥选择表
        self.IP = [2,6,3,1,4,8,5,7]        # 初始置换表
        self.IP_inv = [4,1,3,5,7,2,8,6]    # 最终置换表
        self.EP = [4,1,2,3,2,3,4,1]        # 扩展置换表
        self.P4 = [2,4,3,1]                # 4位置换表
        self.S0/S1 = [...]                 # S盒替换表
        self.LS1/LS2 = [...]               # 左移参数
    
    # 核心方法（按执行流程）
    def permute(self):        # 通用置换操作
    def left_shift(self):     # 循环左移
    def generate_keys(self):  # 生成K1、K2轮密钥
    def xor(self):            # 逐位异或
    def s_box_lookup(self):   # S盒替换
    def f_function(self):     # 轮函数F
    def encrypt_block(self):  # 8位数据块加密
    def decrypt_block(self):  # 8位数据块解密
    def string_to_bits(self): # 字符串转二进制列表
    def bits_to_string(self): # 二进制列表转字符串
    def encrypt_string(self): # 字符串加密（多块处理）
    def decrypt_string(self): # 字符串解密（多块处理）
    def brute_force_attack(self): # 多线程暴力破解

class SDESGUI:  # GUI交互类（依赖Tkinter）
    def __init__(self, master):  # 初始化窗口
    def setup_gui(self):         # 构建界面（输入框、按钮、日志区）
    def encrypt(self):           # 加密按钮点击事件
    def decrypt(self):           # 解密按钮点击事件
    def brute_force(self):       # 暴力破解按钮点击事件
    def clear(self):             # 清空按钮点击事件
    def log_result(self):        # 日志输出`

