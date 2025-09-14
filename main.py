from Modules.Embedder import EmbeddingEngine
from Modules.ingest import pdf_index
from Modules.retriever import Retriever
from Modules.prompt_engine import make_prompt
from Modules.generator import AnswerGen

from bidi.algorithm import get_display
import arabic_reshaper
import os
import shutil

def fix_farsi(text: str) -> str:
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def reset_index():
    if os.path.exists("embeddings"):
        shutil.rmtree("embeddings")
    os.makedirs("embeddings", exist_ok=True)

def run(question: str, engine: EmbeddingEngine, k: int = 4):
    retriever = Retriever(engine, k=k)
    hits = retriever.search(question)

    print(fix_farsi("=== نتایج جستجو (HITS) ==="))
    print(hits)

    top_chunks = [c for c, _ in hits]

    if not top_chunks:
        print(fix_farsi("❌ هیچ چانکی (تکه‌ای) بازیابی نشد. احتمالاً ایندکس خالیه یا سوال نامرتبطه."))
        return

    prompt = make_prompt(question, top_chunks)

    print(fix_farsi("=== پرامپت نهایی ==="))
    print(fix_farsi(prompt if prompt else "پرامپت ساخته نشد."))

    if not prompt:
        print(fix_farsi("❌ پرامپت ساخته نشد یا مقدارش None بود."))
        return

    gen = AnswerGen("google/mt5-base")
    answer = gen.generate(prompt)

    print(fix_farsi("=== سؤال ==="))
    print(fix_farsi(question))

    print(fix_farsi("\n=== پاسخ مدل ==="))
    print(fix_farsi(answer))

    print(fix_farsi("\n=== منابع ==="))
    for ch in top_chunks:
        if "[SOURCE:" in ch:
            src = ch.split("[SOURCE:")[1].split("]")[0].strip()
            print("-", fix_farsi(src))

if __name__ == "__main__":
    reset_index()

    engine = EmbeddingEngine()
    pdf_index("Data", engine)

    question = input("PLease Write Your Question: ")
    run(question, engine)
