from sentence_transformers import SentenceTransformer #For Converting Sentences To Vector
import faiss #For Searching between vectors
import numpy as np #Numeric arrays and mathematical operations
import os  #Working with files...
import pickle #For Save And Loading python objects



# This class is just used for convrting text to vector and indexes...

class EmbeddingEngine:
    def __init__(self, model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        self.model= SentenceTransformer(model_name)
        self.index= None
        self.documents=[]

    def embed_text(self,text):
        embeded_text=self.model.encode(text, convert_to_numpy=True)
        return embeded_text
    
    def building_index(self,text):
        self.documents=text
        embedding_text=self.embed_text(text)
        self.index= faiss.IndexFlatL2(embedding_text.shape[1])
        self.index.add(embedding_text)

    def save_index(self, path='embeddings/faiss.index', meta_path='embeddings/meta.pkl'):
        faiss.write_index(self.index,path)
        with open(meta_path,"wb") as f:
            pickle.dump(self.documents, f)

    def load_index(self, path='embeddings/faiss.index', meta_path='embeddings/meta.pkl'):
        self.index = faiss.read_index(path)
        with open(meta_path, 'rb') as f:
            self.documents = pickle.load(f)



    
       
