from typing import List
import re

# فارسی
SYSTEM_INSTRUCTIONS_FA = (
    "تو یک دستیار پاسخ‌گوی دقیق هستی. فقط بر اساس متن‌های داده‌شده پاسخ بده. "
    "اگر اطلاعات کافی نیست، صادقانه بگو «نمی‌دانم». از حدس زدن خودداری کن."
)
ANSWER_FORMAT_FA = (
    "خروجی را به زبان فارسی و در قالب زیر بده:\n"
    "پاسخ:\n"
    "- ...\n\n"
    "منابع:\n"
    "- [SOURCE: نام_فایل]"
)

# انگلیسی
SYSTEM_INSTRUCTIONS_EN = (
    "You are a precise and helpful assistant. Only answer based on the provided texts. "
    "If the information is not enough, say 'I don't know' honestly. Do not guess."
)
ANSWER_FORMAT_EN = (
    "Respond in English and in the following format:\n"
    "Answer:\n"
    "- ...\n\n"
    "Sources:\n"
    "- [SOURCE: filename]"
)

def detect_language(text: str) -> str:
    fa_chars = re.findall(r"[\u0600-\u06FF]", text)
    en_chars = re.findall(r"[a-zA-Z]", text)
    return "fa" if len(fa_chars) > len(en_chars) else "en"

def build_context(chunks: List[str], max_char: int = 1500) -> str:
    ctx = ""
    for tmp in chunks:
        if len(ctx) + len(tmp) > max_char:
            break
        ctx += tmp.strip() + "\n-----\n"
    return ctx

def make_prompt(question: str, top_chunks: List[str]) -> str:
    lang = detect_language(question)
    final_context = build_context(top_chunks)

    if lang == "fa":
        return (
            f"{SYSTEM_INSTRUCTIONS_FA}\n\n"
            f"سؤال کاربر:\n{question}\n\n"
            f"متن‌های مرتبط:\n{final_context}\n\n"
            f"{ANSWER_FORMAT_FA}\n"
            f"توجه: اگر پاسخ در متن‌های بالا نبود، فقط بگو «نمی‌دانم»."
        )
    else:
        return (
            f"{SYSTEM_INSTRUCTIONS_EN}\n\n"
            f"User Question:\n{question}\n\n"
            f"Relevant Texts:\n{final_context}\n\n"
            f"{ANSWER_FORMAT_EN}\n"
            f"Note: If the answer is not found in the above texts, just say 'I don't know'."
        )
