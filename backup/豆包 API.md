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

## 豆包改图下载本地

```
import os
import sys
import subprocess
import requests

# ===== 自动安装依赖 =====
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

try:
    from volcenginesdkarkruntime import Ark
except ImportError:
    install("volcengine-python-sdk[ark]")
    from volcenginesdkarkruntime import Ark

# ===== 初始化 Ark 客户端 =====
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="xxx",  # 建议改成 os.getenv("ARK_API_KEY")
)

# ===== 配置 =====
TXT_FILE = r"c:\prompts.txt"   # 提示词文件
SAVE_DIR = r"C:\doubao\i2i"   # 下载保存目录
os.makedirs(SAVE_DIR, exist_ok=True)

# ===== 读取提示词文件并逐行调用 =====
with open(TXT_FILE, "r", encoding="utf-8") as f:
    prompts = [line.strip() for line in f if line.strip()]

for idx, prompt in enumerate(prompts, start=1):
    try:
        imagesResponse = client.images.generate(
            model="doubao-seededit-3-0-i2i-250628",
            prompt=prompt,  # 每行作为提示词
            image="https://ark-project.tos-cn-beijing.volces.com/doc_image/seededit_i2i.jpeg",
            seed=123,
            guidance_scale=5.5,
            size="adaptive",
            watermark=True
        )
        url = imagesResponse.data[0].url
        print(f"[{idx}] 提示词: {prompt} -> 图片地址: {url}")

        # ===== 下载图片 =====
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200:
            # 文件名：序号_前10个字符提示词.jpg
            safe_prompt = "".join(c for c in prompt if c.isalnum())[:10]
            filename = os.path.join(SAVE_DIR, f"{idx:03d}_{safe_prompt}.jpg")
            with open(filename, "wb") as f:
                f.write(resp.content)
            print(f"    已保存到: {filename}")
        else:
            print(f"    下载失败: HTTP {resp.status_code}")

    except Exception as e:
        print(f"[{idx}] 提示词: {prompt} -> 生成失败: {e}")
```