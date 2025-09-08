from typing import List

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

def build_context(chunks:List[str] , max_char:int=1500)->str:
    ctx=""
    for tmp in chunks:
        if len(ctx)+len(tmp)>max_char:
            break
        ctx=ctx+tmp.strip()+"\n-----\n"
    return ctx

def make_persian_prompt(question:str, top_chunks:List[str])->str:
    final_context=build_context(top_chunks)

    prompt = (
        f"{SYSTEM_INSTRUCTIONS_FA}\n\n"
        f"سؤال کاربر:\n{question}\n\n"
        f"متن‌های مرتبط:\n{final_context}\n\n"
        f"{ANSWER_FORMAT_FA}\n"
        f"توجه: اگر پاسخ در متن‌های بالا نبود، فقط بگو «نمی‌دانم»."
    )



