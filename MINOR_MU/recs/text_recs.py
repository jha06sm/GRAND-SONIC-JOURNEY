import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

CAT_PATH = "data/tracks_catalog.csv"

def _local_or_hf(model_name):
    import os
    local = f"models/{model_name.replace('/','__')}"
    return local if os.path.isdir(local) else model_name

def init_embedder(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    cat = pd.read_csv(CAT_PATH)
    model = SentenceTransformer(_local_or_hf(model_name))
    texts = (cat['title'].fillna('') + ' ' + cat['artist'].fillna('') + ' ' + cat['tags'].fillna('')).tolist()
    X = model.encode(texts, normalize_embeddings=True)
    index = faiss.IndexFlatIP(X.shape[1])
    index.add(X.astype('float32'))
    return {'catalog': cat, 'model': model, 'index': index, 'emb': X}

def recommend_by_prompt(state, prompt, lang=None, bpm_range=(0,999), top_k=5):
    cat = state['catalog'].copy()
    model = state['model']
    index = state['index']
    q = model.encode([prompt], normalize_embeddings=True).astype('float32')
    D, I = index.search(q, top_k*3)
    out = cat.iloc[I[0]].copy()
    lo, hi = bpm_range
    mask = (out['bpm'] >= lo) & (out['bpm'] <= hi)
    if lang:
        mask &= out['lang'].str.lower().eq(lang.lower())
    out = out[mask].head(top_k)
    out.insert(0, 'score', D[0][:len(out)])
    return out



# ✅ Wrapper to make it easy for Streamlit integration
_embed_state = None

def get_text_recommendations(prompt, lang=None, bpm_range=(0, 999), top_k=5):
    global _embed_state
    if _embed_state is None:
        _embed_state = init_embedder()   # initialize only once
    results = recommend_by_prompt(_embed_state, prompt, lang=lang, bpm_range=bpm_range, top_k=top_k)
    return [f"{row['title']} - {row['artist']}" for _, row in results.iterrows()]
