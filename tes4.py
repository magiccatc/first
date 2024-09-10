import cairosvg
from PIL import Image

# Step 1: 使用 cairosvg 将 .svg 转换为透明背景的 .png
svg_path = "E:\\Desktop\\pythonProject\\舰艇.svg"
png_path = "E:\\Desktop\\pythonProject\\舰艇_no_bg.png"
cairosvg.svg2png(url=svg_path, write_to=png_path)

# Step 2: 使用 PIL 打开生成的 .png，并为背景填充浅蓝色
image = Image.open(png_path)

# 设置浅蓝色背景颜色 (173, 216, 230)
background_color = (173, 216, 230)
background = Image.new("RGB", image.size, background_color)

# 将原来的 .png 图像粘贴到带背景颜色的图像上
background.paste(image, (0, 0), image)  # 第三个参数是透明度掩膜

# 保存带浅蓝色背景的 .png
output_path = "E:\\Desktop\\pythonProject\\舰艇_with_light_blue_bg.png"
background.save(output_path)

# 显示生成的图片
background.show()
