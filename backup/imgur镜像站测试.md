
检查 imgur 图片在多个镜像站是否可用


```
import requests
import time

# 测试超时（秒）
TIMEOUT = 10

# 测试的镜像站模式
MIRRORS = {
    "StackImgur":      "https://i.stack.imgur.com/{id}",
    "ImgurPics":       "https://imgur.pics/{id}",
    "ImgVue":          "https://imgvue.com/images/{id}",
    "RisuAI":          "https://risuai.com/imgur/{id}",  # 备选
}

def check_url(url):
    """HEAD 方式检查 URL 是否可访问"""
    try:
        r = requests.head(url, timeout=TIMEOUT)
        return r.status_code in (200, 301, 302)
    except:
        return False


def test_imgur_id(img_id, ext="jpg"):
    """检测单个 imgur ID 的可用镜像"""
    print(f"\n===== 测试 ID: {img_id} =====")

    results = {}

    # 拼接文件名
    full = f"{img_id}.{ext}"

    for name, pattern in MIRRORS.items():
        url = pattern.format(id=full)

        ok = check_url(url)
        results[name] = ok

        status = "✔ 可用" if ok else "✘ 不可用"
        print(f"{name:12s} → {status}  ({url})")

        time.sleep(0.2)

    return results


if __name__ == "__main__":
    # 示例 ID，可换成真实 ID
    test_list = [
        "qHxM2",  # 你提供的
        "9xndJ",
        "ciycE",
        "AFFHn",
    ]

    for img_id in test_list:
        test_imgur_id(img_id)
```