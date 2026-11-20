import os
import io
import json
from flask import Flask, request, jsonify
import numpy as np
from PIL import Image

# --- CONFIGURAZIONE DELL'AMBIENTE (come nell'esempio 77) ---

# Keras sopra PyTorch, come nel notebook
os.environ["KERAS_BACKEND"] = "torch"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import keras
import torch
import faiss
from transformers import AutoTokenizer, AutoModel

app = Flask(__name__)

# --- PERCORSI: i file prodotti dal notebook, nella stessa cartella dello script ---
base_path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_path, "chefbot_mobilenetv2.keras")
knowledge_path = os.path.join(base_path, "chefbot_knowledge.json")

IMG_SIZE = (224, 224)
EMBEDDING_MODEL = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"

# --- CARICAMENTO DEL MODELLO DI VISIONE ---
print(f"Caricamento modello da: {model_path}")
# Il modello contiene già augmentation e normalizzazione -1..1 (Rescaling):
# basta passargli l'immagine 224x224 con pixel 0-255
model = keras.models.load_model(model_path)

# --- CARICAMENTO DELLA KNOWLEDGE BASE ---
with open(knowledge_path, encoding="utf-8") as f:
    knowledge_base = json.load(f)
# L'ordine delle chiavi è lo stesso di CLASSI_SCELTE nel notebook (verificato con un assert)
classi = list(knowledge_base.keys())


# --- EMBEDDER (classe SimpleEmbedder dell'esempio 76) ---
class SimpleEmbedder:
    def __init__(self, model_name):
        print(f"Caricamento del modello Hugging Face in corso: {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()

    def encode(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Mean pooling escludendo il padding
        token_embeddings = outputs.last_hidden_state
        attention_mask = inputs["attention_mask"]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return (sum_embeddings / sum_mask).numpy()


# --- INDICE FAISS: stesso corpus del notebook (descrizione + mood + ingredienti) ---
embedder = SimpleEmbedder(EMBEDDING_MODEL)
testi_piatti = [
    f"{s['description']} Mood: {s['mood']}. Ingredients: {', '.join(s['ingredients'])}."
    for s in knowledge_base.values()
]
emb_piatti = embedder.encode(testi_piatti)
faiss.normalize_L2(emb_piatti)
indice_faiss = faiss.IndexFlatIP(emb_piatti.shape[1])
indice_faiss.add(emb_piatti)
print(f"Piatti indicizzati: {indice_faiss.ntotal}")


# --- DEFINIZIONE DEGLI ENDPOINT ---

@app.route("/predict", methods=["POST"])
def predict():
    """
    Riceve una foto (campo 'file'), riconosce il piatto
    e restituisce la scheda informativa più le alternative.
    """
    if "file" not in request.files:
        return jsonify({"error": "Nessun file caricato"}), 400

    file = request.files["file"].read()
    # Bytes -> immagine PIL RGB 224x224 -> array con dimensione batch
    img = Image.open(io.BytesIO(file)).convert("RGB").resize(IMG_SIZE)
    x = keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    probs = keras.ops.convert_to_numpy(model.predict(x, verbose=0))[0]
    migliori = np.argsort(probs)[::-1][:3]
    piatto = classi[migliori[0]]

    return jsonify({
        "dish": piatto,
        "confidence": float(probs[migliori[0]]),
        "info": knowledge_base[piatto],
        "alternatives": [{"dish": classi[i], "confidence": float(probs[i])} for i in migliori[1:]],
    })


@app.route("/search", methods=["POST"])
def search():
    """
    Ricerca per umore: riceve un JSON {"text": "...", "k": 3}
    e restituisce i piatti semanticamente più vicini.
    """
    dati = request.get_json(silent=True) or {}
    frase = dati.get("text", "").strip()
    if not frase:
        return jsonify({"error": "Campo 'text' mancante"}), 400
    k = int(dati.get("k", 3))

    vettore = embedder.encode([frase])
    faiss.normalize_L2(vettore)
    punteggi, indici = indice_faiss.search(vettore, k)

    return jsonify({
        "query": frase,
        "results": [
            {"dish": classi[i], "similarity": float(s), "info": knowledge_base[classi[i]]}
            for s, i in zip(punteggi[0], indici[0])
        ],
    })


# --- AVVIO DELL'APPLICAZIONE ---

if __name__ == "__main__":
    app.run(port=5000)

# Esempi per testare gli endpoint da terminale (PowerShell: usare curl.exe):
# curl.exe -X POST http://127.0.0.1:5000/predict -F "file=@foto_piatti/mia_foto.jpg"
# curl.exe -X POST http://127.0.0.1:5000/search -H "Content-Type: application/json" -d "{\"text\": \"I want something fresh and light\"}"
