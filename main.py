from Modules.Embedder import EmbeddingEngine
from Modules.ingest import pdf_index
from Modules.retriever import Retriever

engine = EmbeddingEngine(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
try:
    engine.load_index() #preventing from repetitive loading pdf text again
except:
    pass
pdf_count,chunk_count=pdf_index(pdf_route="Data",engine=engine)
print(f"Ingested PDFs: {pdf_count}, total new chunks: {chunk_count}")
query=input("Please write your text : \n")

retriever = Retriever(engine, k=4)
results = retriever.search(query)

for i, (chunk, dist) in enumerate(results, 1):
    print(f"{i}. dist={dist:.4f} =>  {chunk[:180]} ...")
