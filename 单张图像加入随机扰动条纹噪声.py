from PIL import Image
import numpy as np
# 安装库pip install pillow
# 控制噪声的强度修改最底下noise_probability参数就可以了
def add_vertical_noise(input_image_path, output_image_path, noise_probability):
    # 打开灰度图像
    img = Image.open(input_image_path).convert('L')
    # 转换为NumPy数组
    img_array = np.array(img)
    # 获取图像尺寸
    height, width = img_array.shape
    # 添加随机竖条噪声
    for i in range(width):
        if np.random.rand() < noise_probability:
            # 生成随机竖条的灰度值
            noise_value = np.random.randint(0, 256)
            # 将竖条的每个像素设置为随机灰度值
            img_array[:, i] = noise_value
    # 从NumPy数组创建新的图像
    noisy_img = Image.fromarray(img_array)
    # 保存输出图像
    noisy_img.save(output_image_path)

# 调用函数并指定输入输出图像的文件路径
add_vertical_noise('./ceres_train_500/0001.png', './result/0010_striped.png', noise_probability=0.2)
