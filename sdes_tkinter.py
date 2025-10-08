import itertools
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk


class SDES:
    def __init__(self):
        # 定义所有置换盒和S盒
        self.P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.IP = [2, 6, 3, 1, 4, 8, 5, 7]
        self.IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
        self.EP = [4, 1, 2, 3, 2, 3, 4, 1]
        self.P4 = [2, 4, 3, 1]

        self.S0 = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 0, 2]
        ]

        self.S1 = [
            [0, 1, 2, 3],
            [2, 3, 1, 0],
            [3, 0, 1, 2],
            [2, 1, 0, 3]
        ]

        self.LS1 = [2, 3, 4, 5, 1]  # 左移1位
        self.LS2 = [3, 4, 5, 1, 2]  # 左移2位

    def permute(self, bits, permutation):
        """执行置换操作"""
        return [bits[i - 1] for i in permutation]

    def left_shift(self, bits, shift_table):
        """执行左移操作"""
        return [bits[i - 1] for i in shift_table]

    def generate_keys(self, key):
        """生成两个子密钥k1和k2"""
        # P10置换
        p10_key = self.permute(key, self.P10)

        # 分割成左右两部分
        left = p10_key[:5]
        right = p10_key[5:]

        # 生成k1：左移1位 + P8置换
        left_ls1 = self.left_shift(left, self.LS1)
        right_ls1 = self.left_shift(right, self.LS1)
        k1 = self.permute(left_ls1 + right_ls1, self.P8)

        # 生成k2：左移2位 + P8置换
        left_ls2 = self.left_shift(left_ls1, self.LS2)
        right_ls2 = self.left_shift(right_ls1, self.LS2)
        k2 = self.permute(left_ls2 + right_ls2, self.P8)

        return k1, k2

    def xor(self, bits1, bits2):
        """执行异或操作"""
        return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

    def s_box_lookup(self, bits, s_box):
        """S盒查找"""
        row = bits[0] * 2 + bits[3]  # 第1位和第4位决定行
        col = bits[1] * 2 + bits[2]  # 第2位和第3位决定列
        value = s_box[row][col]
        return [(value >> 1) & 1, value & 1]

    def f_function(self, right, key):
        """轮函数F"""
        # 扩展置换
        expanded = self.permute(right, self.EP)

        # 与密钥异或
        xor_result = self.xor(expanded, key)

        # S盒替换
        left_s = self.s_box_lookup(xor_result[:4], self.S0)
        right_s = self.s_box_lookup(xor_result[4:], self.S1)

        # P4置换
        s_result = left_s + right_s
        return self.permute(s_result, self.P4)

    def encrypt_block(self, plaintext, key):
        """加密一个8位数据块"""
        k1, k2 = self.generate_keys(key)

        # 初始置换
        ip_text = self.permute(plaintext, self.IP)

        # 第一轮：F函数 + SW
        left, right = ip_text[:4], ip_text[4:]
        f_result = self.f_function(right, k1)
        new_left = self.xor(left, f_result)

        # 交换
        swapped = right + new_left

        # 第二轮：F函数
        left2, right2 = swapped[:4], swapped[4:]
        f_result2 = self.f_function(right2, k2)
        new_left2 = self.xor(left2, f_result2)

        # 最终置换
        final = new_left2 + right2
        return self.permute(final, self.IP_inv)

    def decrypt_block(self, ciphertext, key):
        """解密一个8位数据块"""
        k1, k2 = self.generate_keys(key)

        # 初始置换
        ip_text = self.permute(ciphertext, self.IP)

        # 第一轮：F函数 + SW
        left, right = ip_text[:4], ip_text[4:]
        f_result = self.f_function(right, k2)
        new_left = self.xor(left, f_result)

        # 交换
        swapped = right + new_left

        # 第二轮：F函数
        left2, right2 = swapped[:4], swapped[4:]
        f_result2 = self.f_function(right2, k1)
        new_left2 = self.xor(left2, f_result2)

        # 最终置换
        final = new_left2 + right2
        return self.permute(final, self.IP_inv)

    def binary_string_to_bits(self, binary_str):
        """将二进制字符串转换为比特列表"""
        return [int(bit) for bit in binary_str if bit in '01']

    def bits_to_binary_string(self, bits):
        """将比特列表转换为二进制字符串"""
        return ''.join(str(bit) for bit in bits)

    def encrypt_binary(self, plaintext_binary, key_binary):
        """直接加密二进制字符串"""
        plaintext_bits = self.binary_string_to_bits(plaintext_binary)
        key_bits = self.binary_string_to_bits(key_binary)

        if len(plaintext_bits) != 8:
            raise ValueError("明文必须是8位二进制")
        if len(key_bits) != 10:
            raise ValueError("密钥必须是10位二进制")

        cipher_bits = self.encrypt_block(plaintext_bits, key_bits)
        return self.bits_to_binary_string(cipher_bits)

    def decrypt_binary(self, ciphertext_binary, key_binary):
        """直接解密密文二进制字符串"""
        ciphertext_bits = self.binary_string_to_bits(ciphertext_binary)
        key_bits = self.binary_string_to_bits(key_binary)

        if len(ciphertext_bits) != 8:
            raise ValueError("密文必须是8位二进制")
        if len(key_bits) != 10:
            raise ValueError("密钥必须是10位二进制")

        plain_bits = self.decrypt_block(ciphertext_bits, key_bits)
        return self.bits_to_binary_string(plain_bits)

    def brute_force_attack(self, plaintext, ciphertext, max_threads=4):
        """暴力破解密钥"""
        found_keys = []
        lock = threading.Lock()

        def check_keys(key_range):
            sdes = SDES()
            for key_bits in key_range:
                try:
                    encrypted = sdes.encrypt_block(plaintext, key_bits)
                    if encrypted == ciphertext:
                        with lock:
                            found_keys.append(key_bits)
                except:
                    continue

        all_keys = list(itertools.product([0, 1], repeat=10))
        chunk_size = len(all_keys) // max_threads
        threads = []

        start_time = time.time()

        for i in range(max_threads):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < max_threads - 1 else len(all_keys)
            thread = threading.Thread(target=check_keys, args=(all_keys[start:end],))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()

        return found_keys, end_time - start_time


class SDESGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("S-DES加密系统")
        self.master.geometry("600x500")
        self.sdes = SDES()
        self.setup_gui()

    def setup_gui(self):
        """设置GUI界面"""
        # 标题
        title_label = tk.Label(self.master, text="S-DES加密系统", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # 明文输入
        tk.Label(self.master, text="明文:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.plaintext_entry = tk.Entry(self.master, width=50)
        self.plaintext_entry.grid(row=1, column=1, padx=5, pady=5)

        # 密钥输入
        tk.Label(self.master, text="密钥:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.key_entry = tk.Entry(self.master, width=50)
        self.key_entry.grid(row=2, column=1, padx=5, pady=5)

        # 密文输出
        tk.Label(self.master, text="密文:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.ciphertext_entry = tk.Entry(self.master, width=50)
        self.ciphertext_entry.grid(row=3, column=1, padx=5, pady=5)

        # 按钮框架
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(button_frame, text="加密", command=self.encrypt, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="解密", command=self.decrypt, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="暴力破解", command=self.brute_force, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="清空", command=self.clear, width=10).pack(side=tk.LEFT, padx=5)

        # 结果显示
        tk.Label(self.master, text="操作结果:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.result_text = tk.Text(self.master, height=12, width=70)
        self.result_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        scrollbar = tk.Scrollbar(self.master, command=self.result_text.yview)
        scrollbar.grid(row=6, column=2, sticky=tk.NS)
        self.result_text.config(yscrollcommand=scrollbar.set)

    def encrypt(self):
        """加密操作"""
        try:
            plaintext = self.plaintext_entry.get().strip()
            key = self.key_entry.get().strip()

            # 输入验证
            if len(plaintext) != 8 or not all(bit in '01' for bit in plaintext):
                messagebox.showerror("错误", "明文必须是8位二进制数 (0和1)")
                return

            if len(key) != 10 or not all(bit in '01' for bit in key):
                messagebox.showerror("错误", "密钥必须是10位二进制数 (0和1)")
                return

            # 加密
            ciphertext = self.sdes.encrypt_binary(plaintext, key)

            # 显示结果
            self.ciphertext_entry.delete(0, tk.END)
            self.ciphertext_entry.insert(0, ciphertext)

            self.log_result(f"加密成功!\n明文: {plaintext}\n密钥: {key}\n密文: {ciphertext}")

        except Exception as e:
            messagebox.showerror("错误", f"加密失败: {str(e)}")

    def decrypt(self):
        """解密操作"""
        try:
            ciphertext = self.ciphertext_entry.get().strip()
            key = self.key_entry.get().strip()

            # 输入验证
            if len(ciphertext) != 8 or not all(bit in '01' for bit in ciphertext):
                messagebox.showerror("错误", "密文必须是8位二进制数 (0和1)")
                return

            if len(key) != 10 or not all(bit in '01' for bit in key):
                messagebox.showerror("错误", "密钥必须是10位二进制数 (0和1)")
                return

            # 解密
            plaintext = self.sdes.decrypt_binary(ciphertext, key)

            # 显示结果
            self.plaintext_entry.delete(0, tk.END)
            self.plaintext_entry.insert(0, plaintext)

            self.log_result(f"解密成功!\n密文: {ciphertext}\n密钥: {key}\n明文: {plaintext}")

        except Exception as e:
            messagebox.showerror("错误", f"解密失败: {str(e)}")

    def brute_force(self):
        """暴力破解"""
        try:
            plaintext = self.plaintext_entry.get().strip()
            ciphertext = self.ciphertext_entry.get().strip()

            if not plaintext or not ciphertext:
                messagebox.showerror("错误", "需要提供明文和密文")
                return

            # 输入验证
            if len(plaintext) != 8 or not all(bit in '01' for bit in plaintext):
                messagebox.showerror("错误", "明文必须是8位二进制数")
                return

            if len(ciphertext) != 8 or not all(bit in '01' for bit in ciphertext):
                messagebox.showerror("错误", "密文必须是8位二进制数")
                return

            # 转换为比特
            plain_bits = self.sdes.binary_string_to_bits(plaintext)
            cipher_bits = self.sdes.binary_string_to_bits(ciphertext)

            self.log_result("开始暴力破解...请等待")
            self.master.update()

            keys, time_taken = self.sdes.brute_force_attack(plain_bits, cipher_bits)

            if keys:
                result = f"暴力破解完成! 用时: {time_taken:.4f}秒\n找到 {len(keys)} 个匹配密钥:\n"
                for i, key in enumerate(keys):
                    key_str = ''.join(str(bit) for bit in key)
                    result += f"密钥{i + 1}: {key_str}\n"
                self.log_result(result)
            else:
                self.log_result(f"暴力破解完成! 用时: {time_taken:.4f}秒\n未找到匹配的密钥")

        except Exception as e:
            messagebox.showerror("错误", f"暴力破解失败: {str(e)}")

    def clear(self):
        """清空所有输入"""
        self.plaintext_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.ciphertext_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)

    def log_result(self, message):
        """在结果区域显示消息"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, message)


def main():
    # 启动GUI
    root = tk.Tk()
    app = SDESGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()