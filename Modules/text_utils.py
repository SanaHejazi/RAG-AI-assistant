import re #"Regular Expretion"---> Just for Conducting Operation in Texts
from typing import List

# converting long text to small pieces



def CleanText(s:str) -> str:
    s = s.replace('\u200c', ' ')
    s=re.sub(r'\s+',' ',s).strip()

def Chunk_Text(string:str , chunk_size:int=600, overlap:int=300)->List[str]:
    s =CleanText(string)
    chunks=[]
    start=0
    while start <len(s):
        end=min(start+chunk_size,len(s))
        chunk=s[start:end]
        chunks.append[chunk]

        if end == len(s):
            break

        start=end-overlap

        if start<0:
            start=0

        return chunks

