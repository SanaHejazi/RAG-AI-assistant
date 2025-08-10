import os
from typing import List, Tuple
import fitz  # PyMuPDF
from text_utils import Chunk_Text, CleanText
from Embedder import EmbeddingEngine


def ExtractPDF(pdf_patch:str)->str:
    doc=fitz.open(pdf_patch)
    text= []
    for page in doc:
        text.append(page.get_text('text'))
    doc.close()
    return CleanText("\n".join(text)) #connect all texts with new line...


def pdf_index(pdf_route:str,engine:EmbeddingEngine, chunk_size:int=600,overlap:int=100)->Tuple[int, int]:
    pdf_files=[]
    for f in os.listdir(pdf_route):
        if f.lower().endswith(".pdf"):
            pdf_files.append(f)
    all_chunks=[]
    for f in pdf_files:
        full = os.path.join(pdf_route,f)
        text =ExtractPDF(full)
        chunks=Chunk_Text(text,chunk_size=chunk_size,overlap=overlap)
        chunks = [f"[SOURCE: {f}]" + c for c in chunks]
        all_chunks.extend(chunks)
        if not all_chunks:
            return(0,0)
        if engine.index is None or len(engine.documents)==0:
            engine.building_index(all_chunks)
        else:
            emb=engine.embed_text(all_chunks)
            engine.index.add(emb)
            engine.documents.extend(all_chunks)

    os.makedirs("embeddings", exist_ok=True)
    engine.save_index()
    return (len(pdf_files), len(all_chunks))

