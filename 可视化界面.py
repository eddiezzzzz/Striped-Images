# 支持灰度及RGB图像，但只支持jpg和png格式
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import numpy as np
from tkinter import ttk
import time

def add_vertical_noise(input_folder, output_folder, num_augmentations, noise_intensity, progress_var):
    # 获取输入文件夹中所有文件的数量
    total_files = len([filename for filename in os.listdir(input_folder) if filename.endswith((".png", ".jpg"))])
    # 当前处理的文件计数
    current_file = 0

    # 遍历输入文件夹中的每个文件
    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg")):
            input_path = os.path.join(input_folder, filename)

            # 对每个文件执行指定次数的增强操作
            for i in range(num_augmentations):
                current_file += 1
                output_filename = f"{os.path.splitext(filename)[0]}_{i + 1}.png"
                output_path = os.path.join(output_folder, output_filename)

                # 调用添加噪声的函数
                add_vertical_noise_to_image(input_path, output_path, noise_intensity)

                # 更新进度条的值
                progress_var.set(current_file / total_files * 100)
                root.update_idletasks()

def add_vertical_noise_to_image(input_image_path, output_image_path, noise_probability):
    # 打开图像并将其转换为NumPy数组
    img = Image.open(input_image_path)
    img_array = np.array(img)

    # 根据图像的通道数执行相应的操作
    if len(img_array.shape) == 2:  # 灰度图像
        height, width = img_array.shape
        for i in range(width):
            if np.random.rand() < noise_probability:
                noise_value = np.random.randint(0, 256)
                img_array[:, i] = noise_value
    elif len(img_array.shape) == 3:  # 彩色图像
        height, width, channels = img_array.shape
        for channel in range(channels):
            for i in range(width):
                if np.random.rand() < noise_probability:
                    noise_value = np.random.randint(0, 256)
                    img_array[:, i, channel] = noise_value

    # 从NumPy数组创建新的图像并保存
    noisy_img = Image.fromarray(img_array)
    noisy_img.save(output_image_path)

def browse_input_folder():
    # 通过文件对话框选择输入文件夹
    input_folder = filedialog.askdirectory()
    input_folder_entry.delete(0, END)
    input_folder_entry.insert(0, input_folder)

def browse_output_folder():
    # 通过文件对话框选择输出文件夹
    output_folder = filedialog.askdirectory()
    output_folder_entry.delete(0, END)
    output_folder_entry.insert(0, output_folder)

def generate_images():
    # 获取用户输入的参数
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    num_augmentations = int(num_augmentations_entry.get())
    noise_intensity = float(noise_intensity_entry.get())

    # 设置进度条初始值并启动
    progress_var.set(0)
    progress_bar.start()

    # 记录程序开始时间
    start_time = time.time()

    # 调用生成图像的函数
    add_vertical_noise(input_folder, output_folder, num_augmentations, noise_intensity, progress_var)

    # 停止进度条并显示完成信息
    progress_bar.stop()
    result_label.config(text="Images generated successfully!")

    # 计算程序执行时间
    execution_time = time.time() - start_time
    execution_time_label.config(text=f"Execution Time: {execution_time:.2f} seconds")

# 创建主窗口
root = Tk()
root.title("Image Augmentation Tool")

# 创建GUI元素
Label(root, text="Input Folder:").grid(row=0, column=0, pady=10)
input_folder_entry = Entry(root, width=50)
input_folder_entry.grid(row=0, column=1, pady=10)
Button(root, text="Browse", command=browse_input_folder).grid(row=0, column=2, pady=10)

Label(root, text="Output Folder:").grid(row=1, column=0, pady=10)
output_folder_entry = Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, pady=10)
Button(root, text="Browse", command=browse_output_folder).grid(row=1, column=2, pady=10)

Label(root, text="Number of Augmentations:").grid(row=2, column=0, pady=10)
num_augmentations_entry = Entry(root, width=10)
num_augmentations_entry.grid(row=2, column=1, pady=10)

Label(root, text="Noise Intensity (0-1):").grid(row=3, column=0, pady=10)
noise_intensity_entry = Entry(root, width=10)
noise_intensity_entry.grid(row=3, column=1, pady=10)

Button(root, text="Generate Images", command=generate_images).grid(row=4, column=0, columnspan=3, pady=20)

# 创建进度条
progress_var = DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, length=300, mode='determinate')
progress_bar.grid(row=5, column=0, columnspan=3, pady=10)

# 显示结果信息的标签
result_label = Label(root, text="")
result_label.grid(row=6, column=0, columnspan=3)

# 显示程序执行时间的标签
execution_time_label = Label(root, text="")
execution_time_label.grid(row=7, column=0, columnspan=3)

# 启动主循环
root.mainloop()