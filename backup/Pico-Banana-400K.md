苹果发布的香蕉图像编辑数据集
- [https://github.com/apple/pico-banana-400k](https://github.com/apple/pico-banana-400k)


逐行读取 JSONL 文件，下载 open_image 和 output_image。
命名格式：
000001_open_image.png
000001_output_image.png

增强功能：
- ✅ 从指定 JSONL 行号开始（断点续传）
- ✅ 编号与行号同步（例如从第 98233 行开始 → 文件名从 098233 开始）
- ✅ 任一下载失败则两者都不保留
- ✅ 记录所有错误日志

## 预览数据集图片
```
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>通用媒体提取器：图片 + 视频 + BBCode 支持</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;line-height:1.5;margin:0;padding:24px;background:#0b0c0f;color:#e6e6e6;scroll-behavior:smooth}
    h1{font-size:20px;margin:0 0 12px}
    textarea{width:100%;min-height:160px;padding:12px;border-radius:12px;border:1px solid #2b2f36;background:#12141a;color:#e6e6e6;resize:vertical;margin-bottom:12px}
    button{background:#3b82f6;border:none;color:white;padding:10px 14px;border-radius:10px;cursor:pointer;font-weight:600;margin-right:8px}
    button.secondary{background:#2b2f36;color:#d0d0d0}
    .tip{font-size:12px;color:#9aa0a6;margin:8px 0 16px}
    .grid{display:flex;flex-wrap:wrap;gap:12px}
    figure{margin:0;background:#12141a;border:1px solid #2b2f36;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:8px;max-width:400px}
    figure>img,figure>video{max-width:100%;height:auto;object-fit:contain;background:#0b0c0f;cursor:pointer;border-radius:10px}
    figcaption{font-size:12px;padding:6px 4px;color:#9aa0a6;word-break:break-all}
    .err{color:#ff8a8a}
    #topBtn{position:fixed;bottom:24px;right:24px;background:#3b82f6;color:white;border:none;border-radius:50%;width:48px;height:48px;font-size:20px;cursor:pointer;display:none;box-shadow:0 4px 10px rgba(0,0,0,0.3)}
    #topBtn:hover{background:#2563eb}
  </style>
</head>
<body>
  <h1>通用媒体提取器（支持图片、视频、BBCode）</h1>

  <textarea id="urls" placeholder="可粘贴任意文字，自动提取图片/视频链接，如：\n#3 http://x.cn/a.jpg http://x.cn/b.png [img]http://x.cn/c.webp[/img] [url=\"http://x.cn/d.jpg\"]http://x.cn/e.jpg[/url]\nhttp://x.cn/f.mp4"></textarea>

  <button id="render">显示媒体</button>
  <button id="clear" class="secondary">清空</button>

  <div class="tip">自动识别常见图片格式（.jpg/.jpeg/.png/.gif/.webp/.svg/.avif/.tiff/.bmp）及视频格式（.mp4/.webm/.mov）。支持 [IMG]、[URL] 等 BBCode 混合。点击图片或视频可在新标签打开原文件。</div>

  <div id="grid" class="grid"></div>
  <button id="topBtn" title="返回顶部">↑</button>

  <script>
    const $ = s => document.querySelector(s);
    const urlsEl = $('#urls');
    const grid = $('#grid');
    const topBtn = $('#topBtn');

    const IMG_EXT = ['jpg','jpeg','png','gif','webp','bmp','svg','avif','tiff'];
    const VID_EXT = ['mp4','webm','mov'];

    function sanitizeUrl(u){
      try{
        const url = new URL(u);
        if(!/^https?:$/.test(url.protocol)) return null;
        return url.toString();
      }catch{ return null }
    }

    function extractUrlsFromText(text){
      text = text.replace(/\[img\]|\[\/img\]|\[url.*?\]|\[\/url\]/gi, ' ');
      const regex = /https?:\/\/[^\s\"]+/gi;
      const matches = text.match(regex) || [];
      return matches.map(m=>m.replace(/["\)\]\>]+$/,'').trim());
    }

    function render(){
      grid.innerHTML='';
      const allText = urlsEl.value;
      const urls = extractUrlsFromText(allText);
      let idx=0;
      for(const raw of urls){
        const u = sanitizeUrl(raw);
        if(!u) continue;
        const ext = (u.split('.').pop()||'').toLowerCase().split('?')[0];
        if(IMG_EXT.includes(ext)){
          idx++; addCard('img',u,`#${idx} ${u}`);
        } else if(VID_EXT.includes(ext)){
          idx++; addCard('video',u,`#${idx} ${u}`);
        }
      }
      if(idx===0) grid.innerHTML='<div class="err">未检测到图片或视频链接</div>';
    }

    function addCard(type,src,caption){
      const fig = document.createElement('figure');
      const cap = document.createElement('figcaption');
      cap.textContent = caption;

      if(type==='img'){
        const img = document.createElement('img');
        img.loading='lazy';
        img.referrerPolicy='no-referrer';
        img.src=src;
        img.alt=caption;
        img.onclick=()=>window.open(src,'_blank');
        fig.appendChild(img);
      } else if(type==='video'){
        const vid=document.createElement('video');
        vid.controls=true;
        vid.src=src;
        vid.onclick=()=>window.open(src,'_blank');
        fig.appendChild(vid);
      }

      fig.appendChild(cap);
      grid.appendChild(fig);
    }

    $('#render').addEventListener('click', render);
    $('#clear').addEventListener('click', ()=>{ urlsEl.value=''; grid.innerHTML=''; });

    window.addEventListener('scroll', ()=>{
      topBtn.style.display = window.scrollY > 200 ? 'block' : 'none';
    });
    topBtn.addEventListener('click', ()=> window.scrollTo({top:0,behavior:'smooth'}));

    // 示例
    urlsEl.value = [
      '{"open_image_input_url": "https://c1.staticflickr.com/8/7404/9423051591_cb1bf5c5e1_o.jpg", "text": "Remove the red flag and its white pole from the upper right of the image, seamlessly extending the clear blue sky, the sandy dune with its subtle texture, and the wooden fence to fill the void, ensuring the lighting, color, and natural grain of the background are perfectly matched for a realistic and unblemished result.", "output_image": "images/positive-edit/1.png", "edit_type": "Remove an existing object", "summarized_text": "Flag removed; extend sky, dune, and fence seamlessly."}
https://ml-site.cdn-apple.com/datasets/pico-banana-300k/nb/images/positive-edit/1.png
'
    ].join('\n');
  </script>
</body>
</html>
```


## 下载脚本
```
import os
import sys
import json
import subprocess

# ===== 自动安装依赖 =====
required_packages = ["requests", "tqdm"]
for pkg in required_packages:
    try:
        __import__(pkg)
    except ImportError:
        print(f"📦 未找到 {pkg}，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])

import requests
from tqdm import tqdm


# ===== 配置区 =====
JSONL_FILE = r"E:\Pico-Banana-400K\sft.jsonl"   # JSONL 文件路径
BASE_URL = "https://ml-site.cdn-apple.com/datasets/pico-banana-300k/nb/"  # output_image 前缀
SAVE_DIR = r"E:\Pico-Banana-400K\sft"                                                       # 保存目录
FAILED_LOG = os.path.join(SAVE_DIR, "failed_downloads.txt")               # 错误日志路径
START_LINE = 98233  # ←★★ 从第几行开始（自动跳过之前的）

os.makedirs(SAVE_DIR, exist_ok=True)


# ===== 下载函数 =====
def safe_download(url, path):
    """下载文件（成功返回 True，失败返回 False）"""
    try:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            print(f"⏭️ 已存在：{os.path.basename(path)}，跳过")
            return True

        print(f"⬇️ 正在下载：{url}")
        resp = requests.get(url, stream=True, timeout=30)
        if resp.status_code == 200:
            with open(path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            print(f"✅ 下载成功：{os.path.basename(path)}")
            return True
        else:
            print(f"❌ 下载失败（状态码 {resp.status_code}）：{url}")
            with open(FAILED_LOG, "a", encoding="utf-8") as log:
                log.write(f"{url}\t状态码 {resp.status_code}\n")
            return False
    except Exception as e:
        print(f"⚠️ 下载出错：{url}\n{e}")
        with open(FAILED_LOG, "a", encoding="utf-8") as log:
            log.write(f"{url}\t错误 {e}\n")
        return False


# ===== 主逻辑 =====
total = 0
skipped = 0

with open(JSONL_FILE, "r", encoding="utf-8") as f:
    for line_no, line in enumerate(tqdm(f, desc="Processing JSONL"), start=1):
        if line_no < START_LINE:
            continue  # 跳过前面未到起点的行

        line = line.strip()
        if not line:
            continue

        try:
            item = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON 解析错误（第 {line_no} 行）：{e}")
            continue

        # 支持字段兼容
        open_url = item.get("open_image_input_url") or item.get("open_image")
        output_path = item.get("output_image") or item.get("output_image_path")

        if not open_url or not output_path:
            print(f"⚠️ 第 {line_no} 行缺字段，跳过")
            continue

        # 拼接 output_image URL
        if output_path.startswith("http"):
            full_output_url = output_path
        else:
            full_output_url = BASE_URL.rstrip("/") + "/" + output_path.lstrip("/")

        # === 生成文件名 ===
        prefix = f"{line_no:06d}"  # 与 JSONL 行号对应
        open_save = os.path.join(SAVE_DIR, f"{prefix}_open_image.png")
        output_save = os.path.join(SAVE_DIR, f"{prefix}_output_image.png")

        # ---- 下载 open_image ----
        ok_open = safe_download(open_url, open_save)
        if not ok_open:
            skipped += 1
            print(f"🚫 第 {line_no} 行 open_image 下载失败，跳过该条记录")
            continue

        # ---- 下载 output_image ----
        ok_out = safe_download(full_output_url, output_save)
        if not ok_out:
            skipped += 1
            # 删除已下载的 open_image
            if os.path.exists(open_save):
                os.remove(open_save)
                print(f"🗑️ 已删除：{os.path.basename(open_save)}（因为 output_image 下载失败）")
            continue

        total += 1

print(f"\n✅ 下载完成，共成功 {total} 对，跳过 {skipped} 对。")
print(f"📄 错误日志：{FAILED_LOG}")
print(f"▶ 从第 {START_LINE} 行开始处理 JSONL")

```

