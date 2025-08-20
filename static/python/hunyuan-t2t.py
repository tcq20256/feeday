## 混元批量文生文

# -*- coding: utf-8 -*-
import time
import csv
import os
import json
from datetime import datetime
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

# pip install tencentcloud-sdk-python

# === 模型 & 提示词 ===
system_prompt = (
    "你是由腾讯云混元大模型提供的中文文本生成助手，擅长撰写结构清晰、真实、连贯的内容，风格多样，符合指定语体要求。"
)

# === 分类定义 ===
primary_classes = [
    "案件案例", "博客文章", "个人日记", "观点", "广告文案", "技术文档",
    "评论", "散文", "社交媒体帖子", "诗歌", "小说片段", "新闻报道", "学术论文摘要"
]

secondary_classes = [
    "AI", "动物", "情感", "公益", "购物", "古代文明", "交通", "教育", "近代战争", "经济",
    "科幻", "科技", "科普", "历史", "旅行", "美食", "母婴", "奇幻", "气候变化", "三农",
    "社会问题", "摄影", "生活", "时尚", "时政", "体育", "文化", "武器", "校园", "医疗",
    "艺术", "音乐", "影视", "游戏", "娱乐", "育儿", "职场", "植物", "商业"
]

styles = ["正式", "叙事", "情感化", "科普"]

# === 初始化腾讯混元客户端 ===
cred = credential.Credential("AKIDzta6PbbUCkAPVRDnFWbTAhL2XAczDGBI", "AD78KQK4Y0HO9kANgs593qVzNcnlX6Vw")  # ← 替换为你的密钥
httpProfile = HttpProfile()
httpProfile.endpoint = "hunyuan.tencentcloudapi.com"
clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
client = hunyuan_client.HunyuanClient(cred, "", clientProfile)

# === 内容生成函数 ===
def generate_text(primary: str, secondary: str, style: str, max_retries=3) -> str:
    prompt = (
        f"请根据以下要求撰写一段中文内容，结构清晰、语义连贯。\n"
        f"内容长度不少于200字，避免冗长。\n\n"
        f"一级分类：{primary}\n"
        f"二级分类：{secondary}\n"
        f"写作风格：{style}"
    )

    for attempt in range(1, max_retries + 1):
        try:
            req = models.ChatCompletionsRequest()
            params = {
                "Model": "hunyuan-turbo",
                "Messages": [
                    {"Role": "system", "Content": system_prompt},
                    {"Role": "user", "Content": prompt}
                ],
                "Temperature": 0.7,
                "TopP": 0.8,
                "MaxTokens": 500
            }
            req.from_json_string(json.dumps(params))
            resp = client.ChatCompletions(req)
            text = resp.Choices[0].Message.Content.strip()
            if len(text) >= 200:
                return text.replace('\n', ' ')
            else:
                print(f"⚠️ Retry {attempt}: 内容太短（{len(text)} 字符）")
                time.sleep(1)
        except Exception as e:
            print(f"❌ 错误：{primary}-{secondary}-{style} 第 {attempt} 次尝试失败：{e}")
            time.sleep(2)

    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[失败] {primary}-{secondary}-{style}\n")
    return "生成失败：内容为空"

# === 保存 CSV ===
def save_batch_to_csv(rows, batch_num, base_name="output", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{base_name}_{timestamp}_batch{batch_num}.csv"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["编号", "一级类", "二级类", "风格", "内容", "字符数"])
        writer.writerows(rows)
    print(f"✅ 保存第 {batch_num} 批，共 {len(rows)} 条 → {filepath}")

# === 主函数 ===
def main():
    total_tasks = len(primary_classes) * len(secondary_classes) * len(styles)  # = 2028
    task_counter = 0
    batch_data = []
    batch_size = 52
    batch_number = 1
    output_dir = r"D:\zxl_bak\ds\hunyuan_output"  # ← 替换为你自己的保存目录

    for primary in primary_classes:
        for secondary in secondary_classes:
            for style in styles:
                task_counter += 1
                print(f"\n[{task_counter}/{total_tasks}] ⏳ 正在生成：{primary} - {secondary} - {style}")
                content = generate_text(primary, secondary, style)
                length = len(content)
                print(f"→ 内容长度: {length} 字符")
                print("内容：")
                print(content)
                print("=" * 100)

                batch_data.append([task_counter, primary, secondary, style, content, length])

                if len(batch_data) >= batch_size:
                    save_batch_to_csv(batch_data, batch_number, base_name="hunyuan", output_dir=output_dir)
                    batch_data.clear()
                    batch_number += 1
                time.sleep(1)

    if batch_data:
        save_batch_to_csv(batch_data, batch_number, base_name="hunyuan", output_dir=output_dir)

    print("\n🎉 所有 2028 条中文内容生成完毕！")

if __name__ == "__main__":
    main()
