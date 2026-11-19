# 平均 RGB 分布

计算 `0.png` 到 `1999.png` 每张图片的平均 RGB 值，并绘制三维散点图。

## 安装和运行

在装有 Git 和 Python 3 的电脑上运行以下命令，将最后一行的路径替换为图片目录。

```powershell
git clone https://github.com/gehaotian-09/average-rgb.git
cd average-rgb
python -m pip install -r requirements.txt
python average_rgb.py "E:\你的图片目录"
```

图片目录会生成两个文件。

- `average_rgb.csv` 记录每张图片的文件名和平均 R、G、B 值。
- `average_rgb_distribution.png` 展示平均色在 RGB 空间中的分布。每个点的颜色是该图片的平均色。

计算时按像素的不透明度加权。完全透明的像素不参与计算，整张图完全透明时脚本会报错。
