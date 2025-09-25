## 模型定价

模型名称 | 定价元/张
-- | --
doubao-seedream-4.0 | 0.2
doubao-seedream-3.0-t2i | 0.259
doubao-seededit-3.0-i2i | 0.3


## 豆包图像识别

```
import os
import sys
import subprocess

# ===== 安装依赖 =====
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

install("openai>=1.0")

from openai import OpenAI

# 初始化 Ark 客户端（建议方式：从环境变量读取）
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="xxxx",
)

# 调用模型
response = client.chat.completions.create(
    model="doubao-1-5-vision-pro-32k-250115",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"
                    },
                },
                {"type": "text", "text": "这是哪里？"},
            ],
        }
    ],
)

print(response.choices[0].message)
```

## 豆包图像修改

```
import os
import sys
import subprocess

# ===== 自动安装依赖 =====
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

install("volcengine-python-sdk[ark]")

# ===== 导入 SDK =====
from volcenginesdkarkruntime import Ark

# 初始化 Ark 客户端
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="xxxx",
)

# 调用图片生成接口
imagesResponse = client.images.generate(
    model="doubao-seededit-3-0-i2i-250628",
    prompt="改成爱心形状的泡泡",
    image="https://ark-project.tos-cn-beijing.volces.com/doc_image/seededit_i2i.jpeg",
    seed=123,
    guidance_scale=5.5,
    size="adaptive",
    watermark=True
)

# 打印返回图片地址
print(imagesResponse.data[0].url)
```