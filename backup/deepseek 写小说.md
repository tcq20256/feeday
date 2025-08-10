## 写1万字鬼故事

```
from openai import OpenAI
import os
import time
from datetime import datetime

# ============ 必填：你的 DeepSeek Key 与 API 基址 ============
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY") or "sk-xxxx",  # ← 改成你的
    base_url="https://api.deepseek.com"  # 兼容 /v1
)

# ============ 生成参数 ============
MODEL = "deepseek-chat"
TARGET_CHARS = 10000           # 目标中文字符数（≈1万字）
CHUNK_CHARS = 1300             # 每段大致字数（模型会有波动）
MAX_TOKENS_PER_CALL = 1600     # 每次调用返回的 token 上限（可按账户限额调整）
SLEEP_BETWEEN_CALLS = 1.0      # 调用间隔，防限流
OUTPUT_DIR = r"F:\x"
TITLE = "雾钟巷"                # 小说名（可自定义）
THEME = "恐怖鬼故事 · 都市传说 · 心理悬疑 · 地下空间与旧楼"

# ============ 初始系统/用户提示词 ============
SYSTEM_PROMPT = """你是一位擅长中文长篇恐怖小说创作的作家。
写作要求：
- 类型：恐怖/鬼故事/心理悬疑，营造压迫感、诡秘氛围，避免血腥直给，重视伏笔与反转。
- 统一世界观与时间线，人物设定前后一致，不重置、不穿帮。
- 多用具象细节与多感官描写（声、光、味、触、温度、湿度），少用空泛形容。
- 章节之间要承接上文，不要重复复述前情。
- 避免“总结式”叙述，尽量“现场化”展示。
- 语言自然克制，少堆砌华丽辞藻，注重节奏与留白。
- 允许出现都市传说元素，但要自圆其说。
"""

# 第一轮先要“设定表 + 大纲 + 开篇”，后续只做“无缝续写”
FIRST_USER_PROMPT = f"""请围绕主题《{TITLE}》（{THEME}）创作一部长篇恐怖小说，总字数≈{TARGET_CHARS}个中文字符。
输出分两部分：
1) 【故事设定表】（100-200字）：主角、配角、关键地点、时间线、叙事视角、核心秘密（不直接剧透结局，仅提示暗线）、叙事禁忌（避免套路）。
2) 【正文开篇】（约{CHUNK_CHARS}字）：直接进入戏剧场景，不要写“我准备写一个故事”；避免复述设定；用“现场化”描写推动情节。
注意：正文不要写小结，不要自我解释，不要结束故事。
"""

CONTINUE_PROMPT = f"""请严格延续上文内容进行【无缝续写】，约{CHUNK_CHARS}个中文字符：
- 承接上段最后一句的语义与场景，不要复述前情或回滚时间线。
- 维持既定人设、地点、线索与暗线，推动进展或制造新错觉。
- 继续使用“现场化”描写，避免总结与说教。
- 不要写“本章完”“未完待续”，不要写标题。
只输出续写正文。"""

FINALIZE_PROMPT = """请根据全文已写内容，输出：
1) 目录（8-14个自然段落名，仿章节标题风格，避免剧透）。
2) 正文不改动的前提下，给出一个不超过120字的“压缩式文案”，用于书腰宣传语（不剧透）。
"""

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def chat_once(messages, max_tokens=MAX_TOKENS_PER_CALL, temperature=0.9):
    """ 调一次模型，返回 content 文本 """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return resp.choices[0].message.content.strip()

def main():
    ensure_dir(OUTPUT_DIR)
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    out_txt = os.path.join(OUTPUT_DIR, f"horror_novel_{ts}.txt")

    # —— 会话上下文（保留以便续写）——
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": FIRST_USER_PROMPT}
    ]

    total_chars = 0
    chunks = []

    # —— 第一段：设定表 + 正文开篇 ——
    print(">>> 生成设定表与开篇…")
    first = chat_once(messages)
    chunks.append(first)
    total_chars += len(first.replace("\n", ""))
    messages.append({"role": "assistant", "content": first})

    # 写入文件（边写边存，防断线）
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(first + "\n\n")
    print(f"[累计字数] {total_chars} 字 | 已写入：{out_txt}")
    time.sleep(SLEEP_BETWEEN_CALLS)

    # —— 持续续写，直到达到目标字数 ——
    while total_chars < TARGET_CHARS:
        print(">>> 续写中…")
        messages.append({"role": "user", "content": CONTINUE_PROMPT})
        part = chat_once(messages)
        # 简单“防复读”清洗：去除开头常见客套提示
        for prefix in ("续写：", "续写", "继续：", "继续", "正文：", "内容："):
            if part.startswith(prefix):
                part = part[len(prefix):].lstrip()

        clean = part.strip()
        chunks.append(clean)
        total_chars += len(clean.replace("\n", ""))

        # 记录到会话与文件
        messages.append({"role": "assistant", "content": clean})
        with open(out_txt, "a", encoding="utf-8") as f:
            f.write(clean + "\n\n")

        print(f"[累计字数] {total_chars} 字 | +{len(clean)} 字")
        time.sleep(SLEEP_BETWEEN_CALLS)

        # 保险：如果某段异常很短，稍作重试
        if len(clean) < 200:
            print(">>> 本段过短，追加一次补写…")
            messages.append({"role": "user", "content": CONTINUE_PROMPT})
            extra = chat_once(messages, temperature=0.95)
            extra = extra.strip()
            chunks.append(extra)
            total_chars += len(extra.replace("\n", ""))
            messages.append({"role": "assistant", "content": extra})
            with open(out_txt, "a", encoding="utf-8") as f:
                f.write(extra + "\n\n")
            print(f"[累计字数] {total_chars} 字 | +{len(extra)} 字")
            time.sleep(SLEEP_BETWEEN_CALLS)

    # —— 收尾：生成目录与书腰文案（不改正文） ——
    print(">>> 生成目录与书腰文案…")
    messages_for_final = messages[:]  # 克隆上下文
    messages_for_final.append({"role": "user", "content": FINALIZE_PROMPT})
    finalize = chat_once(messages_for_final, max_tokens=800, temperature=0.7)

    with open(out_txt, "a", encoding="utf-8") as f:
        f.write("\n\n====== 目录与书腰文案 ======\n")
        f.write(finalize + "\n")

    print("\n=== 完成！===")
    print(f"成稿路径：{out_txt}")
    print(f"累计约：{total_chars} 字（含换行清理前后会有少量偏差）")

if __name__ == "__main__":
    main()

```