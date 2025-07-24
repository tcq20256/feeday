批量生成测试


##  [https://openkey.cloud](https://openkey.cloud/register?aff=22CVF)
```
from openai import OpenAI
import csv
import time

# 你的OpenAI API Key和代理地址
client = OpenAI(
    api_key="sk-xxx",
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

def main():
    total_tasks = len(primary_classes) * len(secondary_classes) * len(styles)
    task_counter = 0

    with open("output_all_classes.tsv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["一级类", "二级类", "风格", "内容"])  # 表头

        for primary in primary_classes:
            for secondary in secondary_classes:
                for style in styles:
                    task_counter += 1
                    print(f"[{task_counter}/{total_tasks}] Generating: {primary} - {secondary} - {style}")
                    content = generate_text(primary, secondary, style)
                    print(f"Generated chars: {char_count(content)}")
                    print("Full content:\n" + content)
                    print("="*60 + "\n")
                    writer.writerow([primary, secondary, style, content])
                    time.sleep(1)  # 限流等待

if __name__ == "__main__":
    main()
```