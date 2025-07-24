文本模型批量生成文本测试


## ChatGPT 

第三方代理接口

-  [https://openkey.cloud](https://openkey.cloud/register?aff=22CVF)

### 执行脚本
```
from openai import OpenAI
import time
import csv
import os
from datetime import datetime

# 初始化客户端
client = OpenAI(
    api_key="sk-x",
    base_url="https://openkey.cloud/v1"
)

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

category_map = {
    "案件案例": "Case Study",
    "博客文章": "Blog Article",
    "个人日记": "Personal Diary",
    "观点": "Opinion",
    "广告文案": "Advertising Copy",
    "技术文档": "Technical Document",
    "评论": "Review",
    "散文": "Essay",
    "社交媒体帖子": "Social Media Post",
    "诗歌": "Poetry",
    "小说片段": "Fiction Excerpt",
    "新闻报道": "News Report",
    "学术论文摘要": "Academic Abstract",
    "AI": "Artificial Intelligence",
    "动物": "Animals",
    "情感": "Emotion",
    "公益": "Public Welfare",
    "购物": "Shopping",
    "古代文明": "Ancient Civilization",
    "交通": "Transportation",
    "教育": "Education",
    "近代战争": "Modern War",
    "经济": "Economics",
    "科幻": "Science Fiction",
    "科技": "Technology",
    "科普": "Popular Science",
    "历史": "History",
    "旅行": "Travel",
    "美食": "Cuisine",
    "母婴": "Mother and Baby",
    "奇幻": "Fantasy",
    "气候变化": "Climate Change",
    "三农": "Agriculture and Rural Affairs",
    "社会问题": "Social Issues",
    "摄影": "Photography",
    "生活": "Lifestyle",
    "时尚": "Fashion",
    "时政": "Current Politics",
    "体育": "Sports",
    "文化": "Culture",
    "武器": "Weapons",
    "校园": "Campus",
    "医疗": "Medical",
    "艺术": "Art",
    "音乐": "Music",
    "影视": "Film and TV",
    "游戏": "Gaming",
    "娱乐": "Entertainment",
    "育儿": "Parenting",
    "职场": "Workplace",
    "植物": "Plants",
    "商业": "Business",
    "正式": "Formal",
    "叙事": "Narrative",
    "情感化": "Emotional",
    "科普": "Popular Science"
}

def char_count(text: str) -> int:
    return len(text)

def generate_text(primary, secondary, style, max_retries=3):
    primary_en = category_map.get(primary, primary)
    secondary_en = category_map.get(secondary, secondary)
    style_en = category_map.get(style, style)

    prompt = (
        f"Please write a coherent, well-structured English text with at least 250 characters and preferably no more than 350 characters about the following:\n"
        f"Primary category: {primary_en}\n"
        f"Secondary category: {secondary_en}\n"
        f"Writing style: {style_en}\n"
        f"Important: The entire text must be in English without any Chinese characters or words."
    )
    text = ""
    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=900
            )
            text = response.choices[0].message.content.strip()
            char_num = char_count(text)
            if char_num >= 250:
                return text
            else:
                print(f"Retry {attempt} for {primary}-{secondary}-{style}, char count {char_num} < 250")
                time.sleep(1)
        except Exception as e:
            print(f"Error for {primary}-{secondary}-{style}: {e}")
            time.sleep(2)
    print(f"Max retries reached for {primary}-{secondary}-{style}, returning last result")
    return text

def write_to_csv_with_timestamp(base_name, rows, batch_size, output_dir="D:/data/output"):
    os.makedirs(output_dir, exist_ok=True)
    now_str = datetime.now().strftime("%Y%m%d%H%M")
    filename = f"{base_name}_{now_str}_{batch_size}.csv"
    full_path = os.path.join(output_dir, filename)
    with open(full_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["编号", "一级类", "二级类", "风格", "内容", "字符数"])
        writer.writerows(rows)
    print(f"Saved batch of {len(rows)} records to {full_path}")

def main():
    total_tasks = len(primary_classes) * len(secondary_classes) * len(styles)
    task_counter = 0
    batch_size = 5  # 没生成5条保存成表
    buffer = []
    base_name = "generated_texts"
    output_dir = r"C:\test"  # 你需要的输出目录，请修改为你想要的路径

    for primary in primary_classes:
        for secondary in secondary_classes:
            for style in styles:
                task_counter += 1
                print(f"\n[{task_counter}/{total_tasks}] Generating: {primary} - {secondary} - {style}\n")
                content = generate_text(primary, secondary, style)
                char_num = char_count(content)
                print(f"Content ({char_num} chars):\n")
                print(content)
                print("\n" + "="*80 + "\n")

                buffer.append([task_counter, primary, secondary, style, content, char_num])

                if len(buffer) >= batch_size:
                    write_to_csv_with_timestamp(base_name, buffer, batch_size, output_dir=output_dir)
                    buffer.clear()

                time.sleep(1)  # 限流防封禁

    if buffer:
        write_to_csv_with_timestamp(base_name, buffer, len(buffer), output_dir=output_dir)

    print("All done!")

if __name__ == "__main__":
    main()
```
### 输出结果
```
[354/2028] Generating: 个人日记 - 科幻 - 叙事
Generated chars: 400
Full content:
October 12, 2147

Today, I stumbled upon an ancient device in the ruins of an old library—an old smartphone. Its screen flickered to life, revealing images of a world long gone. I felt a surge of nostalgia for a time when humans thrived on connection, not just data. As I scrolled through its apps, I wondered what stories lay hidden in its memory, waiting to bridge the gap between past and present.
```

## DeepSeek
- [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
### 运行脚本
```
from openai import OpenAI
import time

# 初始化客户端，替换成 DeepSeek 的 base_url 和 api_key
client = OpenAI(
    api_key="sk-xxx",  # 这里换成你在 DeepSeek 申请的 API Key
    base_url="https://api.deepseek.com"    # DeepSeek API 地址，带/v1也可以
)


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

def generate_text(primary: str, secondary: str, style: str, max_retries=3) -> str:
    prompt = (
        f"Please write an English text about the following topic.\n"
        f"The text must be coherent and well-structured,\n"
        f"with at least 200 characters. Avoid making the text too long.\n\n"
        f"Primary category: {primary}\n"
        f"Secondary category: {secondary}\n"
        f"Writing style: {style}"
    )
    text = ""
    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500  # 允许稍长文本，模型自动控制长度
            )
            text = response.choices[0].message.content.strip()
            length = len(text)
            if length >= 200:
                return text.replace('\n', ' ')
            else:
                print(f"Retry {attempt} for {primary} - {secondary} - {style}: char count {length} < 200")
                time.sleep(1)
        except Exception as e:
            print(f"Error on {primary} - {secondary} - {style}: {e}")
            time.sleep(2)

    print(f"Max retries reached for {primary} - {secondary} - {style}. Returning last result.")
    if text:
        return text.replace('\n', ' ')
    return ""

def main():
    total_tasks = len(primary_classes) * len(secondary_classes) * len(styles)
    task_counter = 0

    for primary in primary_classes:
        for secondary in secondary_classes:
            for style in styles:
                task_counter += 1
                print(f"\n[{task_counter}/{total_tasks}] Generating: {primary} - {secondary} - {style}\n")
                content = generate_text(primary, secondary, style)
                length = len(content)
                print(f"Content ({length} characters):\n")
                print(content)
                print("\n" + "="*100 + "\n")
                time.sleep(1)  # 避免请求过快被限流

if __name__ == "__main__":
    main()
```
### 输出结果
```
[15/2028] Generating: 案件案例 - 公益 - 情感化

Content (827 characters):

**A Beacon of Hope: The Power of Compassion in Legal Cases**    In the midst of cold courtrooms and rigid laws, some cases shine as reminders of humanity’s warmth. Take the story of an elderly woman evicted unfairly—her plight moved strangers to crowdfund her legal fees. Or the pro bono lawyers who fought for a child’s right to education against all odds. These stories aren’t just about justice; they’re about hearts uniting to lift others up.    Every such case whispers a truth: the law is stronger when wrapped in kindness. Behind every docket number is a life, and behind every verdict, a chance to heal. Let’s celebrate these unsung heroes—the donors, volunteers, and advocates—who turn legal battles into triumphs of empathy. Because justice, when paired with love, doesn’t just win—it transforms.    (Characters: 598)
```
