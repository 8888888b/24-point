import tkinter as tk
from tkinter import messagebox, ttk
import itertools
import math
import os
from datetime import datetime

# 可用操作
OPERATORS = ['+', '-', '*', '/', '**', 'sqrt', '-']

# 创建日志文件
def create_log(status):
    log_dir = ".temp"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    log_filename = f"{timestamp}_0001.log"
    log_filepath = os.path.join(log_dir, log_filename)

    log_content = {
        "Run_time": now.strftime("%Y.%m.%d_%H:%M:%S"),
        "How_to_run": status,
        "User": os.getenv('USERNAME', os.getenv('USER', 'unknown_user'))
    }

    with open(log_filepath, 'w', encoding='utf-8') as log_file:
        log_file.write(str(log_content))

# 计算所有可能的操作
def calc_possible_results(nums, only_basic_ops=False):
    operations = OPERATORS[:4] if only_basic_ops else OPERATORS  # 如果只使用加减乘除
    solutions = set()  # 使用集合来避免重复解法

    # 判断一个表达式结果是否等于24且为整数
    def is_valid_result(result):
        return result == 24 and isinstance(result, int)

    # 所有数字的排列组合
    for nums_perm in itertools.permutations(nums):
        # 生成操作符组合
        for ops in itertools.product(operations, repeat=3):
            # 使用四则运算
            expr = f"({nums_perm[0]} {ops[0]} {nums_perm[1]}) {ops[1]} ({nums_perm[2]} {ops[2]} {nums_perm[3]})"
            try:
                result = eval(expr)
                if is_valid_result(result):
                    solutions.add(expr.replace("**", "^").replace("sqrt", "√"))
            except ZeroDivisionError:  # 防止除以零
                continue
            except:
                continue

    return list(solutions)  # 将集合转回列表，以便显示

# 处理"→"键，自动切换焦点
def move_focus(event, next_entry):
    next_entry.focus()

# 处理"←"键，自动切换焦点
def move_focus_back(event, prev_entry):
    prev_entry.focus()

# 清空输入框
def clear_entries():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)
    entry4.delete(0, tk.END)

# 清除缓存（删除.temp目录下所有日志文件）
def clear_cache():
    log_dir = ".temp"
    if os.path.exists(log_dir):
        for file in os.listdir(log_dir):
            os.remove(os.path.join(log_dir, file))
        messagebox.showinfo("清除缓存", "缓存已清除")
    else:
        messagebox.showinfo("清除缓存", "没有缓存可清除")

# 界面构建
def solve():
    try:
        nums = list(map(int, [entry1.get(), entry2.get(), entry3.get(), entry4.get()]))  # 强制转换为整数
        only_basic_ops = basic_ops_var.get()

        if any(num <= 0 for num in nums): 
            messagebox.showerror("输入错误", "请输入有效的正整数！")
            return

        solutions = calc_possible_results(nums, only_basic_ops)
        if solutions:
            result_text = "\n".join(solutions)  # 组合所有解法，按行显示
            result_text = "找到解法：\n" + result_text  # 结果前加标题
            result_label.delete(1.0, tk.END)  # 清空显示区域
            result_label.insert(tk.END, result_text)  # 插入新结果
            create_log(1)  # 正常运行
        else:
            result_label.delete(1.0, tk.END)  # 清空显示区域
            result_label.insert(tk.END, "没有找到解法")
            create_log(1)  # 正常运行

    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的整数！")
        create_log(0)  # 非正常运行

# 创建窗口
window = tk.Tk()
window.title("24点求解器")
window.geometry("600x600")
window.config(bg="#f4f4f9")  # 设置背景颜色

# 添加滚动条框架
main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# 标题标签
title_label = tk.Label(scrollable_frame, text="24点求解器", font=("Arial", 24, "bold"), bg="#f4f4f9", fg="#333333")
title_label.grid(row=0, columnspan=4, pady=20)

# 输入框
entry1 = tk.Entry(scrollable_frame, width=10, font=("Arial", 14), bd=2, relief="solid", justify="center")
entry1.grid(row=1, column=0, padx=10, pady=10)
entry2 = tk.Entry(scrollable_frame, width=10, font=("Arial", 14), bd=2, relief="solid", justify="center")
entry2.grid(row=1, column=1, padx=10, pady=10)
entry3 = tk.Entry(scrollable_frame, width=10, font=("Arial", 14), bd=2, relief="solid", justify="center")
entry3.grid(row=1, column=2, padx=10, pady=10)
entry4 = tk.Entry(scrollable_frame, width=10, font=("Arial", 14), bd=2, relief="solid", justify="center")
entry4.grid(row=1, column=3, padx=10, pady=10)

# 为每个输入框绑定“→”键事件，切换焦点
entry1.bind("<Right>", lambda event: move_focus(event, entry2))
entry2.bind("<Right>", lambda event: move_focus(event, entry3))
entry3.bind("<Right>", lambda event: move_focus(event, entry4))
entry4.bind("<Right>", lambda event: move_focus(event, entry1))  # 最后一个回到第一个输入框

# 为每个输入框绑定“←”键事件，切换焦点
entry1.bind("<Left>", lambda event: move_focus_back(event, entry4))  # 第一个回到最后一个输入框
entry2.bind("<Left>", lambda event: move_focus_back(event, entry1))
entry3.bind("<Left>", lambda event: move_focus_back(event, entry2))
entry4.bind("<Left>", lambda event: move_focus_back(event, entry3))

# 选择框（只用加减乘除）
basic_ops_var = tk.IntVar()
basic_ops_check = tk.Checkbutton(scrollable_frame, text="只用加减乘除", variable=basic_ops_var, font=("Arial", 12), bg="#f4f4f9")
basic_ops_check.grid(row=2, columnspan=4)

# 求解按钮
solve_button = tk.Button(scrollable_frame, text="求解", command=solve, font=("Arial", 16), fg="white", bg="#4CAF50", relief="flat", width=20, height=2)
solve_button.grid(row=3, columnspan=4, pady=20)

# 清空按钮
clear_button = tk.Button(scrollable_frame, text="清空", command=clear_entries, font=("Arial", 16), fg="white", bg="#f44336", relief="flat", width=20, height=2)
clear_button.grid(row=4, columnspan=4, pady=10)

# 结果显示区域（Text控件）
result_label = tk.Text(scrollable_frame, width=60, height=15, wrap=tk.WORD, font=("Arial", 12), bd=2, relief="solid", bg="#f9f9f9")
result_label.grid(row=5, columnspan=4, padx=10, pady=10)

# 清除缓存按钮
clear_cache_button = tk.Button(scrollable_frame, text="清除缓存", command=clear_cache, font=("Arial", 16), fg="white", bg="#FF5722", relief="flat", width=20, height=2)
clear_cache_button.grid(row=6, columnspan=4, pady=10)

# 运行日志创建函数
create_log(1)  # 正常运行

# 运行主循环
window.mainloop()
